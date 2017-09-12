from django.contrib.auth.models import AbstractUser
from django.db import models


#class User(AbstractUser):
#   pass

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField('email address',unique=True) # changes email to unique and blank to false
        #already uses an email validator to check email address

    # username = models.CharField('username',
    #     max_length=150,
    #     unique=False,
    #     blank=True)
    REQUIRED_FIELDS = [] # This variable is used in superuser creation only