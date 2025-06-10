from core.models._base import *


class Profile(models.Model):
    id = models.UUIDField(
        editable=False, unique=True, primary_key=True, default=uuid.uuid4
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True, region=None)
    address = models.TextField(blank=True, null=True)

    @property
    def full_name(self):
        full_name = (
            f"{self.first_name} {self.other_names} {self.last_name}"
            if self.other_names
            else f"{self.first_name} {self.last_name}"
        )
        return full_name

    def __str__(self) -> str:
        return self.full_name

    def profile_accounts(self):
        """Get all accounts linked to this profile"""
        return self.profile_accounts.all()
