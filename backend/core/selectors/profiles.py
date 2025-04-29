from core.models.profiles import Profile
from core.serializers.profiles import ProfileSerializer


def get_profile_by_id(profile_id: str) -> Profile:
    """
    Get a profile by its ID.
    """
    try:
        return Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return None
