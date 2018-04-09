# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

from .forms import *

from .models import Goal, Tag, TagGoal

from django.http import HttpResponse, HttpResponseRedirect, Http404

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
		if form.is_valid():
			username = form.data['email']
			password = form.data['password']
			user = authenticate(request, email=username, password=password)
			login(request, user)
			return redirect('index')
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
	tmpl_vars = {'tag_list': Tag.objects.all(), 'is_authenticated': request.user.is_authenticated}
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
def view_profile(request):
	return render(request, 'view_profile.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})


@login_required(login_url='/karma/login/')
def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('view_profile')
	else:
		form = EditProfileForm()

	return render(request, 'edit_profile.html', {'form': form, 'is_authenticated': request.user.is_authenticated})



@login_required(login_url='/karma/login/')
def myprojects(request):
	return render(request, 'myprojects.html', {'projects': request.user.projects(), 'is_authenticated': request.user.is_authenticated})

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

	return render(request, 'create_project.html', {'form': form, 'is_authenticated': request.user.is_authenticated})

@login_required(login_url='/karma/login/')
def edit_project(request, project_id):
	project = Project.objects.all().filter(id=project_id)[0]
	if request.user != project.user:
		raise Exception("AuthenticationError")

	if request.method == 'POST':
		form = EditProjectForm(request.POST, instance=project)
		if form.is_valid():
			project = form.save(commit=False)
			project.user = request.user
			project.save()
			return redirect('project_detail', project_id)
	else:
		form = EditProjectForm()

	return render(request, 'create_project.html', {'form': form, 'is_authenticated': request.user.is_authenticated})

@login_required(login_url='/karma/login/')
def add_progress(request, project_id):
	project = Project.objects.all().filter(id=project_id)[0]
	if request.user != project.user:
		raise Exception("AuthenticationError")

	if request.method == 'POST':
		form = AddProgressForm(request.POST)
		if form.is_valid():
			progress = form.save(commit=False)
			progress.project = project
			progress.save()
			return redirect('project_detail', project_id)
	else:
		form = AddProgressForm()
	return render(request, 'add_progress.html', {'form': form, 'is_authenticated': request.user.is_authenticated})

@login_required(login_url='/karma/login/')
def edit_progress(request, progress_id):
	progress = Progress.objects.all().filter(id=progress_id)[0]
	project = progress.project
	if request.user != project.user:
		raise Exception("AuthenticationError")

	if request.method == 'POST':
		form = EditProgressForm(request.POST, instance=progress)
		if form.is_valid():
			progress = form.save(commit=False)
			progress.project = project
			progress.save()
			return redirect('project_detail', project.id)
	else:
		form = EditProgressForm()
	return render(request, 'edit_progress.html', {'form': form, 'is_authenticated': request.user.is_authenticated})


def view_goals(request):
	tmpl_vars = {'goal_list': Goal.objects.all(), 'is_authenticated': request.user.is_authenticated}
	return render(request, 'goals.html', tmpl_vars)

def goal_detail(request, goal_id):
	goal = get_object_or_404(Goal, pk=goal_id)
	comments = goal.comments()
	followers = goal.followers()
	total_followers = len(followers)
	projects = goal.projects()
	a = GoalFollowing.objects.all().filter(user=request.user, goal=goal)
	if len(a):
		isFollow = True
	else:
		isFollow = False
	return render(request, 'goal_detail.html', {'projects':projects,'isFollow':isFollow,'total_followers':total_followers, 'followers':followers,'goal': goal, 'comments':comments,'is_authenticated': request.user.is_authenticated})

def project_detail(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (project.isPublic or project.user == request.user):
		raise Http404
	progress = project.progresses()
	comments = project.comments()
	print progress
	followers = project.followers()
	total_followers = len(followers)
	a = ProjectFollowing.objects.all().filter(user=request.user, project=project)
	if len(a):
		isFollow = True
	else:
		isFollow = False
	return render(request, 'project_detail.html', {'isFollow': isFollow, 'total_followers':total_followers,'project': project, 'progress': progress, 'comments':comments, 'is_authenticated': request.user.is_authenticated})

def view_projects(request):
	tmpl_vars = {'project_list': Project.objects.all().filter(isPublic=True), 'is_authenticated': request.user.is_authenticated}
	return render(request, 'projects.html', tmpl_vars)

@anonymous_required
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			return redirect('index')
		else:
			print form.errors, len(form.errors)

	else:
		form = RegisterForm()

	return render(request, 'register.html', {'form': form})

@login_required(login_url='/karma/login/')
def comment_goal(request, goal_id):
	if request.method == 'POST':
		form = CommentOnGoalForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.goal = Goal.objects.all().filter(id=goal_id)[0]
			comment.user = request.user
			comment.save()
			return redirect('goal_detail', goal_id)
		else:
			print form.errors, len(form.errors)

	else:
		form = CommentOnGoalForm()

	return render(request, 'commentgoal.html', {'form': form, 'is_authenticated': request.user.is_authenticated})

@login_required(login_url='/karma/login/')
def comment_project(request, project_id):
	project = Project.objects.all().filter(id=project_id)[0]
	if project.user != request.user and not project.isPublic:
		raise Exception("AuthenticationError")

	if request.method == 'POST':
		form = CommentOnProjectForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.project = project
			comment.user = request.user
			comment.save()
			return redirect('project_detail', project_id)
		else:
			print form.errors, len(form.errors)

	else:
		form = CommentOnProjectForm()

	return render(request, 'commentproject.html', {'form': form, 'is_authenticated': request.user.is_authenticated})

@login_required(login_url='/karma/login/')
def comment_progress(request, progress_id):
	progress = Progress.objects.all().filter(id=progress_id)[0]
	project = progress.project
	if project.user != request.user and not project.isPublic:
		raise Exception("AuthenticationError")

	if request.method == 'POST':
		form = CommentOnProgressForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.progress = progress
			comment.user = request.user
			comment.save()
			return redirect('project_detail', project.id)
		else:
			print form.errors, len(form.errors)

	else:
		form = CommentOnProgressForm()

	return render(request, 'commentprogress.html', {'form': form, 'is_authenticated': request.user.is_authenticated})


@login_required(login_url='/karma/login/')
def follow_goal(request, goal_id):
	a = GoalFollowing()
	a.goal = Goal.objects.all().filter(id=goal_id)[0]
	a.user = request.user
	a.save()
	return redirect(goal_detail, goal_id)

@login_required(login_url='/karma/login/')
def unfollow_goal(request, goal_id):
	goal = Goal.objects.all().filter(id=goal_id)[0]
	a = GoalFollowing.objects.all().filter(user=request.user, goal=goal)[0]
	a.delete()
	return redirect(goal_detail, goal_id)

@login_required(login_url='/karma/login/')
def follow_project(request, project_id):
	a = ProjectFollowing()
	a.project = Project.objects.all().filter(id=project_id)[0]
	a.user = request.user
	a.save()
	return redirect(project_detail, project_id)

@login_required(login_url='/karma/login/')
def unfollow_project(request, project_id):
	project = Project.objects.all().filter(id=project_id)[0]
	a = ProjectFollowing.objects.all().filter(user=request.user, project=project)[0]
	a.delete()
	return redirect(project_detail, project_id)