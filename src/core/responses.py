from rest_framework.response import Response


class ApiResponse(Response):
    def __init__(self, data=None, message='', success=True, status_code=200):
        std_data = {
            "status": success,
            "message": message,
            "data": data
        }
        super().__init__(std_data, status=status_code)
