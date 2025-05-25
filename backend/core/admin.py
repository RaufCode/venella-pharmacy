from django.contrib import admin
from core.models.accounts import UserAccount
from core.models.profiles import Profile

admin.site.site_header = "Venella Admin"
admin.site.site_title = "Venella Admin Portal"
admin.site.index_title = "Welcome to Venella Admin Portal"


admin.site.register(UserAccount)
admin.site.register(Profile)
