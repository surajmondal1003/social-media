from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class User_Personal(models.Model):

    #create relationship with user model
    user = models.OneToOneField(User,on_delete=models.CASCADE,)


    #additional fields
    dob=models.DateField()
    gender=models.CharField(max_length=50)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    profilepic=models.ImageField(upload_to='profile_pics',blank=True)
    about_text=models.TextField(blank=True)


    def __str__(self):

        #built in field of model User
        return self.user.username


class Request(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friendship_requests_sent')
    request_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friendship_requests_received')
    request_date = models.DateField(default=timezone.now())
    request_status = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username + '-->' + self.request_user.username


class Friends(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_id')
    friend=models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend_id')

    def __str__(self):
        return self.user.username+ '<-->' + self.friend.username



class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_user_id')
    post_text=models.TextField()
    post_pic=models.ImageField(upload_to='post_pics',blank=True)
    post_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.user.username

