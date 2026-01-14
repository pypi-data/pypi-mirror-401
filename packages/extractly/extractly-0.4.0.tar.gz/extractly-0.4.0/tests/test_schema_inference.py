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
def invoice_schema() -> Schema:
    return Schema(name="Invoice", description="Invoice schema", entities=[])


@pytest.fixture
def bank_statement_schema() -> Schema:
    return Schema(
        name="Bank Statement", description="Bank statement schema", entities=[]
    )


@pytest.fixture
def schemas(invoice_schema: Schema, bank_statement_schema: Schema) -> list[Schema]:
    return [invoice_schema, bank_statement_schema]


@patch("extractly.extractor.Extractor.from_file")
@patch("extractly.extractor.Extractor.identify_schema")
def test_schema_inference_success(
    mock_identify_schema: MagicMock,
    mock_from_file: MagicMock,
    schemas: list[Schema],
):
    """Test that the correct schema is identified and used."""
    # Setup mock child extractor
    mock_child = MagicMock()
    mock_child.content = "Bank Statement Content"
    mock_extracted_result = ExtractedSchema(name="Bank Statement", entities=[])
    mock_child.extract_fields.return_value = mock_extracted_result
    mock_from_file.return_value = mock_child

    # Mock successful identification
    mock_identify_schema.return_value = "Bank Statement"

    extractor = Extractor(schemas=schemas)
    doc = DocumentInput(file_path="statement.pdf", infer_schema=True)

    result = extractor.extract_fields(documents=[doc])

    assert isinstance(result, BatchExtractionResult)
    assert len(result.successful_results) == 1

    # Verify identify_schema was called
    mock_identify_schema.assert_called_once_with("Bank Statement Content")

    # Verify the result has the correct schema name
    assert result.results[0].schema_name == "Bank Statement"
    assert result.results[0].extracted_schema == mock_extracted_result


@patch("extractly.extractor.Extractor.from_file")
@patch("extractly.extractor.Extractor.identify_schema")
def test_schema_inference_no_match(
    mock_identify_schema: MagicMock, mock_from_file: MagicMock, schemas: list[Schema]
):
    """Test behavior when no schema is identified."""
    mock_child = MagicMock()
    mock_child.content = "Unknown Content"
    mock_from_file.return_value = mock_child

    # Mock identification failure
    mock_identify_schema.return_value = None

    extractor = Extractor(schemas=schemas)
    doc = DocumentInput(file_path="unknown.pdf", infer_schema=True)

    result = extractor.extract_fields(documents=[doc])

    assert isinstance(result, BatchExtractionResult)
    assert len(result.failed_results) == 1
    error = result.results[0].error
    assert error is not None
    assert "Failed to identify" in error or "not found" in error


@patch("extractly.extractor.Extractor.from_file")
@patch("extractly.extractor.Extractor.identify_schema")
def test_mixed_explicit_and_diferred(
    mock_identify_schema: MagicMock, mock_from_file: MagicMock, schemas: list[Schema]
):
    """Test batch with both explicit schema and inferred schema."""
    mock_child = MagicMock()
    mock_child.content = "Content"
    # We need to handle multiple calls to extract_fields on the child mock or just generic return
    mock_child.extract_fields.return_value = ExtractedSchema(name="Any", entities=[])
    mock_from_file.return_value = mock_child

    mock_identify_schema.return_value = "Invoice"

    extractor = Extractor(schemas=schemas)

    doc1 = DocumentInput(file_path="invoice.pdf", infer_schema=True)
    doc2 = DocumentInput(file_path="statement.pdf", schema_name="Bank Statement")

    result = extractor.extract_fields(documents=[doc1, doc2])

    assert isinstance(result, BatchExtractionResult)
    assert len(result.results) == 2
    assert result.results[0].schema_name == "Invoice"  # Inferred
    assert result.results[1].schema_name == "Bank Statement"  # Explicit

    # identify_schema should be called only once (for doc1)
    mock_identify_schema.assert_called_once()
