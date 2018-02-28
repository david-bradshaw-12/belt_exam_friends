from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.login_page),
	url(r'^main$', views.main_friends),
	url(r'logout$', views.log_out),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^add_friend$', views.add_friend),
	url(r'^rem_friend$', views.remove_friend),
	url(r'user/(?P<id>\d+)$', views.friend_page),
]