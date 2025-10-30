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
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    OUTPUT_NODE = True  # CRITICAL: Forces execution even without output connections
    
    def execute(self, value, id):
        STORAGE[id] = value
        print(f"[DDM Set] Stored '{id}' | Storage: {list(STORAGE.keys())}")
        return {"ui": {"text": [f"Stored: {id}"]}, "result": (value,)}


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
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "DDM Bundle"
    
    @classmethod
    def IS_CHANGED(cls, id):
        # Always re-execute
        return float("nan")
    
    def execute(self, id):
        print(f"[DDM Get] Looking for '{id}' | Available: {list(STORAGE.keys())}")
        
        if id not in STORAGE:
            raise ValueError(
                f"Get Node Error: '{id}' not found!\n"
                f"Available IDs: {list(STORAGE.keys())}\n"
                f"Make sure the Set node with id='{id}' is connected to your workflow."
            )
        
        return (STORAGE[id],)


NODE_CLASS_MAPPINGS = {
    "DDM_SetNode": DDM_SetNode,
    "DDM_GetNode": DDM_GetNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DDM_SetNode": "DDM Set Node",
    "DDM_GetNode": "DDM Get Node",
}
```

**The KEY fix:** `OUTPUT_NODE = True` on Set node

This tells ComfyUI "execute this node even if nothing uses its output" - which is essential for Set nodes to work.

**However**, there's still one requirement: **The Set node must be connected to something in your workflow that leads to the final output.** Otherwise ComfyUI won't include it in the execution graph at all.

So the workflow should be:
```
Input → Set Node → Continue your workflow → Output
           ↓ (stores value)
           (no connection)
           ↑ (retrieves value)
        Get Node → Use somewhere else
