class Response:
    def __init__(self, description: str, headers=None, schema=None):
        self.description = description
        self.headers = headers
        self.schema = schema

    def __repr__(self):
        return f"schema: {self.schema}"
