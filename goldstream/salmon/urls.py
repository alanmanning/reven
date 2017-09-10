from django.conf.urls import url, include


from . import views

#app_name = 'salmon'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register', views.register, name='register'),
	url(r'^show_users',views.ShowUsers.as_view(), name='show_users'),
	url(r'^user_home', views.userhome, name='user_home'),

	url('^', include('django.contrib.auth.urls')),

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