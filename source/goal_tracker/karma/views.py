# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

from .forms import *

from .models import Goal, Tag, TagGoal

from django.http import HttpResponse

def index(request):
	tmpl_vars = {}
	return render(request, 'index.html', tmpl_vars)

def view_tags(request):
	tmpl_vars = {'tag_list': Tag.objects.all()}
	return render(request, 'tags.html', tmpl_vars)


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
					continue
				t = Tag()
				t.tag_name = tag
				t.save()
				print tag
				tg = TagGoal()
				tg.goal = goal
				tg.tag = t
				tg.save()
				
			tmpl_vars = {}
			return redirect('index')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = CreateGoalForm()

	return render(request, 'create_goal.html', {'form': form})

def view_goals(request):
	tmpl_vars = {'goal_list': Goal.objects.all()}
	return render(request, 'goals.html', tmpl_vars)

def goal_detail(request, goal_id):
	goal = get_object_or_404(Goal, pk=goal_id)
	return render(request, 'goal_detail.html', {'goal': goal})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			tmpl_vars = {}
			return redirect('index')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = RegisterForm()

	return render(request, 'register.html', {'form': form})
