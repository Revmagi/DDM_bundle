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
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (any_type,),
                "id": ("STRING", {
                    "default": "value",
                    "multiline": False
                }),
            },
        }
    
    RETURN_TYPES = (any_type,)
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
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {
                    "default": "value",
                    "multiline": False
                }),
            },
            "optional": {
                "default": (any_type,),
            },
        }
    
    RETURN_TYPES = (any_type,)
    FUNCTION = "get_value"
    CATEGORY = "DDM Bundle"
    
    @classmethod
    def VALIDATE_INPUTS(cls, id, default=None, **kwargs):
        """
        CRITICAL: Always return True to pass validation.
        This prevents the node from being marked invalid during workflow loading
        when STORAGE is empty (before Set nodes have executed).
        """
        return True
    
    @classmethod
    def IS_CHANGED(cls, id, default=None, **kwargs):
        """
        Force re-execution every time.
        This ensures we always get fresh values from STORAGE.
        """
        return float("nan")
    
    def get_value(self, id, default=None, **kwargs):
        """
        Retrieve the stored value.
        By the time this executes, Set nodes should have already run.
        """
        if id in STORAGE:
            return (STORAGE[id],)
        elif default is not None:
            return (default,)
        else:
            # This should rarely happen if the workflow is properly connected
            print(f"Warning: DDM_GetNode couldn't find value for id '{id}'")
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
