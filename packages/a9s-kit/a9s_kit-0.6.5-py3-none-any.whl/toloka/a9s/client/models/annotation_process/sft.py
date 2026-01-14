# pyright: reportGeneralTypeIssues=false


from typing import Any, Literal, Mapping, Sequence

from pydantic import BaseModel, SerializeAsAny

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.parameters import SftAnnotationProcessParameters
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model.sft import (
    SftAnnotationProcessView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.sft.web.form import (
    SftConfigForm,
    UpdateSftForm,
    UpdateSftLogForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.sft.web.view import (
    SftConfigView,
    SftLogsView,
    SftLogView,
)
from toloka.a9s.client.models.types import (
    AnnotationProcessId,
    BatchId,
    ProjectId,
    SftConfigId,
    SftLogId,
    SftLogStatus,
    WorkflowItemStatus,
)


class SftConfigViewStrict(SftConfigView):
    id: SftConfigId
    workflow_name: str
    solution_id: str


class SftAnnotationProcessViewDataStrict(SftAnnotationProcessView):
    type: Literal['sft'] = 'sft'

    workflow_name: str
    solution_id: str
    instance_id: str
    status: WorkflowItemStatus
    priority: int
    version: int
    upload_id: str
    source_file_name: str
    submitted_items_link_id: str | None = None
    input_data: Mapping[str, Any]


class SftAnnotationProcessParametersStrict(SftAnnotationProcessParameters):
    type: Literal['sft'] = 'sft'

    sft_status: WorkflowItemStatus
    source_file_name: str
    version: int
    upload_id: str
    submitted_items_link_id: str | None
    priority: int
    instance_id: str
    input_data: Mapping[str, Any]
    completed: bool


class SftLogViewStrict(SftLogView):
    id: SftLogId
    snapshot: Mapping[str, Any]
    sft_process_id: str
    created_at: str
    modified_at: str
    step_name: str
    component_name: str | None = None
    input_data: Mapping[str, Any] | None = None
    output_data: Mapping[str, Any] | None = None
    meta: Mapping[str, Any]
    step_type: str
    status: SftLogStatus
    vendor_type: str
    steps_history: Sequence[Mapping[str, Any]]
    run_id: str
    workflow_name: str
    retry_key: str
    workflow_id: str
    iteration: int
    dimensions: Mapping[str, Any] | None = None
    is_deleted: bool


class UpdateSftLogFormStrict(UpdateSftLogForm):
    snapshot: Mapping[str, Any]
    step_name: str
    component_name: str | None
    step_type: str
    status: SftLogStatus
    input_data: Mapping[str, Any] | SerializeAsAny[BaseModel] | None
    output_data: Mapping[str, Any] | SerializeAsAny[BaseModel] | None
    meta: Mapping[str, Any] | SerializeAsAny[BaseModel]
    steps_history: Sequence[Mapping[str, Any] | SerializeAsAny[BaseModel]]
    run_id: str
    workflow_name: str
    vendor_type: str
    retry_key: str
    workflow_id: str
    iteration: int
    dependent_item_ids: Sequence[str] | None
    dimensions: Mapping[str, Any] | SerializeAsAny[BaseModel] | None
    deleted: bool


class SftLogsViewStrict(SftLogsView):
    logs: Sequence[SftLogViewStrict]


class UpdateSftFormStrict(UpdateSftForm):
    annotation_process_id: AnnotationProcessId
    sft_status: WorkflowItemStatus
    source_file_name: str
    version: int
    upload_id: str
    submitted_items_link_id: str | None
    priority: int
    instance_id: str
    input_data: Mapping[str, Any]
    completed: bool


class ProjectSftConfigFormStrict(SftConfigForm):
    project_id: ProjectId
    batch_id: None = None
    workflow_name: str
    solution_id: str


class BatchSftConfigFormStrict(SftConfigForm):
    project_id: None = None
    batch_id: BatchId
    workflow_name: str
    solution_id: str
