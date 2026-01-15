from amsdal.contrib.auth.models.user import User as User
from amsdal.models.mixins import TimestampMixin as TimestampMixin
from amsdal_models.classes.data_models.constraints import UniqueConstraint
from amsdal_models.classes.data_models.indexes import IndexInfo
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from typing import Any, ClassVar

class Account(TimestampMixin, Model):
    """Account (Company/Organization) model.

    Represents a company or organization in the CRM system.
    Owned by individual users with permission controls.
    """
    __module_type__: ClassVar[ModuleType] = ...
    __constraints__: ClassVar[list[UniqueConstraint]] = ...
    __indexes__: ClassVar[list[IndexInfo]] = ...
    name: str = ...
    website: str | None = ...
    phone: str | None = ...
    industry: str | None = ...
    billing_street: str | None = ...
    billing_city: str | None = ...
    billing_state: str | None = ...
    billing_postal_code: str | None = ...
    billing_country: str | None = ...
    owner_email: str = ...
    custom_fields: dict[str, Any] | None = ...
    @property
    def display_name(self) -> str:
        """Return display name for the account."""
    def has_object_permission(self, user: User, action: str) -> bool:
        """Check if user has permission to perform action on this account.

        Args:
            user: The user attempting the action
            action: The action being attempted (read, create, update, delete)

        Returns:
            True if user has permission, False otherwise
        """
    def pre_create(self) -> None:
        """Hook called before creating account."""
    async def apre_create(self) -> None:
        """Async hook called before creating account."""
    def pre_update(self) -> None:
        """Hook called before updating account."""
    async def apre_update(self) -> None:
        """Async hook called before updating account."""
    def post_update(self) -> None:
        """Hook called after updating account."""
    async def apost_update(self) -> None:
        """Async hook called after updating account."""
