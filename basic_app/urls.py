from django.urls import path, re_path
from . import views

app_name = 'basic_app'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('signup/', views.UserSignUp.as_view(), name='user_signup'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
    path('create_group/', views.CreateGroup.as_view(), name='create_group'),
    path('groups/', views.ListGroups.as_view(), name='groups_list'),
]