# pyright: reportAny=false, reportExplicitAny=false, reportUnknownMemberType=false
import logging
from typing import Any, cast
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from pytest import LogCaptureFixture, MonkeyPatch

import extractly.ocr as ocr_module
from extractly.ocr import OCR, _get_mistral_client
from mistralai.models.ocrpageobject import OCRPageObject


def test_build_document_for_image():
    document = OCR._build_document("http://example.com/image", is_image=True)

    assert document == {"type": "image_url", "image_url": "http://example.com/image"}


def test_build_document_for_document():
    document = OCR._build_document("http://example.com/document", is_image=False)

    assert document == {
        "type": "document_url",
        "document_url": "http://example.com/document",
    }


def test_render_pages_combines_markdown_sections():
    pages = cast(
        list[OCRPageObject],
        [
            SimpleNamespace(markdown="Page 1"),
            SimpleNamespace(markdown="   "),
            SimpleNamespace(markdown="Page 2"),
        ],
    )

    result = OCR._render_pages(pages)

    assert result == "Page 1\n\nPage 2"


def test_render_pages_raises_when_no_text():
    pages = cast(list[OCRPageObject], [SimpleNamespace(markdown=""), SimpleNamespace()])

    with pytest.raises(ValueError):
        _ = OCR._render_pages(pages)


def test_get_client_creates_client_with_explicit_api_key(monkeypatch: MonkeyPatch):
    mock_client = Mock()
    mock_mistral = Mock(return_value=mock_client)
    monkeypatch.setattr(ocr_module, "Mistral", mock_mistral)

    client = _get_mistral_client(api_key="api-key")

    assert client is mock_client
    mock_mistral.assert_called_once_with(api_key="api-key")


def test_get_client_uses_environment_api_key(monkeypatch: MonkeyPatch):
    mock_client = Mock()
    mock_mistral = Mock(return_value=mock_client)
    monkeypatch.setattr(ocr_module, "Mistral", mock_mistral)
    monkeypatch.setenv("MISTRAL_API_KEY", "env-key")

    client = _get_mistral_client()

    assert client is mock_client
    mock_mistral.assert_called_once_with(api_key="env-key")


def test_get_client_warns_when_both_client_and_key_provided(
    monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
):
    provided_client = Mock()
    mock_mistral = Mock()
    monkeypatch.setattr(ocr_module, "Mistral", mock_mistral)

    with caplog.at_level(logging.WARNING):
        client = _get_mistral_client(api_key="provided-key", client=provided_client)

    assert client is provided_client
    assert "ignoring the API key" in caplog.text
    mock_mistral.assert_not_called()


def test_get_client_requires_credentials(monkeypatch: MonkeyPatch):
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)

    with pytest.raises(KeyError):
        _ = _get_mistral_client()


def test_get_ocr_service_creates_instances(monkeypatch: MonkeyPatch):
    mock_client = Mock()
    mock_get_client = Mock(return_value=mock_client)
    monkeypatch.setattr(ocr_module, "_get_mistral_client", mock_get_client)

    service_one = OCR(api_key="api-key")
    service_two = OCR(api_key="api-key")

    assert isinstance(service_one, OCR)
    assert isinstance(service_two, OCR)
    assert service_one._client is mock_client
    assert service_two._client is mock_client
    assert mock_get_client.call_count == 2
    mock_get_client.assert_called_with("api-key", None)


def test_extract_text_from_file_url_delegates_to_internal_helper():
    client = Mock()
    service = OCR(client=client)

    with patch.object(
        service, "_extract_from_url", return_value="extracted"
    ) as mock_extract:
        result = service.extract_text_from_file_url(
            "http://example.com/document", "file.pdf", is_image=True
        )

    assert result == "extracted"
    mock_extract.assert_called_once_with(
        client, "http://example.com/document", is_image=True
    )


def test_extract_text_from_file_url_detects_image_from_filename():
    client = Mock()
    service = OCR(client=client)

    with patch.object(
        service, "_extract_from_url", return_value="detected"
    ) as mock_extract:
        result = service.extract_text_from_file_url(
            "http://example.com/image", "photo.png"
        )

    assert result == "detected"
    mock_extract.assert_called_once_with(
        client, "http://example.com/image", is_image=True
    )


def test_extract_text_from_bytes_uploads_and_extracts():
    files_mock = Mock()
    files_mock.upload.return_value = SimpleNamespace(id="file-id")
    files_mock.get_signed_url.return_value = SimpleNamespace(url="http://signed")
    client: Any = Mock(files=files_mock)
    service = OCR(client=client)

    with patch.object(
        service, "_extract_from_url", return_value="extracted-text"
    ) as mock_extract:
        result = service.extract_text_from_bytes(
            b"binary-data", "file.pdf", is_image=True
        )

    assert result == "extracted-text"
    files_mock.upload.assert_called_once_with(
        file={"file_name": "file.pdf", "content": b"binary-data"}, purpose="ocr"
    )
    files_mock.get_signed_url.assert_called_once_with(file_id="file-id")
    mock_extract.assert_called_once_with(client, "http://signed", is_image=True)


