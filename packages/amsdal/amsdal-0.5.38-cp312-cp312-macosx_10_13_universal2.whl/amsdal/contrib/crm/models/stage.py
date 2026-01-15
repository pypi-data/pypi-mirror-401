"""Stage Model."""

from typing import TYPE_CHECKING
from typing import ClassVar

from amsdal_models.classes.data_models.constraints import UniqueConstraint
from amsdal_models.classes.data_models.indexes import IndexInfo
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic import ConfigDict
from pydantic.fields import Field

if TYPE_CHECKING:
    from amsdal.contrib.crm.models.pipeline import Pipeline


class Stage(Model):
    """Pipeline stage model.

    Represents a stage within a sales pipeline with win probability
    and closed status indicators.
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

    __module_type__: ClassVar[ModuleType] = ModuleType.CONTRIB
    __constraints__: ClassVar[list[UniqueConstraint]] = [
        UniqueConstraint(name='unq_stage_pipeline_name', fields=['pipeline', 'name'])
    ]
    __indexes__: ClassVar[list[IndexInfo]] = [
        IndexInfo(name='idx_stage_order', field='order'),
    ]

    pipeline: 'Pipeline' = Field(title='Pipeline')
    name: str = Field(title='Stage Name')
    order: int = Field(title='Order')
    probability: float = Field(default=0.0, title='Win Probability (%)', ge=0, le=100)
    is_closed_won: bool = Field(default=False, title='Is Closed Won')
    is_closed_lost: bool = Field(default=False, title='Is Closed Lost')

    @property
    def display_name(self) -> str:
        """Return display name for the stage."""
        if isinstance(self.pipeline, str):
            return f'{self.pipeline} - {self.name}'
        return f'{self.pipeline.display_name} - {self.name}'
