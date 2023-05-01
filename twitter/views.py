from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, MyUserCreationForm, PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import User, Post, Follow
from django.http import JsonResponse
# Create your views here.


def register(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        print("form", form)
        if form.is_valid():
            user = form.save(commit=False)
            print('user', user)
            user.username = user.username.lower()
            user.save()
            auth_login(request, user)
            # userex = User.objects.get(username=user.username)
            # print(userex)

            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            return redirect('register')

    return render(request, 'twitter/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'twitter/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'twitter/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    # fetch from Follower  po
    if request.user.is_authenticated: 
        user = request.user  
        following = Follow.objects.filter(follower__id=request.user.id)
        
        users_following = [follow.following for follow in following]
        # users_following = User.objects.filter(id__in=following)
        # feth the user they that i am following   
        #  from fllow follower_id = requet.user.id   // i know the users i am
        #  from  user.filter(id = ff)
        posts_fol = Post.objects.filter(Q(author=user) | Q(author__in=users_following))
        print("following",following)
        # print("uer_iam_following", users_following)
        form = PostForm(request.POST, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                post = Post(
                    content=form.cleaned_data['content'],
                    image=form.cleaned_data.get('image'),
                    author=request.user,
                )
                print("post", post)
                post.save()
                messages.success(request, 'Post created successfully.')
            print('form is invalid')
            return redirect('home')

        posts = posts_fol
        return render(request, 'twitter/home.html', {"posts": posts, "form": form})
    else:
        posts = posts_fol
        context = {"posts": posts," following":following , "usf":users_following}
        return render(request, 'twitter/home.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    posts = Post.objects.filter(author__id=int(pk))
    is_following = False
    user = User.objects.get(id = pk)
    follower = request.user
    followertrue = Follow.objects.filter(follower=follower, following=user).first()
    if followertrue:
        is_following = True
    context = {'posts': posts, 'user': user, 'is_following':is_following}
    print('isfollowing',is_following)
    return render(request, 'twitter/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

@login_required(login_url='login')
def postLike(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(id = pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You Must Be Logged First!"))
        return redirect('home')

def follow_toggle(request, pk):
        user =User.objects.get(id=pk)
        if not user:
           message= "user is not found"
        follower = request.user
        try:
            Follow.objects.get(follower=follower, following=user).delete()
            message = 'Unfollowed successfully!'
            is_following = False
        except Follow.DoesNotExist:
            Follow.objects.create(follower=follower, following=user)
            message = 'Followed successfully!'
            is_following = True
        context = {'message': message, 'is_following': is_following}
        return redirect(request.META.get("HTTP_REFERER"))
        
    