document.addEventListener("DOMContentLoaded", function () {
    // UI elements
    const loginForm = document.getElementById("login-form");
    const logoutSection = document.getElementById("logout-section");
    const loggedInUserSpan = document.getElementById("logged-in-user");
    const loginButton = document.getElementById("login-button");
    const logoutButton = document.getElementById("logout-button");
  
    const stlFileInput = document.getElementById("stl-file");
    const printerTypeSelect = document.getElementById("printer-type");
    const printerSelect = document.getElementById("printer");
    const printSettingSelect = document.getElementById("print-setting");
    const jobNameInput = document.getElementById("job-name");
  
    const addPrinterIpButton = document.getElementById("add-printer-ip-button");
    const discoverPrintersButton = document.getElementById("discover-printers-button");
  
    const uploadQueueButton = document.getElementById("upload-queue-button");
    const printNowButton = document.getElementById("print-now-button");
  
    const slicingProgress = document.getElementById("slicing-progress");
    const progressText = document.getElementById("progress-text");
  
    let currentOperationId = null;
    let pollingInterval = null;
    let materialsData = null;
  
    // --- Login / Logout ---
    loginButton.addEventListener("click", function () {
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      fetch("/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.access_token) {
            loggedInUserSpan.textContent = "Logged in as: " + username;
            loginForm.style.display = "none";
            logoutSection.style.display = "block";
          } else {
            alert("Login failed");
          }
        })
        .catch((err) => {
          alert("Error during login: " + err);
        });
    });
  
    logoutButton.addEventListener("click", function () {
      fetch("/api/logout/", { method: "POST" })
        .then((response) => response.json())
        .then(() => {
          loginForm.style.display = "block";
          logoutSection.style.display = "none";
          loggedInUserSpan.textContent = "";
        })
        .catch((err) => {
          alert("Error during logout: " + err);
        });
    });
  
    // --- Load Materials (Printer Types and Print Settings) ---
    function loadMaterials() {
      fetch("/api/list-materials/")
        .then((response) => response.json())
        .then((data) => {
          materialsData = data;
          printerTypeSelect.innerHTML = "";
          data.printer_types.forEach((pt) => {
            let option = document.createElement("option");
            option.value = pt.label;
            option.textContent = pt.label;
            printerTypeSelect.appendChild(option);
          });
          loadPrintSettings(printerTypeSelect.value);
        })
        .catch((err) => console.error("Error loading materials:", err));
    }
  
    function loadPrintSettings(printerType) {
      printSettingSelect.innerHTML = "";
      if (!materialsData) return;
      let ptData = materialsData.printer_types.find((pt) => pt.label === printerType);
      if (ptData) {
        ptData.materials.forEach((material) => {
          material.material_settings.forEach((setting) => {
            let option = document.createElement("option");
            // Pass the scene settings as a JSON string (to be later parsed by the submit endpoint)
            option.value = JSON.stringify(setting.scene_settings);
            option.textContent = material.label + " " + setting.label;
            printSettingSelect.appendChild(option);
          });
        });
      }
    }
  
    printerTypeSelect.addEventListener("change", function () {
      loadPrintSettings(printerTypeSelect.value);
    });
  
    // --- Load Devices (Printers) ---
    function loadDevices() {
      fetch("/api/devices/?can_print=true")
        .then((response) => response.json())
        .then((data) => {
          printerSelect.innerHTML = "";
          data.devices.forEach((device) => {
            let option = document.createElement("option");
        //     if selected_printer_data["product_name"] == PRINTER_GROUP_PRODUCT_NAME:
        //     return selected_printer_data["dashboard_queue_id"]
        // else:
        //     return selected_printer_data["id"]
            option.value = device.product_name == "Printer Group" ? device.dashboard_queue_id : device.id;
            option.textContent = `[${device.product_name}] ${device.id} - ${device.status}`;
            printerSelect.appendChild(option);
          });
        })
        .catch((err) => console.error("Error loading devices:", err));
    }
  
    // --- Add Printer by IP ---
    addPrinterIpButton.addEventListener("click", function () {
      const ip = prompt("Enter printer IP address:");
      if (ip) {
        fetch("/api/discover-devices/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ timeout_seconds: 10, ip_address: ip }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.count > 0) {
              alert("Printer successfully added");
              loadDevices();
            } else {
              alert("No printers found at that IP");
            }
          })
          .catch((err) => alert("Error discovering printer: " + err));
      }
    });
  
    // --- Discover Printers ---
    discoverPrintersButton.addEventListener("click", function () {
      alert("Starting printer discovery...");
      fetch("/api/discover-devices/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ timeout_seconds: 10 }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert("Discovery finished. Found " + data.count + " devices.");
          loadDevices();
        })
        .catch((err) => alert("Error during discovery: " + err));
    });
  
    // --- Submit Print Job ---
    function submitPrint(print_now) {
      if (stlFileInput.files.length === 0) {
        alert("Please select a .STL file to upload.");
        return;
      }
      const file = stlFileInput.files[0];
  
      const formData = new FormData();
      formData.append("file", file);
      formData.append("printer", printerSelect.value);
      formData.append("job_name", jobNameInput.value);
      formData.append("print_now", print_now);
      formData.append("print_setting_json", printSettingSelect.value);
  
      fetch("/submit_print", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.operation_id) {
            currentOperationId = data.operation_id;
            alert("Print job submitted. Operation ID: " + currentOperationId);
            startPolling();
          } else if (data.error) {
            alert("Error: " + data.error);
          }
        })
        .catch((err) => alert("Error submitting print job: " + err));
    }
  
    uploadQueueButton.addEventListener("click", function () {
      submitPrint(false);
    });
    printNowButton.addEventListener("click", function () {
      submitPrint(true);
    });
  
    // --- Polling for Job Status ---
    function startPolling() {
      slicingProgress.style.display = "block";
      pollingInterval = setInterval(function () {
        fetch("/job_status/" + currentOperationId)
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "SUCCEEDED") {
              progressText.textContent = "Print job uploaded successfully!";
              slicingProgress.value = 100;
              clearInterval(pollingInterval);
            } else if (data.status === "FAILED") {
              progressText.textContent =
                "Print job failed: " + data.result.error.message;
              clearInterval(pollingInterval);
            } else {
              let prog = data.progress ? data.progress * 100 : 0;
              progressText.textContent = "Progress: " + prog.toFixed(2) + "%";
              slicingProgress.value = prog;
            }
          })
          .catch((err) => console.error("Error polling job status:", err));
      }, 1000);
    }
  
    // --- Initial Loading ---
    loadMaterials();
    loadDevices();
  });
  