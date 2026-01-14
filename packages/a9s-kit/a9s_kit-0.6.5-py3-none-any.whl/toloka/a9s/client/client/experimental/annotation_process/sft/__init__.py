__all__ = ['AsyncAnnotationStudioSftClient']

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.client.experimental.annotation_process.sft.logs import (
    AsyncAnnotationStudioSftLogsClient,
)
from toloka.a9s.client.models.annotation_process.sft import (
    BatchSftConfigFormStrict,
    ProjectSftConfigFormStrict,
    SftConfigViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import SftAnnotationProcessViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.sft.web.form import (
    UpdateSftForm,
)
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.common.http.client import AsyncHttpClient


class AsyncAnnotationStudioSftClient(AsyncBaseAnnotationStudioClient):
    logs: AsyncAnnotationStudioSftLogsClient

    def __init__(self, transport: AsyncHttpClient) -> None:
        super().__init__(transport)
        self.logs = AsyncAnnotationStudioSftLogsClient(transport)

    async def update(self, form: UpdateSftForm) -> SftAnnotationProcessViewStrict:
        """Update an existing sft annotation process.

        Args:
            form: The update form containing the new configuration for the process

        Returns:
            SftAnnotationProcessViewStrict: The updated sft annotation process view
        """
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/sft/update',
            body=model_dump_a9s(form),
        )
        return SftAnnotationProcessViewStrict.model_validate(response.json())

    async def set_project_defaults(self, form: ProjectSftConfigFormStrict) -> SftConfigViewStrict:
        """Set default configuration for sft annotation processes at the project level.

        Args:
            form: The configuration form containing the default settings

        Returns:
            SftConfigViewStrict: The updated sft configuration view
        """
        response = await self.client.make_retriable_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/sft/set-project-defaults',
            body=model_dump_a9s(form),
        )
        return SftConfigViewStrict.model_validate(response.json())

    async def set_batch_defaults(self, form: BatchSftConfigFormStrict) -> SftConfigViewStrict:
        """Set default configuration for sft annotation processes at the batch level.

        Args:
            form: The configuration form containing the default settings

        Returns:
            SftConfigViewStrict: The updated sft configuration view
        """
        response = await self.client.make_retriable_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/sft/set-batch-defaults',
            body=model_dump_a9s(form),
        )
        return SftConfigViewStrict.model_validate(response.json())
