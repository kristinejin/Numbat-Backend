# define Python user-defined exceptions
class DuplicateFileError(Exception):
    """Base class for other exceptions"""
    pass

class WrongPassword(Exception):
    """Base class for other exceptions"""
    pass
