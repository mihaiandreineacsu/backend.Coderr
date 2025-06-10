from django.contrib import admin
from profiles_app.models import Profile

class CustomAdmin(admin.ModelAdmin):
    list_filter = []

admin.site.register(Profile , CustomAdmin)
