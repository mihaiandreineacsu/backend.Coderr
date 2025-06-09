from django.contrib import admin
from .models import UserProfile

class CustomAdmin(admin.ModelAdmin):
    list_filter = ["type"]

admin.site.register(UserProfile , CustomAdmin)