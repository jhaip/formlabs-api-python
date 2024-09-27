# DuplicateModelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of duplicates to create | [optional] 

## Example

```python
from formlabs_local_api.models.duplicate_model_request import DuplicateModelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DuplicateModelRequest from a JSON string
duplicate_model_request_instance = DuplicateModelRequest.from_json(json)
# print the JSON string representation of the object
print(DuplicateModelRequest.to_json())

# convert the object into a dict
duplicate_model_request_dict = duplicate_model_request_instance.to_dict()
# create an instance of DuplicateModelRequest from a dict
duplicate_model_request_from_dict = DuplicateModelRequest.from_dict(duplicate_model_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


