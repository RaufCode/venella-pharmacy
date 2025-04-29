from core.views._base import *
from core.models.profiles import Profile
from core.serializers.profiles import ProfileSerializer
from core.services.profiles import update_profile


class ProfileViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @list_profiles_schema
    def list(self, request, *args, **kwargs):
        """
        List all profiles
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retrieve_profile_schema
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single profile by ID
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @update_profile_schema
    def update(self, request, *args, **kwargs):
        """
        Update an existing profile
        """
        instance = self.get_object()
        profile, errors = update_profile(instance, request.data)
        if not profile:
            context = {"detail": "Could not update profile", "errors": errors}
            raise ValidationError(context)

        return Response(profile.data, status=status.HTTP_200_OK)

    @delete_profile_schema
    def destroy(self, request, *args, **kwargs):
        """
        Delete a profile
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
