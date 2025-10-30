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
