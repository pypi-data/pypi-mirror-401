# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportAny=false, reportExplicitAny=false
from pathlib import Path
from typing import Any, Callable, cast
from collections.abc import Iterator

import pytest
from unittest.mock import patch
from typing_extensions import override

from extractly.actions.defaults import (
    handle_add_new_field,
    handle_add_row_to_existing_table_field,
    handle_add_value_to_existing_list,
    handle_replace_value_in_existing_field,
)
from extractly.actions.schemas import Action
from extractly.extractor import Extractor
from extractly.fields import FieldRepository
from extractly.ocr import OCR
from extractly.schemas import ExtractedField, FieldResponse, Schema, Table


class RecordingExtractor(Extractor):
    """Test double that records processed chunks and returns pre-defined responses."""

    def __init__(
        self,
        content: str,
        *,
        responses: list[list[FieldResponse]] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(content, **kwargs)
        self._responses: Iterator[list[FieldResponse]] = iter(responses or [])
        self.processed_chunks: list[tuple[str, bool]] = []

    @override
    def process_chunk(self, chunk: str, dry_run: bool = False) -> list[FieldResponse]:
        self.processed_chunks.append((chunk, dry_run))
        if dry_run:
            return []
        return next(self._responses, [])


def build_content(*sections: str) -> str:
    return "\n\n".join(
        f"# Section {index + 1}\n\n{body}" for index, body in enumerate(sections)
    )


ADD_NEW = handle_add_new_field.__qualname__
REPLACE = handle_replace_value_in_existing_field.__qualname__
ADD_TO_LIST = handle_add_value_to_existing_list.__qualname__
ADD_TABLE_ROW = handle_add_row_to_existing_table_field.__qualname__


def make_response(field: ExtractedField, action_name: str) -> FieldResponse:
    return FieldResponse.model_construct(field=field, action=action_name)


def test_from_file_runs_ocr_when_enabled(tmp_path: Path) -> None:
    input_file = tmp_path / "invoice.jpg"
    _ = input_file.write_bytes(b"binary-data")
    output_file = tmp_path / "ocr_output.md"

    class StubOCR:
        def __init__(self) -> None:
            self.calls: list[tuple[Path, Path | None, str | None, bool | None]] = []

        def extract_text_from_file_path(
            self,
            input_file_path: Path,
            output_file_path: Path | None = None,
            filename: str | None = None,
            is_image: bool | None = None,
        ) -> str:
            self.calls.append((input_file_path, output_file_path, filename, is_image))
            return "ocr-content"

    ocr_service = StubOCR()

    extractor = Extractor.from_file(
        input_file_path=input_file,
        use_ocr=True,
        ocr_service=cast(OCR, cast(object, ocr_service)),
        ocr_output_file_path=output_file,
        ocr_is_image=True,
        identify_fields=False,
    )

    assert ocr_service.calls == [(input_file, output_file, None, True)]
    assert extractor.content == "ocr-content"


def test_from_file_reads_text_without_ocr(tmp_path: Path) -> None:
    text_file = tmp_path / "notes.txt"
    _ = text_file.write_text("plain text content")

    extractor = Extractor.from_file(input_file_path=text_file, identify_fields=False)

    assert extractor.content == "plain text content"


def test_from_file_accepts_string_paths(tmp_path: Path) -> None:
    text_file = tmp_path / "notes.txt"
    _ = text_file.write_text("from string path")

    extractor = Extractor.from_file(
        input_file_path=str(text_file), identify_fields=False
    )

    assert extractor.content == "from string path"


def test_from_file_passes_filename_through_to_ocr(tmp_path: Path) -> None:
    input_file = tmp_path / "invoice.bin"
    _ = input_file.write_bytes(b"binary-data")

    class StubOCR:
        def __init__(self) -> None:
            self.calls: list[tuple[Path, Path | None, str | None, bool | None]] = []

        def extract_text_from_file_path(
            self,
            input_file_path: Path,
            output_file_path: Path | None = None,
            filename: str | None = None,
            is_image: bool | None = None,
        ) -> str:
            self.calls.append((input_file_path, output_file_path, filename, is_image))
            return "ocr-content"

    service = StubOCR()

    _ = Extractor.from_file(
        input_file_path=input_file,
        use_ocr=True,
        ocr_service=cast(OCR, cast(object, service)),
        ocr_filename="uploaded.jpg",
        ocr_is_image=False,
        identify_fields=False,
    )

    assert service.calls == [(input_file, None, "uploaded.jpg", False)]


def test_from_file_raises_friendly_decode_error(tmp_path: Path) -> None:
    text_file = tmp_path / "notes.txt"
    _ = text_file.write_bytes(b"\xff\xfe\xfa")  # invalid utf-8

    with pytest.raises(ValueError) as excinfo:
        _ = Extractor.from_file(input_file_path=text_file, identify_fields=False)

    assert "Could not decode" in str(excinfo.value)
    assert "use_ocr=True" in str(excinfo.value)


def test_extract_fields_dry_run_skips_agent(
    make_extractor: Callable[..., Extractor],
):
    extractor = make_extractor("single chunk text")

    def fail_dry_run(*_args: object, **_kwargs: object) -> None:
        pytest.fail("agent should not be called during dry_run")

    with patch.object(extractor.agent, "run_sync", side_effect=fail_dry_run):
        _ = extractor.extract_fields(dry_run=True)

    assert [field.id for field in extractor.fields.extracted_fields.values()] == []


def test_extract_fields_aggregates_agent_responses(
    make_field: Callable[..., ExtractedField],
):
    first_chunk_field = make_field(
        name="Vendors",
        data_type="list",
        value=["Vendor A"],
        entity_name="vendor_list",
        confidence=0.7,
    )
    second_chunk_field = make_field(
        name="Vendors",
        data_type="list",
        value=["Vendor B"],
        entity_name="vendor_list",
        confidence=0.9,
    )

    responses = [
        [make_response(first_chunk_field, ADD_NEW)],
        [make_response(second_chunk_field, ADD_TO_LIST)],
    ]
    content = build_content(
        "Details about Vendor A and the services they provide.",
        "Coverage of Vendor B and their support commitments.",
    )

    extractor = RecordingExtractor(content, responses=responses, max_chunk_size=120)
    extracted_schema = extractor.extract_fields()

    field_id = "vendor_list.Vendors"
    field_ids = [
        field.id for entity in extracted_schema.entities for field in entity.fields
    ]
    assert field_id in field_ids
    field = next(
        (
            field
            for entity in extracted_schema.entities
            for field in entity.fields
            if field.id == field_id
        ),
        None,
    )
    assert field is not None
    assert field.value == ["Vendor A", "Vendor B"]
    assert field.confidence == pytest.approx(0.9)


def test_process_chunk_handles_missing_agent_output(
    make_extractor: Callable[..., Extractor],
):
    class StubPromptService:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def get_user_message(self, chunk: str, **_kwargs: Any) -> str:
            self.calls.append(chunk)
            return f"formatted::{chunk}"

    class StubAgentResult:
        def __init__(self) -> None:
            self.output: list[FieldResponse] = []

        def usage(self) -> dict[str, int]:
            return {}

    extractor = make_extractor("report content")
    stub_prompt = StubPromptService()
    extractor.prompt_service = cast(Any, stub_prompt)
    with patch.object(extractor.agent, "run_sync", return_value=StubAgentResult()):
        responses = extractor.process_chunk("input segment")

    assert responses == []
    assert stub_prompt.calls == ["input segment"]


def test_extractor_initializes_with_schema(
    make_extractor: Callable[..., Extractor], sample_schema: Schema
) -> None:
    extractor = make_extractor(schema=sample_schema)

    assert extractor.fields._schema is sample_schema
    assert extractor.prompt_service.schema is sample_schema


def test_extractor_respects_identify_fields_flag(
    make_extractor: Callable[..., Extractor],
):
    extractor = make_extractor(identify_fields=False)

    assert extractor.identify_fields is False
    assert extractor.prompt_service.identify_fields is False


def test_custom_chunk_size_breaks_content_into_chunks():
    content = build_content(
        "This section outlines the first half of the agreement.",
        "Companion section with the remainder of the obligations.",
        "Final section that would normally be processed together.",
    )

    extractor = RecordingExtractor(content, max_chunk_size=80)
    _ = extractor.extract_fields(dry_run=True)

    assert len(extractor.processed_chunks) == 3
    assert all(flag is True for _, flag in extractor.processed_chunks)


def test_multiple_chunks_with_different_actions(
    make_field: Callable[..., ExtractedField],
):
    total_initial = make_field(
        name="Total",
        data_type="float",
        value=100.0,
        entity_name="invoice",
        confidence=0.8,
    )
    total_updated = make_field(
        name="Total",
        data_type="float",
        value=150.0,
        entity_name="invoice",
        confidence=0.95,
    )
    items_initial = make_field(
        name="Items",
        data_type="list",
        value=["Item A"],
        entity_name="invoice",
        confidence=0.9,
    )
    items_append = make_field(
        name="Items",
        data_type="list",
        value=["Item B"],
        entity_name="invoice",
        confidence=0.9,
    )

    responses = [
        [make_response(total_initial, ADD_NEW)],
        [make_response(total_updated, REPLACE)],
        [
            make_response(items_initial, ADD_NEW),
            make_response(items_append, ADD_TO_LIST),
        ],
    ]
    content = build_content(
        "Initial financial summary.",
        "Updated totals after adjustments.",
        "Detailed list of items sold.",
    )

    extractor = RecordingExtractor(content, responses=responses, max_chunk_size=50)
    extracted_schema = extractor.extract_fields()

    total_field = next(
        (
            field
            for entity in extracted_schema.entities
            for field in entity.fields
            if field.id == "invoice.Total"
        ),
        None,
    )
    items_field = next(
        (
            field
            for entity in extracted_schema.entities
            for field in entity.fields
            if field.id == "invoice.Items"
        ),
        None,
    )
    assert total_field is not None
    assert total_field.value == 150.0
    assert total_field.confidence == pytest.approx(0.95)
    assert items_field is not None
    assert items_field.value == ["Item A", "Item B"]


def test_extractor_supports_custom_actions(
    make_field: Callable[..., ExtractedField],
):
    calls: list[str] = []

    def uppercase_handler(
        field_response: FieldResponse, fields: FieldRepository
    ) -> None:
        calls.append(field_response.field.id)
        field = field_response.field
        if isinstance(field.value, str):
            field.value = field.value.upper()
        fields.upsert_extracted_field(field)

    action = Action(handler=uppercase_handler, description="Uppercase string values")
    field = make_field(
        name="Title",
        data_type="string",
        value="hello world",
        entity_name="document",
    )
    responses = [[make_response(field, action.name)]]

    extractor = RecordingExtractor(
        build_content("Document metadata lives here."),
        responses=responses,
        actions=[action],
        max_chunk_size=60,
    )
    extracted_schema = extractor.extract_fields()

    assert calls == [field.id]
    stored_field = next(
        (
            f
            for entity in extracted_schema.entities
            for f in entity.fields
            if f.id == field.id
        ),
        None,
    )
    assert stored_field is not None
    assert stored_field.value == "HELLO WORLD"


def test_empty_content_extracts_no_fields() -> None:
    extractor = RecordingExtractor("")
    _ = extractor.extract_fields(dry_run=True)

    assert [field.id for field in extractor.fields.extracted_fields.values()] == []
    assert extractor.processed_chunks == []


def test_table_rows_are_merged_through_action(
    make_field: Callable[..., ExtractedField],
):
    initial_table = Table(
        headers=["Name", "Quantity"],
        rows=[["Widget A", "5"]],
    )
    append_table = Table(
        headers=["Name", "Quantity"],
        rows=[["Widget B", "3"]],
    )

    responses = [
        [
            make_response(
                make_field(
                    name="Line Items",
                    data_type="table",
                    value=initial_table,
                    entity_name="invoice",
                ),
                ADD_NEW,
            )
        ],
        [
            make_response(
                make_field(
                    name="Line Items",
                    data_type="table",
                    value=append_table,
                    entity_name="invoice",
                ),
                ADD_TABLE_ROW,
            )
        ],
    ]
    content = build_content(
        "Line items extracted from the first page.",
        "Line items extracted from the second page.",
    )

    extractor = RecordingExtractor(content, responses=responses, max_chunk_size=85)
    extracted_schema = extractor.extract_fields()

    table_field = next(
        (
            field
            for entity in extracted_schema.entities
            for field in entity.fields
            if field.id == "invoice.Line Items"
        ),
        None,
    )
    assert table_field is not None
    table_value = table_field.value
    assert isinstance(table_value, Table)
    assert table_value.rows == [["Widget A", "5"], ["Widget B", "3"]]
