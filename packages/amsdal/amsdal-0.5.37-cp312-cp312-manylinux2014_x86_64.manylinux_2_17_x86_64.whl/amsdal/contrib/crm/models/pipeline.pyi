from amsdal_models.classes.data_models.constraints import UniqueConstraint
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from typing import ClassVar

class Pipeline(Model):
    """Sales pipeline model.

    Represents a sales pipeline with multiple stages.
    Pipelines are system-wide and not owned by individual users.
    """
    __module_type__: ClassVar[ModuleType] = ...
    __constraints__: ClassVar[list[UniqueConstraint]] = ...
    name: str = ...
    description: str | None = ...
    is_active: bool = ...
    @property
    def display_name(self) -> str:
        """Return display name for the pipeline."""
