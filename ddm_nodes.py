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
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (any_type,),
                "id": ("STRING", {
                    "default": "value",
                }),
            },
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    OUTPUT_NODE = False
    
    def execute(self, value, id):
        """Store the value and pass it through"""
        STORAGE[id] = value
        return (value,)


class DDM_GetNode:
    """
    Retrieve a stored value by identifier.
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {
                    "default": "value",
                }),
            },
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    OUTPUT_NODE = False
    
    @classmethod
    def VALIDATE_INPUTS(cls, id):
        """
        Always return True - validation happens at execution time
        """
        return True
    
    @classmethod
    def IS_CHANGED(cls, id):
        """
        Force re-execution every time
        """
        return float("nan")
    
    def execute(self, id):
        """
        Retrieve the stored value
        """
        if id not in STORAGE:
            print(f"Warning: DDM_GetNode - ID '{id}' not found in storage")
            print(f"Available IDs: {list(STORAGE.keys())}")
            # Return a dummy value to prevent validation errors
            return (None,)
        
        return (STORAGE[id],)


# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "DDM_SetNode": DDM_SetNode,
    "DDM_GetNode": DDM_GetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DDM_SetNode": "DDM Set Node",
    "DDM_GetNode": "DDM Get Node",
}
