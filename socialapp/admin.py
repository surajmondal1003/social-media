from django.contrib import admin
from socialapp.models import User_Personal,Request,Friends,Post,Comment
# Register your models here.

admin.site.register(User_Personal)
admin.site.register(Request)
admin.site.register(Friends)
admin.site.register(Post)
admin.site.register(Comment)

