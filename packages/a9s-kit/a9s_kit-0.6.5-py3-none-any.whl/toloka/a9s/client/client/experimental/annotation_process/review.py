__all__ = [
    'AsyncAnnotationStudioReviewClient',
    'ReviewAnnotationProcessViewStrict',
    'ReviewConfigViewStrict',
    'ReviewConfigFormV1',
    'ReviewFormV1',
]

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process.review import (
    ReviewAnnotationProcessViewDataStrict,
    ReviewConfigViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    ReviewAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.review.web.v1.form import (
    ReviewConfigFormV1,
    ReviewFormV1,
    UiAttributesFormV1,
)
from toloka.a9s.client.models.types import AnnotationProcessId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioReviewClient(AsyncBaseAnnotationStudioClient):
    async def update_review(
        self, form: ReviewFormV1, process_id: AnnotationProcessId
    ) -> ReviewAnnotationProcessViewDataStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/review/{process_id}',
            body=model_dump_a9s(form),
        )
        return ReviewAnnotationProcessViewDataStrict.model_validate(response.json())

    async def update_ui_attributes(self, form: UiAttributesFormV1) -> ReviewAnnotationProcessViewDataStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/review/ui-attributes',
            body=model_dump_a9s(form),
        )
        return ReviewAnnotationProcessViewDataStrict.model_validate(response.json())

    async def set_batch_defaults(self, form: ReviewConfigFormV1) -> ReviewConfigViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/review/set-batch-defaults',
            body=model_dump_a9s(form),
        )
        return ReviewConfigViewStrict.model_validate(response.json())

    async def set_project_defaults(self, form: ReviewConfigFormV1) -> ReviewConfigViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/review/set-project-defaults',
            body=model_dump_a9s(form),
        )
        return ReviewConfigViewStrict.model_validate(response.json())

    async def get_project_defaults(self, project_id: str) -> ReviewConfigViewStrict | None:
        try:
            response = await self.client.make_request(
                method='GET',
                params={'project_id': project_id},
                url=f'{self.V1_PREFIX}/annotation-processes/review/get-project-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return ReviewConfigViewStrict.model_validate(response.json())

    async def get_batch_defaults(self, batch_id: str) -> ReviewConfigViewStrict | None:
        try:
            response = await self.client.make_request(
                method='GET',
                params={'batch_id': batch_id},
                url=f'{self.V1_PREFIX}/annotation-processes/review/get-batch-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return ReviewConfigViewStrict.model_validate(response.json())
