# formlabs_local_api.DevicesApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**discover_devices**](DevicesApi.md#discover_devices) | **POST** /discover-devices/ | Discover Devices
[**get_device**](DevicesApi.md#get_device) | **GET** /devices/{id}/ | Get Device
[**get_devices**](DevicesApi.md#get_devices) | **GET** /devices/ | Get Devices


# **discover_devices**
> DiscoverDevices200Response discover_devices(discover_devices_request)

Discover Devices

Discover new devices on the network

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.discover_devices200_response import DiscoverDevices200Response
from formlabs_local_api.models.discover_devices_request import DiscoverDevicesRequest
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
    api_instance = formlabs_local_api.DevicesApi(api_client)
    discover_devices_request = {"timeout_seconds":10} # DiscoverDevicesRequest | 

    try:
        # Discover Devices
        api_response = api_instance.discover_devices(discover_devices_request)
        print("The response of DevicesApi->discover_devices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->discover_devices: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **discover_devices_request** | [**DiscoverDevicesRequest**](DiscoverDevicesRequest.md)|  | 

### Return type

[**DiscoverDevices200Response**](DiscoverDevices200Response.md)

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

# **get_device**
> DeviceStatusModel get_device(id)

Get Device

Get a previously discovered device's status

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.device_status_model import DeviceStatusModel
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
    api_instance = formlabs_local_api.DevicesApi(api_client)
    id = 'id_example' # str | The unique identifier of the printer

    try:
        # Get Device
        api_response = api_instance.get_device(id)
        print("The response of DevicesApi->get_device:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->get_device: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the printer | 

### Return type

[**DeviceStatusModel**](DeviceStatusModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices**
> GetDevices200Response get_devices()

Get Devices

List of previously discovered device statuses

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.get_devices200_response import GetDevices200Response
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
    api_instance = formlabs_local_api.DevicesApi(api_client)

    try:
        # Get Devices
        api_response = api_instance.get_devices()
        print("The response of DevicesApi->get_devices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->get_devices: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetDevices200Response**](GetDevices200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

