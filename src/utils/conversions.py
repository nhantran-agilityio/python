import json
import re
from collections import OrderedDict


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def parse_request_data(data):
    return {camel_to_snake(k): v for k, v in data.items()}


def validate_and_respond(serializer_class, instance=None, data=None, partial=False, context=None):
    serializer = serializer_class(instance, data=data, partial=partial, context=context)
    serializer.is_valid(raise_exception=True)
    return serializer, None


def flatten_bracket_keys_to_nested(data: dict) -> dict:
    """
    Convert flat keys like 'job[department]' → nested dict: {'job': {'department': ...}}
    """
    result = {}

    for key, value in data.items():
        parts = re.split(r'\[|\]', key)
        parts = [p for p in parts if p]  # remove empty

        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value

    return result


def convert_request_data_keys_to_snake_and_flat_nested(request, json_fields=None):
    if json_fields is None:
        json_fields = []

    original_data = request.data.copy()
    snake_data = OrderedDict()

    # step 1: convert camelCase to snake_case
    for key, value in original_data.items():
        snake_key = camel_to_snake(key)
        snake_data[snake_key] = value

    # step 2: convert bracket notation to nested dict
    nested_data = flatten_bracket_keys_to_nested(snake_data)

    # step 3: parse JSON string fields if needed
    for field in json_fields:
        if field in nested_data and isinstance(nested_data[field], str):
            try:
                nested_data[field] = json.loads(nested_data[field])
            except json.JSONDecodeError:
                pass  # keep as-is

    # patch back into DRF request._full_data
    request._full_data = nested_data
