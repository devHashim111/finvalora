import uuid

from django.conf import settings
from django.db import models


# ==========================================================
# Choices
# ==========================================================

class NotificationType(models.TextChoices):
    INFO = "info", "Info"
    SUCCESS = "success", "Success"
    WARNING = "warning", "Warning"
    ERROR = "error", "Error"


class NotificationChannel(models.TextChoices):
    EMAIL = "email", "Email"
    SMS = "sms", "SMS"
    PUSH = "push", "Push"
    IN_APP = "in_app", "In App"


class QueueStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SENT = "sent", "Sent"
    FAILED = "failed", "Failed"


# ==========================================================
# Notification
# In-App notification
# ==========================================================

class Notification(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.title


# ==========================================================
# Notification Template
# ==========================================================

class NotificationTemplate(models.Model):

    name = models.CharField(max_length=100, unique=True)

    subject = models.CharField(max_length=255)

    body = models.TextField()

    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
    )

    active = models.BooleanField(default=True)

    
    def __str__(self):
        return self.name


# ==========================================================
# Notification Preferences
# ==========================================================

class NotificationPreference(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
    )

    email_enabled = models.BooleanField(default=True)

    sms_enabled = models.BooleanField(default=False)

    push_enabled = models.BooleanField(default=True)

    in_app_enabled = models.BooleanField(default=True)

    trade_alerts = models.BooleanField(default=True)

    price_alerts = models.BooleanField(default=True)

    security_alerts = models.BooleanField(default=True)

    marketing = models.BooleanField(default=False)

  

# ==========================================================
# Device Token
# ==========================================================

class DeviceToken(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="device_tokens",
    )

    device_name = models.CharField(max_length=100)

    token = models.TextField(unique=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

   

# ==========================================================
# Email Queue
# ==========================================================

class EmailQueue(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    subject = models.CharField(max_length=255)

    body = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=QueueStatus.choices,
        default=QueueStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    sent_at = models.DateTimeField(null=True, blank=True)

   


# ==========================================================
# SMS Queue
# ==========================================================

class SMSQueue(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    phone = models.CharField(max_length=30)

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=QueueStatus.choices,
        default=QueueStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    sent_at = models.DateTimeField(null=True, blank=True)

 
# ==========================================================
# Push Queue
# ==========================================================

class PushQueue(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=QueueStatus.choices,
        default=QueueStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    sent_at = models.DateTimeField(null=True, blank=True)

 

# ==========================================================
# Notification Log
# Audit Table
# ==========================================================

class NotificationLog(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=QueueStatus.choices,
    )

    reference = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

