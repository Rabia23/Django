from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^success/$', views.register_success, name='register_success'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^validate_user/$', views.validate_user, name='validate_user'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^edit_user_profile/$', views.edit_user_profile, name='edit_user_profile'),
    url(r'^profile_success/$', views.profile_success, name='profile_success'),
]