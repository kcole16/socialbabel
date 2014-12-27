from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class UserAuth (models.Model):
	user = models.ForeignKey(User)
	access_token = models.CharField(max_length=500)

class Profile(models.Model):
	profile_id = models.CharField(max_length=1000)
	user = models.ForeignKey(User)
	service = models.CharField(max_length=200)
	username = models.CharField(max_length=200)

class Update(models.Model):
	user = models.ForeignKey(User)
	profile = models.ForeignKey(Profile)
	uid = models.CharField(max_length=160)
	raw_update = models.CharField(max_length=1000)
	translated_update = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)









