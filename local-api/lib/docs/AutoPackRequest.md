# AutoPackRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_spacing_mm** | **float** | The minimum spacing between models when packing | [optional] 

## Example

```python
from formlabs_local_api.models.auto_pack_request import AutoPackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AutoPackRequest from a JSON string
auto_pack_request_instance = AutoPackRequest.from_json(json)
# print the JSON string representation of the object
print(AutoPackRequest.to_json())

# convert the object into a dict
auto_pack_request_dict = auto_pack_request_instance.to_dict()
# create an instance of AutoPackRequest from a dict
auto_pack_request_from_dict = AutoPackRequest.from_dict(auto_pack_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


