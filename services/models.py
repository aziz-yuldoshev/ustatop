from django.conf import settings
from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=50,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Xizmat kategoriyasi"
        verbose_name_plural = "Xizmat kategoriyalari"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MasterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="master_profile"
    )

    profession = models.CharField(
        max_length=150
    )

    bio = models.TextField(
        blank=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    service_area = models.CharField(
        max_length=255,
        blank=True
    )

    hourly_rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_available = models.BooleanField(
        default=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    completed_orders = models.PositiveIntegerField(
        default=0
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Usta profili"
        verbose_name_plural = "Usta profillari"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.get_full_name() or self.user.username} "
            f"— {self.profession}"
        )


class Service(models.Model):
    PRICE_TYPE_CHOICES = [
        ("fixed", "Belgilangan narx"),
        ("hourly", "Soatlik"),
        ("from", "Boshlang‘ich narx"),
    ]

    master = models.ForeignKey(
        MasterProfile,
        on_delete=models.CASCADE,
        related_name="services"
    )

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="services"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    price_type = models.CharField(
        max_length=20,
        choices=PRICE_TYPE_CHOICES,
        default="fixed"
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.master}"


