from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import pathlib
from pathlib import Path
import formlabs_local_api as formlabs
import subprocess
import sys

# Directory where jobs are stored
JOBS_DIR = 'jobs'
UPLOAD_FOLDER = '/tmp'

pathToPreformServer = None
if sys.platform == 'win32':
    pathToPreformServer = pathlib.Path().resolve().parents[1] / "PreFormServer.exe"
elif sys.platform == 'darwin':
    pathToPreformServer = pathlib.Path().resolve().parents[1] / "PreFormServer.app/Contents/MacOS/PreFormServer"
else:
    print("Unsupported platform")
    sys.exit(1)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


class PreFormApi:
    def __init__(self):
        self.api = None

    def load_form(self, form_file_path):
        print(f"Loading form: {form_file_path}")
        self.api.load_form_post(formlabs.LoadFormPostRequest(file=form_file_path))

    def import_model(self, model_path):
        self.api.scene_import_model_post({"file": model_path})

    def auto_pack(self):
        self.api.scene_auto_pack_post(formlabs.SceneAutoPackPostRequest())

    def save_screenshot(self, screenshot_path):
        self.api.scene_save_screenshot_post(formlabs.SceneSaveScreenshotPostRequest(file=screenshot_path))

    def get_scene(self):
        return self.api.scene_get()

    def save_form(self, form_file_path):
        self.api.scene_save_form_post(formlabs.LoadFormPostRequest(file=form_file_path))

api = PreFormApi()


def merge(job_id, uploaded_file_paths):
    job_folder = os.path.join(JOBS_DIR, job_id)
    existing_job_form_path = os.path.abspath(os.path.join(job_folder, f"{job_id}.form"))
    existing_screenshot_path = os.path.abspath(os.path.join(job_folder, f"{job_id}.png"))
    existing_metadata_path = os.path.abspath(os.path.join(job_folder, 'metadata.json'))
    print("loading form")
    api.load_form(existing_job_form_path)
    for file_path in uploaded_file_paths:
        print("importing model")
        api.import_model(file_path)
    try:
        print("running auto pack")
        api.auto_pack()
    except:
        print("ERROR running auto pack")
        raise Exception("Failed to auto pack")
    scene_data = api.get_scene().to_dict()
    for model in scene_data['models']:
        if not model["in_bounds"]:
            print("ERROR: model out of build volume.")
            raise Exception("Failed post auto pack in-bounds model check")
    print("saving screenshot")
    api.save_screenshot(existing_screenshot_path)
    print("saving .form file")
    api.save_form(existing_job_form_path)
    print("getting scene data")
    return scene_data


def get_job_form_path(job_id):
    job_folder = os.path.join(JOBS_DIR, job_id)
    form_files = [f for f in os.listdir(job_folder) if f.endswith('.form')]
    if form_files:
        return os.path.join(job_folder, form_files[0])
    return None


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/list', methods=['GET'])
def list_jobs():
    jobs = []
    job_folders = [x for x in os.listdir(JOBS_DIR) if x.isdigit()]
    sorted_job_folders = sorted(job_folders, key=lambda x: int(x))
    for job_folder in sorted_job_folders:
        job_path = os.path.join(JOBS_DIR, job_folder)
        if os.path.isdir(job_path):
            metadata_path = os.path.join(job_path, 'metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path) as f:
                    metadata = json.load(f)
                jobs.append(metadata)
    return jsonify(jobs)

@app.route('/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    job_folder = os.path.join(JOBS_DIR, job_id)
    if os.path.exists(job_folder):
        for file in os.listdir(job_folder):
            os.remove(os.path.join(job_folder, file))
        os.rmdir(job_folder)
        return jsonify({'success': 'Job deleted successfully'})
    return jsonify({'error': 'Job not found'}), 404

@app.route('/download/<job_id>', methods=['GET'])
def download_form(job_id):
    form_path = get_job_form_path(job_id)
    if form_path:
        return send_from_directory(os.path.dirname(form_path), os.path.basename(form_path), as_attachment=True)
    return jsonify({'error': 'Job not found or form file missing'}), 404

@app.route('/thumbnails/<job_id>/thumbnail.png', methods=['GET'])
def download_image(job_id):
    job_folder = os.path.join(JOBS_DIR, job_id)
    img_files = [f for f in os.listdir(job_folder) if f.endswith('.png')]
    if img_files:
        return send_from_directory(job_folder, img_files[0], as_attachment=True)
    return jsonify({'error': 'Job not found or image file missing'}), 404

@app.route('/new-from-form', methods=['POST'])
def create_new_from_form():
    data = request.form
    owner_email = data.get('owner_email')
    owner_name = data.get('owner_name', owner_email)
    file = request.files['file']
    # Creat a new ID for the job
    last_id = max([0] + [int(x) for x in os.listdir(JOBS_DIR) if x.isdigit()])
    id = last_id + 1
    job_name = f"{id}"
    # Make new directory in with the name of the ID
    job_folder = os.path.join(JOBS_DIR, job_name)
    os.makedirs(job_folder)
    # Save the file to the new directory with the name ID.form
    filename = f"{job_name}.form"
    file.save(os.path.join(job_folder, filename))
    # Use API to get metadata and screenshot from scene
    api.load_form(os.path.abspath(os.path.join(job_folder, filename)))
    scene_metadata = api.get_scene().to_dict()
    metadata = {
        'id': id,
        'owner': {'name': owner_name, 'email': owner_email},
        'people': [{'name': owner_name, 'email': owner_email}],
        'scene': scene_metadata
    }
    # Save metadata to the new directory with the name metadata.json
    with open(os.path.join(job_folder, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
    # Use API to get screenshot of new file
    # Save screenshot to the new directory with the name screenshot.png
    api.save_screenshot(os.path.abspath(os.path.join(job_folder, f"{job_name}.png")))
    return jsonify({'success': 'New job created successfully', 'id': id})


@app.route('/import-models/<job_id>', methods=['POST'])
def import_parts(job_id):
    data = request.form
    person_email = data.get('person_email')
    person_name = data.get('person_name', person_email)
    files = request.files.getlist('files')

    job_folder = os.path.join(JOBS_DIR, job_id)
    if not os.path.exists(job_folder):
        return jsonify({'error': 'Job ID not found'}), 404

    # Save these to a temp directory instead
    uploaded_file_paths = []
    for file in files:
        if file.filename.endswith(('.stl', '.form')):
            filename = secure_filename(file.filename)
            saved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_file_path)
            uploaded_file_paths.append(saved_file_path)

    try:
        scene_data = merge(job_id, uploaded_file_paths)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Update metadata
    metadata_path = os.path.join(job_folder, 'metadata.json')
    if os.path.exists(metadata_path):
        with open(metadata_path) as f:
            metadata = json.load(f)
        metadata['people'].append({'name': person_name, 'email': person_email})
        metadata['scene'] = scene_data
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

    return jsonify({'success': 'Parts added successfully to the job'})

if __name__ == '__main__':
    with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer) as preform:
        api.api = preform.api
        subprocess.Popen(["open", "http://localhost:8323"])
        app.run(port=8323, debug=False)
