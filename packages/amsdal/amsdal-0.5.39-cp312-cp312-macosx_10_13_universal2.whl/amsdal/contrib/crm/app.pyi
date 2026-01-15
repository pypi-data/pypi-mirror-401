from amsdal.contrib.app_config import AppConfig as AppConfig
from amsdal.contrib.crm.constants import CRMLifecycleEvent as CRMLifecycleEvent

class CRMAppConfig(AppConfig):
    """Configuration for the CRM application."""
    def on_ready(self) -> None:
        """Set up CRM lifecycle listeners and initialize module."""
