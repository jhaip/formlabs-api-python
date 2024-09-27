# ListMaterials200ResponsePrinterTypesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | [optional] 
**materials** | [**List[ListMaterials200ResponsePrinterTypesInnerMaterialsInner]**](ListMaterials200ResponsePrinterTypesInnerMaterialsInner.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.list_materials200_response_printer_types_inner import ListMaterials200ResponsePrinterTypesInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListMaterials200ResponsePrinterTypesInner from a JSON string
list_materials200_response_printer_types_inner_instance = ListMaterials200ResponsePrinterTypesInner.from_json(json)
# print the JSON string representation of the object
print(ListMaterials200ResponsePrinterTypesInner.to_json())

# convert the object into a dict
list_materials200_response_printer_types_inner_dict = list_materials200_response_printer_types_inner_instance.to_dict()
# create an instance of ListMaterials200ResponsePrinterTypesInner from a dict
list_materials200_response_printer_types_inner_from_dict = ListMaterials200ResponsePrinterTypesInner.from_dict(list_materials200_response_printer_types_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


