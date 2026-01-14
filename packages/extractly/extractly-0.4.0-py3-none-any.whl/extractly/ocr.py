import logging
import os
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import urlparse

import tenacity
from mistralai import Mistral
from mistralai.models import DocumentTypedDict
from mistralai.models.ocrpageobject import OCRPageObject

logger = logging.getLogger(__name__)

_IMAGE_EXTENSIONS = {
    ".bmp",
    ".gif",
    ".heic",
    ".heif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


def _get_mistral_client(
    api_key: str | None = None, client: Mistral | None = None
) -> Mistral:
    if api_key is None:
        api_key = os.environ.get("MISTRAL_API_KEY")
    if api_key is None and client is None:
        raise KeyError(
            "you must pass an api_key or a client, or set the MISTRAL_API_KEY environment variable"
        )
    if client is not None and api_key is not None:
        logger.warning(
            "you have provided an API key while also providing an initialized client, ignoring the API key"
        )
    elif client is None:
        client = Mistral(api_key=api_key)

    return client


class OCR:
    """Service for handling OCR operations using Mistral."""

    _client: Mistral

    def __init__(
        self, api_key: str | None = None, client: Mistral | None = None
    ) -> None:
        self._client = _get_mistral_client(api_key, client)

    @staticmethod
    def _resolve_is_image(
        is_image: bool | None,
        *,
        filename: str | None = None,
        url: str | None = None,
        content: bytes | None = None,
    ) -> bool:
        if is_image is not None:
            return is_image

        if content:
            header = content[:12]
            if header.startswith(b"\xff\xd8\xff"):  # JPEG
                return True
            if header.startswith(b"\x89PNG\r\n\x1a\n"):  # PNG
                return True
            if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):  # GIF
                return True
            if header.startswith(b"BM"):  # BMP
                return True
            if header.startswith(b"II*\x00") or header.startswith(b"MM\x00*"):  # TIFF
                return True
            if (
                len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP"
            ):  # WEBP
                return True

        def _has_image_extension(name: str | None) -> bool:
            if not name:
                return False
            parsed = urlparse(name)
            candidate = parsed.path or name
            return Path(candidate).suffix.lower() in _IMAGE_EXTENSIONS

        if _has_image_extension(filename) or _has_image_extension(url):
            return True

        return False

    @staticmethod
    def _build_document(url: str, is_image: bool) -> DocumentTypedDict:
        document: DocumentTypedDict
        if is_image:
            document = {
                "type": "image_url",
                "image_url": url,
            }
        else:
            document = {
                "type": "document_url",
                "document_url": url,
            }
        return document

    def _extract_from_url(self, client: Mistral, url: str, *, is_image: bool) -> str:
        document = self._build_document(url, is_image=is_image)
        response = client.ocr.process(
            model="mistral-ocr-latest",
            document=document,
            include_image_base64=is_image,
        )
        logger.info("OCR processed %d pages", len(response.pages))
        return self._render_pages(response.pages)

    @staticmethod
    def _render_pages(pages: Iterable[OCRPageObject]) -> str:
        sections = [
            getattr(page, "markdown", "")
            for page in pages
            if getattr(page, "markdown", "").strip()
        ]
        if not sections:
            raise ValueError("No text could be extracted from the file")
        return "\n\n".join(sections)

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=15),
        reraise=True,
    )
    def extract_text_from_file_url(
        self, file_url: str, filename: str, is_image: bool | None = None
    ) -> str:
        """Extract text from a URL-accessible file using Mistral OCR."""
        resolved_is_image = self._resolve_is_image(
            is_image, filename=filename, url=file_url
        )
        logger.info(
            "Starting OCR extraction for file %s from URL %s (%s)",
            filename,
            file_url,
            "image" if resolved_is_image else "document",
        )
        text = self._extract_from_url(
            self._client, file_url, is_image=resolved_is_image
        )
        logger.info("OCR extraction completed for %s", filename)
        return text

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=15),
        reraise=True,
    )
    def extract_text_from_bytes(
        self,
        content: bytes,
        filename: str,
        is_image: bool | None = None,
    ) -> str:
        """Extract text from bytes using Mistral OCR"""
        resolved_is_image = self._resolve_is_image(
            is_image, filename=filename, content=content
        )
        logger.info(
            "Starting OCR extraction for file %s (%d bytes, %s)",
            filename,
            len(content),
            "image" if resolved_is_image else "document",
        )
        uploaded_file = self._client.files.upload(
            file={"file_name": filename, "content": content},
            purpose="ocr",
        )
        logger.info("Uploaded file %s as %s", filename, uploaded_file.id)
        signed_url = self._client.files.get_signed_url(file_id=uploaded_file.id)
        text = self._extract_from_url(
            self._client, signed_url.url, is_image=resolved_is_image
        )
        logger.info("OCR extraction completed for %s", filename)
        return text

    def extract_text_from_file_path(
        self,
        input_file_path: Path,
        output_file_path: Path | None = None,
        filename: str | None = None,
        is_image: bool | None = None,
    ) -> str:
        """Extract text from a file-like object using Mistral OCR."""
        logger.info("Starting OCR extraction from file path")
        filename = filename or input_file_path.name

        with open(input_file_path, "rb") as content:
            _ = content.seek(0)
            file_bytes = content.read()
        if not file_bytes:
            raise ValueError("The supplied file is empty.")
        logger.info("Read %d bytes from %s", len(file_bytes), filename)
        content = self.extract_text_from_bytes(file_bytes, filename, is_image)
        if output_file_path:
            with open(output_file_path, "w") as f:
                _ = f.write(content)
        return content
