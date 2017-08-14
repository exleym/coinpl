"""
    Errors for API Routes
    ==========================================
    The IWBT API is designed around providing full CRUD functionality
    plus dataset access to allow complete decoupling of the data-management
    and backend from the user experience. This means the API must be
    full featured and robust, which means verbose error handling for
    the client.
    These error classes standardize the responses to various client or
    server-side errors generated when using the API. These classes are
    meant to be used with the Validator classes found in `api_validators.py`
"""
from flask import jsonify

class BaseError(object):
    """ Abstract class from which all API classes can derive an appropriate
        interface
    """
    def __init__(self):
        self.name = "BaseError (Abstract)"
        self.shallow = {"Error": "undefined"}
        self.verbose = {"Details": "undefined"}
        self.err_code = 500

    def __repr__(self):
        return "<{}>".format(self.name)

    def json_response(self, verbose=False):
        if verbose:
            data = {}
            data.update(self.shallow)
            data.update(self.verbose)
            data.update({"ErrorName": self.name})
            return jsonify(data), self.err_code
        else:
            return jsonify(self.shallow), self.err_code


class MissingJSONError(BaseError):
    def __init__(self):
        super(MissingJSONError, self).__init__()
        self.name = "MissingJSONError"
        self.err_code = 400
        self.shallow = {"Error": "POST request did contain required JSON"}
        self.verbose = {"Details": "You must POST JSON to create a new item!"}


class PostValidationError(BaseError):
    def __init__(self, missing=True):
        super(PostValidationError, self).__init__()
        self.name = "PostValidationError"
        self.err_code = 400
        self.shallow = {"Error": "POST request did not pass validation"}
        if missing:
            self.verbose = {"Details": "You missed a field!"}
        else:
            self.verbose = {"Details": "You passed an unacceptable field!"}


class DatabaseIntegrityError(BaseError):
    def __init__(self):
        super(DatabaseIntegrityError, self).__init__()
        self.name = "DatabaseIntegrityError"
        self.err_code = 400
        self.shallow = {"Error": "Insert failed due to database integrity check"}
        self.verbose = {"Details": "You attempted to add something that " + \
                        "broke the database's integrity check. This was " +\
                        "most likely a ForeignKey violation or a duplicate" + \
                        "resource."}


class MissingResourceError(BaseError):
    def __init__(self, resource_name):
        super(MissingResourceError, self).__init__()
        self.name = "MissingResourceError"
        self.err_code = 404
        self.shallow = {"Error": "The resource you requested is missing"}
        self.verbose = {"Details": "You requested a resource of class: " + \
                        "<{}>, but we could not find a matching instance".format(resource_name)}
