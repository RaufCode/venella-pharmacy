from rest_framework import serializers
from core.models.profiles import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes the Profile model
    """

    class Meta:
        model = Profile
        fields = "__all__"
