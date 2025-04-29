from core.serializers.profiles import ProfileSerializer
from core.models.profiles import Profile


def create_profile(data: dict):
    """
    Create a new profile instance.
    """
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    return None, serializer.errors


def update_profile(profile: Profile, data: dict):
    """
    Update an existing profile instance.
    """
    serializer = ProfileSerializer(instance=profile, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    return None, serializer.errors
