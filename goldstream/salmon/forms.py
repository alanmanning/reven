from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils.translation import ugettext_lazy as _


class RegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Please enter a valid email address.')
	class Meta:
		model = User
		fields = ('email','password1','password2')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			match = User.objects.get(email=email)
			if match.is_active:
				raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
			else:
				raise forms.ValidationError(_("This email address already in use but has not been activated."),code='resend_act_email')
		except User.DoesNotExist:
			#we're ok: this is a new User
			return email