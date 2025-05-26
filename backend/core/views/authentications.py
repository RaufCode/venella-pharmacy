from core.views._base import *
from core.selectors.accounts import *


# class PasswordViewSet(viewsets.ViewSet):
#     """Manages password change and reset"""

#     def request_token(self, request):
#         """Request password reset token"""
#         data = request.data
#         user = get_user_by_email(data.get("email"))
#         if not user:
#             context = {
#                 "detail": "No account found",
#                 "errors": {"email": [f"no account exists for '{data.get('email')}' "]},
#             }
#             raise NotFound(context)

#         email_thread = threading.Thread(
#             target=password_reset, args=[user, user.email, OTP_LENGTH]
#         )
#         email_thread.start()

#         context = {"detail": "password reset verification token sent"}
#         return Response(context, status.HTTP_200_OK)

#     def reset_password(self, request):
#         """
#         Reset password for a user account
#         """
#         email = request.data.get("email")
#         otp = request.data.get("otp")
#         password = request.data.get("password")

#         # validate the provided data
#         err: bool = False
#         errors: dict = {}
#         if not email:
#             err = True
#             errors.update({"email": ["this field is required"]})
#         if not password:
#             err = True
#             errors.update({"password": ["this field is required"]})
#         if not otp:
#             err = True
#             errors.update({"otp": ["this field is required"]})

#         if err:
#             context = {"detail": "invalid data", "errors": errors}
#             raise ValidationException(context)

#         user = get_user_by_email(email)
#         if not user:
#             context = {
#                 "detail": "user not found",
#                 "errors": {"email": [f"no account found for '{email}' "]},
#             }
#             raise NotFound(context)

#         token = get_password_reset_token(email)
#         if not token:
#             context = {"detail": "request verification token"}
#             raise NotFound(context)

#         if otp != token.otp:
#             context = {"detail": "invalid otp provided"}
#             raise NotAcceptable(context)

#         if UTC.localize(datetime.now()) >= token.time_generated + timedelta(minutes=30):
#             context = {"detail": "expired otp, request a new one"}
#             raise NotAcceptable(context)

#         user.set_password(password)
#         user.save()
#         token.delete()

#         e_t = threading.Thread(target=password_reset_confirmation, args=[user, email])
#         e_t.start()

#         context = {"detail": "password reset successful"}
#         return Response(context, status=status.HTTP_200_OK)

#     def change_password(self, request, user_id):
#         """Change password for a user account"""
#         current_password = request.data.get("current_password")
#         password = request.data.get("password")

#         err: bool = False
#         errors: dict = {}
#         if not current_password:
#             err = True
#             errors.update({"current_password": ["this field is required"]})
#         if not password:
#             err = True
#             errors.update({"password": ["this field is required"]})

#         if err:
#             context = {"detail": "missing required data", "errors": errors}
#             raise ValidationException(context)

#         user = get_user_by_id(user_id)
#         if not user:
#             context = {
#                 "detail": "user not found",
#                 "errors": {
#                     "email": [f"invalid pk'{user_id}' - object does not exist "]
#                 },
#             }
#             raise NotFound(context)

#         if not user.check_password(current_password):
#             context = {"detail": "incorrect current password"}
#             raise NotAcceptable(context)

#         user.set_password(password)
#         user.save()

#         context = {"detail": "password successfully changed"}
#         return Response(context, status.HTTP_200_OK)


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
