from typing import Any, Mapping, overload

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process import (
    AnnotationProcessConfigListViewStrict,
    AnnotationProcessListViewStrict,
    UploadFormV1Strict,
    UploadViewV1Strict,
    is_annotation_process_instance,
)
from toloka.a9s.client.models.annotation_process.metric_provider import MetricProviderAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.quorum import (
    QuorumAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.review import ReviewAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.sft import SftAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    AnnotationProcessData,
    AnnotationProcessViewStrict,
    MetricProviderAnnotationProcessViewStrict,
    QuorumAnnotationProcessViewStrict,
    ReviewAnnotationProcessViewStrict,
    SftAnnotationProcessViewStrict,
    StatusWorkflowAnnotationProcessViewStrict,
    UnrecognizedAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.sft.web.form import (
    SftAnnotationProcessForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.ui.form import (
    MetricProviderAnnotationProcessForm,
    ReviewAnnotationProcessForm,
    StatusWorkflowAnnotationProcessForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.ui.view import (
    AnnotationProcessesProgressView,
)
from toloka.a9s.client.models.types import AnnotationId, AnnotationProcessId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationProcessesClient(AsyncBaseAnnotationStudioClient):
    async def get_all(
        self,
        annotation_id: str | None = None,
        annotation_group_id: str | None = None,
        batch_id: str | None = None,
    ) -> AnnotationProcessListViewStrict:
        params = {'annotation_id': annotation_id, 'annotation_group_id': annotation_group_id, 'batch_id': batch_id}
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.UI_API_PREFIX}/annotation-processes', params=params
        )
        return AnnotationProcessListViewStrict.model_validate(response.json())

    async def get(self, id: str) -> AnnotationProcessViewStrict[Any]:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.UI_API_PREFIX}/annotation-processes/{id}'
        )
        return AnnotationProcessViewStrict.model_validate(response.json())

    async def get_all_progress(self, batch_id: str) -> AnnotationProcessesProgressView:
        response = await self.client.make_retriable_request(
            method='GET', url=f'{self.UI_API_PREFIX}/annotation-processes/progress', params={'batch_id': batch_id}
        )
        return AnnotationProcessesProgressView.model_validate(response.json())

    @overload
    async def create(self, form: StatusWorkflowAnnotationProcessForm) -> StatusWorkflowAnnotationProcessViewStrict: ...

    @overload
    async def create(self, form: SftAnnotationProcessForm) -> SftAnnotationProcessViewStrict: ...

    @overload
    async def create(self, form: MetricProviderAnnotationProcessForm) -> MetricProviderAnnotationProcessViewStrict: ...

    @overload
    async def create(self, form: ReviewAnnotationProcessForm) -> ReviewAnnotationProcessViewStrict: ...

    async def create(
        self,
        form: StatusWorkflowAnnotationProcessForm
        | SftAnnotationProcessForm
        | MetricProviderAnnotationProcessForm
        | ReviewAnnotationProcessForm,
    ) -> (
        AnnotationProcessViewStrict[
            AnnotationProcessData | Mapping[str, Any] | UnrecognizedAnnotationProcessViewDataStrict
        ]
        | StatusWorkflowAnnotationProcessViewStrict
        | SftAnnotationProcessViewStrict
        | MetricProviderAnnotationProcessViewStrict
        | ReviewAnnotationProcessViewStrict
    ):
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes',
            body=model_dump_a9s(form),
        )
        return AnnotationProcessViewStrict.model_validate(response.json())

    async def upload_data(self, form: UploadFormV1Strict) -> UploadViewV1Strict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/upload-data',
            body=model_dump_a9s(form),
        )
        return UploadViewV1Strict.model_validate(response.json())

    async def get_status_workflow(
        self, annotation_id: AnnotationId
    ) -> StatusWorkflowAnnotationProcessViewStrict | None:
        processes = [
            process
            for process in (await self.get_all(annotation_id=annotation_id)).processes
            if is_annotation_process_instance(process, StatusWorkflowAnnotationProcessViewDataStrict)
        ]
        if len(processes) == 0:
            return None
        assert len(processes) == 1, 'At most one status workflow per annotation is allowed'
        return processes[0]

    async def get_quorum(self, annotation_group_id: str) -> QuorumAnnotationProcessViewStrict | None:
        processes = [
            process
            for process in (await self.get_all(annotation_group_id=annotation_group_id)).processes
            if is_annotation_process_instance(process, QuorumAnnotationProcessViewDataStrict)
        ]
        if len(processes) == 0:
            return None
        assert len(processes) == 1, 'At most one quorum per annotation group is allowed'
        return processes[0]

    async def get_sft(self, annotation_process_id: AnnotationProcessId) -> SftAnnotationProcessViewStrict | None:
        try:
            response = await self.client.make_retriable_request(
                method='GET', url=f'{self.UI_API_PREFIX}/annotation-processes/{annotation_process_id}'
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return SftAnnotationProcessViewStrict.model_validate(response.json())

    async def get_sft_by_annotation_id(self, annotation_id: AnnotationId) -> SftAnnotationProcessViewStrict | None:
        processes = [
            process
            for process in (await self.get_all(annotation_id=annotation_id)).processes
            if is_annotation_process_instance(process, SftAnnotationProcessViewDataStrict)
        ]
        if len(processes) == 0:
            return None
        assert len(processes) == 1, 'At most one SFT process per annotation is allowed'
        return processes[0]

    async def get_review_process_by_annotation_id(
        self, annotation_id: AnnotationId
    ) -> ReviewAnnotationProcessViewStrict | None:
        processes = [
            process
            for process in (await self.get_all(annotation_id=annotation_id)).processes
            if is_annotation_process_instance(process, ReviewAnnotationProcessViewDataStrict)
        ]
        if len(processes) == 0:
            return None
        assert len(processes) == 1, 'At most one Review process per annotation is allowed'
        return processes[0]

    async def get_metric_provider_process_by_annotation_id(
        self, annotation_id: AnnotationId
    ) -> MetricProviderAnnotationProcessViewStrict | None:
        processes = [
            process
            for process in (await self.get_all(annotation_id=annotation_id)).processes
            if is_annotation_process_instance(process, MetricProviderAnnotationProcessViewDataStrict)
        ]
        if len(processes) == 0:
            return None
        return processes[0]

    async def get_configs(self, project_id: str, batch_id: str) -> AnnotationProcessConfigListViewStrict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/annotation-processes/configs',
            params={'project_id': project_id, 'batch_id': batch_id},
        )
        return AnnotationProcessConfigListViewStrict.model_validate(response.json())
