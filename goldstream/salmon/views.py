from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm

# Create your views here.
def index(request):
	return HttpResponse("You're at the index of Salmon")

def login(request):
	return HttpResponse("You're at the login page")

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid()
			form.save()
			return redirect('salmon:user_list')

	else:
	form = RegisterForm()
	return render(request,'salmon/register.html', {'form':form})