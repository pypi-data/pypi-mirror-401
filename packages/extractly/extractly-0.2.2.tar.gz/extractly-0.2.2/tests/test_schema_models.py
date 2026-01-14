from typing import Callable
from extractly.schemas import ExtractedField, Schema


def test_extracted_field_generates_id(make_field: Callable[..., ExtractedField]):
    field = make_field(
        name="Invoice Date",
        data_type="date",
        value="2024-01-15",
        entity_name="invoice",
    )

    assert field.id == "invoice.Invoice Date"


def test_schema_field_lookup(sample_schema: Schema):
    invoice_number = sample_schema.get_field("invoice.Invoice Number")
    assert invoice_number is not None
    assert invoice_number.name == "Invoice Number"
    assert invoice_number.data_type == "string"

    assert sample_schema.get_field("invoice.Unknown") is None
