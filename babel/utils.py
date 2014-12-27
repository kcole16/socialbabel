from django.contrib.auth.models import User
from social.apps.django_app.default.models import *
from base.settings import *

import requests
import json
import os

def add_to_queue(text, profile, due_at, access_token):
    url = 'https://api.bufferapp.com/1/updates/create.json?access_token=%s' % access_token
    data = {'text':text, 'profile_ids[]': profile, 'scheduled_at':due_at}
    r = requests.post(url, data=data)
    if r.ok:
        return True
    else:
        return False

def get_update_text(update_id, access_token):
    url = 'https://api.bufferapp.com/1/updates/%s.json?access_token=%s' % (update_id, access_token)
    r = requests.get(url)
    text = r.json()['text']
    profile = r.json()['profile_id']
    due_at = r.json()['due_at']
    return text, due_at, profile

def get_source_lang(text, yandex_key):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect?key=%s&text=%s' % (yandex_key, text)
    r = requests.get(url)
    source_lang = r.json()['lang']
    return source_lang

def translate_update(update_id, lang, access_token):
    text, due_at, profile = get_update_text(update_id, access_token)
    yandex_key = os.environ['YANDEX_KEY']
    source_lang = get_source_lang(text, yandex_key)
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&lang=%s-%s&text=%s' % (yandex_key, source_lang, lang, text)
    r = requests.get(url)
    translated_text = r.json()['text'][0]
    success = add_to_queue(translated_text, profile, due_at, access_token)
    if success != True:
        translated_text = "Exists"
    return text, translated_text, profile

def authenticate_buffer(code):
    url = 'https://api.bufferapp.com/1/oauth2/token.json'
    client_id = os.environ['BUFFER_CLIENT_ID']
    client_secret = os.environ['BUFFER_CLIENT_SECRET']
    data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': 'http://babelbuffer.herokuapp.com/oauth/',
    'code': code,
    'grant_type': 'authorization_code'
    }
    r = requests.post(url, data=data)
    access_token = r.json()['access_token']
    print access_token
    return access_token

def get_profiles(access_token):
    url = 'https://api.bufferapp.com/1/profiles.json?access_token=%s' % access_token
    r = requests.get(url)
    profiles = r.json()
    return profiles

def get_updates(access_token, profile_id):
    url = 'https://api.bufferapp.com/1/profiles/%s/updates/pending.json?access_token=%s' % (profile_id, access_token)
    r = requests.get(url)
    updates = r.json()['updates']
    return updates



