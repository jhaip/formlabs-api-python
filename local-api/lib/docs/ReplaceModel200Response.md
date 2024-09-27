# ReplaceModel200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | **List[str]** |  | [optional] 
**model_properties** | [**ModelProperties**](ModelProperties.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.replace_model200_response import ReplaceModel200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceModel200Response from a JSON string
replace_model200_response_instance = ReplaceModel200Response.from_json(json)
# print the JSON string representation of the object
print(ReplaceModel200Response.to_json())

# convert the object into a dict
replace_model200_response_dict = replace_model200_response_instance.to_dict()
# create an instance of ReplaceModel200Response from a dict
replace_model200_response_from_dict = ReplaceModel200Response.from_dict(replace_model200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


