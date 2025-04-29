from django.contrib import admin
from core.models.accounts import UserAccount
from core.models.profiles import Profile



admin.site.register(UserAccount)
admin.site.register(Profile)