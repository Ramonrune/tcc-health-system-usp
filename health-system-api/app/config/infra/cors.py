
class Cors():


    def __init__(self):
        self.allowed_origins = [
                                "http://localhost:9000"  
                                ]


    def add_cors_headers(self, request, response):
        origin = request.headers.get("Origin")
        if origin in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, PATCH, DELETE"
            response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
            return response

        return response
        