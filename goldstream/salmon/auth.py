from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def get_send_activation_email_url(user):
    url = render_to_string('salmon/user_auth_url.html', {
        'user':user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': send_activation_email_token.make_token(user),
    })
    print('get_user_auth_url returns: ', url)
    return url


def send_activation_email(request,user):
    current_site = get_current_site(request)
    message = render_to_string('salmon/activate_email.html', {
        'user':user, 
        'domain':current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    mail_subject = 'Activate your XXX account.'
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()

## from https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



# From https://farhadurfahim.github.io/post/django-registration-with-confirmation-email/
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    key_salt = "e4e36f0d-ca2b-5940-a7fe-a61287b5a2d8/PARTNROFF=1/lk&35l0.b,><2!!"
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

class SendAccountActivationEmailTokenGenerator(PasswordResetTokenGenerator):
    key_salt = "302cbea65a24373240b4240144c894066681ef4ebf7ab24dbaf359729d92941f"
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()
send_activation_email_token = SendAccountActivationEmailTokenGenerator()