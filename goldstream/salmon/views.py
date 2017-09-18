from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.views import generic
from .models import User
from django.contrib.auth import views as auth_views

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

class MyPasswordChangeView(auth_views.PasswordChangeView):
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        I've overwritten this from django.views.generic.edit.FormView, which
        PasswordChangeView inherits from. I want to set a session variable
        that will be checked in password change done so that users can't just
        go to password change done without having done this page first.
        """
        form = self.get_form()
        if form.is_valid():
            request.session['from_password_change'] = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class MyPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    def get(self, request, *args, **kwargs):
        ok = request.session.pop('from_password_change',False)
        if ok:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return redirect('user_home',permanent=True)

@login_required
def user_home(request):
	return render(request,'salmon/userhome.html')


########################################################
##### Views for authorization/authenication system #####
########################################################
