# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class User_manager(models.Manager):
	def basic_validation(self, postData):
		errors = {}
		if len(postData['name']) < 2:
			errors["name"] = "name should be at least 2 characters"
		if len(postData['alias']) < 2:
			errors["alias"] = "alias should be at least 2 characters"
		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "email must match standard email format"
		if postData['password'] != postData['password2']:
			errors['password2'] = "passwords needs to match"
		if postData['dob'] == None:
			errors['birthday'] = "How freakin' old are you?"
		if len(postData['password']) < 8:
			errors['password'] = "password needs to be at least 8 characters"
		return errors

class Users(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	birthday = models.DateField()
	friends = models.ManyToManyField("self", related_name="of_friends")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = User_manager()