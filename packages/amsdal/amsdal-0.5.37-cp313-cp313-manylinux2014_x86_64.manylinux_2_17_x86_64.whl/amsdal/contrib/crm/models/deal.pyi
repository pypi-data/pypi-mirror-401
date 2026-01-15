import datetime as _dt
from amsdal.contrib.auth.models.user import User as User
from amsdal.contrib.crm.models.account import Account as Account
from amsdal.contrib.crm.models.contact import Contact as Contact
from amsdal.contrib.crm.models.stage import Stage as Stage
from amsdal.models.mixins import TimestampMixin as TimestampMixin
from amsdal_models.classes.data_models.indexes import IndexInfo
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from typing import Any, ClassVar

class Deal(TimestampMixin, Model):
    """Deal (Sales Opportunity) model.

    Represents a sales opportunity linked to an account and contact,
    progressing through pipeline stages.
    """
    __module_type__: ClassVar[ModuleType] = ...
    __indexes__: ClassVar[list[IndexInfo]] = ...
    name: str = ...
    amount: float | None = ...
    currency: str = ...
    account: Account | None = ...
    contact: Contact | None = ...
    stage: Stage = ...
    owner_email: str = ...
    expected_close_date: _dt.datetime | None = ...
    closed_date: _dt.datetime | None = ...
    is_closed: bool = ...
    is_won: bool = ...
    custom_fields: dict[str, Any] | None = ...
    @property
    def display_name(self) -> str:
        """Return display name for the deal."""
    @property
    def stage_name(self) -> str:
        """Returns stage name for display."""
    def has_object_permission(self, user: User, action: str) -> bool:
        """Check if user has permission to perform action on this deal.

        Args:
            user: The user attempting the action
            action: The action being attempted (read, create, update, delete)

        Returns:
            True if user has permission, False otherwise
        """
    def pre_create(self) -> None:
        """Hook called before creating deal."""
    async def apre_create(self) -> None:
        """Async hook called before creating deal."""
    def pre_update(self) -> None:
        """Hook called before updating deal.

        Automatically syncs is_closed and is_won status with stage,
        and sets closed_date when deal is closed.
        """
    async def apre_update(self) -> None:
        """Async hook called before updating deal.

        Automatically syncs is_closed and is_won status with stage,
        and sets closed_date when deal is closed.
        """
    def post_update(self) -> None:
        """Hook called after updating deal."""
    async def apost_update(self) -> None:
        """Async hook called after updating deal."""
