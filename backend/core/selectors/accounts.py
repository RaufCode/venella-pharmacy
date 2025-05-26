from core.serializers.accounts import UserAccountSerializer
from core.models.accounts import UserAccount


def get_user_account_by_id(user_account_id: str) -> UserAccount:
    """
    Get a user account by its ID
    """
    try:
        return UserAccount.objects.get(id=user_account_id)
    except UserAccount.DoesNotExist:
        return None


def get_user_account_by_email(email: str) -> UserAccount:
    """
    Get a user account by its email
    """
    try:
        return UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
        return None


def get_all_users() -> UserAccount:
    return UserAccount.objects.all()


def user_account_representation(
    request, user_account: UserAccount, many: bool = False
) -> dict:
    """
    Get user account data
    """
    serializer = UserAccountSerializer(
        user_account, many=many, context={"request": request}
    )
    return serializer.data
