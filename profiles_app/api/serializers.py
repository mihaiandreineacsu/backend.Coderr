from rest_framework import serializers
from django.contrib.auth.models import User
from profiles_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for profile list / patch when pk is current user
    """
    user = serializers.IntegerField(source="user.user.id", read_only=True)
    username = serializers.CharField(source="user.user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    created_at = serializers.DateTimeField(
        source="user.user.date_joined", read_only=True
    )

    first_name = serializers.CharField(source="user.user.first_name", max_length=150)
    last_name = serializers.CharField(source="user.user.last_name", max_length=150)
    email = serializers.EmailField(source="user.user.email")

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = ["user", "username", "type", "created_at", "file"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {}).get("user", {})
        user = instance.user.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class BusinessProfileListSerializer(ProfileSerializer):
    """
    Serializer for business profiles list.
    """

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "created_at",
            "type",
        ]


class CustomerProfileListSerializer(ProfileSerializer):
    """
    Serializer for customer profiles list.
    """

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "type",
        ]
