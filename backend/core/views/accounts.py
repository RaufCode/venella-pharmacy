from core.views._base import *
from core.selectors.accounts import *
from core.selectors.profiles import get_profile_by_id
from core.services.accounts import *
from core.services.profiles import create_profile
from core.utils.general import validate_posted_data, InMemoryUploadedFileHandler


class UserAccountViewset(viewsets.ViewSet):
    """Manages user account creation and management"""

    @create_account_schema
    def create(self, request):
        """
        Create a new user account
        """
        data = request.data
        # Validate the posted data
        err, errors = validate_posted_data(
            data,
            [
                "email",
                "password",
                "first_name",
                "last_name",
                "phone",
                "address",
            ],
        )
        if err:
            context = {"detail": "Missing required fields", "errors": errors}
            raise ValidationError(context)

        user = get_user_account_by_email(data.get("email"))
        if user:
            context = {"detail": "Account with this email already exists"}
            raise ValidationError(context)

        # Create a profile for the user
        profile_data = {
            "first_name": data.pop("first_name"),
            "last_name": data.pop("last_name"),
            "other_names": data.pop("other_name", None),
            "phone": data.pop("phone"),
            "address": data.pop("address"),
            "image": data.pop("image", None),
        }

        if profile_data.get("image"):
            image = profile_data.get("image")
            if isinstance(image, str):
                handler = InMemoryUploadedFileHandler()
                image = handler.from_img_path(image)
                print("image created", image)

            profile_data["image"] = image

        profile_data, profile_errors = create_profile(profile_data)
        if not profile_data:
            context = {
                "detail": "Could not create user profile",
                "errors": profile_errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile_by_id(profile_data.get("id"))

        data.update({"role": "customer"})
        user_data, errors = create_user_account(data)
        if not user_data:
            context = {"detail": "Could not create user account", "errors": errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_account_by_id(user_data.get("id"))
        user.set_password(data["password"])
        user.profile = profile
        user.save()

        context = {"detail": "Account created successfully"}
        return Response(context, status=status.HTTP_201_CREATED)

    @add_sales_person_schema
    def add_sales_person(self, request):

        data = request.data
        # Validate the posted data
        err, errors = validate_posted_data(
            data,
            [
                "email",
                "password",
                "first_name",
                "last_name",
                "phone",
                "address",
            ],
        )
        if err:
            context = {"detail": "Missing required fields", "errors": errors}
            raise ValidationError(context)

        user = get_user_account_by_email(data.get("email"))
        if user:
            context = {"detail": "Account with this email already exists"}
            raise ValidationError(context)

        # Create a profile for the user
        profile_data = {
            "first_name": data.pop("first_name")[0],
            "last_name": data.pop("last_name")[0],
            "other_names": (
                data.pop("other_name")[0] if data.get("other_name") else None
            ),
            "phone": data.pop("phone")[0],
            "address": data.pop("address")[0],
            "image": data.pop("image", None)[0],
        }

        if profile_data.get("image"):
            image = profile_data.get("image")
            if isinstance(image, str):
                handler = InMemoryUploadedFileHandler()
                image = handler.from_img_path(image)

            profile_data["image"] = image

        profile_data, profile_errors = create_profile(profile_data)
        if not profile_data:
            context = {
                "detail": "Could not create user profile",
                "errors": profile_errors,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        profile = get_profile_by_id(profile_data.get("id"))

        data.update({"role": "salesperson"})
        user_data, errors = create_user_account(data)
        if not user_data:
            context = {"detail": "Could not create user account", "errors": errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_account_by_id(user_data.get("id"))
        user.set_password(data["password"])
        user.profile = profile
        user.save()

        context = {"detail": "Sales persson added successfully"}
        return Response(context, status=status.HTTP_201_CREATED)

    @list_accounts_schema
    def list(self, request):
        users = get_all_users()
        context = user_account_info(request, users, many=True)
        return Response(context, status=status.HTTP_200_OK)

    @retrieve_account_schema
    def retrieve(self, request, user_id):
        """
        Retrieve a user account by ID
        """
        user = get_user_account_by_id(user_id)
        if not user:
            context = {"detail": "User account not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        context = user_account_info(request, user)
        return Response(context, status=status.HTTP_200_OK)

    @update_account_schema
    def update(self, request, user_id):
        """
        Update a user account by ID
        """
        user = get_user_account_by_id(user_id)
        if not user:
            context = {"detail": "User account not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        updated_user_data = update_user_account(data, user)
        if not updated_user_data:
            context = {"detail": "Could not update user account"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        context = {"detail": "User account updated successfully"}
        return Response(context, status=status.HTTP_200_OK)

    @delete_account_schema
    def destroy(self, request, user_id):
        """
        Delete a user account by ID
        """
        user = get_user_account_by_id(user_id)
        if not user:
            context = {"detail": "User account not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        delete_user_account(user)

        context = {"detail": "User account deleted successfully"}
        return Response(context, status=status.HTTP_204_NO_CONTENT)
