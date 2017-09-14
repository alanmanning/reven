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

@login_required
def user_home(request):
	return render(request,'salmon/userhome.html')


########################################################
##### Views for authorization/authenication system #####
########################################################
