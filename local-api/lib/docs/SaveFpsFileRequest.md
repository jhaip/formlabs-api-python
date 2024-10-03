# SaveFpsFileRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** | The file path to save the .fps file to | 

## Example

```python
from formlabs_local_api.models.save_fps_file_request import SaveFpsFileRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SaveFpsFileRequest from a JSON string
save_fps_file_request_instance = SaveFpsFileRequest.from_json(json)
# print the JSON string representation of the object
print(SaveFpsFileRequest.to_json())

# convert the object into a dict
save_fps_file_request_dict = save_fps_file_request_instance.to_dict()
# create an instance of SaveFpsFileRequest from a dict
save_fps_file_request_from_dict = SaveFpsFileRequest.from_dict(save_fps_file_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


