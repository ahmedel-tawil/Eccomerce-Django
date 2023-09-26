from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_order_confirmation_email(email, order):
    body = render_to_string('home/order_confirmation_email.html', {'email': email, 'order': order})
    mail = EmailMessage(
        subject='Order Placed!',
        body=body,
        # FIXME: EMAIL_BACKEND Is for testing
        from_email=settings.EMAIL_BACKEND,
        to=[email],
    )
    mail.content_subtype = 'html'
    # TODO: Recommendation is use celery for background tasks.
    return mail.send(fail_silently=False)
