# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

from .forms import *

from .models import Goal, Tag, TagGoal

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

 
def anonymous_required( view_function, redirect_to = '/karma/index' ):
	return AnonymousRequired( view_function, redirect_to )
 
class AnonymousRequired( object ):
	def __init__( self, view_function, redirect_to ):
		if redirect_to is None:
			from django.conf import settings
			redirect_to = settings.LOGIN_REDIRECT_URL
		self.view_function = view_function
		self.redirect_to = redirect_to

	def __call__( self, request, *args, **kwargs ):
		if request.user is not None and request.user.is_authenticated():
			return HttpResponseRedirect( self.redirect_to ) 
		return self.view_function( request, *args, **kwargs )

@anonymous_required
def login_user(request):
	if request.method == 'POST':
		form = CreateProjectForm(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			project.user = request.user
			project.save()
			return redirect('index')
	else:
		form = CreateProjectForm()

	if request.method == 'POST':
		form = LoginForm(request.POST)
		username = form.data['email']
		password = form.data['password']
		user = authenticate(request, email=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			raise AuthenticationError('Incorrect email or password')
	else :
		form = LoginForm()
	return render(request, 'login.html', {'form': form})

@login_required(login_url='/karma/login/')
def logout_user(request):
	logout(request)
	return redirect('index')


def index(request):
	tmpl_vars = {'user' : request.user, 'is_authenticated': request.user.is_authenticated}
	print request.user
	return render(request, 'index.html', tmpl_vars)

def view_tags(request):
	tmpl_vars = {'tag_list': Tag.objects.all()}
	return render(request, 'tags.html', tmpl_vars)


@login_required(login_url='/karma/login/')
def create_goal(request):
	if request.method == 'POST':
		form = CreateGoalForm(request.POST)
		if form.is_valid():
			goal = form.save()
			taglist = str(form.cleaned_data['taglist']).split(',')
			for tag in taglist:
				tag = tag.lower()
				qs = Tag.objects.filter(tag_name=tag)
				if qs.exists():
					#increment goal counter
					continue
				else:
					t = Tag()
					t.tag_name = tag
					t.save()
					tg = TagGoal()
					tg.goal = goal
					tg.tag = t
					tg.save()
					#goal counter = 1
				
			return redirect('index')

	else:
		form = CreateGoalForm()

	return render(request, 'create_goal.html', {'form': form})

@login_required(login_url='/karma/login/')
def create_project(request):
	if request.method == 'POST':
		form = CreateProjectForm(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			project.user = request.user
			project.save()
			return redirect('index')
	else:
		form = CreateProjectForm()

	return render(request, 'create_project.html', {'form': form})

def view_goals(request):
	tmpl_vars = {'goal_list': Goal.objects.all()}
	return render(request, 'goals.html', tmpl_vars)

def goal_detail(request, goal_id):
	goal = get_object_or_404(Goal, pk=goal_id)
	return render(request, 'goal_detail.html', {'goal': goal})

def project_detail(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	return render(request, 'project_detail.html', {'project': project})

def view_projects(request):
	tmpl_vars = {'project_list': Project.objects.all()}
	return render(request, 'projects.html', tmpl_vars)


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			return redirect('index')

	else:
		form = RegisterForm()

	return render(request, 'register.html', {'form': form})
