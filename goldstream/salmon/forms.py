from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Please enter a valid email address.')
	class Meta:
		model = User
		fields = ('email','password1','password2')