

def legacy(replaced_by=None):
    """Mark as legacy method, kept around for backwards compatibility."""

    def wrapper(func):
        func.__is_legacy = True
        func.__replaced_by = replaced_by
        return func

    return wrapper
