from _typeshed import Incomplete
from pydantic_settings import BaseSettings

class CRMSettings(BaseSettings):
    """Settings for the CRM module."""
    model_config: Incomplete
    DEFAULT_ACTIVITY_TIMELINE_LIMIT: int
    MAX_CUSTOM_FIELDS_PER_ENTITY: int
    MAX_WORKFLOW_RULES_PER_ENTITY: int
    DEFAULT_CURRENCY: str

crm_settings: Incomplete
