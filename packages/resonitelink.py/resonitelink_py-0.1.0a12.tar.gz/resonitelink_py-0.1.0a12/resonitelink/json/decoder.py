from .models import get_model_for_type_name
from typing import Any, Dict
from json import JSONDecoder
import logging

logger = logging.getLogger("ResoniteLinkJSONDecoder")
logger.setLevel(logging.DEBUG)

class ResoniteLinkJSONDecoder(JSONDecoder):
    """
    Custom decoder for ResoniteLink model classes.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self._object_hook, **kwargs)

    def _object_hook(self, obj : Dict[str, Any]) -> Any:
        """
        Implements logic to decode custom model structure.

        """
        type_name : Any = obj.get('$type', None)
        if type_name is not None:
            try:
                # Try retrieving a model to check if the JSON object's $type corresponds to a registered model
                model = get_model_for_type_name(type_name)
            
            except KeyError:
                # Object has $type, but no model for that type name is registered, log warning
                logger.warning(f"Encountered JSON object with unknown type name '{type_name}': {obj}")

            else:
                # Model found, JSON object will be decoded into an instance of the model's data class
                data_class : Any = model.data_class()
                for name, value in obj.items():
                    if name == "$type":
                        # Skip the '$type' entry as we already know it
                        continue
                    
                    # Try to get the property key associated with the name of the JSON attribute
                    key = model._property_name_mapping.get(name, None)

                    if key:
                        # JSON attribute is associated with a JSONProperty
                        # TODO: Type validation?
                        setattr(data_class, key, value)

                    else:
                        # JSON attribute isn't associated with a JSONProperty, log warning
                        logger.warning(f"Attribute '{name}' in JSON object isn't associated with a JSONProperty of model '{model}': {obj}")
                    
                return data_class

        return obj