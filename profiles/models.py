from django.db import models
from django.contrib.auth.models import User
from ..auth_app.models import UserProfile


class Profile(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="profile"
    )

    @property
    def first_name(self):
        return self.user_profile.user.first_name

    @property
    def last_name(self):
        return self.user_profile.user.last_name

    # TODO: Hier fortsetzten Profile daten anlegen
