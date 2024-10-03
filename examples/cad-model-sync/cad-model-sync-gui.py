# python3 -m pip install PySimpleGUI
# On MacOS: brew install python-tk@3.11

import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import pathlib
import formlabs
import subprocess
import sys
import time

pathToPreformServer = pathlib.Path().resolve().parents[1] / "PreFormServer.app/Contents/MacOS/PreFormServer"

def doStuff(formFilePath, selected_version, partName="part1"):
    global progress_label_textvar, progress_label
    progress_label_textvar.set("Updating Formlabs job setup...")
    progress_label.update()
    print(f"Updating with {formFilePath}")
    # In a real CAD application, the STL file would be generated and saved to a temporary location.
    # Here, we just used the pre-generated selected version
    new_version_stl_file_path = f"{selected_version}.stl"
    with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer) as preform:
        preform.api.load_form_post(formlabs.LoadFormPostRequest(file=formFilePath))
        scene_response = preform.api.scene_get()
        matching_model_ids = [model["id"] for model in scene_response["models"] if model["name"] == partName]
        if len(matching_model_ids) == 0:
            print(f"No models found with name {partName}, falling back to first model ID")
            # TODO: make error appropriate for this GUI application
            # sys.exit(1)
            matching_model_ids = [model["id"] for model in scene_response["models"][:1]]
        print(f"Found {len(matching_model_ids)} models with name {partName}")
        for model_id in matching_model_ids:
            try:
                replace_response = preform.api.scene_models_id_replace_post(model_id, formlabs.SceneModelsIdReplacePostRequest(file=new_version_stl_file_path))
                replaced_model_id = replace_response.id
                print("replace model success")
            except formlabs.exceptions.ApiException as e:
                if e.status == 400:
                    progress_label_textvar.set("")
                    progress_label.update()
                    messagebox.showerror("Error", f"Job could not be updated automatially. Please try manually in PreForm.")
                    # e.data.error == "AUTO_LAYOUT_FAILED"
                    # Goal here is that the old setup model is removed and the new one is added, but with no supports 
                    # TODO: use Preform API to simply import new model to the scene?
                    # TODO: or maybe updated replace model API to allow partial success?
            # todo: rename new model to part1?
        preform.api.scene_save_form_post(formlabs.LoadFormPostRequest(file=formFilePath))
        progress_label_textvar.set("")
        progress_label.update()
        messagebox.showinfo("Success", f"Job update completed. Opening PreForm...")
        subprocess.Popen(["/Applications/PreForm 3.34.app/Contents/MacOS/PreForm", formFilePath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to save the selected version file to a user-specified location
def save_version(selected_version):
    if selected_version not in versions:
        print("Invalid version selected.")
        return
    
    # File path of the selected version
    source_file_path = f"{selected_version}.stl"
    
    # Open file dialog to select the destination
    destination_path = filedialog.asksaveasfilename(defaultextension=".stl", 
                                                    filetypes=[("STL files", "*.stl")])
    
    if destination_path:
        # Copy the selected file to the chosen location
        shutil.copy(source_file_path, destination_path)
        print(f"Saved {selected_version}.stl to {destination_path}")

# Function to select an existing file and use it with `doStuff`
def select_file(selected_version):
    selected_file_path = filedialog.askopenfilename(filetypes=[("PreForm Job files", "*.form"), ("All files", "*.*")])
    
    if selected_file_path:
        doStuff(selected_file_path, selected_version)

# GUI Setup
root = tk.Tk()
root.title("Demo CAD Application")
root.geometry('400x200')

# Frame for the version dropdown and label
version_frame = tk.Frame(root)
version_frame.pack(pady=10)

# Label for the version dropdown
version_label = tk.Label(version_frame, text="Pretend working on CAD model version: ")
version_label.pack(side=tk.LEFT)

# Dropdown for file versions
versions = ["part1", "v2", "v3", "v4"]
selected_version = tk.StringVar(root)
selected_version.set(versions[0])  # default value

version_menu = tk.OptionMenu(version_frame, selected_version, *versions)
version_menu.pack(side=tk.LEFT)

# Button to save the selected version to a location
save_button = tk.Button(root, text="Export .STL", command=lambda: save_version(selected_version.get()))
save_button.pack(pady=10)

# Button to select an existing file and use it with `doStuff`
select_button = tk.Button(root, text="Sync Print Setup", command=lambda: select_file(selected_version.get()))
select_button.pack(pady=10)

# Label to display the progress message
progress_label_textvar = tk.StringVar(root)
progress_label = tk.Label(root, textvariable=progress_label_textvar)
progress_label.pack(pady=10)

# Run the application
root.mainloop()
