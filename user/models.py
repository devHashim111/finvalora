import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Choices


class ThemeChoices(models.TextChoices):
    LIGHT = "light", "Light"
    DARK = "dark", "Dark"
    SYSTEM = "system", "System"


class LanguageChoices(models.TextChoices):
    ENGLISH = "en", "English"
    URDU = "ur", "Urdu"


class KYCStatus(models.TextChoices):
    NOT_STARTED = "not_started", "Not Started"
    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


class DeviceType(models.TextChoices):
    WEB = "web", "Web"
    MOBILE = "mobile", "Mobile"
    TABLET = "tablet", "Tablet"
    DESKTOP = "desktop", "Desktop"


class APIProvider(models.TextChoices):
    BINANCE = "binance", "Binance"
    BYBIT = "bybit", "Bybit"
    COINBASE = "coinbase", "Coinbase"
    KRAKEN = "kraken", "Kraken"


class UserRole(models.TextChoices):
    SUPERUSER = "superuser", "Superuser"
    USER = "user", "User"
# Custom User


class CustomUser(AbstractUser):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    country = models.CharField(
        max_length=80,
        blank=True
    )

    timezone = models.CharField(
        max_length=60,
        default="UTC"
    )

    language = models.CharField(
        max_length=10,
        choices=LanguageChoices.choices,
        default=LanguageChoices.ENGLISH
    )

    avatar = models.URLField(blank=True)

    is_email_verified = models.BooleanField(default=False)

    is_phone_verified = models.BooleanField(default=False)

    is_2fa_enabled = models.BooleanField(default=False)

    kyc_status = models.CharField(
        max_length=20,
        choices=KYCStatus.choices,
        default=KYCStatus.NOT_STARTED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-created_at"]



    def save(self, *args, **kwargs):
        # Sync Django superuser flag with the admin role
        if self.is_superuser:
            self.role = UserRole.SUPERUSER
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"


# Profile


class UserProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    bio = models.TextField(blank=True)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(blank=True)

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}"



# User Preferences


class UserPreference(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="preferences"
    )

    theme = models.CharField(
        max_length=20,
        choices=ThemeChoices.choices,
        default=ThemeChoices.SYSTEM
    )

    chart_theme = models.CharField(
        max_length=30,
        default="dark"
    )

    default_exchange = models.CharField(
        max_length=50,
        default="Binance"
    )

    default_timeframe = models.CharField(
        max_length=10,
        default="1h"
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    notifications_enabled = models.BooleanField(default=True)

    email_notifications = models.BooleanField(default=True)

    sms_notifications = models.BooleanField(default=False)

    push_notifications = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)


# User Session


class UserSession(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    session_key = models.CharField(
        max_length=255,
        unique=True
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    last_activity = models.DateTimeField(default=timezone.now)

# Login History


class LoginHistory(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="login_history"
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    device = models.CharField(
        max_length=120,
        blank=True
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    login_time = models.DateTimeField(auto_now_add=True)

    success = models.BooleanField(default=True)


# Exchange API Keys


class APIKey(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="exchange_keys"
    )

    provider = models.CharField(
        max_length=30,
        choices=APIProvider.choices
    )

    api_key = models.TextField()

    secret_key = models.TextField()

    passphrase = models.CharField(
        max_length=255,
        blank=True
    )

    is_testnet = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "provider")


# User Devices


class UserDevice(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="devices"
    )

    device_name = models.CharField(max_length=120)

    device_type = models.CharField(
        max_length=20,
        choices=DeviceType.choices
    )

    device_id = models.CharField(
        max_length=255,
        unique=True
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    trusted = models.BooleanField(default=False)

    last_seen = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)



# Email Verification


class EmailVerification(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="email_verification"
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    expires_at = models.DateTimeField()

    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


# Password Reset


class PasswordReset(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="password_resets"
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    expires_at = models.DateTimeField()

    used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)