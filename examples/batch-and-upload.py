import re
import os
import sys
import time
import pathlib
import shutil
import formlabs
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from formlabs.models.scene_auto_orient_post_request import SceneAutoOrientPostRequest
from formlabs.models.scene_auto_layout_post_request import SceneAutoLayoutPostRequest
from formlabs.models.scene_type_model import SceneTypeModel
from formlabs.models.scene_type_model_layer_thickness import SceneTypeModelLayerThicknessMm
from formlabs.models.models_selection_model import ModelsSelectionModel
from formlabs.models.load_form_post_request import LoadFormPostRequest


FORMLABS_MATERIAL_SELECTION = SceneTypeModel(
    machine_type="FRMB-3-0",
    material_code="FLGPGR04", # TODO: change this
    layer_thickness_mm=SceneTypeModelLayerThicknessMm("0.1"),
    print_setting="DEFAULT", # TODO: change this
)

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
    OrderType.GENERIC: r"C:\Users\haip_formlabs\Desktop\Demo\2. Approved",
}
PATH_TO_OUTPUT_FOLDERS = {
    OrderType.GENERIC: r"C:\Users\haip_formlabs\Desktop\Demo\3. Printing",
}
CACHE_OF_INPUT_FOLDERS = {
    OrderType.GENERIC: set(),
}
PATH_TO_FOLDER_FOR_SAVING_PRINT_FILES = r"C:\Users\haip_formlabs\Desktop\Job File Output"
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
    print("Parsed order parameters", order_parameters)
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

    def clear_scene(preform):
        nonlocal batch_has_unsaved_changed, batch_results
        print("Clearing scene")
        preform.api.scene_post(FORMLABS_MATERIAL_SELECTION)
        batch_has_unsaved_changed = False
        batch_results.append(BatchResult(0))
    
    def save_batch_form(preform):
        nonlocal current_batch
        save_path = os.path.join(PATH_TO_FOLDER_FOR_SAVING_PRINT_FILES, f"{order_parameters.order_id}_batch{current_batch}.form")
        print(f"Saving batch {current_batch} to {save_path}")
        preform.api.scene_save_form_post(LoadFormPostRequest(file=save_path))
        print("Batch saved")
        # Upload batch to Fleet Control as well
        print("Uploading batch to Fleet Control")
        preform.api.login_post(formlabs.models.LoginPostRequest(formlabs.models.UsernameAndPassword(username="hype55", password="hype55")))
        preform.api.scene_print_post(formlabs.models.ScenePrintPostRequest(printer="6e0e46db-5fca-49f0-8024-599eacdd8437", job_name=f"{order_parameters.order_id}_batch{current_batch}.form"))
        current_batch += 1

    with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer) as preform:
        clear_scene(preform)
        for stl_file_and_quantity in order_parameters.stl_files_and_quantities:
            qty_to_print = stl_file_and_quantity.quantity
            while qty_to_print >= 1:
                print(f"Importing model {stl_file_and_quantity.filename} qty {qty_to_print}/{stl_file_and_quantity.quantity}")
                new_model = preform.api.scene_import_model_post({"file": os.path.join(order_parameters.order_folder_path, stl_file_and_quantity.filename)})
                print(f"Auto orienting {new_model.id}")
                preform.api.scene_auto_orient_post(
                    SceneAutoOrientPostRequest(models=ModelsSelectionModel([new_model.id]), mode="DENTAL", tilt=0)
                )
                try:
                    print(f"Auto layouting all")
                    preform.api.scene_auto_layout_post_with_http_info(
                        SceneAutoLayoutPostRequest(models=ModelsSelectionModel("ALL"))
                    )
                    batch_has_unsaved_changed = True
                    batch_results[-1].part_quantity_in_this_print += 1
                    qty_to_print -= 1
                    print(f"Model {stl_file_and_quantity.filename} added to scene")
                except formlabs.exceptions.ApiException as e:
                    print("Not all models can fit, removing model")
                    preform.api.scene_models_id_delete(str(new_model.id))
                    save_batch_form(preform)
                    clear_scene(preform)
                except Exception as e:
                    print("Error during auto layout")
                    print(e)
                    raise e

        if batch_has_unsaved_changed:
            save_batch_form(preform)

    return batch_results


if __name__ == "__main__":
    print("Running automatic Formlabs job preparation\n")
    print("\nNew orders in those folders will be processed automatically")
    while True:
        check_input_folder(OrderType.GENERIC)
        time.sleep(DELAY_BETWEEN_NEW_ORDER_FOLDER_CHECKS_SECONDS)
