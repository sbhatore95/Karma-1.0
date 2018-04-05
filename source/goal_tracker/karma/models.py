# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Tag(models.Model):
	tag_name = models.CharField(max_length=50)
	goals = models.IntegerField(default=0)

class Goal(models.Model):
	goal_title = models.CharField(max_length=200)
	goal_description = models.CharField(max_length=500)
	created_at = models.DateTimeField() #give default value??

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

	created_at = models.DateTimeField()

class Progress(models.Model):
	project = models.ForeignKey('Project', on_delete=models.CASCADE)

	progress_description = models.CharField(max_length=500)
	created_at = models.DateTimeField()

class CommentOnGoal(models.Model):
	#user
	goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
	content = models.CharField(max_length=250)
	created_at = models.DateTimeField()

class CommentOnProject(models.Model):
	#user
	project = models.ForeignKey('Project', on_delete=models.CASCADE)
	content = models.CharField(max_length=250)
	created_at = models.DateTimeField()

class CommentOnProgress(models.Model):
	#user
	progress = models.ForeignKey('Progress', on_delete=models.CASCADE)
	content = models.CharField(max_length=250)
	created_at = models.DateTimeField()
