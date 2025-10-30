"""
DDM Bundle - Set/Get Nodes for ComfyUI
Clean workflow routing without spaghetti connections
"""

# Global storage for values
STORAGE = {}

# Wildcard type that accepts anything
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")


class DDM_SetNode:
    """
    Store any value with a unique identifier.
    Use this to clean up your workflow by avoiding long connection lines.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (any_type,),
                "id": ("STRING", {
                    "default": "my_value",
                    "multiline": False
                }),
            },
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "set_value"
    CATEGORY = "DDM Bundle"
    OUTPUT_NODE = True
    
    def set_value(self, value, id):
        """Store the value and pass it through"""
        STORAGE[id] = value
        return (value,)


class DDM_GetNode:
    """
    Retrieve a stored value by identifier.
    Must match the ID used in a Set Node.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {
                    "default": "my_value",
                    "multiline": False
                }),
            },
            "optional": {
                "default": (any_type,),
            }
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "get_value"
    CATEGORY = "DDM Bundle"
    
    @classmethod
    def VALIDATE_INPUTS(cls, id, default=None):
        """
        Allow validation to pass even if the value isn't stored yet.
        This prevents validation errors during workflow loading.
        """
        return True
    
    @classmethod
    def IS_CHANGED(cls, id, default=None):
        """
        Force re-execution every time to ensure fresh values.
        Using float("nan") ensures the node always re-executes.
        """
        return float("nan")
    
    def get_value(self, id, default=None):
        """Retrieve the stored value, or return default if not found"""
        if id in STORAGE:
            return (STORAGE[id],)
        elif default is not None:
            return (default,)
        else:
            # Fallback: return None if no value found
            print(f"Warning: DDM_GetNode couldn't find value for id '{id}' and no default provided")
            return (None,)


# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "DDM_SetNode": DDM_SetNode,
    "DDM_GetNode": DDM_GetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DDM_SetNode": "DDM Set Value",
    "DDM_GetNode": "DDM Get Value",
}
