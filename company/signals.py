from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone

from company.models import User


@receiver(user_logged_in, sender=User)
def track_user_login_datetime(sender, request, user, **kwargs):
    request.user.is_verified = True
    request.user.login_datetime = timezone.now()
    request.user.save()
    print('Successfully login in {} and saved logout datetime'.format(user.email))


@receiver(user_logged_out, sender=User)
def track_user_logout_datetime(sender, request, user, **kwargs):
    request.user.is_verified = True
    request.user.logout_datetime = timezone.now()
    request.user.save()
    print('Successfully logged out user {} and saved logout datetime'.format(user.email))
