from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.views import generic
from .models import User

# Create your views here.
def index(request):
	return HttpResponse("You're at the index of Salmon")

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('show_users')

	else:
		form = RegisterForm()
	return render(request,'registration/register.html', {'form':form})

class ShowUsers(generic.ListView):
	template_name = 'salmon/show_users.html'
	context_object_name = 'user_list'

	def get_queryset(self):
		return User.objects.all()

########################################################
##### Views for authorization/authenication system #####
########################################################


# login_required() does the following:
#  If the user isn’t logged in, redirect to settings.LOGIN_URL, passing the current absolute path in the query string. Example: /accounts/login/?next=/polls/3/.
#  If the user is logged in, execute the view normally. The view code is free to assume the user is logged in.
@login_required
def userhome(request):
	return HttpResponse("You've been successfully logged in and are at the user homepage")