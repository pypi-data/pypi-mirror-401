# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportAny=false, reportExplicitAny=false
import pytest
from unittest.mock import MagicMock, patch
from extractly.extractor import Extractor
from extractly.schemas import (
    Schema,
    DocumentInput,
    BatchExtractionResult,
    ExtractedSchema,
)


@pytest.fixture
def mock_schema():
    return Schema(name="TestSchema", description="A test schema", entities=[])


@pytest.fixture
def multiple_schemas():
    return [
        Schema(name="SchemaA", description="A", entities=[]),
        Schema(name="SchemaB", description="B", entities=[]),
    ]


def test_batch_extraction_no_documents(mock_schema: Schema):
    extractor = Extractor(schemas=[mock_schema])
    result = extractor.extract_fields(documents=[])
    assert isinstance(result, BatchExtractionResult)
    assert len(result.results) == 0


def test_batch_extraction_schema_not_found(mock_schema: Schema):
    extractor = Extractor(schemas=[mock_schema])
    doc = DocumentInput(file_path="test.txt", schema_name="NonExistent")

    result = extractor.extract_fields(documents=[doc])

    assert isinstance(result, BatchExtractionResult)
    assert len(result.results) == 1
    assert result.results[0].error is not None
    assert "not found" in result.results[0].error


@patch("extractly.extractor.Extractor.from_file")
def test_batch_extraction_success(
    mock_from_file: MagicMock, multiple_schemas: list[Schema]
):
    # Setup mock child extractor
    mock_child = MagicMock()
    mock_extracted_schema = ExtractedSchema(name="SchemaA", entities=[])
    mock_child.extract_fields.return_value = mock_extracted_schema
    mock_from_file.return_value = mock_child

    extractor = Extractor(schemas=multiple_schemas)

    docs = [
        DocumentInput(file_path="doc1.txt", schema_name="SchemaA"),
        DocumentInput(file_path="doc2.txt", schema_name="SchemaB"),
    ]

    # We need to mock returning different schema results if we want to be precise,
    # but for now let's just check if it calls from_file correctly.

    result = extractor.extract_fields(documents=docs)

    assert isinstance(result, BatchExtractionResult)
    assert len(result.results) == 2
    assert result.successful_results == result.results

    # Verify Extractor.from_file was called twice with correct args
    assert mock_from_file.call_count == 2

    # Check first call args
    call_args_list = mock_from_file.call_args_list
    _, kwargs1 = call_args_list[0]
    assert kwargs1["input_file_path"] == "doc1.txt"
    # cast to Schema to avoid reportAny on .name access if possible, or just ignore for mock
    assert kwargs1["schema"].name == "SchemaA"

    _, kwargs2 = call_args_list[1]
    assert kwargs2["input_file_path"] == "doc2.txt"
    assert kwargs2["schema"].name == "SchemaB"


@patch("extractly.extractor.Extractor.from_file")
def test_batch_extraction_child_error(mock_from_file: MagicMock, mock_schema: Schema):
    mock_from_file.side_effect = Exception("OCR failed")

    extractor = Extractor(schemas=[mock_schema])
    doc = DocumentInput(file_path="broken.txt", schema_name="TestSchema")

    result = extractor.extract_fields(documents=[doc])

    assert isinstance(result, BatchExtractionResult)
    assert len(result.results) == 1
    assert result.results[0].error == "OCR failed"
