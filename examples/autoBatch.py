import re
import os
import sys
import time
import pathlib
import shutil
import requests
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import formlabs_local_api_minimal as formlabs

USERNAME = "username"
PASSWORD = "password"

FORMLABS_MATERIAL_SELECTION = {
    "machine_type": "FRMB-3-0",
    "material_code": "FLGPGR04",
    "layer_thickness_mm": 0.1,
    "print_setting": "DEFAULT",
}

class OrderType(Enum):
    GENERIC = 1

@dataclass
class StlModelAndQuantity:
    filename: str
    quantity: int

@dataclass
class OrderParameters:
    order_id: str
    order_type: OrderType
    order_folder_path: str
    quantity: int
    stl_files_and_quantities: list[StlModelAndQuantity]

@dataclass
class BatchResult:
    part_quantity_in_this_print: int

PATH_TO_INPUT_FOLDERS = {
    OrderType.GENERIC: r"/Users/haip/Documents/Orders/2. Approved",
}
PATH_TO_OUTPUT_FOLDERS = {
    OrderType.GENERIC: r"/Users/haip/Documents/Orders/3. Printing",
}
CACHE_OF_INPUT_FOLDERS = {
    OrderType.GENERIC: set(),
}
PATH_TO_FOLDER_FOR_SAVING_PRINT_FILES = r"/Users/haip/Documents/Orders/Job File Output"
DELAY_BETWEEN_NEW_ORDER_FOLDER_CHECKS_SECONDS = 2

pathToPreformServer = None
if sys.platform == 'win32':
    pathToPreformServer = pathlib.Path().resolve() / "PreFormServer.exe"
elif sys.platform == 'darwin':
    pathToPreformServer = pathlib.Path().resolve() / "PreFormServer.app/Contents/MacOS/PreFormServer"
else:
    print("Unsupported platform")
    sys.exit(1)


def check_input_folder(order_type: OrderType):
    global CACHE_OF_INPUT_FOLDERS
    input_folder = PATH_TO_INPUT_FOLDERS[order_type]
    current_folders = set(f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f)))
    new_folders = current_folders - CACHE_OF_INPUT_FOLDERS[order_type]
    for new_folder in new_folders:
        process_order(os.path.join(input_folder, new_folder), order_type)
    CACHE_OF_INPUT_FOLDERS[order_type] = current_folders


def process_order(order_folder_path, order_type: OrderType):
    print("Processing order", order_folder_path, order_type)
    order_parameters = parse_order_parameters(order_folder_path, order_type)
    # print("Parsed order parameters", order_parameters)
    if order_parameters is None:
        print("Unable to parse order folder name, skipping order")
        return
    if order_parameters.quantity == 0:
        print("No quantity detected, skipping order")
        return
    order_parameters = update_order_parameters_with_stl_files(order_parameters)
    print("Updated order parameters with STL info", order_parameters)
    batch_results = process_order_models(order_parameters)
    print("Batching result:", batch_results)
    move_order_order_to_completed_folder(order_folder_path, order_type)
    print("Order moved to completed folder")


def move_order_order_to_completed_folder(order_folder_path, order_type: OrderType):
    order_folder_new_path = os.path.join(PATH_TO_OUTPUT_FOLDERS[order_type], os.path.basename(order_folder_path))
    if os.path.exists(order_folder_new_path):
        print("Folder already exists in completed folder, deleting it so the new version can be moved")
        shutil.rmtree(order_folder_new_path)
    shutil.move(order_folder_path, PATH_TO_OUTPUT_FOLDERS[order_type])


def parse_order_parameters(order_folder_path, order_type) -> OrderParameters:
    folder_name = os.path.basename(order_folder_path)
    # Parse something like "1000385 Qty 1"
    pattern = re.compile(r"(?P<order_id>\d+) Qty (?P<quantity>\d+)")
    match = pattern.match(folder_name)
    if match:
        quantity = int(match.group('quantity') or 0)
        return OrderParameters(
            match.group('order_id'),
            OrderType.GENERIC,
            order_folder_path,
            quantity,
            []
        )
    else:
        raise Exception("Unable to parse order folder name")


