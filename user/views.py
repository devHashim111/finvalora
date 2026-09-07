from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    KYCSerializer,
    UserProfileSerializer,
    UserPreferenceSerializer,
    UserSessionSerializer,
    LoginHistorySerializer,
    APIKeySerializer,
    APIKeyListSerializer,
    UserDeviceSerializer,
    EmailVerificationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    LoginSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action in ["create", "signup"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["create", "signup"]:
            return UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        if not self.request.user or self.request.user.is_anonymous:
            return CustomUser.objects.none()

        if self.request.user.is_staff:
            return CustomUser.objects.all()

        return CustomUser.objects.filter(
            id=self.request.user.id
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        url_path="signup",
    )
    def signup(self, request):
        serializer = UserCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
    )
    def me(self, request):
        user = request.user

        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data)

        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            UserSerializer(user).data
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class PasswordViewSet(viewsets.GenericViewSet):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        url_path="change",
    )
    def change(self, request):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()

        return Response(
            {
                "detail":
                "Password changed successfully."
            },
            status=status.HTTP_200_OK,
        )


class KYCViewSet(viewsets.GenericViewSet):
    serializer_class = KYCSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="status",
    )
    def status(self, request):
        user = request.user

        if request.method == "GET":
            return Response({
                "kyc_status": user.kyc_status,
                "phone": user.phone,
                "country": user.country,
            })

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()

        return Response({
            "detail":
            "KYC information updated.",
            "kyc_status":
            user.kyc_status,
        })


class UserSessionViewSet(
    viewsets.ReadOnlyModelViewSet
):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="revoke",
    )
    def revoke(self, request, pk=None):
        session = self.get_object()

        session.is_active = False
        session.save(
            update_fields=["is_active"]
        )

        return Response({
            "detail": "Session revoked."
        })


class LoginHistoryViewSet(
    viewsets.ReadOnlyModelViewSet
):
    queryset = LoginHistory.objects.all()
    serializer_class = LoginHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LoginHistory.objects.filter(
            user=self.request.user
        ).order_by("-login_time")


class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return APIKey.objects.filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action in [
            "list",
            "retrieve",
        ]:
            return APIKeyListSerializer

        return APIKeySerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class UserDeviceViewSet(viewsets.ModelViewSet):
    queryset = UserDevice.objects.all()
    serializer_class = UserDeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDevice.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="trust",
    )
    def trust(self, request, pk=None):
        device = self.get_object()

        device.trusted = True
        device.save(
            update_fields=["trusted"]
        )

        return Response({
            "detail": "Device trusted."
        })

    @action(
        detail=True,
        methods=["post"],
        url_path="untrust",
    )
    def untrust(self, request, pk=None):
        device = self.get_object()

        device.trusted = False
        device.save(
            update_fields=["trusted"]
        )

        return Response({
            "detail": "Device untrusted."
        })


class EmailVerificationViewSet(
    viewsets.GenericViewSet
):
    serializer_class = EmailVerificationSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        url_path="verify",
    )
    def verify(self, request):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()

        return Response({
            "detail":
            "Email verified successfully."
        })


class PasswordResetViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "confirm":
            return PasswordResetConfirmSerializer

        return PasswordResetRequestSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="request",
    )
    def request_reset(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        return Response({
            "detail":
            "If the account exists, a reset email will be sent."
        })

    @action(
        detail=False,
        methods=["post"],
        url_path="confirm",
    )
    def confirm(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()

        return Response({
            "detail":
            "Password reset successfully."
        })


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="login",
    )
    def login(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={
                "request": request
            },
        )
        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        ip_address = self.get_client_ip(request)

        user_agent = request.META.get(
            "HTTP_USER_AGENT",
            "",
        )

        LoginHistory.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
        )

        return Response(
            {
                "detail":
                "Login successful.",
                "access":
                str(refresh.access_token),
                "refresh":
                str(refresh),
                "user":
                UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get(
            "HTTP_X_FORWARDED_FOR"
        )

        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]

        return request.META.get(
            "REMOTE_ADDR",
            None,
        )