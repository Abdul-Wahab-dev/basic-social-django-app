from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),    
    path('signup', views.signup , name="signup"),    
    path('signin', views.signin , name="signin"),    
    path('logout', views.user_logout , name="logout"),    
    path('setting', views.user_setting , name="setting"),    
    path('upload' , views.upload , name="upload"),
    path('like' , views.like_post , name='like'),
    path('profile/<str:pk>' , views.profile , name="profile"),
    path('follow' , views.follow , name="follow" ), 
    
]