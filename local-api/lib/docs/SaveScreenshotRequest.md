# SaveScreenshotRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** | The file path to save the .png screenshot to | 
**view_type** | **str** | The type of view to use when taking the screenshot | [optional] [default to 'ZOOM_ON_MODELS']
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.save_screenshot_request import SaveScreenshotRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SaveScreenshotRequest from a JSON string
save_screenshot_request_instance = SaveScreenshotRequest.from_json(json)
# print the JSON string representation of the object
print(SaveScreenshotRequest.to_json())

# convert the object into a dict
save_screenshot_request_dict = save_screenshot_request_instance.to_dict()
# create an instance of SaveScreenshotRequest from a dict
save_screenshot_request_from_dict = SaveScreenshotRequest.from_dict(save_screenshot_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


