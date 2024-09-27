# ListMaterials200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**printer_types** | [**List[ListMaterials200ResponsePrinterTypesInner]**](ListMaterials200ResponsePrinterTypesInner.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.list_materials200_response import ListMaterials200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListMaterials200Response from a JSON string
list_materials200_response_instance = ListMaterials200Response.from_json(json)
# print the JSON string representation of the object
print(ListMaterials200Response.to_json())

# convert the object into a dict
list_materials200_response_dict = list_materials200_response_instance.to_dict()
# create an instance of ListMaterials200Response from a dict
list_materials200_response_from_dict = ListMaterials200Response.from_dict(list_materials200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


