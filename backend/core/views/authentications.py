from core.views._base import *
from core.selectors.accounts import *
from core.utils.general import validate_posted_data


class PasswordViewSet(viewsets.ViewSet):
    """Manages password change and reset"""

    @change_password_schema
    def change_password(self, request, user_id):
        """Change password for a user account"""

        err, errors = validate_posted_data(
            request.data, ["current_password", "new_password"]
        )
        if err:
            context = {"detail": "missing required data", "errors": errors}
            raise ValidationError(context)

        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        user = get_user_account_by_id(user_id)
        if not user:
            context = {
                "detail": "user not found",
                "errors": {
                    "email": [f"invalid pk'{user_id}' - object does not exist "]
                },
            }
            raise NotFound(context)

        if not user.check_password(current_password):
            context = {"detail": "incorrect current password"}
            raise NotAcceptable(context)

        user.set_password(new_password)
        user.save()

        context = {"detail": "password successfully changed"}
        return Response(context, status.HTTP_200_OK)


class SignInView(APIView):

    permission_classes = [AllowAny]

    @login_schema
    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("missing required login credential")

        user = get_user_account_by_email(email)

        if not user:
            context = {
                "detail": "User not found",
                "errors": {"email": [f"no account found for '{email}'"]},
            }
            raise NotFound(context)

        if user.check_password(password) and user.is_active:
            # generate token for user
            token = RefreshToken.for_user(user)
            user_data = user_account_representation(request, user)
            context = {
                "detail": "Login successful",
                "user": user_data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            }
            return Response(context, status=status.HTTP_200_OK)

        raise AuthenticationFailed("Incorrect login credentials provided")
