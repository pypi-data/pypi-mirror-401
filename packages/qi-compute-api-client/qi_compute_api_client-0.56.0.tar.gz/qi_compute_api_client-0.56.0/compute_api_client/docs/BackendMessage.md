# BackendMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** | Content of the message | [optional] [default to '']

## Example

```python
from compute_api_client.models.backend_message import BackendMessage

# TODO update the JSON string below
json = "{}"
# create an instance of BackendMessage from a JSON string
backend_message_instance = BackendMessage.from_json(json)
# print the JSON string representation of the object
print(BackendMessage.to_json())

# convert the object into a dict
backend_message_dict = backend_message_instance.to_dict()
# create an instance of BackendMessage from a dict
backend_message_from_dict = BackendMessage.from_dict(backend_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


