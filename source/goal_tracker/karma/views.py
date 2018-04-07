# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .forms import *

from django.http import HttpResponse

def index(request):
	tmpl_vars = {}
	return render(request, 'index.html', tmpl_vars)


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
