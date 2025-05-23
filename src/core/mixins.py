from rest_framework import status
from core.responses import ApiResponse


class CustomRetrieveModelMixin:
    """
    Custom retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return ApiResponse(
            data=data,
            message="Request was successful",
            status_code=status.HTTP_200_OK,
        )


class CustomUpdateModelMixin:
    """
    Custom update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        data = serializer.data
        return ApiResponse(
            data=data,
            message="Request was successful",
            status_code=status.HTTP_200_OK,
        )
