from django.conf.urls import url


from . import views

app_name = 'salmon'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login', views.login, name='login'),
	url(r'^register', views.register, name='register'),
	url(r'^show_users',views.ShowUsers.as_view(), name='show_users'),
	url(r'^user_home', views.userhome, name='user_home'),

	]