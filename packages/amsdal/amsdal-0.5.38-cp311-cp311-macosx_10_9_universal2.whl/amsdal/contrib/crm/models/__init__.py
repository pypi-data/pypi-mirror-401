"""CRM Models."""

# Import File first for Attachment's forward reference
from amsdal.contrib.crm.models.account import Account
from amsdal.contrib.crm.models.activity import Activity
from amsdal.contrib.crm.models.activity import ActivityRelatedTo
from amsdal.contrib.crm.models.activity import ActivityType
from amsdal.contrib.crm.models.activity import Call
from amsdal.contrib.crm.models.activity import EmailActivity
from amsdal.contrib.crm.models.activity import Event
from amsdal.contrib.crm.models.activity import Note
from amsdal.contrib.crm.models.activity import Task
from amsdal.contrib.crm.models.attachment import Attachment
from amsdal.contrib.crm.models.contact import Contact
from amsdal.contrib.crm.models.custom_field_definition import CustomFieldDefinition
from amsdal.contrib.crm.models.deal import Deal
from amsdal.contrib.crm.models.pipeline import Pipeline
from amsdal.contrib.crm.models.stage import Stage
from amsdal.contrib.crm.models.workflow_rule import WorkflowRule
from amsdal.models.core.file import File  # noqa: F401

__all__ = [
    'Account',
    'Activity',
    'ActivityRelatedTo',
    'ActivityType',
    'Attachment',
    'Call',
    'Contact',
    'CustomFieldDefinition',
    'Deal',
    'EmailActivity',
    'Event',
    'Note',
    'Pipeline',
    'Stage',
    'Task',
    'WorkflowRule',
]

# Rebuild models to resolve forward references
Contact.model_rebuild()
Deal.model_rebuild()
Stage.model_rebuild()
Attachment.model_rebuild()
