from rest_framework import serializers
from core.models.accounts import UserAccount
from core.serializers.profiles import ProfileSerializer


class UserAccountSerializer(serializers.ModelSerializer):
    """
    Serializes the UserAccount model
    """

    class Meta:
        model = UserAccount
        exclude = [
            "is_superuser",
            "is_staff",
            "date_created",
            "last_login",
            "groups",
            "user_permissions",
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["profile"] = (
            ProfileSerializer(
                instance.profile, context={"request": self.context.get("request")}
            ).data
            if instance.profile
            else None
        )
        data["account_type"] = instance.get_account_type()
        data.pop("role", None)
        data.pop("password", None)
        data["has_profile"] = True if instance.profile else False
        return data
