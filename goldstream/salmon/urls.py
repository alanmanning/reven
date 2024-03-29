from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views

#app_name = 'salmon'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register', views.register, name='register'),
	url(r'^show_users',views.ShowUsers.as_view(), name='show_users'),
	url(r'^myhome', views.user_home, name='user_home'),

	#url('^', include('django.contrib.auth.urls')),

    #LoginView redirects to settings.LOGIN_REDIRECT_URL after a successful login
    url(r'^login/$', auth_views.LoginView.as_view(template_name='auth/login.html'),
    	name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='auth/logout.html'),
    	name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^send_act_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.send_act_email_view, name='send_act_email'),

#    url(r'^password_change/$',
#    	auth_views.PasswordChangeView.as_view(template_name='auth/password_change_form.html'),
#    	name='password_change'),
    url(r'^password_change/$',
       views.MyPasswordChangeView.as_view(template_name='auth/password_change_form.html'),
       name='password_change'),
    url(r'^password_change/done/$',
    	views.MyPasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'),
    	name='password_change_done'),
    url(r'^password_reset/$',
    	views.MyPasswordResetView.as_view(template_name='auth/password_reset_email.html'),
    	name='password_reset'),
    url(r'^password_reset/done/$',
    	auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
    	name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/done/$',
    	auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
    	name='password_reset_complete'),


	]


# # NOTE: this line
# # '' url('^', include('django.contrib.auth.urls')), ''
# # includes the following URL patterns:
# urlpatterns = [
#     url(r'^login/$', views.LoginView.as_view(), name='login'),
#     url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

#     url(r'^password_change/$', views.PasswordChangeView.as_view(), name='password_change'),
#     url(r'^password_change/done/$', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

#     url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
#     url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     url(r'^reset/done/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
#]