from amsdal.contrib.crm.models.activity import Activity as Activity, ActivityRelatedTo as ActivityRelatedTo

class ActivityService:
    """Service for querying and managing activities."""
    @classmethod
    def get_timeline(cls, related_to_type: ActivityRelatedTo, related_to_id: str, limit: int = 100) -> list[Activity]:
        """Get chronological activity timeline for a record.

        Args:
            related_to_type: Type of record (Contact, Account, Deal)
            related_to_id: ID of the record
            limit: Maximum number of activities to return

        Returns:
            List of activities sorted by created_at desc (newest first)
        """
    @classmethod
    async def aget_timeline(cls, related_to_type: ActivityRelatedTo, related_to_id: str, limit: int = 100) -> list[Activity]:
        """Async version of get_timeline.

        Args:
            related_to_type: Type of record (Contact, Account, Deal)
            related_to_id: ID of the record
            limit: Maximum number of activities to return

        Returns:
            List of activities sorted by created_at desc (newest first)
        """