def test_extract_text_from_bytes_detects_image_from_header():
    files_mock = Mock()
    files_mock.upload.return_value = SimpleNamespace(id="file-id")
    files_mock.get_signed_url.return_value = SimpleNamespace(url="http://signed")
    client: Any = Mock(files=files_mock)
    service = OCR(client=client)
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8

    with patch.object(
        service, "_extract_from_url", return_value="image-text"
    ) as mock_extract:
        result = service.extract_text_from_bytes(png_bytes, "file.bin")

    assert result == "image-text"
    files_mock.upload.assert_called_once_with(
        file={"file_name": "file.bin", "content": png_bytes}, purpose="ocr"
    )
    files_mock.get_signed_url.assert_called_once_with(file_id="file-id")
    mock_extract.assert_called_once_with(client, "http://signed", is_image=True)


def test_extract_text_from_file_path_reads_file_and_delegates(tmp_path: Any):
    file_path = tmp_path / "sample.pdf"
    file_path.write_bytes(b"content")
    service = OCR(client=Mock())

    with patch.object(
        service, "extract_text_from_bytes", return_value="ocr-text"
    ) as mock_extract:
        result = service.extract_text_from_file_path(file_path, is_image=False)

    assert result == "ocr-text"
    mock_extract.assert_called_once_with(b"content", "sample.pdf", False)


def test_extract_text_from_file_path_writes_to_output_file(tmp_path: Any):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.txt"
    input_file.write_bytes(b"content")
    service = OCR(client=Mock())

    with patch.object(
        service, "extract_text_from_bytes", return_value="extracted-text-content"
    ) as mock_extract:
        result = service.extract_text_from_file_path(
            input_file, output_file_path=output_file, is_image=False
        )

    assert result == "extracted-text-content"
    assert output_file.exists()
    assert output_file.read_text() == "extracted-text-content"
    mock_extract.assert_called_once_with(b"content", "input.pdf", False)


def test_extract_text_from_file_path_with_custom_filename(tmp_path: Any):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.txt"
    input_file.write_bytes(b"content")
    service = OCR(client=Mock())

    with patch.object(
        service, "extract_text_from_bytes", return_value="extracted-text"
    ) as mock_extract:
        result = service.extract_text_from_file_path(
            input_file,
            output_file_path=output_file,
            filename="custom.pdf",
            is_image=True,
        )

    assert result == "extracted-text"
    assert output_file.read_text() == "extracted-text"
    mock_extract.assert_called_once_with(b"content", "custom.pdf", True)


def test_extract_text_from_file_path_detects_image(tmp_path: Any):
    input_file = tmp_path / "image.png"
    input_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8)
    files_mock = Mock()
    files_mock.upload.return_value = SimpleNamespace(id="file-id")
    files_mock.get_signed_url.return_value = SimpleNamespace(url="http://signed")
    client: Any = Mock(files=files_mock)
    service = OCR(client=client)

    with patch.object(
        service, "_extract_from_url", return_value="image-text"
    ) as mock_extract:
        result = service.extract_text_from_file_path(input_file)

    assert result == "image-text"
    files_mock.upload.assert_called_once_with(
        file={"file_name": "image.png", "content": input_file.read_bytes()},
        purpose="ocr",
    )
    files_mock.get_signed_url.assert_called_once_with(file_id="file-id")
    mock_extract.assert_called_once_with(client, "http://signed", is_image=True)


def test_extract_text_from_file_path_raises_on_empty_file(tmp_path: Any):
    file_path = tmp_path / "empty.pdf"
    file_path.write_bytes(b"")
    service = OCR(client=Mock())

    with pytest.raises(ValueError):
        _ = service.extract_text_from_file_path(file_path)


def test_extract_from_url_calls_mistral_and_renders():
    client: Mock = Mock()
    client.ocr = Mock()
    response = SimpleNamespace(pages=[SimpleNamespace(markdown="data")])
    client.ocr.process.return_value = response
    service = OCR(client=client)

    with patch.object(service, "_render_pages", return_value="rendered") as mock_render:
        result = service._extract_from_url(client, "http://file", is_image=True)

    assert result == "rendered"
    client.ocr.process.assert_called_once_with(
        model="mistral-ocr-latest",
        document={"type": "image_url", "image_url": "http://file"},
        include_image_base64=True,
    )
    mock_render.assert_called_once_with(response.pages)
