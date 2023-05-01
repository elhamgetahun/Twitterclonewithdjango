from django.urls  import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('update-user/', views.updateUser, name="update-user"),
    
    path('profile/<str:pk>/', views.userProfile, name="user-profile"), 
    path('post/<str:pk>/', views.postLike, name="post-like"), 
    path('follow/<str:pk>/', views.follow_toggle, name="follow-user"), 
    
    
    
    # path('create-post', views.create_post, name="post_create")
]