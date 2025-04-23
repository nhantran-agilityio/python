from constants.base import ROLE_ADMIN
from constants.enums import LeaveStatus


def is_pending_recall(instance):
    return instance.is_recalled and instance.recall_status == LeaveStatus.PENDING


def is_admin(request):
    return request.user.role == ROLE_ADMIN
