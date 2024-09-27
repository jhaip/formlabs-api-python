# DiscoverDevicesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timeout_seconds** | **int** | Number of seconds to wait when discovering devices | [optional] 
**ip_address** | **str** | Local network IP address to attempt to discover a device at | [optional] 

## Example

```python
from formlabs_local_api.models.discover_devices_request import DiscoverDevicesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DiscoverDevicesRequest from a JSON string
discover_devices_request_instance = DiscoverDevicesRequest.from_json(json)
# print the JSON string representation of the object
print(DiscoverDevicesRequest.to_json())

# convert the object into a dict
discover_devices_request_dict = discover_devices_request_instance.to_dict()
# create an instance of DiscoverDevicesRequest from a dict
discover_devices_request_from_dict = DiscoverDevicesRequest.from_dict(discover_devices_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


