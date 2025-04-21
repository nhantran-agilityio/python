from rest_framework import pagination
from rest_framework.response import Response


class LeaveApplicationPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 50
    page_size = 10

    def paginate_queryset(self, queryset, request, view=None):
        """
        Override paginate_queryset to handle invalid page numbers.
        """
        try:
            return super().paginate_queryset(queryset, request, view)
        except pagination.NotFound:
            # Return an empty list if the page does not exist
            self.page = None
            return []

    def get_paginated_response(self, data):
        """
        Return a paginated response with an empty array if the page is invalid.
        """
        if self.page is None:
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'results': []
            })
        else:
            return Response({
                "metaData": {
                    "limit": self.page.paginator.per_page,
                    "page": self.page.number,
                    "totalCount": self.page.paginator.count
                },
                "results": data
            })
        return super().get_paginated_response(data)
