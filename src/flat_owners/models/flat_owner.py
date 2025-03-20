from src.authentication.models import CustomUser
from src.flat_owners.managers.flat_owner import FlatOwnerManager


class FlatOwner(CustomUser):
    objects = FlatOwnerManager()

    class Meta:
        proxy = True