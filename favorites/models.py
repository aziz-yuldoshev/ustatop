from django.conf import settings
from django.db import models

from services.models import Service


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Sevimli xizmat"
        verbose_name_plural = "Sevimli xizmatlar"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "service"],
                name="unique_user_service_favorite",
            )
        ]

    def __str__(self):
        return f"{self.user.username} — {self.service.title}"