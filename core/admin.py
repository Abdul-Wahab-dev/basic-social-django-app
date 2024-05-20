from django.contrib import admin
from .models import Profile , Post, LikePost , FollowersCount
from django.db import models
# Register your models here.

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'bio']
    
    
@admin.register(Post)
class AdminProfile(admin.ModelAdmin):
    list_display = ['id' , 'user']
    
    
@admin.register(LikePost)
class AdminProfile(admin.ModelAdmin):
    list_display = ['username' , 'post_id']

@admin.register(FollowersCount)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user' , 'follower']
