from django.conf import settings
from django.db import models

from services.models import Service
from orders.models import Order


class Review(models.Model):

    RATING_CHOICES = (
        (1, "1 ⭐"),
        (2, "2 ⭐"),
        (3, "3 ⭐"),
        (4, "4 ⭐"),
        (5, "5 ⭐"),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="review",
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField(
        blank=True
    )

    is_visible = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.customer.username} — "
            f"{self.service.title} — "
            f"{self.rating} ⭐"
        )