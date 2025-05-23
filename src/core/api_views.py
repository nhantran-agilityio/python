from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated

from core.responses import ApiResponse


class CommonViewSet:
    """
    Common view set with standardized response
    """

    def ok(self, data=None, message="Request was successful"):
        return ApiResponse(data=data, message=message,
                           status_code=status.HTTP_200_OK)

    def created(self, data=None, message="Created successfully"):
        return ApiResponse(data=data, message=message,
                           status_code=status.HTTP_201_CREATED)

    def no_content(self, message="No content"):
        return ApiResponse(data=None, message=message,
                           status_code=status.HTTP_204_NO_CONTENT)

    def not_found(self, message="Resource not found"):
        return ApiResponse(data=None, message=message,
                           status_code=status.HTTP_404_NOT_FOUND)

    def forbidden(self, message="Permission denied"):
        return ApiResponse(data=None, message=message,
                           status_code=status.HTTP_403_FORBIDDEN)

    def bad_request(self, message="Bad request", code=None):
        return ApiResponse(
            data={"code": code},
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def not_implemented(self, message="Not implemented") -> ApiResponse:
        return ApiResponse(data=None, message=message,
                           status_code=status.HTTP_501_NOT_IMPLEMENTED)


class AuthenticatedViewSet:
    permission_classes = [IsAuthenticated]


class BaseViewSet(ViewSet, CommonViewSet):
    """
    Base view set for views accept DTO data rather than Django model
    """


class BaseModelViewSet(ModelViewSet, CommonViewSet):
    """
    Base view set for Django model
    """
    def finalize_response(self, request, response, *args, **kwargs):
        """
        Wrap non-standard responses in a consistent API format
        """
        response = super().finalize_response(request, response, *args, **kwargs)

        if not isinstance(response, Response):
            return ApiResponse(
                data=None,
                message="Internal server error: Invalid response type",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # If already wrapped in standardized format, return as is
        if isinstance(response.data, dict) and all(k in response.data for k in ("data", "message", "status_code")):
            return response

        wrapped_response = ApiResponse(
            data=response.data,
            message="Request completed",
            status_code=response.status_code
        )

        wrapped_response.accepted_renderer = response.accepted_renderer
        wrapped_response.accepted_media_type = response.accepted_media_type
        wrapped_response.renderer_context = response.renderer_context

        return wrapped_response


class BaseAuthenticatedViewSet(BaseViewSet, AuthenticatedViewSet):
    """
    Base view set with authentication
    """


class BaseAuthenticatedModelViewSet(BaseModelViewSet, AuthenticatedViewSet):
    """
    Base view set for Django model with authentication
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return self.ok(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.ok(data=serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.created(data=response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.ok(data=response.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.no_content(message="Deleted successfully")
