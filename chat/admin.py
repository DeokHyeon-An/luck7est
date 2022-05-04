from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ChatRoom, User

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += (("Custom fields", {"fields":("nickname","profile_pic","intro","point")}),)