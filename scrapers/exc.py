
class GroceryScrapersExceptions(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message):
        self.message = message
        super().__init__(message)



class SchemaOrgException(GroceryScrapersExceptions):
    """Error in parsing or missing portion of the Schema.org data org the page"""

    def __init__(self, message):
        super().__init__(message)