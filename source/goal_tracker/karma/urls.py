from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('index/', views.index, name='index'),
    url('login/', views.login_user, name='login_user'),
    url('logout/', views.logout_user, name='logout_user'),
    url('register/', views.register, name='register'),
    url('edit_profile/', views.edit_profile, name='edit_profile'),
    url('profile/', views.view_profile, name='view_profile'),
    url('create_goal/', views.create_goal, name='create_goal'),
    url('create_project/', views.create_project, name='create_project'),
    url('goals/', views.view_goals, name='view_goals'),
    url('myprojects/', views.myprojects, name='myprojects'),
    url('projects/', views.view_projects, name='view_projects'),
    url('tags/', views.view_tags, name='view_tags'),
    url('goal/(?P<goal_id>\d+)/$', views.goal_detail, name='goal_detail'),
    url('project/(?P<project_id>\d+)/$', views.project_detail, name='project_detail'),
]
