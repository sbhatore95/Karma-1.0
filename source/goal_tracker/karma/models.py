# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)

from datetime import datetime
# Create your models here.


#FUTURE BUG = Solve date issue http://paltman.com/a-default-bug-in-django/

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		"""
		Creates and saves a superuser with the given email and password.
		"""
		user = self.create_user(
			email,
			password=password,
		)
		user.admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False) 
	admin = models.BooleanField(default=False) # a superuser
	# notice the absence of a "Password field", that's built in.
	objects = UserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] # Email & Password are required by default.

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	def __str__(self):              # __unicode__ on Python 2
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

class Tag(models.Model):
	tag_name = models.CharField(max_length=50)
	goals = models.IntegerField(default=0)

class Goal(models.Model):
	goal_title = models.CharField(max_length=200)
	goal_description = models.CharField(max_length=500)
	created_at = models.DateTimeField(default=datetime.now()) #give default value??

class TagGoal(models.Model):
	tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
	goal = models.ForeignKey('Goal', on_delete=models.CASCADE)

class Project(models.Model):
	goal = models.ForeignKey('Goal', on_delete=models.PROTECT)
	#user

	project_title = models.CharField(max_length=200)
	project_description = models.CharField(max_length=500)
	cover_pic_url = models.CharField(max_length=250)
	status = models.IntegerField() #what is this
	confidentiality = models.IntegerField(default=0) # 0-private, 1-public

	created_at = models.DateTimeField(default=datetime.now())

class Progress(models.Model):
	project = models.ForeignKey('Project', on_delete=models.CASCADE)

	progress_description = models.CharField(max_length=500)
	created_at = models.DateTimeField(default=datetime.now())

class CommentOnGoal(models.Model):
	#user
	goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
	content = models.CharField(max_length=250)
	created_at = models.DateTimeField(default=datetime.now())

class CommentOnProject(models.Model):
	#user
	project = models.ForeignKey('Project', on_delete=models.CASCADE)
	content = models.CharField(max_length=250)
	created_at = models.DateTimeField(default=datetime.now())

class CommentOnProgress(models.Model):
	#user
	progress = models.ForeignKey('Progress', on_delete=models.CASCADE)
	content = models.CharField(max_length=250)
	created_at = models.DateTimeField(default=datetime.now())
