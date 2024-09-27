# DiscoverDevices200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of newly discovered devices | [optional] 
**devices** | [**List[DeviceStatusModel]**](DeviceStatusModel.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.discover_devices200_response import DiscoverDevices200Response

# TODO update the JSON string below
json = "{}"
# create an instance of DiscoverDevices200Response from a JSON string
discover_devices200_response_instance = DiscoverDevices200Response.from_json(json)
# print the JSON string representation of the object
print(DiscoverDevices200Response.to_json())

# convert the object into a dict
discover_devices200_response_dict = discover_devices200_response_instance.to_dict()
# create an instance of DiscoverDevices200Response from a dict
discover_devices200_response_from_dict = DiscoverDevices200Response.from_dict(discover_devices200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


