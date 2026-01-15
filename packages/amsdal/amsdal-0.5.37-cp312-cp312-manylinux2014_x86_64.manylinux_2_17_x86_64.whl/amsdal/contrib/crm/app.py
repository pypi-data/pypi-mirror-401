"""CRM App Configuration."""

from amsdal_utils.lifecycle.enum import LifecycleEvent
from amsdal_utils.lifecycle.producer import LifecycleProducer

from amsdal.contrib.app_config import AppConfig
from amsdal.contrib.crm.constants import CRMLifecycleEvent


class CRMAppConfig(AppConfig):
    """Configuration for the CRM application."""

    def on_ready(self) -> None:
        """Set up CRM lifecycle listeners and initialize module."""
        from amsdal.contrib.crm.lifecycle.consumer import DealWonNotificationConsumer
        from amsdal.contrib.crm.lifecycle.consumer import LoadCRMFixturesConsumer

        # Load fixtures on startup
        LifecycleProducer.add_listener(LifecycleEvent.ON_SERVER_STARTUP, LoadCRMFixturesConsumer)

        # Custom CRM events
        LifecycleProducer.add_listener(CRMLifecycleEvent.ON_DEAL_WON, DealWonNotificationConsumer)  # type: ignore[arg-type]

        # Additional event listeners can be added here
        # LifecycleProducer.add_listener(CRMLifecycleEvent.ON_DEAL_LOST, DealLostNotificationConsumer)