def update_order_parameters_with_stl_files(order_parameters: OrderParameters) -> OrderParameters:
    stl_files_and_quantities: list[StlModelAndQuantity] = []
    for file in os.listdir(order_parameters.order_folder_path):
        if file.endswith(".stl"):
            stl_files_and_quantities.append(StlModelAndQuantity(file, order_parameters.quantity))
    order_parameters.stl_files_and_quantities = stl_files_and_quantities
    return order_parameters


def process_order_models(order_parameters: OrderParameters) -> list[BatchResult]:
    current_batch = 1
    batch_results: list[BatchResult] = []
    batch_has_unsaved_changed = False

    def clear_scene():
        nonlocal batch_has_unsaved_changed, batch_results
        print("Clearing scene")
        response = requests.request(
            "POST",
            "http://localhost:44388/scene/",
            json=FORMLABS_MATERIAL_SELECTION,
        )
        response.raise_for_status()
        batch_has_unsaved_changed = False
        batch_results.append(BatchResult(0))
    
    def save_batch_form():
        nonlocal current_batch
        save_path = os.path.join(PATH_TO_FOLDER_FOR_SAVING_PRINT_FILES, f"{order_parameters.order_id}_batch{current_batch}.form")
        print(f"Saving batch {current_batch} to {save_path}")
        save_form_response = requests.request(
            "POST",
            "http://localhost:44388/scene/save-form/",
            json={
                "file": save_path,
            },
        )
        save_form_response.raise_for_status()
        print("Batch saved")
        # Upload batch to Fleet Control as well
        print("Uploading batch to Fleet Control")
        login_response = requests.request(
            "POST",
            "http://localhost:44388/login/",
            json={
                "username": USERNAME,
                "password": PASSWORD,
            },
        )
        login_response.raise_for_status()
        try:
            print_response = requests.request(
                "POST",
                "http://localhost:44388/scene/print/",
                json={
                    "printer": "6e0e46db-5fca-49f0-8024-599eacdd8437",
                    "job_name": f"{order_parameters.order_id}_batch{current_batch}",
                },
            )
            print_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Error uploading to Fleet Control:", e)
            print(e.response.text)
        current_batch += 1

    with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer) as preform:
        clear_scene()
        for stl_file_and_quantity in order_parameters.stl_files_and_quantities:
            qty_to_print = stl_file_and_quantity.quantity
            while qty_to_print >= 1:
                print(f"Importing model {stl_file_and_quantity.filename} qty {qty_to_print}/{stl_file_and_quantity.quantity}")
                import_model_response = requests.request(
                    "POST",
                    "http://localhost:44388/scene/import-model/",
                    json={
                        "file": os.path.join(order_parameters.order_folder_path, stl_file_and_quantity.filename),
                        "repair_behavior": "IGNORE",
                    },
                )
                import_model_response.raise_for_status()
                new_model_id = import_model_response.json()["id"]
                print(f"Auto orienting {new_model_id}")
                auto_orient_response = requests.request(
                    "POST",
                    "http://localhost:44388/scene/auto-orient/",
                    json={
                        "models": [new_model_id],
                        "mode": "DENTAL",
                        "tilt": 0,
                    },
                )
                auto_orient_response.raise_for_status()
                print(f"Auto layouting all")
                layout_response = requests.request(
                    "POST",
                    "http://localhost:44388/scene/auto-layout/",
                    json={
                        "models": "ALL",
                    },
                )
                if layout_response.status_code != 200:
                    print("Not all models can fit, removing model")
                    delete_response = requests.request(
                        "DELETE",
                        f"http://localhost:44388/scene/models/{str(new_model_id)}/",
                    )
                    delete_response.raise_for_status()
                    save_batch_form()
                    clear_scene()
                else:
                    batch_has_unsaved_changed = True
                    batch_results[-1].part_quantity_in_this_print += 1
                    qty_to_print -= 1
                    print(f"Model {stl_file_and_quantity.filename} added to scene")

        if batch_has_unsaved_changed:
            save_batch_form()

    return batch_results


if __name__ == "__main__":
    print("Running automatic Formlabs job preparation\n")
    print("\nNew orders in those folders will be processed automatically")
    while True:
        check_input_folder(OrderType.GENERIC)
        time.sleep(DELAY_BETWEEN_NEW_ORDER_FOLDER_CHECKS_SECONDS)
