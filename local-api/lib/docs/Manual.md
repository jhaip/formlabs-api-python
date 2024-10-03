# Manual


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**machine_type** | **str** | The machine type of the scene | 
**material_code** | **str** | The material code of the scene | 
**print_setting** | **str** | The print setting of the scene | [optional] 
**layer_thickness_mm** | [**ManualLayerThicknessMm**](ManualLayerThicknessMm.md) |  | 
**custom_print_setting_id** | **str** | The ID of the custom print setting used, if any. | [optional] 

## Example

```python
from formlabs_local_api.models.manual import Manual

# TODO update the JSON string below
json = "{}"
# create an instance of Manual from a JSON string
manual_instance = Manual.from_json(json)
# print the JSON string representation of the object
print(Manual.to_json())

# convert the object into a dict
manual_dict = manual_instance.to_dict()
# create an instance of Manual from a dict
manual_from_dict = Manual.from_dict(manual_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


