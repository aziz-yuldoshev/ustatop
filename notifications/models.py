from django.conf import settings
from django.db import models


class Notification(models.Model):

    TYPE_CHOICES = (
        ("order", "Buyurtma"),
        ("review", "Sharh"),
        ("system", "Tizim"),
        ("message", "Xabar"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="system",
    )

    link = models.CharField(
        max_length=500,
        blank=True,
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Bildirishnoma"
        verbose_name_plural = "Bildirishnomalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} — {self.title}"