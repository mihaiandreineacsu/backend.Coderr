from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CUSTOMER,
    )

    def __str__(self):
        return self.user.username
