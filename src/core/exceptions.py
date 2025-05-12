import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import force_str

logger = logging.getLogger(__name__)


class CustomExceptionHandler:
    """
    Class-based exception handler for DRF that logs exceptions
    and returns a standardized error response.
    """

    def handle(self, exc, context):
        """
        Entry point to handle exceptions.
        """
        response = exception_handler(exc, context)
        request = context.get("request", None)
        user = getattr(request, "user", None)
        path = request.get_full_path() if request else "unknown"

        if response is not None:
            return self._handle_known_exception(request, response, exc, user, path)

        return self._handle_unknown_exception(request, exc, user, path)

    def _handle_known_exception(self, request, response, exc, user, path):
        """
        Handles exceptions with existing DRF responses (e.g. 400, 403).
        """
        logger.warning(
            f"[{request.method}] {path} | Status {response.status_code} | User: {user} | Exception: {exc}"
        )

        message = force_str(response.data.get("detail", "An error occurred"))
        errors = response.data if "detail" not in response.data else None

        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors,
            },
            status=response.status_code,
        )

    def _handle_unknown_exception(self, request, exc, user, path):
        """
        Handles unhandled or internal exceptions (500+).
        """
        logger.error(
            f"[{request.method}] {path} | Status 500 | User: {user} | Unhandled exception: {exc}",
            exc_info=True,
        )

        return Response(
            {
                "success": False,
                "message": "Internal server error. Please try again later.",
                "errors": None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def custom_exception_handler(exc, context):
    return CustomExceptionHandler().handle(exc, context)
