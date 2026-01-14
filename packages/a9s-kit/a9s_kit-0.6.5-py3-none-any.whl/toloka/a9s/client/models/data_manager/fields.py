import inspect
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, Literal, NewType, Sequence, TypeVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing_extensions import Self

NestableSortField = Literal['values']

NestableFilterField = Literal[
    'values',
    'annotation_values',
    'active_edit_values',
    'any_values',
    'metadata',
    'sft_dimensions',
    'sft_input_data',
    'sft_dependent_item_ids',
    'sft_log_input_data',
    'sft_log_output_data',
    'sft_meta',
    'sft_snapshot',
    'sft_steps_history',
]


NestableFieldType = TypeVar('NestableFieldType', bound=str, covariant=True)


# pydantic ignores __get_pydantic_core_schema__ for specified generic dataclasses for some reason
if TYPE_CHECKING:

    @dataclass
    class NestedField(str, Generic[NestableFieldType]):
        field: NestableFieldType
        path: Sequence[str]

        @classmethod
        def from_string(cls, value: str) -> 'NestedField[Any]':
            raise NotImplementedError('from_string is not implemented for TYPE_CHECKING')
else:

    @dataclass
    class NestedField(str):
        field: str
        path: Sequence[str]

        def __new__(cls, *args: Any, **kwargs: Any) -> Self:
            bound = inspect.signature(cls.__init__).bind(object(), *args, **kwargs)
            bound.apply_defaults()
            bound_dict = dict(bound.arguments)
            bound_dict.pop('self')

            value = NestedField._params_to_string(
                bound_dict['field'],
                bound_dict['path'],
            )

            return super().__new__(cls, value)

        def __class_getitem__(cls, *args, **kwargs):
            return cls

        def __deepcopy__(self, memo: Any) -> 'NestedField':
            return NestedField(self.field, deepcopy(self.path))

        @classmethod
        def from_string(cls, value: str) -> 'NestedField':
            if '.' not in value:
                return cls(value, [])
            field, path_str = value.split('.', 1)
            path = path_str.split('.')
            return cls(field, path)

        @staticmethod
        def _params_to_string(field: str, path: Sequence[str]) -> str:
            return f'{field}{"." + ".".join(path) if path else ""}'

        def __str__(self) -> str:
            return self._params_to_string(self.field, self.path)

        @classmethod
        def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
            string_schema = core_schema.no_info_after_validator_function(
                cls.from_string,
                schema=core_schema.str_schema(),
            )
            python_schema = core_schema.is_instance_schema(cls)

            return core_schema.union_schema(
                [python_schema, string_schema],
                serialization=core_schema.to_string_ser_schema(),
                mode='left_to_right',
            )


UnknownField = NewType('UnknownField', str)


SortField = (
    Literal[
        'annotation_count',
        'created_at',
        'group_id',
        'group_status',
        'modified_at',
        'quorum_priority_order',
        'status_workflow_priority_order_max_in_group',
        'status_workflow_priority_order_min_in_group',
        'status_workflow_status_priority_order_max_in_group',
        'status_workflow_status_priority_order_min_in_group',
    ]
    | NestedField[NestableSortField | UnknownField]
    | UnknownField
)


FilterField = (
    Literal[
        'account_id',
        'quorum_unavailable_for',
        'status_workflow_completed',
        'status_workflow_id',
        'status_workflow_responsible',
        'status_workflow_status',
        'status_workflow_status_is_initial',
        'status_workflow_unavailable_for',
        'sft_component_name',
        'sft_dependent_item_ids',
        'sft_instance_id',
        'sft_iteration',
        'sft_log_created_at',
        'sft_log_id',
        'sft_log_input_data',
        'sft_log_modified_at',
        'sft_log_output_data',
        'sft_log_workflow_name',
        'sft_meta',
        'sft_priority',
        'sft_process_id',
        'sft_retry_key',
        'sft_run_id',
        'sft_snapshot',
        'sft_solution_id',
        'sft_source_file_name',
        'sft_status',
        'sft_step_name',
        'sft_step_status',
        'sft_step_type',
        'sft_steps_history',
        'sft_submitted_items_link_id',
        'sft_upload_id',
        'sft_vendor_type',
        'sft_version',
        'sft_workflow_id',
        'sft_workflow_name',
    ]
    | NestedField[NestableFilterField | UnknownField]
    | SortField
    | UnknownField
)
