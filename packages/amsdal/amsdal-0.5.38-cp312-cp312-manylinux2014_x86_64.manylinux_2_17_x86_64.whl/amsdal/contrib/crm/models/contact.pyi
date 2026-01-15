from amsdal.contrib.auth.models.user import User as User
from amsdal.contrib.crm.models.account import Account as Account
from amsdal.models.mixins import TimestampMixin as TimestampMixin
from amsdal_models.classes.data_models.constraints import UniqueConstraint
from amsdal_models.classes.data_models.indexes import IndexInfo
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from typing import Any, ClassVar

class Contact(TimestampMixin, Model):
    """Contact (Person) model.

    Represents a person in the CRM system, optionally linked to an Account.
    Owned by individual users with permission controls.
    """
    __module_type__: ClassVar[ModuleType] = ...
    __constraints__: ClassVar[list[UniqueConstraint]] = ...
    __indexes__: ClassVar[list[IndexInfo]] = ...
    first_name: str = ...
    last_name: str = ...
    email: str = ...
    phone: str | None = ...
    mobile: str | None = ...
    title: str | None = ...
    account: Account | None = ...
    owner_email: str = ...
    custom_fields: dict[str, Any] | None = ...
    @property
    def display_name(self) -> str:
        """Return display name for the contact."""
    @property
    def full_name(self) -> str:
        """Return full name of the contact."""
    def has_object_permission(self, user: User, action: str) -> bool:
        """Check if user has permission to perform action on this contact.

        Args:
            user: The user attempting the action
            action: The action being attempted (read, create, update, delete)

        Returns:
            True if user has permission, False otherwise
        """
    def pre_create(self) -> None:
        """Hook called before creating contact."""
    async def apre_create(self) -> None:
        """Async hook called before creating contact."""
    def pre_update(self) -> None:
        """Hook called before updating contact."""
    async def apre_update(self) -> None:
        """Async hook called before updating contact."""
    def post_update(self) -> None:
        """Hook called after updating contact."""
    async def apost_update(self) -> None:
        """Async hook called after updating contact."""
