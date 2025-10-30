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
    Dynamically displays the type of data connected.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (any_type,),
            },
            "optional": {
                "id": ("STRING", {
                    "default": "value",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("*",)
    FUNCTION = "set_value"
    CATEGORY = "DDM Bundle"
    OUTPUT_NODE = True
    
    def set_value(self, value, id="value"):
        """Store the value and pass it through"""
        STORAGE[id] = value
        return (value,)


class DDM_GetNode:
    """
    Retrieve a stored value by identifier.
    Dropdown automatically shows all available Set node IDs.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        # Get list of all stored IDs for the dropdown
        stored_ids = list(STORAGE.keys())
        if not stored_ids:
            stored_ids = [""]
        
        return {
            "required": {
                "id": (stored_ids, {
                    "default": stored_ids[0] if stored_ids else ""
                }),
            },
            "optional": {
                "default": (any_type,),
            }
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("*",)
    FUNCTION = "get_value"
    CATEGORY = "DDM Bundle"
    
    @classmethod
    def VALIDATE_INPUTS(cls, id, default=None):
        """Allow validation to pass even if the value isn't stored yet"""
        return True
    
    @classmethod
    def IS_CHANGED(cls, id, default=None):
        """Force re-execution to ensure fresh values and update dropdown"""
        # This also helps refresh the dropdown list
        return float("nan")
    
    def get_value(self, id, default=None):
        """Retrieve the stored value, or return default if not found"""
        if id in STORAGE:
            return (STORAGE[id],)
        elif default is not None:
            return (default,)
        else:
            print(f"Warning: DDM_GetNode couldn't find value for id '{id}' and no default provided")
            return (None,)


# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "DDM_SetNode": DDM_SetNode,
    "DDM_GetNode": DDM_GetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DDM_SetNode": "DDM Set Node",
    "DDM_GetNode": "DDM Get Node",
}
