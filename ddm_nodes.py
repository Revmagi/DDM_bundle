"""
DDM Bundle - Set/Get Nodes for ComfyUI
Clean workflow routing without spaghetti connections
"""

STORAGE = {}

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")


class DDM_SetNode:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (any_type,),
                "id": ("STRING", {"default": "value"}),
            },
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    
    def execute(self, value, id):
        STORAGE[id] = value
        return (value,)


class DDM_GetNode:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "value"}),
            },
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    
    @classmethod
    def VALIDATE_INPUTS(cls, id):
        return True
    
    @classmethod
    def IS_CHANGED(cls, id):
        return float("nan")
    
    def execute(self, id):
        if id not in STORAGE:
            raise ValueError(f"DDM Get Node Error: ID '{id}' not found in storage!")
        return (STORAGE[id],)


NODE_CLASS_MAPPINGS = {
    "DDM_SetNode": DDM_SetNode,
    "DDM_GetNode": DDM_GetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DDM_SetNode": "DDM Set Node",
    "DDM_GetNode": "DDM Get Node",
}
