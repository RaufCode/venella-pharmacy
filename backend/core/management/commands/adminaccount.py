from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models.profiles import Profile


class Command(BaseCommand):
    help = "Creates a default admin user after first migration"

    def handle(self, *args, **options):
        User = get_user_model()
        email = "admin@venella.com"
        if not User.objects.filter(email=email).exists():
            # Create a default profile for the admin user
            profile, created = Profile.objects.get_or_create(
                first_name="Admin",
                last_name="User",
            )
            admin_user = User.objects.create_superuser(
                email=email,
                password="admin1234",
                profile=profile,
                is_active=True,
                role="admin",
            )
            admin_user.set_password("admin1234")
            admin_user.save()

            self.stdout.write(self.style.SUCCESS(f"Admin user {email} created."))
        else:
            self.stdout.write(self.style.WARNING(f"Admin user {email} already exists."))
