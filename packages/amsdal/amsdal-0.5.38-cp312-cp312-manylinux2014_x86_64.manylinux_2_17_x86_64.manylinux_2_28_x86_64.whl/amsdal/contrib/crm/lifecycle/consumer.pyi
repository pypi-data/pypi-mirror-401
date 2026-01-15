from amsdal.contrib.crm.models.deal import Deal as Deal
from amsdal_utils.lifecycle.consumer import LifecycleConsumer

class LoadCRMFixturesConsumer(LifecycleConsumer):
    """Consumer that loads CRM fixtures on server startup."""
    def on_event(self) -> None:
        """Load CRM fixtures (pipelines, stages, permissions)."""
    async def on_event_async(self) -> None:
        """Async version of on_event."""

class DealWonNotificationConsumer(LifecycleConsumer):
    """Consumer that handles deal won events.

    Placeholder for future notification system integration.
    """
    def on_event(self, deal: Deal, user_email: str) -> None:
        """Handle deal won event.

        Args:
            deal: The deal that was won
            user_email: Email of user who closed the deal
        """
    async def on_event_async(self, deal: Deal, user_email: str) -> None:
        """Async version of on_event."""
