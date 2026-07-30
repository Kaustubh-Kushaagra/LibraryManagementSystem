from django.conf import settings
from django.db import models


class AuditLog(models.Model):

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=100,
    )

    details = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = ["-timestamp"]

    def __str__(self):

        username = self.user.username if self.user else "System"

        return f"{self.timestamp:%d-%m-%Y %H:%M} - {username} - {self.action}"