import os
import requests

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from babel.models import Profile, UserAuth
from babel.utils import get_profiles


class RestBackend(object):

    def authenticate(self,access_token=None):
        profiles = get_profiles(access_token)
        username = profiles[0]['service_username']
        try:
            user = User.objects.get(username=username)
            try:
                user_auth = UserAuth.objects.get(user=user)
                try:
                    user_auth['access_token'] = access_token
                except TypeError:
                    pass
            except ObjectDoesNotExist:
                user_auth = UserAuth(user=user, access_token=access_token)
            user_auth.save()
        except User.DoesNotExist:
            user = User(username=username, password='None')
            user.save()
            user_auth = UserAuth(user=user, access_token=access_token)
            user_auth.save()
            for profile in profiles:
                new_profile = Profile(profile_id=profile['id'],user=user, service=profile['service'], username=profile['service_username'])
                new_profile.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None