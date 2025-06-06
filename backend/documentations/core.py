from documentations._base import *

# Authentications
login_schema = extend_schema(
    summary="Login",
    description="This signs in a user",
    request=inline_serializer(
        name="SignInRequest",
        fields={
            "email": serializers.EmailField(),
            "password": serializers.CharField(),
        },
    ),
    responses={
        200: inline_serializer(
            name="SignInResponse",
            fields={
                "detail": serializers.CharField(),
                "user": UserInfoSerializer(),
                "token": inline_serializer(
                    name="Token",
                    fields={
                        "access": serializers.CharField(),
                        "refresh": serializers.CharField(),
                    },
                ),
            },
        ),
    },
    tags=["Authentication"],
)

change_password_schema = extend_schema(
    summary="Change Password",
    description="This changes the password of a user",
    request=inline_serializer(
        name="ChangePasswordRequest",
        fields={
            "current_password": serializers.CharField(),
            "new_password": serializers.CharField(),
        },
    ),
    responses={
        200: inline_serializer(
            name="ChangePasswordResponse", fields={"detail": serializers.CharField()}
        ),
    },
    tags=["Authentication"],
)

# Accounts
list_accounts_schema = extend_schema(
    summary="List Users",
    description="This lists all users",
    responses={
        200: UserInfoSerializer(many=True),
    },
    tags=["Accounts"],
)

retrieve_account_schema = extend_schema(
    summary="Retrieve User Account",
    description="This retrieves a specific user account",
    responses={
        200: UserInfoSerializer(),
    },
    tags=["Accounts"],
)

create_account_schema = extend_schema(
    summary="Create User Account",
    description="This creates a user account",
    request=inline_serializer(
        name="CreateUserAccount",
        fields={
            "email": serializers.EmailField(),
            "password": serializers.CharField(),
            "first_name": serializers.CharField(),
            "last_name": serializers.CharField(),
            "other_names": serializers.CharField(),
            "phone": serializers.CharField(),
            "address": serializers.CharField(),
            "role": serializers.CharField(),
            "image": serializers.ImageField(),
        },
    ),
    responses={
        201: OpenApiResponse(
            inline_serializer(
                name="CreateAccountResponse", fields={"detail": serializers.CharField()}
            )
        ),
    },
    tags=["Accounts"],
)

add_sales_person_schema = extend_schema(
    summary="Create Sales Person Account",
    description="This adds a sales person account",
    request=inline_serializer(
        name="CreateSalePersonAccount",
        fields={
            "email": serializers.EmailField(),
            # "password": serializers.CharField(),
            "first_name": serializers.CharField(),
            "last_name": serializers.CharField(),
            "other_names": serializers.CharField(),
            "phone": serializers.CharField(),
            "address": serializers.CharField(),
            # "image": serializers.ImageField(),
        },
    ),
    responses={
        201: OpenApiResponse(
            inline_serializer(
                name="AddSalesResponse", fields={"detail": serializers.CharField()}
            )
        ),
    },
    tags=["Accounts"],
)

list_sales_persons_schema = extend_schema(
    summary="List Sales Persons",
    description="This lists all sales persons",
    responses={
        200: UserInfoSerializer(many=True),
    },
    tags=["Accounts"],
)

remove_sales_person_schema = extend_schema(
    summary="Remove Sales Person",
    description="This removes a sales person",
    request=UserInfoSerializer,
    responses={
        204: OpenApiResponse(
            inline_serializer(
                name="RemoveSalesResponse", fields={"detail": serializers.CharField()}
            )
        ),
    },
    tags=["Accounts"],
)

update_account_schema = extend_schema(
    summary="Update User Account",
    description="This update a user account",
    request=inline_serializer(
        name="UpdateUserAccount",
        fields={
            "email": serializers.EmailField(),
            "role": serializers.CharField(),
        },
    ),
    responses={
        201: OpenApiResponse(
            inline_serializer(
                name="UpdateAccountResponse", fields={"detail": serializers.CharField()}
            )
        ),
    },
    tags=["Accounts"],
)

delete_account_schema = extend_schema(
    summary="Delete Account",
    description="This deletes a account",
    responses={
        204: OpenApiResponse(
            inline_serializer(
                name="DeleteAccountResponse", fields={"detail": serializers.CharField()}
            )
        ),
    },
    tags=["Accounts"],
)


# Profiles
list_profiles_schema = extend_schema(
    summary="List Profiles",
    description="This lists all profiles",
    responses={
        200: ProfileSerializer(many=True),
    },
    tags=["Profiles"],
)

retrieve_profile_schema = extend_schema(
    summary="Retrieve Profile",
    description="This retrieves a specific profile",
    responses={
        200: ProfileSerializer(),
    },
    tags=["Profiles"],
)

update_profile_schema = extend_schema(
    summary="Update Profile",
    description="This updates a profile",
    request=ProfileSerializer(),
    responses={
        200: ProfileSerializer(),
    },
    tags=["Profiles"],
)

delete_profile_schema = extend_schema(
    summary="Delete Profile",
    description="This deletes a profile",
    responses={
        204: OpenApiResponse(
            inline_serializer(
                name="DeleteProfileResponse", fields={"detail": serializers.CharField()}
            )
        ),
    },
    tags=["Profiles"],
)
