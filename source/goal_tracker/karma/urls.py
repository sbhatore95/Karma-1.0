from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('index/', views.index, name='index'),
    url('register/', views.register, name='register'),
    url('create_goal/', views.create_goal, name='create_goal'),
    url('goals/', views.view_goals, name='view_goals'),
    url('tags/', views.view_tags, name='view_tags'),
    url('goal/(?P<goal_id>\d+)/$', views.goal_detail, name='goal_detail'),
]
