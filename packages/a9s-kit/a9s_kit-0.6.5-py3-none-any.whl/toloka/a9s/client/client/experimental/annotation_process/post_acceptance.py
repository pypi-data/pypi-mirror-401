from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process.view import PostAcceptanceAnnotationProcessViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.post_acceptance.web.ui.form import (
    UpdateVerdictForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.post_acceptance.web.v1.form import (
    PostAcceptanceConfigFormV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.post_acceptance.web.v1.view import (
    PostAcceptanceConfigViewV1,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioPostAcceptanceClient(AsyncBaseAnnotationStudioClient):
    async def update_verdict(self, form: UpdateVerdictForm) -> PostAcceptanceAnnotationProcessViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.UI_API_PREFIX}/annotation-processes/post-acceptance/update-verdict',
            body=model_dump_a9s(form),
        )
        return PostAcceptanceAnnotationProcessViewStrict.model_validate(response.json())

    async def set_batch_defaults(self, form: PostAcceptanceConfigFormV1) -> PostAcceptanceConfigViewV1:
        """Set default configuration for post acceptance annotation processes at the batch level.

        Args:
            form: The configuration form containing the default settings

        Returns:
            PostAcceptanceConfigViewV1: The updated post acceptance configuration view
        """
        response = await self.client.make_retriable_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/post-acceptance/set-batch-defaults',
            body=model_dump_a9s(form),
        )
        return PostAcceptanceConfigViewV1.model_validate(response.json())

    async def get_batch_defaults(self, batch_id: str) -> PostAcceptanceConfigViewV1 | None:
        """Get default configuration for post acceptance annotation processes at the batch level.

        Args:
            batch_id: The batch ID to get configuration for

        Returns:
            PostAcceptanceConfigViewV1 or None if not found
        """
        try:
            response = await self.client.make_retriable_request(
                method='GET',
                params={'batch_id': batch_id},
                url=f'{self.V1_PREFIX}/annotation-processes/post-acceptance/get-batch-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return PostAcceptanceConfigViewV1.model_validate(response.json())

    async def set_project_defaults(self, form: PostAcceptanceConfigFormV1) -> PostAcceptanceConfigViewV1:
        """Set default configuration for post acceptance annotation processes at the project level.

        Args:
            form: The configuration form containing the default settings

        Returns:
            PostAcceptanceConfigViewV1: The updated post acceptance configuration view
        """
        response = await self.client.make_retriable_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/post-acceptance/set-project-defaults',
            body=model_dump_a9s(form),
        )
        return PostAcceptanceConfigViewV1.model_validate(response.json())

    async def get_project_defaults(self, project_id: str) -> PostAcceptanceConfigViewV1 | None:
        """Get default configuration for post acceptance annotation processes at the project level.

        Args:
            project_id: The project ID to get configuration for

        Returns:
            PostAcceptanceConfigViewV1 or None if not found
        """
        try:
            response = await self.client.make_retriable_request(
                method='GET',
                params={'project_id': project_id},
                url=f'{self.V1_PREFIX}/annotation-processes/post-acceptance/get-project-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return PostAcceptanceConfigViewV1.model_validate(response.json())
