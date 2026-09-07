from django.test import TestCase

from user.models import CustomUser

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


class NotificationTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="trader",
            email="trader@example.com",
            password="TestPassword123"
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(
            user=self.user,
            title="Trade Executed",
            message="Your BTC order was executed."
        )

        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.title, "Trade Executed")
        self.assertEqual(notification.message, "Your BTC order was executed.")
        self.assertEqual(notification.notification_type, "info")
        self.assertFalse(notification.is_read)

    def test_notification_template_creation(self):
        template = NotificationTemplate.objects.create(
            name="trade_executed",
            subject="Trade Executed",
            body="Your order has been executed.",
            channel="email"
        )

        self.assertEqual(template.name, "trade_executed")
        self.assertEqual(template.subject, "Trade Executed")
        self.assertEqual(template.channel, "email")
        self.assertTrue(template.active)

    def test_notification_preferences(self):
        preferences = NotificationPreference.objects.create(
            user=self.user
        )

        self.assertEqual(preferences.user, self.user)
        self.assertTrue(preferences.email_enabled)
        self.assertFalse(preferences.sms_enabled)
        self.assertTrue(preferences.push_enabled)
        self.assertTrue(preferences.in_app_enabled)
        self.assertTrue(preferences.trade_alerts)
        self.assertTrue(preferences.price_alerts)
        self.assertTrue(preferences.security_alerts)
        self.assertFalse(preferences.marketing)

    def test_device_token_creation(self):
        device = DeviceToken.objects.create(
            user=self.user,
            device_name="Test Phone",
            token="test-device-token-123"
        )

        self.assertEqual(device.user, self.user)
        self.assertEqual(device.device_name, "Test Phone")
        self.assertEqual(device.token, "test-device-token-123")
        self.assertTrue(device.active)

    def test_email_queue(self):
        email = EmailQueue.objects.create(
            user=self.user,
            subject="Test Email",
            body="This is a test email."
        )

        self.assertEqual(email.user, self.user)
        self.assertEqual(email.subject, "Test Email")
        self.assertEqual(email.body, "This is a test email.")
        self.assertEqual(email.status, "pending")
        self.assertIsNone(email.sent_at)

    def test_sms_queue(self):
        sms = SMSQueue.objects.create(
            user=self.user,
            phone="+923001234567",
            message="Test SMS"
        )

        self.assertEqual(sms.user, self.user)
        self.assertEqual(sms.phone, "+923001234567")
        self.assertEqual(sms.message, "Test SMS")
        self.assertEqual(sms.status, "pending")
        self.assertIsNone(sms.sent_at)

    def test_push_queue(self):
        push = PushQueue.objects.create(
            user=self.user,
            title="Price Alert",
            message="BTC reached your target price."
        )

        self.assertEqual(push.user, self.user)
        self.assertEqual(push.title, "Price Alert")
        self.assertEqual(push.message, "BTC reached your target price.")
        self.assertEqual(push.status, "pending")
        self.assertIsNone(push.sent_at)

    def test_notification_log(self):
        log = NotificationLog.objects.create(
            user=self.user,
            channel="email",
            status="sent",
            reference="trade-123"
        )

        self.assertEqual(log.user, self.user)
        self.assertEqual(log.channel, "email")
        self.assertEqual(log.status, "sent")
        self.assertEqual(log.reference, "trade-123")