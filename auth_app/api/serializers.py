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

    def validate(self, attrs):
        pw = attrs.get("password")
        repeated_pw = attrs.get("repeated_password")
        email = attrs.get("email")

        if pw != repeated_pw:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email is already in use."})

        return attrs

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        user_type = validated_data.pop("type")

        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()

        UserProfile.objects.create(user=user, type=user_type)
        return user
