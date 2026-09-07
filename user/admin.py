from django.contrib import admin

from .models import (
    CustomUser,
    UserProfile,
    UserPreference,
    UserSession,
    LoginHistory,
    APIKey,
    UserDevice,
    EmailVerification,
    PasswordReset,
)


# ==========================================================
# Custom User
# ==========================================================

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "username",
        "role",
        "kyc_status",
        "is_email_verified",
        "is_phone_verified",
        "is_2fa_enabled",
        "is_active",
        "is_staff",
        "created_at",
    )

    list_filter = (
        "role",
        "kyc_status",
        "language",
        "is_email_verified",
        "is_phone_verified",
        "is_2fa_enabled",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    search_fields = (
        "email",
        "username",
        "phone",
        "country",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "last_login",
        "date_joined",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Account",
            {
                "fields": (
                    "id",
                    "email",
                    "username",
                    "password",
                )
            },
        ),
        (
            "Role & Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "phone",
                    "country",
                    "timezone",
                    "language",
                    "avatar",
                )
            },
        ),
        (
            "Verification & Security",
            {
                "fields": (
                    "is_email_verified",
                    "is_phone_verified",
                    "is_2fa_enabled",
                    "kyc_status",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


# ==========================================================
# User Profile
# ==========================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "first_name",
        "last_name",
        "city",
        "state",
        "profile_completed",
    )

    list_filter = (
        "profile_completed",
        "gender",
        "state",
        "city",
    )

    search_fields = (
        "user__email",
        "user__username",
        "first_name",
        "last_name",
        "city",
        "state",
        "postal_code",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "user__email",
    )


# ==========================================================
# User Preferences
# ==========================================================

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "theme",
        "chart_theme",
        "default_exchange",
        "default_timeframe",
        "currency",
        "notifications_enabled",
        "email_notifications",
        "sms_notifications",
        "push_notifications",
        "updated_at",
    )

    list_filter = (
        "theme",
        "default_exchange",
        "currency",
        "notifications_enabled",
        "email_notifications",
        "sms_notifications",
        "push_notifications",
        "updated_at",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

    readonly_fields = (
        "updated_at",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-updated_at",
    )


# ==========================================================
# User Session
# ==========================================================

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "session_key",
        "ip_address",
        "created_at",
        "expires_at",
        "is_active",
        "last_activity",
    )

    list_filter = (
        "is_active",
        "created_at",
        "expires_at",
        "last_activity",
    )

    search_fields = (
        "user__email",
        "user__username",
        "session_key",
        "ip_address",
        "user_agent",
    )

    readonly_fields = (
        "created_at",
        "last_activity",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-last_activity",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Login History
# ==========================================================

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "ip_address",
        "device",
        "location",
        "login_time",
        "success",
    )

    list_filter = (
        "success",
        "device",
        "location",
        "login_time",
    )

    search_fields = (
        "user__email",
        "user__username",
        "ip_address",
        "device",
        "location",
        "user_agent",
    )

    readonly_fields = (
        "login_time",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-login_time",
    )

    date_hierarchy = "login_time"


# ==========================================================
# Exchange API Keys
# ==========================================================

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "provider",
        "is_testnet",
        "is_active",
        "created_at",
    )

    list_filter = (
        "provider",
        "is_testnet",
        "is_active",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "provider",
    )

    readonly_fields = (
        "created_at",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-created_at",
    )

    exclude = (
        "api_key",
        "secret_key",
        "passphrase",
    )


# ==========================================================
# User Devices
# ==========================================================

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "device_name",
        "device_type",
        "device_id",
        "ip_address",
        "trusted",
        "last_seen",
        "created_at",
    )

    list_filter = (
        "device_type",
        "trusted",
        "created_at",
        "last_seen",
    )

    search_fields = (
        "user__email",
        "user__username",
        "device_name",
        "device_id",
        "ip_address",
        "user_agent",
    )

    readonly_fields = (
        "last_seen",
        "created_at",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-last_seen",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Email Verification
# ==========================================================

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "verified",
        "expires_at",
        "created_at",
    )

    list_filter = (
        "verified",
        "expires_at",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

    readonly_fields = (
        "token",
        "created_at",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Password Reset
# ==========================================================

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "used",
        "expires_at",
        "created_at",
    )

    list_filter = (
        "used",
        "expires_at",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

    readonly_fields = (
        "token",
        "created_at",
    )

    list_select_related = (
        "user",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"