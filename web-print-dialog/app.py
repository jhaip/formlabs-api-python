import os
import sys
import time
import json
import atexit
import pathlib
from flask import Flask, request, jsonify
import requests
import formlabs_local_api_minimal as formlabs

app = Flask(__name__, static_folder="static")

# Global variable for the PreFormServer process handle
preform_server_process = None

def start_preform_server():
    print("Starting PreFormServer...")
    global preform_server_process
    # Assume the PreFormServer is located in a subfolder "PreFormServer"
    # In Docker, we use Wine to run the Windows executable.
    path_to_preform = os.path.join(os.getcwd(), "PreFormServer", "PreFormServer.exe")
    if not os.path.exists(path_to_preform):
        sys.exit("PreFormServer executable not found at: " + path_to_preform)
    preform_server_process = formlabs.PreFormApi.start_preform_sync(
        pathToPreformServer=path_to_preform, command_prefix="/usr/bin/wine"
    )
    print("PreFormServer started successfully.")

def stop_preform_server():
    global preform_server_process
    if preform_server_process:
        preform_server_process.stop_preform_server()

# Ensure the PreFormServer stops when the Flask app exits
atexit.register(stop_preform_server)

@app.route("/")
def index():
    # Serve the static UI (index.html in the "static" folder)
    return app.send_static_file("index.html")

# ------------------------------
# API Proxy Endpoints
# ------------------------------
# These endpoints proxy requests from the web UI to the PreFormServer running on localhost:44388.

@app.route("/api/<path:path>", methods=["GET", "POST"])
def api_proxy(path):
    method = request.method
    url = f"http://localhost:44388/{path}"
    try:
        if method == "GET":
            resp = requests.get(url, params=request.args)
        else:
            # Forward JSON payload if any
            json_data = request.get_json() if request.is_json else None
            resp = requests.request(method, url, json=json_data)
        # Return the response directly to the client
        return (resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------
# Print Job Submission Endpoint
# ------------------------------
@app.route("/submit_print", methods=["POST"])
def submit_print():
    # Check if file part is present
    if "file" not in request.files:
        return jsonify({"error": "No file part provided."}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    # Save the STL file to an uploads directory
    print("Saving file...")
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    filename = f"{int(time.time())}_{file.filename}"
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)

    # Get additional form data
    print("Getting form data...")
    try:
        printer = request.form["printer"]
        job_name = request.form["job_name"]
        # print_now is passed as "true" or "false"
        print_now = request.form.get("print_now", "false").lower() == "true"
        # Print setting is passed as a JSON string (from the UI dropdown)
        print_setting_json_str = request.form["print_setting_json"]
        print_setting_json = json.loads(print_setting_json_str)
    except Exception as e:
        return jsonify({"error": f"Missing or invalid form data: {e}"}), 400

    try:
        print("creating scene...")
        # 1. Create an empty scene using the selected print setting
        scene_url = "http://localhost:44388/scene/"
        resp1 = requests.post(scene_url, json=print_setting_json)
        resp1.raise_for_status()

        print("importing stl...")
        # 2. Import the STL model into the scene
        import_url = "http://localhost:44388/scene/import-model/"
        payload = {"file": file_path}
        resp2 = requests.post(import_url, json=payload)
        resp2.raise_for_status()

        print("submitting print job...")
        # 3. Submit the print job to the selected printer (async job)
        print_url = "http://localhost:44388/scene/print/?async=true"
        payload = {
            "printer": printer, # Is "Sheep" ok here?
            "job_name": job_name,
            "print_now": print_now,
        }
        resp3 = requests.post(print_url, json=payload)
        resp3.raise_for_status()

        print("getting operation ID...")
        operation_id = resp3.json().get("operationId")
        return jsonify({"operation_id": operation_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------
# Job Status Endpoint
# ------------------------------
@app.route("/job_status/<operation_id>", methods=["GET"])
def job_status(operation_id):
    url = f"http://localhost:44388/operations/{operation_id}/"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------
# Main Entry Point
# ------------------------------
if __name__ == "__main__":
    # Start the PreFormServer on startup
    start_preform_server()
    try:
        # Run Flask on 0.0.0.0:8080
        app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
    finally:
        stop_preform_server()
