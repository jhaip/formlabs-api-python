# formlabs_local_api.ModifyingASceneApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auto_layout**](ModifyingASceneApi.md#auto_layout) | **POST** /scene/auto-layout/ | Auto Layout
[**auto_orient**](ModifyingASceneApi.md#auto_orient) | **POST** /scene/auto-orient/ | Auto Orient
[**auto_pack**](ModifyingASceneApi.md#auto_pack) | **POST** /scene/auto-pack/ | Auto Pack
[**auto_support**](ModifyingASceneApi.md#auto_support) | **POST** /scene/auto-support/ | Auto Support
[**create_scene**](ModifyingASceneApi.md#create_scene) | **POST** /scene/ | Create Scene
[**delete_model**](ModifyingASceneApi.md#delete_model) | **DELETE** /scene/models/{id}/ | Delete model
[**duplicate_model**](ModifyingASceneApi.md#duplicate_model) | **POST** /scene/models/{id}/duplicate/ | Duplicate model
[**import_model**](ModifyingASceneApi.md#import_model) | **POST** /scene/import-model/ | Import model
[**load_form_file**](ModifyingASceneApi.md#load_form_file) | **POST** /load-form/ | Load .form file
[**replace_model**](ModifyingASceneApi.md#replace_model) | **POST** /scene/models/{id}/replace/ | Replace model
[**update_model**](ModifyingASceneApi.md#update_model) | **POST** /scene/models/{id}/ | Update model
[**update_scene**](ModifyingASceneApi.md#update_scene) | **PUT** /scene/ | Update Scene


# **auto_layout**
> SceneModel auto_layout(auto_layout_request)

Auto Layout

Run auto layout operation. Only applies to SLA-type scenes like the Form 4

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_layout_request import AutoLayoutRequest
from formlabs_local_api.models.scene_model import SceneModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    auto_layout_request = {"models":"ALL","model_spacing_mm":1.0,"allow_overlapping_supports":false,"lock_rotation":false,"build_platform_2_optimized":false} # AutoLayoutRequest | Models to run the auto layout operation on

    try:
        # Auto Layout
        api_response = api_instance.auto_layout(auto_layout_request)
        print("The response of ModifyingASceneApi->auto_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **auto_layout_request** | [**AutoLayoutRequest**](AutoLayoutRequest.md)| Models to run the auto layout operation on | 

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | ## Bad Request  The scene will not be modified if any error occurs. The response will contain an error message.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auto_orient**
> auto_orient(auto_orient_request)

Auto Orient

Run auto orient operation

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_orient_request import AutoOrientRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    auto_orient_request = {"models":"ALL"} # AutoOrientRequest | Models to run the auto orient operation on

    try:
        # Auto Orient
        api_instance.auto_orient(auto_orient_request)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_orient: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **auto_orient_request** | [**AutoOrientRequest**](AutoOrientRequest.md)| Models to run the auto orient operation on | 

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

# **auto_pack**
> SceneModel auto_pack(auto_pack_request)

Auto Pack

Run auto pack operation. Only applies to SLS-type scenes like the Fuse 1+

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_pack_request import AutoPackRequest
from formlabs_local_api.models.scene_model import SceneModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    auto_pack_request = formlabs_local_api.AutoPackRequest() # AutoPackRequest | Auto pack parameters

    try:
        # Auto Pack
        api_response = api_instance.auto_pack(auto_pack_request)
        print("The response of ModifyingASceneApi->auto_pack:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_pack: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **auto_pack_request** | [**AutoPackRequest**](AutoPackRequest.md)| Auto pack parameters | 

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | ## Bad Request  The scene will not be modified if any error occurs. The response will contain an error message.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auto_support**
> auto_support(auto_support_request)

Auto Support

Run auto support operation

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_support_request import AutoSupportRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    auto_support_request = {"models":"ALL"} # AutoSupportRequest | Models to run the auto support operation on

    try:
        # Auto Support
        api_instance.auto_support(auto_support_request)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_support: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **auto_support_request** | [**AutoSupportRequest**](AutoSupportRequest.md)| Models to run the auto support operation on | 

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

# **create_scene**
> SceneModel create_scene(scene_type_model)

Create Scene

Create a new scene

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scene_model import SceneModel
from formlabs_local_api.models.scene_type_model import SceneTypeModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_type_model = {"machine_type":"FORM-4-0","material_code":"FLGPBK05","print_setting":"DEFAULT","layer_thickness_mm":0.025} # SceneTypeModel | Create a scene with a given printing setup. For a full list of possible settings, call the GET /list-materials/ endpoint 

    try:
        # Create Scene
        api_response = api_instance.create_scene(scene_type_model)
        print("The response of ModifyingASceneApi->create_scene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->create_scene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_type_model** | [**SceneTypeModel**](SceneTypeModel.md)| Create a scene with a given printing setup. For a full list of possible settings, call the GET /list-materials/ endpoint  | 

### Return type

[**SceneModel**](SceneModel.md)

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

# **delete_model**
> delete_model(id)

Delete model

Delete a model from the current scene

### Example


```python
import formlabs_local_api
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model

    try:
        # Delete model
        api_instance.delete_model(id)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->delete_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **duplicate_model**
> SceneModel duplicate_model(id, duplicate_model_request)

Duplicate model

Duplicate a model

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.duplicate_model_request import DuplicateModelRequest
from formlabs_local_api.models.scene_model import SceneModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    duplicate_model_request = formlabs_local_api.DuplicateModelRequest() # DuplicateModelRequest | 

    try:
        # Duplicate model
        api_response = api_instance.duplicate_model(id, duplicate_model_request)
        print("The response of ModifyingASceneApi->duplicate_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->duplicate_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **duplicate_model_request** | [**DuplicateModelRequest**](DuplicateModelRequest.md)|  | 

### Return type

[**SceneModel**](SceneModel.md)

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

# **import_model**
> ModelProperties import_model(import_model_request)

Import model

Import a model into the current scene

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.import_model_request import ImportModelRequest
from formlabs_local_api.models.model_properties import ModelProperties
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    import_model_request = {"file":"C:\\Users\\user\\Desktop\\test.stl"} # ImportModelRequest | 

    try:
        # Import model
        api_response = api_instance.import_model(import_model_request)
        print("The response of ModifyingASceneApi->import_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->import_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **import_model_request** | [**ImportModelRequest**](ImportModelRequest.md)|  | 

### Return type

[**ModelProperties**](ModelProperties.md)

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

# **load_form_file**
> SceneModel load_form_file(load_form_file_request)

Load .form file

Load a .form file and create a new scene from it

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.load_form_file_request import LoadFormFileRequest
from formlabs_local_api.models.scene_model import SceneModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    load_form_file_request = {"file":"C:\\Users\\user\\Desktop\\test.form"} # LoadFormFileRequest | Full path to the .form file to load

    try:
        # Load .form file
        api_response = api_instance.load_form_file(load_form_file_request)
        print("The response of ModifyingASceneApi->load_form_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->load_form_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **load_form_file_request** | [**LoadFormFileRequest**](LoadFormFileRequest.md)| Full path to the .form file to load | 

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Scene description |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_model**
> ReplaceModel200Response replace_model(id, replace_model_request)

Replace model

Replace a model currently in the scene with a new model, copying the existing models setup and supports

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.replace_model200_response import ReplaceModel200Response
from formlabs_local_api.models.replace_model_request import ReplaceModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    replace_model_request = formlabs_local_api.ReplaceModelRequest() # ReplaceModelRequest | 

    try:
        # Replace model
        api_response = api_instance.replace_model(id, replace_model_request)
        print("The response of ModifyingASceneApi->replace_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->replace_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **replace_model_request** | [**ReplaceModelRequest**](ReplaceModelRequest.md)|  | 

### Return type

[**ReplaceModel200Response**](ReplaceModel200Response.md)

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

# **update_model**
> update_model(id, update_model_request)

Update model

Update a model's properties

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.update_model_request import UpdateModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    update_model_request = {"position":{"x":10,"y":1,"z":2}} # UpdateModelRequest | Model properties to update

    try:
        # Update model
        api_instance.update_model(id, update_model_request)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->update_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **update_model_request** | [**UpdateModelRequest**](UpdateModelRequest.md)| Model properties to update | 

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

# **update_scene**
> SceneModel update_scene(scene_type_model)

Update Scene

Update the scene's properties

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scene_model import SceneModel
from formlabs_local_api.models.scene_type_model import SceneTypeModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_type_model = {"machine_type":"FORM-4-0","material_code":"FLGPBK05","print_setting":"DEFAULT","layer_thickness_mm":0.025} # SceneTypeModel | 

    try:
        # Update Scene
        api_response = api_instance.update_scene(scene_type_model)
        print("The response of ModifyingASceneApi->update_scene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->update_scene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_type_model** | [**SceneTypeModel**](SceneTypeModel.md)|  | 

### Return type

[**SceneModel**](SceneModel.md)

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

