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
    Store any value with a unique identifier and pass it through.
    """
    
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
        print(f"✓ [DDM Set] Stored '{id}' successfully")
        return (value,)


class DDM_GetNode:
    """
    Retrieve a stored value by identifier.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "value"}),
            },
            "optional": {
                "default": (any_type,),
            },
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    
    @classmethod
    def IS_CHANGED(cls, id, default=None):
        return float("nan")
    
    def execute(self, id, default=None):
        print(f"→ [DDM Get] Attempting to retrieve '{id}'")
        print(f"  Current storage: {list(STORAGE.keys())}")
        
        if id not in STORAGE:
            if default is not None:
                print(f"⚠ [DDM Get] '{id}' not found, using default value")
                return (default,)
            else:
                error_msg = (
                    f"\n{'='*60}\n"
                    f"DDM Get Node Error: ID '{id}' not found!\n"
                    f"Current storage: {list(STORAGE.keys())}\n\n"
                    f"Troubleshooting:\n"
                    f"1. Make sure there's a Set Node with id='{id}'\n"
                    f"2. The Set Node OUTPUT must be connected to your workflow\n"
                    f"3. The Set Node must lead to a final output node\n"
                    f"4. Try adding a 'default' input to this Get Node as backup\n"
                    f"{'='*60}\n"
                )
                print(error_msg)
                raise ValueError(error_msg)
        
        print(f"✓ [DDM Get] Successfully retrieved '{id}'")
        return (STORAGE[id],)


NODE_CLASS_MAPPINGS = {
    "DDM_SetNode": DDM_SetNode,
    "DDM_GetNode": DDM_GetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DDM_SetNode": "DDM Set Node",
    "DDM_GetNode": "DDM Get Node",
}
