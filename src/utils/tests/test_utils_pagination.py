from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from utils.pagination import CustomPagination


class CustomPaginationTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.pagination = CustomPagination()

        # Sample queryset (list of dummy data)
        self.queryset = list(range(1, 101))  # 100 items

    def test_paginate_valid_page(self):
        request = self.factory.get('/dummy-url/?page=2&limit=10')
        request = Request(request)

        paginated = self.pagination.paginate_queryset(self.queryset, request)
        self.assertEqual(paginated, list(range(11, 21)))  # 2nd page
        self.assertIsNotNone(self.pagination.page)

    def test_paginate_invalid_page(self):
        request = self.factory.get('/dummy-url/?page=999&limit=10')
        request = Request(request)

        paginated = self.pagination.paginate_queryset(self.queryset, request)
        self.assertEqual(paginated, [])
        self.assertIsNone(self.pagination.page)

    def test_get_paginated_response_valid(self):
        request = self.factory.get('/dummy-url/?page=1&limit=10')
        request = Request(request)

        paginated = self.pagination.paginate_queryset(self.queryset, request)
        response = self.pagination.get_paginated_response(paginated)
        self.assertEqual(response.status_code, 200)
        self.assertIn('metaData', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['metaData']['page'], 1)

    def test_get_paginated_response_invalid(self):
        self.pagination.page = None
        response = self.pagination.get_paginated_response([])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        })
