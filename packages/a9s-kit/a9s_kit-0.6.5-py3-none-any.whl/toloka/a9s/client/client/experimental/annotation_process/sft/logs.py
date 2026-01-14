from typing import Sequence

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process.sft import (
    SftLogsViewStrict,
    SftLogViewStrict,
    UpdateSftLogFormStrict,
)
from toloka.a9s.client.models.types import AnnotationProcessId, SftLogId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioSftLogsClient(AsyncBaseAnnotationStudioClient):
    async def get_logs(self, sft_process_id: AnnotationProcessId) -> Sequence[SftLogViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/annotation-processes/sft/logs',
            params={'sft_process_id': sft_process_id},
        )
        view = SftLogsViewStrict.model_validate(response.json())
        return view.logs

    async def update(self, sft_log_id: SftLogId, form: UpdateSftLogFormStrict) -> SftLogViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/sft/logs/update',
            body=model_dump_a9s(form),
            params={
                'sft_log_id': sft_log_id,
            },
        )
        return SftLogViewStrict.model_validate(response.json())

    async def create(self, sft_process_id: AnnotationProcessId, form: UpdateSftLogFormStrict) -> SftLogViewStrict:
        response = await self.client.make_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/sft/logs/create',
            body=model_dump_a9s(form),
            params={
                'sft_process_id': sft_process_id,
            },
        )
        return SftLogViewStrict.model_validate(response.json())

    async def get_log(self, log_id: SftLogId) -> SftLogViewStrict | None:
        try:
            response = await self.client.make_retriable_request(
                method='GET',
                url=f'{self.V1_PREFIX}/annotation-processes/sft/logs/get/{log_id}',
            )
            return SftLogViewStrict.model_validate(response.json())
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e

    async def get_logs_by_retry_key(self, retry_key: str) -> Sequence[SftLogViewStrict]:
        try:
            response = await self.client.make_retriable_request(
                method='GET',
                url=f'{self.V1_PREFIX}/annotation-processes/sft/logs/get-by-retry-key/{retry_key}',
            )
            return SftLogsViewStrict.model_validate(response.json()).logs
        except AnnotationStudioError as e:
            if e.status == 404:
                return []
            raise e
