from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserViewSet,
    UserProfileViewSet,
    UserPreferenceViewSet,
    PasswordViewSet,
    KYCViewSet,
    UserSessionViewSet,
    LoginHistoryViewSet,
    APIKeyViewSet,
    UserDeviceViewSet,
    EmailVerificationViewSet,
    PasswordResetViewSet,
    AuthViewSet,
)


router = DefaultRouter(trailing_slash=False)


# ==========================================================
# USERS
# ==========================================================

router.register(
    r"users",
    UserViewSet,
    basename="users",
)


# ==========================================================
# AUTHENTICATION
# ==========================================================

router.register(
    r"auth",
    AuthViewSet,
    basename="auth",
)


# ==========================================================
# PROFILE
# ==========================================================

router.register(
    r"profile",
    UserProfileViewSet,
    basename="profile",
)


# ==========================================================
# PREFERENCES
# ==========================================================

router.register(
    r"preferences",
    UserPreferenceViewSet,
    basename="preferences",
)


# ==========================================================
# PASSWORD
# ==========================================================

router.register(
    r"password",
    PasswordViewSet,
    basename="password",
)


# ==========================================================
# KYC
# ==========================================================

router.register(
    r"kyc",
    KYCViewSet,
    basename="kyc",
)


# ==========================================================
# SESSIONS
# ==========================================================

router.register(
    r"sessions",
    UserSessionViewSet,
    basename="sessions",
)


# ==========================================================
# LOGIN HISTORY
# ==========================================================

router.register(
    r"login-history",
    LoginHistoryViewSet,
    basename="login-history",
)


# ==========================================================
# API KEYS
# ==========================================================

router.register(
    r"api-keys",
    APIKeyViewSet,
    basename="api-keys",
)


# ==========================================================
# DEVICES
# ==========================================================

router.register(
    r"devices",
    UserDeviceViewSet,
    basename="devices",
)


# ==========================================================
# EMAIL VERIFICATION
# ==========================================================

router.register(
    r"email",
    EmailVerificationViewSet,
    basename="email",
)


# ==========================================================
# PASSWORD RESET
# ==========================================================

router.register(
    r"password-reset",
    PasswordResetViewSet,
    basename="password-reset",
)


# ==========================================================
# URLS
# ==========================================================

urlpatterns = [

    # JWT refresh token
    path(
        "auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Router URLs
    path(
        "",
        include(router.urls),
    ),
]