from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

## We're using a custom authentication backend instead of a custom
## user model to implement email login instead of user logine. This
## has the advantage that user model doesn't have to change too much.
## Also, the superuser authentication backend doesn't have to be changed.
## See: https://stackoverflow.com/questions/37332190/django-login-with-email
class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None