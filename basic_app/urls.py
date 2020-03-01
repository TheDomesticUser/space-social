from django.urls import path, re_path
from . import views

app_name = 'basic_app'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('signup/', views.UserSignUp.as_view(), name='user_signup'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
]