class ZvukAPIError(RuntimeError):
    pass

class ZvukAuthError(ZvukAPIError):
    pass

class ZvukValidationError(ZvukAPIError):
    pass