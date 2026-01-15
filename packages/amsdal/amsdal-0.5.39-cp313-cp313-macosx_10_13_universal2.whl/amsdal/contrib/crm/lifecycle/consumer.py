"""CRM Lifecycle Consumers."""

from typing import TYPE_CHECKING

from amsdal_utils.lifecycle.consumer import LifecycleConsumer

if TYPE_CHECKING:
    from amsdal.contrib.crm.models.deal import Deal


class LoadCRMFixturesConsumer(LifecycleConsumer):
    """Consumer that loads CRM fixtures on server startup."""

    def on_event(self) -> None:
        """Load CRM fixtures (pipelines, stages, permissions)."""
        # Note: Fixtures are typically loaded via the FixturesManager
        # This consumer can be used for additional setup if needed
        pass

    async def on_event_async(self) -> None:
        """Async version of on_event."""
        pass


class DealWonNotificationConsumer(LifecycleConsumer):
    """Consumer that handles deal won events.

    Placeholder for future notification system integration.
    """

    def on_event(self, deal: 'Deal', user_email: str) -> None:
        """Handle deal won event.

        Args:
            deal: The deal that was won
            user_email: Email of user who closed the deal
        """
        # TODO: Implement notification logic
        # Could integrate with email service, Slack, etc.
        pass

    async def on_event_async(self, deal: 'Deal', user_email: str) -> None:
        """Async version of on_event."""
        pass
