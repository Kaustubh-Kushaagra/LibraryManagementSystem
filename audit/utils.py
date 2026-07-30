from .models import AuditLog


def log_action(user, action, details=""):

    AuditLog.objects.create(
        user=user,
        action=action,
        details=details,
    )