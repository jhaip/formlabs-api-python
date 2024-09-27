# formlabs_local_api.PrintSettingsApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_materials**](PrintSettingsApi.md#list_materials) | **GET** /list-materials/ | List Materials


# **list_materials**
> ListMaterials200Response list_materials()

List Materials

List all available materials and material settings by printer type. The returned JSON has 3 layers: Printer types (e.g. \"Form 4\"), Materials (e.g. \"Black V5\"), and Material Setting (e.g. \"0.025mm\" or \"0.100mm (Legacy)\"). These \"label\" strings at each level are the preferred way of referring to that printer types, materials, and settings. They can presented in a UI as a 3-level dropdown menu, or a flat filtered list. This list is static (it will not change for a given version of the PreFormServer executable). Each value has `scene_settings` with all data needed to create a new scene. It can be passed directly to a /scene/ POST to create a scene for that printer, material, and materialSettings. 

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.list_materials200_response import ListMaterials200Response
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
    api_instance = formlabs_local_api.PrintSettingsApi(api_client)

    try:
        # List Materials
        api_response = api_instance.list_materials()
        print("The response of PrintSettingsApi->list_materials:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PrintSettingsApi->list_materials: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListMaterials200Response**](ListMaterials200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

