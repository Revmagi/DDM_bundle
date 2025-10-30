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
                "id": ("STRING", {"default": "value"}),
            },
        }
    
    RETURN_TYPES = (any_type, "STRING")
    RETURN_NAMES = ("value", "id_out")
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    
    def execute(self, value, id):
        STORAGE[id] = value
        print(f"[DDM Set] Stored '{id}' | Type: {type(value).__name__} | Storage now has: {list(STORAGE.keys())}")
        return (value, id)


class DDM_GetNode:
    """
    Retrieve a stored value by identifier.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger": ("STRING", {"default": ""}),
                "id": ("STRING", {"default": "value"}),
            },
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    
    @classmethod
    def IS_CHANGED(cls, trigger, id):
        return float("nan")
    
    def execute(self, trigger, id):
        print(f"[DDM Get] Looking for '{id}' | Storage currently has: {list(STORAGE.keys())}")
        
        if id not in STORAGE:
            print(f"[DDM Get] ERROR: '{id}' not found!")
            raise ValueError(f"DDM Get Node: ID '{id}' not found in storage. Available IDs: {list(STORAGE.keys())}")
        
        value = STORAGE[id]
        print(f"[DDM Get] Successfully retrieved '{id}'")
        return (value,)


NODE_CLASS_MAPPINGS = {
    "DDM_SetNode": DDM_SetNode,
    "DDM_GetNode": DDM_GetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DDM_SetNode": "DDM Set Node",
    "DDM_GetNode": "DDM Get Node",
}
```

**Key changes:**
1. Set node now outputs **both the value AND the id**
2. Get node has a **trigger input** (connect the `id_out` from Set to this)
3. Heavy debug printing to see execution order

**How to connect:**
```
[Something] → Set Node (value input)
              Set Node (id_out output) → Get Node (trigger input)
                                         Get Node → [Something else]
