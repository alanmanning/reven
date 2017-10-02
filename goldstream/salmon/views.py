from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.views import generic
from .models import User
from .auth import send_activation_email,account_activation_token, send_activation_email_token, get_send_activation_email_url
from django.contrib.auth import views as auth_views
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from IPython.core.debugger import Tracer; debug_here = Tracer()



def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print('about to check if form is valid')
        if form.is_valid():
            print('Form is valid, about to save user')
            user = form.save(commit=False) #don't save the model bound to form, return it
            user.is_active = False
            user.save()
            print('User saved, calculating url for user')
            url = get_send_activation_email_url(user)
            print('Got url: ', url)
            return redirect(url)
            # send_activation_email(request,user)
            # return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    print(form)
    return render(request,'auth/register.html', {'form':form})

def send_act_email_view(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if (user is not None)\
        and send_activation_email_token.check_token(user, token)\
        and (getattr(user,'is_active',None) == False):
        send_activation_email(request,user)
        print('An activation email has been sent to ', user.email)
        return HttpResponse(('An activation email has been send to %s' % user.email))
    else:
        return HttpResponse('User is invalid. No activation email sent.')


# else:
        #     errors = form.errors.as_data()
        #     try:
        #         code = errors['email'][0].code
        #         if code == 'resend_act_email':
        #             # Get the user
        #             # re-send the activation email.
        #     except:
        #         pass


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
    print('Got user: ', request.user)
    return render(request,'salmon/userhome.html')


########################################################
##### Views for authorization/authenication system #####
########################################################
