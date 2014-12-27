from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.db import IntegrityError, connection, transaction
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from babel.models import Update, UserAuth, Profile
from babel.forms import UpdateForm, ProfileForm
from babel.utils import *

from datetime import datetime

import os

@login_required
def home(request):
	profiles = Profile.objects.filter(user=request.user)
	if request.POST:
		form = ProfileForm(request.POST)
		form.is_valid()
		profile_id = form.cleaned_data['profile']
		url = reverse('babel_updates', args=[profile_id,1,])
		return HttpResponseRedirect(url) 
	else:
		form = ProfileForm()

	return render_to_response('core/home.html',{'form':form, 'profiles':profiles}, context_instance=RequestContext(request))

def user_login(request):
	client_id = os.environ['BUFFER_CLIENT_ID']
	redirect_uri = 'http://babelbuffer.herokuapp.com/oauth/'
	url = 'https://bufferapp.com/oauth2/authorize?client_id=%s&redirect_uri=%s&response_type=code' % (client_id, redirect_uri)
	return HttpResponseRedirect(url)

def oauth(request):
	code = request.GET['code']
	access_token = authenticate_buffer(code)
	user = authenticate(access_token=access_token)
	login(request, user)
	url = reverse('home')
	return HttpResponseRedirect(url) 

def logout_view(request):
	logout(request)
	return redirect('login')

def updates(request, profile_id):
	access_token = UserAuth.objects.get(user_id=request.user.id).access_token
	updates = get_updates(access_token, profile_id)
	paginator = Paginator(updates, 6)
	page = request.GET.get('page', 1)

	try:
		page = int(page)
		updates = paginator.page(page)

	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		updates = paginator.page(1)

	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of
		# results.
		updates = paginator.page(paginator.num_pages)
	# campaigns_list["pages_available"] = pages_available

	service = Profile.objects.get(profile_id=profile_id).service.capitalize()
	return render_to_response('babel/updates.html',{'updates':updates, 'service':service}, context_instance=RequestContext(request))

def new_update(request, update_id):
	user = User.objects.get(id=request.user.id)
	access_token = UserAuth.objects.get(user_id=user.id).access_token
	languages = (('en', 'English'),
		('zh', 'Mandarin Chinese'),
		('es', 'Spanish'),
		('de', 'German'),
		('fr', 'French'),
		('ru', 'Russian'),
		('ar', 'Arabic'),
		('it', 'Italian'),
		('pt', 'Portuguese'))

	language_dict = {'en':'English','zh':'Mandarin Chinese','es':'Spanish','de':'German','fr':'French',
					'ru':'Russian','ar':'Arabic','it':'Italian','pt':'Portuguese'}
	if request.POST:
		form = UpdateForm(request.POST)
		if form.is_valid():
			target_lang = str(form.cleaned_data['target_language'])
			raw_update, translated_update, profile_id = translate_update(update_id, target_lang, access_token)	
			uid = 'a123'
			profile = Profile.objects.get(profile_id=profile_id)
			if translated_update != "Exists":
				new_update = Update(user=user, uid=uid, raw_update=raw_update, 
					translated_update=translated_update, profile=profile)
				new_update.save()				
			success = True
			update_info = {'translated_update':translated_update, 'target_lang':language_dict[target_lang]}
			return render_to_response('babel/new_update.html',{'success':success, 'update_info':update_info}, context_instance=RequestContext(request))
		else:
			print form.errors
	else:
		form = UpdateForm()
	return render_to_response('babel/new_update.html',{'form':form, 'languages':languages, 'update_id':update_id}, context_instance=RequestContext(request))

 



