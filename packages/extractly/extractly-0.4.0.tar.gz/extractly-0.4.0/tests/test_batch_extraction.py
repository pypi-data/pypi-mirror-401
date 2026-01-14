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


@patch("extractly.extractor.Extractor.from_file")
@patch("extractly.extractor.Extractor.identify_schema")
def test_batch_extraction_identify_schema(
    mock_identify_schema: MagicMock,
    mock_from_file: MagicMock,
    multiple_schemas: list[Schema],
):
    # Setup mock child extractor
    mock_child = MagicMock()
    mock_child.content = "Sample content for identification"
    mock_extracted_schema = ExtractedSchema(name="SchemaA", entities=[])
    mock_child.extract_fields.return_value = mock_extracted_schema
    mock_from_file.return_value = mock_child

    # Setup identify schema to return SchemaA
    mock_identify_schema.return_value = "SchemaA"

    extractor = Extractor(schemas=multiple_schemas)

    # Mixed docs: one with schema, one without but with inference
    docs = [
        DocumentInput(file_path="doc1.txt", schema_name="SchemaB"),
        DocumentInput(file_path="doc2.txt", infer_schema=True),
    ]

    result = extractor.extract_fields(documents=docs)

    assert isinstance(result, BatchExtractionResult)
    assert len(result.results) == 2
    assert result.successful_results == result.results

    # Check that identify_schema was called for the second doc
    mock_identify_schema.assert_called_once_with("Sample content for identification")

    # Check results
    assert result.results[0].schema_name == "SchemaB"
    assert result.results[1].schema_name == "SchemaA"  # Identified schema


@patch("extractly.extractor.Extractor.from_file")
@patch("extractly.extractor.Extractor.identify_schema")
def test_batch_extraction_identify_schema_fail(
    mock_identify_schema: MagicMock,
    mock_from_file: MagicMock,
    multiple_schemas: list[Schema],
):
    # Setup mock child extractor
    mock_child = MagicMock()
    mock_child.content = "Sample content"
    mock_from_file.return_value = mock_child

    # Setup identify schema to fail (return None)
    mock_identify_schema.return_value = None

    extractor = Extractor(schemas=multiple_schemas)

    # Case 1: Inference enabled but failed
    doc1 = DocumentInput(file_path="doc_unknown.txt", infer_schema=True)

    # Case 2: No schema provided and inference NOT enabled (should fail immediately)
    doc2 = DocumentInput(file_path="doc_forgotten_schema.txt")

    result = extractor.extract_fields(documents=[doc1, doc2])

    assert isinstance(result, BatchExtractionResult)

    assert len(result.results) == 2
    assert result.results[0].error is not None
    assert (
        "not found" in result.results[0].error
        or "Failed to identify" in result.results[0].error
    )

    assert result.results[1].error is not None
    assert (
        "Schema name not provided and infer_schema is False" in result.results[1].error
    )
