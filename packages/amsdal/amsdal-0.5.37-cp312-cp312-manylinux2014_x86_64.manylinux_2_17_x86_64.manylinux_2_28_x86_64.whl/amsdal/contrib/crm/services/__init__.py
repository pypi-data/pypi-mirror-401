"""CRM Services."""

from amsdal.contrib.crm.services.activity_service import ActivityService
from amsdal.contrib.crm.services.custom_field_service import CustomFieldService
from amsdal.contrib.crm.services.deal_service import DealService
from amsdal.contrib.crm.services.email_service import EmailService
from amsdal.contrib.crm.services.workflow_service import WorkflowService

__all__ = [
    'ActivityService',
    'CustomFieldService',
    'DealService',
    'EmailService',
    'WorkflowService',
]
