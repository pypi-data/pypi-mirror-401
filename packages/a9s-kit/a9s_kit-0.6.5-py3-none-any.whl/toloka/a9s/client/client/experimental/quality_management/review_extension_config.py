from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.review.web.v0.form import ReviewExtensionConfigFormV0
from toloka.a9s.client.models.quality_management.review_extension_config import ReviewExtensionConfigViewV0Strict
from toloka.a9s.client.models.types import ReviewExtensionConfigId


class AsyncQmsReviewExtensionConfigClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/review-extension-config'

    async def get(self, id: ReviewExtensionConfigId) -> ReviewExtensionConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return ReviewExtensionConfigViewV0Strict.model_validate(response.json())

    async def create(self, form: ReviewExtensionConfigFormV0) -> ReviewExtensionConfigViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=form.model_dump(mode='json'),
        )
        return ReviewExtensionConfigViewV0Strict.model_validate(response.json())

    async def update(
        self, id: ReviewExtensionConfigId, form: ReviewExtensionConfigFormV0
    ) -> ReviewExtensionConfigViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=form.model_dump(mode='json'),
        )
        return ReviewExtensionConfigViewV0Strict.model_validate(response.json())
