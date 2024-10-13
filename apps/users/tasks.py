from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

class PremiumNotifier:
    def __init__(self, subject, message):
        self.subject = subject
        self.message = message

    def send_notifications(self):
        premium_users = User.objects.filter(is_premium=True)
        for user in premium_users:
            self.send_email(user)

    def send_email(self, user):
        send_mail(
            self.subject,
            self.message,
            'from@example.com',  # Sender email address
            [user.email],  # Recipient email address
            fail_silently=False,
        )
