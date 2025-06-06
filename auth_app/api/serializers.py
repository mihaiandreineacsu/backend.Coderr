from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "type"]


class RegistrationsSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.UserType.choices, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        pw = self.validated_data["password"]
        repeatet_pw = self.validated_data["repeated_password"]
        email = self.validated_data["email"]

        if pw != repeatet_pw:
            raise serializers.ValidationError({"error": "Password don't match!"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email is already in use!"})

        user = User(email=email, username=self.validated_data["username"])
        user.set_password(pw)
        user.save()

        user_type = self.validated_data["type"]
        UserProfile.objects.create(user=user, type=user_type)

        return user
