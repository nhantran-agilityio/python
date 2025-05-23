from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 50
    page_size = 10

    def paginate_queryset(self, queryset, request, view=None):
        """
        Store the view so we can access it in get_paginated_response
        """
        self.view = view  # store view to use later
        try:
            return super().paginate_queryset(queryset, request, view)
        except pagination.NotFound:
            self.page = None
            return []

    def get_paginated_response(self, data):
        # Get dynamic message from the view, fallback to default
        message = getattr(self.view, 'pagination_message', "Data retrieved successfully")

        if self.page is None:
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'data': [],
                "message": message,
                "status_code": status.HTTP_200_OK
            })

        return Response({
            "metaData": {
                "limit": self.page.paginator.per_page,
                "page": self.page.number,
                "totalCount": self.page.paginator.count
            },
            "data": data,
            "message": message,
            "status_code": status.HTTP_200_OK
        })
