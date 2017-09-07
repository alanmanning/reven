from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.views import generic
from .models import User

# Create your views here.
def index(request):
	return HttpResponse("You're at the index of Salmon")

def login(request):
	return HttpResponse("You're at the login page")

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('salmon:show_users')

	else:
		form = RegisterForm()
	return render(request,'salmon/register.html', {'form':form})

class ShowUsers(generic.ListView):
	template_name = 'salmon/show_users.html'
	context_object_name = 'user_list'

	def get_queryset(self):
		return User.objects.all()
