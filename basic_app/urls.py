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
    re_path(r'^group/(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
    re_path(r'^group/(?P<pk>\d+)/delete/$', views.DeleteGroup.as_view(), name='delete_group'),
    re_path(r'^group/(?P<pk>\d+)/join/$', views.JoinGroup.as_view(), name='join_group'),
    re_path(r'^group/(?P<pk>\d+)/leave/$', views.LeaveGroup.as_view(), name='leave_group'),
    re_path(r'^group/(?P<pk>\d+)/post/$', views.CreatePost.as_view(), name='create_post'),
    re_path(r'^posts/(?P<pk>\d+)/delete/$', views.DeletePost.as_view(), name='delete_post'),
    path('max_groups', views.MaxGroupCount.as_view(), name='max_group_count'),
]