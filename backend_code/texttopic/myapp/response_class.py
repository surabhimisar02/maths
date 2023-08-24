class ResponseClass:
    code = None
    message = None
    data = None

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data