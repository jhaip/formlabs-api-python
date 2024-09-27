# ListMaterials200ResponsePrinterTypesInnerMaterialsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | [optional] 
**material_settings** | [**List[ListMaterials200ResponsePrinterTypesInnerMaterialsInnerMaterialSettingsInner]**](ListMaterials200ResponsePrinterTypesInnerMaterialsInnerMaterialSettingsInner.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.list_materials200_response_printer_types_inner_materials_inner import ListMaterials200ResponsePrinterTypesInnerMaterialsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListMaterials200ResponsePrinterTypesInnerMaterialsInner from a JSON string
list_materials200_response_printer_types_inner_materials_inner_instance = ListMaterials200ResponsePrinterTypesInnerMaterialsInner.from_json(json)
# print the JSON string representation of the object
print(ListMaterials200ResponsePrinterTypesInnerMaterialsInner.to_json())

# convert the object into a dict
list_materials200_response_printer_types_inner_materials_inner_dict = list_materials200_response_printer_types_inner_materials_inner_instance.to_dict()
# create an instance of ListMaterials200ResponsePrinterTypesInnerMaterialsInner from a dict
list_materials200_response_printer_types_inner_materials_inner_from_dict = ListMaterials200ResponsePrinterTypesInnerMaterialsInner.from_dict(list_materials200_response_printer_types_inner_materials_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


