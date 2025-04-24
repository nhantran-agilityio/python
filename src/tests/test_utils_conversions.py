import unittest
from unittest.mock import MagicMock
from utils.conversions import (
    camel_to_snake,
    parse_request_data,
    validate_and_respond,
    flatten_bracket_keys_to_nested,
    convert_request_data_keys_to_snake_and_flat_nested
)


class DummySerializer:
    def __init__(self, instance=None, data=None, partial=False, context=None):
        self.data = data
        self._is_valid = data.get("valid", True)
        self._errors = {"field": "error"} if not self._is_valid else {}

    def is_valid(self):
        return self._is_valid

    @property
    def errors(self):
        return self._errors


class UtilsTestCase(unittest.TestCase):

    def test_camel_to_snake(self):
        self.assertEqual(camel_to_snake("camelCaseTest"), "camel_case_test")
        self.assertEqual(camel_to_snake("CamelCaseTest"), "camel_case_test")

    def test_parse_request_data(self):
        data = {"firstName": "John", "lastName": "Doe"}
        expected = {"first_name": "John", "last_name": "Doe"}
        self.assertEqual(parse_request_data(data), expected)

    def test_validate_and_respond_valid(self):
        data = {"valid": True}
        serializer, errors = validate_and_respond(DummySerializer, data=data)
        self.assertIsNotNone(serializer)
        self.assertIsNone(errors)

    def test_validate_and_respond_invalid(self):
        data = {"valid": False}
        serializer, errors = validate_and_respond(DummySerializer, data=data)
        self.assertIsNone(serializer)
        self.assertEqual(errors, {"field": "error"})

    def test_flatten_bracket_keys_to_nested(self):
        flat = {
            "job[title]": "Engineer",
            "job[department]": "Tech",
            "user[name]": "Alice"
        }
        expected = {
            "job": {"title": "Engineer", "department": "Tech"},
            "user": {"name": "Alice"}
        }
        self.assertEqual(flatten_bracket_keys_to_nested(flat), expected)


class TestConvertRequestDataKeysToSnakeAndFlatNested(unittest.TestCase):

    def test_camel_case_conversion(self):
        request = MagicMock()
        request.data = {'camelCaseKey': 'value'}
        convert_request_data_keys_to_snake_and_flat_nested(request)
        self.assertEqual(request._full_data, {'camel_case_key': 'value'})

    def test_bracket_notation_conversion(self):
        request = MagicMock()
        request.data = {'job[department]': 'Tech'}
        convert_request_data_keys_to_snake_and_flat_nested(request)
        self.assertEqual(request._full_data, {'job': {'department': 'Tech'}})

    def test_json_field_parsing(self):
        request = MagicMock()
        request.data = {'jsonField': '{"key": "value"}'}
        convert_request_data_keys_to_snake_and_flat_nested(request, json_fields=['json_field'])
        self.assertEqual(request._full_data, {'json_field': {'key': 'value'}})

    def test_invalid_json_field(self):
        request = MagicMock()
        request.data = {'jsonField': 'invalid json'}
        convert_request_data_keys_to_snake_and_flat_nested(request, json_fields=['json_field'])
        self.assertEqual(request._full_data, {'json_field': 'invalid json'})

    def test_original_data_not_modified(self):
        request = MagicMock()
        original_data = {'camelCaseKey': 'value'}
        request.data = original_data.copy()
        convert_request_data_keys_to_snake_and_flat_nested(request)
        self.assertEqual(request.data, original_data)

    def test_request_full_data_updated(self):
        request = MagicMock()
        request.data = {'camelCaseKey': 'value'}
        convert_request_data_keys_to_snake_and_flat_nested(request)
        self.assertEqual(request._full_data, {'camel_case_key': 'value'})
