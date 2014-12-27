from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime

class UpdateForm(forms.Form):
    target_language = forms.CharField(max_length=100)

class ProfileForm(forms.Form):
	profile = forms.CharField(max_length=100)