from typing import Literal

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model.review import ReviewAnnotationProcessView
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.review.web.v1.view import (
    ReviewConfigViewV1,
)
from toloka.a9s.client.models.types import ReviewConfigId


class ReviewConfigViewStrict(ReviewConfigViewV1):
    id: ReviewConfigId


class ReviewAnnotationProcessViewDataStrict(ReviewAnnotationProcessView):
    type: Literal['review'] = 'review'
