from core.serializers.accounts import UserAccountSerializer
from core.models.accounts import UserAccount


def create_user_account(data: dict):
    serializer = UserAccountSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    return None, serializer.errors


def update_user_account(data: dict, instance: UserAccount):
    serializer = UserAccountSerializer(data=data, instance=instance, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return None


def delete_user_account(instance: UserAccount):
    if instance.profile:
        instance.profile.delete()
    instance.delete()
    return True
