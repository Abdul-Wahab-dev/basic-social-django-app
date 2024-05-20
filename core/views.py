from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .models import Profile, Post, LikePost , FollowersCount
# Create your views here.

@login_required(login_url="signin")
def index(request):
    user_obj = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_obj)
    
    posts = Post.objects.all()
    print(posts,'posts')
    return render(request , 'index.html' , {'profile' : user_profile , 'posts':posts})

def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.error(request, 'Email has already taken')
                redirect('signup')
            elif User.objects.filter(username = username).exists():
                messages.error(request , 'Username has already taken')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #log user in and redirect to settings page
                login_user = authenticate(request,username=username , password=password)
                login(request, user=login_user)
                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)     
                new_profile.save()
                return redirect('setting')
        else:
            messages.error(request,"password does not match")
            return redirect('signup')
        
    return render(request , 'signup.html')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request , user)
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('signin')
    else:    
        return render(request, 'signin.html')
    
    
@login_required(login_url="signin")    
def user_logout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def user_setting(request):
    profile = Profile.objects.get(user=request.user)

    
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = profile.image
            bio = request.POST['bio']
            location = request.POST['location']
            
            profile.image = image
            profile.bio = bio
            profile.location = location
            profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            profile.image = image
            profile.bio = bio
            profile.location = location
            profile.save()
        return redirect('setting')        
    else:    
        return render(request, 'setting.html' ,{'profile' : profile})
    
    
    
    
def upload(request):
    print(request.FILES ,'request.FILES')
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user= user , caption=caption , image=image)
        new_post.save()
        return redirect('/')
    else:
        
        return redirect('/')
    
    
    
@login_required(login_url='signin')
def like_post(request): 
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id= post_id)
    like_filter = LikePost.objects.filter(post_id = post_id, username = username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes -1
        post.save()
        return redirect('/')
    

def profile(request , pk):
    user_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user = user_object)
    posts = Post.objects.filter(user = pk)
    post_length = len(posts)
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(follower=follower , user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'follow'
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_followings = len(FollowersCount.objects.filter(follower=pk))   
    context = {
        'user_object':user_object,
        'profile':profile,
        'no_of_posts':post_length,
        'posts':posts,
        'button_text':button_text,
        'followers':user_followers,
        'followings': user_followings
    }
    return render(request,'profile.html' , context)    

@login_required(login_url='/signin')
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowersCount.objects.filter(follower=follower , user = user).first():
            delete_follower = FollowersCount.objects.get(follower = follower , user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower , user= user)
            new_follower.save()
            return redirect('/profile/'+user)
        
    else:
        return redirect('/')

        
     
    