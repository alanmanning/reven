from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.views import generic
from .models import User
from .auth import send_activation_email
from django.contrib.auth import views as auth_views
from .auth import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.forms import ValidationError


def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print('about to check if form is valid')
        try:
            valid = form.is_valid()
        except ValidationError as e:
            ### You were here. Check for re-registration code and give
            ### link to send an email
        if form.is_valid():
            print('Form is valid, about to save user')
            user = form.save(commit=False) #don't save the model bound to form, return it
            user.is_active = False
            user.save()
            send_activation_email(request,user)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    return render(request,'auth/register.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

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

class MyPasswordResetView(auth_views.PasswordResetView):
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        I've overwritten this from django.views.generic.edit.FormView, which
        PasswordChangeView inherits from. I want to set a session variable
        that will be checked in password reset done so that users can't just
        go to password change done without having done this page first.
        """
        form = self.get_form()
        if form.is_valid():
            request.session['from_password_reset'] = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@login_required
def user_home(request):
    return render(request,'salmon/userhome.html')


########################################################
##### Views for authorization/authenication system #####
########################################################
