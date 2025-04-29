from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    extend_schema_serializer,
    inline_serializer,
    OpenApiParameter,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from core.serializers.profiles import ProfileSerializer


class UserInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    profile = ProfileSerializer()
    account_type = serializers.CharField()
