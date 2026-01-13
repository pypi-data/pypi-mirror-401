from __future__ import annotations

import sys
from typing import Literal, Union

if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


class TextClassifyParams(TypedDict):
    content: str
    labels: list[str]
    multi_label: NotRequired[bool]


class SingleLabelResult(TypedDict):
    label: str
    confidence: float


class MultiLabelResult(TypedDict):
    label: str
    confidence: float


class TextClassifyResponse(TypedDict):
    success: Literal[True]
    results: SingleLabelResult | dict[str, MultiLabelResult]


class ImageURLInput(TypedDict):
    url: str


class ImageBase64Input(TypedDict):
    base64: str
    media_type: Literal["image/jpeg", "image/png", "image/gif", "image/webp"]


ImageInput = Union[ImageURLInput, ImageBase64Input]


class ImageClassifyParams(TypedDict):
    inputs: list[ImageInput]
    labels: list[str]
    detail: NotRequired[Literal["low", "high", "auto"]]


class ImageClassifyResult(TypedDict):
    input: str
    label: str
    confidence: float


class ImageClassifyResponse(TypedDict):
    success: Literal[True]
    results: list[ImageClassifyResult]


class PDFURLInput(TypedDict):
    url: str


class PDFBase64Input(TypedDict):
    base64: str


PDFInput = Union[PDFURLInput, PDFBase64Input]


class PageRange(TypedDict):
    start: NotRequired[int]
    end: NotRequired[int]


class PDFClassifyParams(TypedDict):
    input: PDFInput
    labels: list[str]
    aggregation: NotRequired[Literal["per_page", "document", "both"]]
    page_range: NotRequired[PageRange]


class PDFPageResult(TypedDict):
    page: int
    label: str
    confidence: float
    failed: NotRequired[bool]


class DocumentLabelResult(TypedDict):
    label: str
    confidence: float


class PDFClassifyResponse(TypedDict):
    success: Literal[True]
    total_pages: int
    processed_pages: int
    failed_pages: NotRequired[int]
    results: list[PDFPageResult]
    document_label: NotRequired[DocumentLabelResult]
    truncated: NotRequired[bool]


class APIError(TypedDict):
    code: str
    message: str


class ErrorResponse(TypedDict):
    success: Literal[False]
    error: APIError


RequestParams = Union[TextClassifyParams, ImageClassifyParams, PDFClassifyParams]
ClassifyResponse = Union[TextClassifyResponse, ImageClassifyResponse, PDFClassifyResponse]
