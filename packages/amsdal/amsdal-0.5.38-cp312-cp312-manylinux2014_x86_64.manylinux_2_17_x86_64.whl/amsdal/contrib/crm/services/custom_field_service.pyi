from amsdal.contrib.crm.errors import CustomFieldValidationError as CustomFieldValidationError
from amsdal.contrib.crm.models.custom_field_definition import CustomFieldDefinition as CustomFieldDefinition
from typing import Any

class CustomFieldService:
    """Service for validating custom field values against their definitions."""
    @classmethod
    def validate_custom_fields(cls, entity_type: str, custom_fields: dict[str, Any] | None) -> dict[str, Any]:
        """Validate custom field values against their definitions.

        Args:
            entity_type: The entity type (Contact, Account, Deal)
            custom_fields: Dictionary of custom field values

        Returns:
            Validated custom_fields dict

        Raises:
            CustomFieldValidationError: If validation fails
        """
    @classmethod
    def _validate_field_value(cls, definition: CustomFieldDefinition, value: Any) -> Any:
        """Validate a single field value against its definition.

        Args:
            definition: The field definition
            value: The value to validate

        Returns:
            The validated (and potentially converted) value

        Raises:
            CustomFieldValidationError: If validation fails
        """
