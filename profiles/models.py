from django.db import models
from django.contrib.auth.models import User
from ..auth_app.models import UserProfile


class Profile(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="profile"
    )
    file = models.CharField( blank=False, default="profile_picture.jpg")
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=30, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"Profile of {self.user.user.username}"

    @property
    def username(self):
        return self.user.user.username

    @property
    def first_name(self):
        return self.user.user.first_name

    @property
    def last_name(self):
        return self.user.user.last_name

    @property
    def email(self):
        return self.user.user.email or ""

    @property
    def type(self):
        return self.user.type

    @property
    def created_at(self):
        return self.user.user.date_joined


{
    "user": 1,
    "username": "max_mustermann",
    "first_name": "Max",
    "last_name": "Mustermann",
    "file": "profile_picture.jpg",
    "location": "Berlin",
    "tel": "123456789",
    "description": "Business description",
    "working_hours": "9-17",
    "type": "business",
    "email": "max@business.de",
    "created_at": "2023-01-01T12:00:00",
}
