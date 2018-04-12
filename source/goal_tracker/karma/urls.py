from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('unfollow_goal/(?P<goal_id>\d+)/$', views.unfollow_goal, name='unfollow_goal'),
    url('follow_goal/(?P<goal_id>\d+)/$', views.follow_goal, name='follow_goal'),
    url('unfollow_project/(?P<project_id>\d+)/$', views.unfollow_project, name='unfollow_project'),
    url('follow_project/(?P<project_id>\d+)/$', views.follow_project, name='follow_project'),
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
    url('commentgoal/(?P<goal_id>\d+)/$', views.comment_goal, name='commentgoal'),
    url('commentproject/(?P<project_id>\d+)/$', views.comment_project, name='commentproject'),
    url('commentprogress/(?P<progress_id>\d+)/$', views.comment_progress, name='commentprogress'),
    url('goal/(?P<goal_id>\d+)/$', views.goal_detail, name='goal_detail'),
    url('edit_project/(?P<project_id>\d+)/$', views.edit_project, name='edit_project'),
    url('project/(?P<project_id>\d+)/$', views.project_detail, name='project_detail'),
    url('add_progress/(?P<project_id>\d+)/$', views.add_progress, name='add_progress'),
    url('edit_progress/(?P<progress_id>\d+)/$', views.edit_progress, name='edit_progress'),
    url('tag_detail/(?P<tag_id>\d+)/$', views.tag_detail, name='tag_detail'),
   
]
