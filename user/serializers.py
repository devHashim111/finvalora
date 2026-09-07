from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework import serializers


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
# USER
# ==========================================================

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            "id",
            "username",
            "email",
            "role",
            "phone",
            "country",
            "timezone",
            "language",
            "avatar",
            "is_email_verified",
            "is_phone_verified",
            "is_2fa_enabled",
            "kyc_status",
            "date_joined",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "role",
            "is_email_verified",
            "is_phone_verified",
            "is_2fa_enabled",
            "kyc_status",
            "date_joined",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# USER REGISTRATION
# ==========================================================

class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    password_confirm = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = CustomUser

        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "phone",
            "country",
        ]

    def validate_email(self, value):

        value = value.lower()

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password_confirm":
                    "Passwords do not match."
                }
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = CustomUser(
            **validated_data
        )

        user.set_password(password)

        user.save()

        return user


# ==========================================================
# USER UPDATE
# ==========================================================

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            "username",
            "phone",
            "country",
            "timezone",
            "language",
            "avatar",
        ]

        read_only_fields = [
            "email",
        ]


# ==========================================================
# PASSWORD CHANGE
# ==========================================================

class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    new_password_confirm = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        user = self.context["request"].user

        if not user.check_password(
            attrs["old_password"]
        ):
            raise serializers.ValidationError(
                {
                    "old_password":
                    "Current password is incorrect."
                }
            )

        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {
                    "new_password_confirm":
                    "Passwords do not match."
                }
            )

        return attrs

    def save(self):

        user = self.context["request"].user

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        return user


# ==========================================================
# KYC
# ==========================================================

class KYCSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            "phone",
            "country",
            "kyc_status",
        ]

        read_only_fields = [
            "kyc_status",
        ]


# ==========================================================
# PROFILE
# ==========================================================

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile

        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "date_of_birth",
            "gender",
            "address",
            "city",
            "state",
            "postal_code",
            "profile_completed",
        ]

        read_only_fields = [
            "id",
            "profile_completed",
        ]


# ==========================================================
# PREFERENCES
# ==========================================================
# Included for backend completeness.
# UI/theme logic can remain in frontend.

class UserPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPreference

        fields = [
            "id",
            "default_exchange",
            "default_timeframe",
            "currency",
            "notifications_enabled",
            "email_notifications",
            "sms_notifications",
            "push_notifications",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "updated_at",
        ]


# ==========================================================
# USER SESSION
# ==========================================================

class UserSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSession

        fields = [
            "id",
            "session_key",
            "ip_address",
            "user_agent",
            "created_at",
            "expires_at",
            "is_active",
            "last_activity",
        ]

        read_only_fields = [
            "id",
            "session_key",
            "ip_address",
            "user_agent",
            "created_at",
            "last_activity",
        ]


# ==========================================================
# LOGIN HISTORY
# ==========================================================

class LoginHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginHistory

        fields = [
            "id",
            "ip_address",
            "user_agent",
            "device",
            "location",
            "login_time",
            "success",
        ]

        read_only_fields = fields


# ==========================================================
# API KEYS
# ==========================================================

class APIKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = APIKey

        fields = [
            "id",
            "provider",
            "api_key",
            "secret_key",
            "passphrase",
            "is_testnet",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

        extra_kwargs = {
            "api_key": {
                "write_only": True,
            },
            "secret_key": {
                "write_only": True,
            },
            "passphrase": {
                "write_only": True,
            },
        }

    def create(self, validated_data):

        return APIKey.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )


# ==========================================================
# API KEY LIST
# Safe response -- never returns credentials
# ==========================================================

class APIKeyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = APIKey

        fields = [
            "id",
            "provider",
            "is_testnet",
            "is_active",
            "created_at",
        ]

        read_only_fields = fields


# ==========================================================
# USER DEVICE
# ==========================================================

class UserDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDevice

        fields = [
            "id",
            "device_name",
            "device_type",
            "device_id",
            "ip_address",
            "user_agent",
            "trusted",
            "last_seen",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "ip_address",
            "user_agent",
            "last_seen",
            "created_at",
        ]

    def create(self, validated_data):

        return UserDevice.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )


# ==========================================================
# EMAIL VERIFICATION
# ==========================================================

class EmailVerificationSerializer(serializers.Serializer):

    token = serializers.UUIDField()

    def validate_token(self, value):

        try:
            verification = EmailVerification.objects.get(
                token=value,
                user=self.context["request"].user,
                verified=False,
            )

        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid verification token."
            )

        if verification.expires_at <= timezone.now():
            raise serializers.ValidationError(
                "Verification token has expired."
            )

        self.verification = verification

        return value

    def save(self):

        verification = self.verification

        verification.verified = True
        verification.save(
            update_fields=["verified"]
        )

        user = verification.user

        user.is_email_verified = True
        user.save(
            update_fields=["is_email_verified"]
        )

        return user


# ==========================================================
# PASSWORD RESET REQUEST
# ==========================================================

class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        value = value.lower()

        if not CustomUser.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "No account exists with this email."
            )

        return value


# ==========================================================
# PASSWORD RESET CONFIRM
# ==========================================================

class PasswordResetConfirmSerializer(serializers.Serializer):

    token = serializers.UUIDField()

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {
                    "new_password_confirm":
                    "Passwords do not match."
                }
            )

        try:
            reset = PasswordReset.objects.get(
                token=attrs["token"],
                used=False,
            )

        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "token":
                    "Invalid password reset token."
                }
            )

        if reset.expires_at <= timezone.now():
            raise serializers.ValidationError(
                {
                    "token":
                    "Password reset token has expired."
                }
            )

        self.reset = reset

        return attrs

    def save(self):

        user = self.reset.user

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        self.reset.used = True

        self.reset.save(
            update_fields=["used"]
        )

        return user



class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                {
                    "detail": "Invalid email or password."
                }
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "detail": "User account is inactive."
                }
            )

        attrs["user"] = user

        return attrs