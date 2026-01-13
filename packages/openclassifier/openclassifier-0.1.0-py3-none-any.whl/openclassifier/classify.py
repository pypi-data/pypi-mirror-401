from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from .types import (
    ImageClassifyResponse,
    ImageInput,
    ImageURLInput,
    PageRange,
    PDFClassifyResponse,
    PDFInput,
    PDFURLInput,
    TextClassifyResponse,
)

if TYPE_CHECKING:
    from ._http import HTTPClient


class Classify:
    """Classification methods for the OpenClassifier API."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def text(
        self,
        content: str,
        labels: list[str],
        *,
        multi_label: bool = False,
    ) -> TextClassifyResponse:
        """
        Classify text content into one or more labels.

        Args:
            content: The text to classify (max 100,000 characters).
            labels: List of classification labels (2-50 unique labels).
            multi_label: If True, returns confidence for all labels.

        Returns:
            Classification result with label and confidence score.
        """
        payload = {
            "content": content,
            "labels": labels,
            "multi_label": multi_label,
        }
        return self._http.post("/api/classify/text", payload)  # type: ignore[return-value]

    def image(
        self,
        inputs: list[str | ImageInput],
        labels: list[str],
        *,
        detail: Literal["low", "high", "auto"] = "low",
    ) -> ImageClassifyResponse:
        """
        Classify one or more images into labels.

        Args:
            inputs: List of image URLs (str) or image input dicts.
                    For URLs, pass strings directly.
                    For base64, pass {"base64": "...", "media_type": "image/jpeg"}.
            labels: List of classification labels (2-50 unique labels).
            detail: Image detail level for processing.

        Returns:
            Classification results for each image.
        """
        normalized_inputs: list[ImageInput] = []
        for inp in inputs:
            if isinstance(inp, str):
                normalized_inputs.append(ImageURLInput(url=inp))
            else:
                normalized_inputs.append(inp)

        payload = {
            "inputs": normalized_inputs,
            "labels": labels,
            "detail": detail,
        }
        return self._http.post("/api/classify/image", payload)  # type: ignore[return-value]

    def pdf(
        self,
        input: str | PDFInput,
        labels: list[str],
        *,
        aggregation: Literal["per_page", "document", "both"] = "both",
        page_range: PageRange | None = None,
    ) -> PDFClassifyResponse:
        """
        Classify a PDF document.

        Args:
            input: PDF URL (str) or input dict with url or base64.
            labels: List of classification labels (2-50 unique labels).
            aggregation: How to aggregate results.
            page_range: Optional page range to process.

        Returns:
            Classification results per page and/or for the whole document.
        """
        normalized_input: PDFInput
        if isinstance(input, str):
            normalized_input = PDFURLInput(url=input)
        else:
            normalized_input = input

        payload: dict[str, Any] = {
            "input": normalized_input,
            "labels": labels,
            "aggregation": aggregation,
        }
        if page_range is not None:
            payload["page_range"] = page_range

        return self._http.post("/api/classify/pdf", payload)  # type: ignore[return-value]
