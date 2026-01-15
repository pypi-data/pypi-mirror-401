from amsdal.contrib.crm.constants import CRMLifecycleEvent as CRMLifecycleEvent
from amsdal.contrib.crm.models.activity import ActivityRelatedTo as ActivityRelatedTo, ActivityType as ActivityType, Note as Note
from amsdal.contrib.crm.models.deal import Deal as Deal
from amsdal.contrib.crm.models.stage import Stage as Stage
from amsdal_data.transactions.decorators import async_transaction, transaction

class DealService:
    """Business logic for deal management."""
    @classmethod
    @transaction
    def move_deal_to_stage(cls, deal: Deal, new_stage_id: str, note: str | None, user_email: str) -> Deal:
        """Move a deal to a new stage with optional note.

        Creates an activity log entry for stage change and emits lifecycle events.

        Args:
            deal: The deal to move
            new_stage_id: ID of the new stage
            note: Optional note about the stage change
            user_email: Email of user performing the action

        Returns:
            The updated deal
        """
    @classmethod
    @async_transaction
    async def amove_deal_to_stage(cls, deal: Deal, new_stage_id: str, note: str | None, user_email: str) -> Deal:
        """Async version of move_deal_to_stage.

        Args:
            deal: The deal to move
            new_stage_id: ID of the new stage
            note: Optional note about the stage change
            user_email: Email of user performing the action

        Returns:
            The updated deal
        """
