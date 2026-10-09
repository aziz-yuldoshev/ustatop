from django.conf import settings
from django.db import models
from django.utils import timezone

from services.models import Service


class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Kutilmoqda"),
        ("accepted", "Qabul qilindi"),
        ("in_progress", "Jarayonda"),
        ("completed", "Tugallandi"),
        ("cancelled", "Bekor qilindi"),
        ("rejected", "Rad etildi"),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_orders"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # Buyurtma berilgan vaqtdagi narxni saqlab qolamiz
    agreed_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    address = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=20
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    customer_note = models.TextField(
        blank=True
    )

    cancel_reason = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id} — {self.customer.username} — {self.service.title}"

    @property
    def master(self):
        return self.service.master

    def mark_completed(self):
        self.status = "completed"
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at", "updated_at"])