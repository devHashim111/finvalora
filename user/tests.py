from django.test import TestCase
from .models import CustomUser


class CustomUserTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("TestPassword123"))

    def test_password_is_hashed(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )

        self.assertNotEqual(user.password, "TestPassword123")
        self.assertTrue(user.check_password("TestPassword123"))

    def test_wrong_password_fails(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )

        self.assertFalse(user.check_password("WrongPassword"))

    def test_user_can_be_retrieved(self):
        CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )

        user = CustomUser.objects.get(email="test@example.com")

        self.assertEqual(user.username, "testuser")