# PrintRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**printer** | **str** | Printer serial name, IP address, or Fleet Control Queue ID | 
**job_name** | **str** |  | 

## Example

```python
from formlabs_local_api.models.print_request import PrintRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PrintRequest from a JSON string
print_request_instance = PrintRequest.from_json(json)
# print the JSON string representation of the object
print(PrintRequest.to_json())

# convert the object into a dict
print_request_dict = print_request_instance.to_dict()
# create an instance of PrintRequest from a dict
print_request_from_dict = PrintRequest.from_dict(print_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


