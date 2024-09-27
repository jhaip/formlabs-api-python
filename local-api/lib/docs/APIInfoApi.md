# formlabs_local_api.APIInfoApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_api_version**](APIInfoApi.md#get_api_version) | **GET** / | Get API Version


# **get_api_version**
> GetApiVersion200Response get_api_version()

Get API Version

Get the version of the API

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.get_api_version200_response import GetApiVersion200Response
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
    api_instance = formlabs_local_api.APIInfoApi(api_client)

    try:
        # Get API Version
        api_response = api_instance.get_api_version()
        print("The response of APIInfoApi->get_api_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIInfoApi->get_api_version: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetApiVersion200Response**](GetApiVersion200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API version |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

