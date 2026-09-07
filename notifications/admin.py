from django.contrib import admin

from .models import (
    Notification,
    NotificationTemplate,
    NotificationPreference,
    DeviceToken,
    EmailQueue,
    SMSQueue,
    PushQueue,
    NotificationLog,
)


# ==========================================================
# Notification
# ==========================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "notification_type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
        "user__email",
        "user__username",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Notification Template
# ==========================================================

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "subject",
        "channel",
        "active",
    )

    list_filter = (
        "channel",
        "active",
    )

    search_fields = (
        "name",
        "subject",
        "body",
    )

    ordering = (
        "name",
    )


# ==========================================================
# Notification Preferences
# ==========================================================

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "email_enabled",
        "sms_enabled",
        "push_enabled",
        "in_app_enabled",
        "trade_alerts",
        "price_alerts",
        "security_alerts",
        "marketing",
    )

    list_filter = (
        "email_enabled",
        "sms_enabled",
        "push_enabled",
        "in_app_enabled",
        "trade_alerts",
        "price_alerts",
        "security_alerts",
        "marketing",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

    list_select_related = (
        "user",
    )


# ==========================================================
# Device Token
# ==========================================================

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "device_name",
        "active",
        "created_at",
    )

    list_filter = (
        "active",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "device_name",
    )

    readonly_fields = (
        "created_at",
        "token",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-created_at",
    )


# ==========================================================
# Email Queue
# ==========================================================

@admin.register(EmailQueue)
class EmailQueueAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "subject",
        "status",
        "created_at",
        "sent_at",
    )

    list_filter = (
        "status",
        "created_at",
        "sent_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "subject",
        "body",
    )

    readonly_fields = (
        "created_at",
        "sent_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "created_at"


# ==========================================================
# SMS Queue
# ==========================================================

@admin.register(SMSQueue)
class SMSQueueAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "status",
        "created_at",
        "sent_at",
    )

    list_filter = (
        "status",
        "created_at",
        "sent_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "phone",
        "message",
    )

    readonly_fields = (
        "created_at",
        "sent_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Push Queue
# ==========================================================

@admin.register(PushQueue)
class PushQueueAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "title",
        "status",
        "created_at",
        "sent_at",
    )

    list_filter = (
        "status",
        "created_at",
        "sent_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "title",
        "message",
    )

    readonly_fields = (
        "created_at",
        "sent_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Notification Log
# ==========================================================

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "channel",
        "status",
        "reference",
        "created_at",
    )

    list_filter = (
        "channel",
        "status",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "reference",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "created_at"