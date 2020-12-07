from django.contrib import admin
from users.models import Profile

admin.site.site_header = "Giving 2020 | Administration"
admin.site.site_title = "Giving 2020"

admin.site.register(Profile)
