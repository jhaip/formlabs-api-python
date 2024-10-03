# formlabs_local_api.ExportingApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**save_form_file**](ExportingApi.md#save_form_file) | **POST** /scene/save-form/ | Save .form file
[**save_fps_file**](ExportingApi.md#save_fps_file) | **POST** /scene/save-fps-file/ | Save FPS file
[**save_screenshot**](ExportingApi.md#save_screenshot) | **POST** /scene/save-screenshot/ | Save screenshot file


# **save_form_file**
> save_form_file(load_form_file_request)

Save .form file

Save the current scene to a .form file

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.load_form_file_request import LoadFormFileRequest
from formlabs_local_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:44388
# See configuration.py for a list of all supported configuration parameters.
configuration = formlabs_local_api.Configuration(
    host = "http://localhost:44388"
)


# Enter a context with an instance of the API client
with formlabs_local_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = formlabs_local_api.ExportingApi(api_client)
    load_form_file_request = {"file":"C:\\Users\\user\\Desktop\\test.form"} # LoadFormFileRequest | Full path where the file should be saved

    try:
        # Save .form file
        api_instance.save_form_file(load_form_file_request)
    except Exception as e:
        print("Exception when calling ExportingApi->save_form_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **load_form_file_request** | [**LoadFormFileRequest**](LoadFormFileRequest.md)| Full path where the file should be saved | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_fps_file**
> save_fps_file(save_fps_file_request)

Save FPS file

Save the print settings of the current scene to a .fps file

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.save_fps_file_request import SaveFpsFileRequest
from formlabs_local_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:44388
# See configuration.py for a list of all supported configuration parameters.
configuration = formlabs_local_api.Configuration(
    host = "http://localhost:44388"
)


# Enter a context with an instance of the API client
with formlabs_local_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = formlabs_local_api.ExportingApi(api_client)
    save_fps_file_request = {"file":"C:\\Users\\user\\Desktop\\custom-grey.fps"} # SaveFpsFileRequest | Full path where the FPS file should be saved

    try:
        # Save FPS file
        api_instance.save_fps_file(save_fps_file_request)
    except Exception as e:
        print("Exception when calling ExportingApi->save_fps_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **save_fps_file_request** | [**SaveFpsFileRequest**](SaveFpsFileRequest.md)| Full path where the FPS file should be saved | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_screenshot**
> save_screenshot(save_screenshot_request)

Save screenshot file

Save a screenshot of the current scene.

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.save_screenshot_request import SaveScreenshotRequest
from formlabs_local_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:44388
# See configuration.py for a list of all supported configuration parameters.
configuration = formlabs_local_api.Configuration(
    host = "http://localhost:44388"
)


# Enter a context with an instance of the API client
with formlabs_local_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = formlabs_local_api.ExportingApi(api_client)
    save_screenshot_request = {"file":"C:\\Users\\user\\Desktop\\screenshot.png"} # SaveScreenshotRequest | Full path where the image should be saved

    try:
        # Save screenshot file
        api_instance.save_screenshot(save_screenshot_request)
    except Exception as e:
        print("Exception when calling ExportingApi->save_screenshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **save_screenshot_request** | [**SaveScreenshotRequest**](SaveScreenshotRequest.md)| Full path where the image should be saved | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

