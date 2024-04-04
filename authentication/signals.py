from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from authentication.models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_email(sender, instance, created, **kwargs):
    user = {"full_name": instance.full_name, "email": instance.email}
    login_url = settings.LOGIN_URL
    if created:
        user["full_name"] = user["full_name"].title()
        message = get_template("email_templates/welcome.html").render({"user": user, "login_url":login_url})
        full_name = user.get("full_name").title()
        mail = EmailMessage(
            subject=f"{full_name}, Welcome to Bidding System - Let's get started!",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[instance.email],
        )
        mail.content_subtype = "html"
        return mail.send()
