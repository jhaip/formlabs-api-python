# ReplaceModelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** | Full path to the file to load | [optional] 
**repair_behavior** | [**RepairBehaviorModel**](RepairBehaviorModel.md) |  | [optional] [default to RepairBehaviorModel.IGNORE]

## Example

```python
from formlabs_local_api.models.replace_model_request import ReplaceModelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceModelRequest from a JSON string
replace_model_request_instance = ReplaceModelRequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceModelRequest.to_json())

# convert the object into a dict
replace_model_request_dict = replace_model_request_instance.to_dict()
# create an instance of ReplaceModelRequest from a dict
replace_model_request_from_dict = ReplaceModelRequest.from_dict(replace_model_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


