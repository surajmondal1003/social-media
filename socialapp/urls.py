from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from socialapp import views

app_name='socialapp'

urlpatterns = [

    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('newsfeed',views.newsfeed,name='newsfeed'),
    path('newsfeed_friends',views.newsfeed_friends,name='newsfeed_friends'),
    path('newsfeed_messages',views.newsfeed_messages,name='newsfeed_messages'),
    path('timeline_about',views.timeline_about,name='timeline_about'),
    path('see_other_profile/<id_user>',views.see_other_profile,name='see_other_profile'),
    path('edit_profile_basic',views.edit_profile_basic,name='edit_profile_basic'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('add_friend/<id_user>',views.add_friend,name='add_friend'),
    path('accept_friend/<id_request>/<id_user>',views.accept_friend,name='accept_friend'),
    path('request_notifications',views.request_notifications,name='request_notifications'),
    path('create_post',views.create_post,name='create_post'),
    path('like_post/<post_id>',views.like_post,name='like_post'),
    path('404',views.notfound404,name='404'),


]