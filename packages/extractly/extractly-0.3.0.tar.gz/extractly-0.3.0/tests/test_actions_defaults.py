# pyright: reportUnknownMemberType=false
from typing import Callable

import pytest

from extractly.actions.defaults import (
    handle_add_new_field,
    handle_add_row_to_existing_table_field,
    handle_add_value_to_existing_list,
    handle_replace_value_in_existing_field,
)
from extractly.fields import FieldRepository
from extractly.schemas import ExtractedField, FieldResponse, Table


def make_response(
    field: ExtractedField, handler: Callable[..., object]
) -> FieldResponse:
    return FieldResponse.model_construct(field=field, action=handler.__qualname__)


def test_add_new_field_stores_value(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    field = make_field(
        name="Invoice Number",
        data_type="string",
        value="INV-123",
        entity_name="invoice",
    )

    handle_add_new_field(make_response(field, handle_add_new_field), fields)

    assert fields.extracted_fields[field.id].value == "INV-123"


def test_replace_value_updates_existing(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    initial = make_field(
        name="Status",
        data_type="string",
        value="pending",
        entity_name="order",
        confidence=0.8,
    )
    updated = make_field(
        name="Status",
        data_type="string",
        value="complete",
        entity_name="order",
        confidence=0.95,
    )

    handle_add_new_field(make_response(initial, handle_add_new_field), fields)
    handle_replace_value_in_existing_field(
        make_response(updated, handle_replace_value_in_existing_field),
        fields,
    )

    stored = fields.extracted_fields[initial.id]
    assert stored.value == "complete"
    assert stored.confidence == pytest.approx(0.95)


def test_replace_value_adds_when_missing(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    field = make_field(
        name="Amount",
        data_type="float",
        value=42.5,
        entity_name="invoice",
    )

    handle_replace_value_in_existing_field(
        make_response(field, handle_replace_value_in_existing_field), fields
    )

    assert field.id in fields.extracted_fields


def test_add_to_list_appends_unique_values(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    initial = make_field(
        name="Tags",
        data_type="list",
        value=["electronics", "gadget"],
        entity_name="product",
        confidence=0.8,
    )
    new_values = make_field(
        name="Tags",
        data_type="list",
        value=["portable"],
        entity_name="product",
        confidence=0.9,
    )

    handle_add_new_field(make_response(initial, handle_add_new_field), fields)
    handle_add_value_to_existing_list(
        make_response(new_values, handle_add_value_to_existing_list),
        fields,
    )

    stored = fields.extracted_fields[initial.id]
    assert stored.value == ["electronics", "gadget", "portable"]
    assert stored.confidence == pytest.approx(0.9)


def test_add_to_list_ignores_duplicates(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    initial = make_field(
        name="Categories",
        data_type="list",
        value=["tech", "hardware"],
        entity_name="product",
    )
    duplicate = make_field(
        name="Categories",
        data_type="list",
        value=["tech"],
        entity_name="product",
    )

    handle_add_new_field(make_response(initial, handle_add_new_field), fields)
    handle_add_value_to_existing_list(
        make_response(duplicate, handle_add_value_to_existing_list),
        fields,
    )

    stored = fields.extracted_fields[initial.id]
    assert stored.value == ["tech", "hardware"]


def test_add_to_list_adds_when_missing(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    field = make_field(
        name="Items",
        data_type="list",
        value=["item1"],
        entity_name="order",
    )

    handle_add_value_to_existing_list(
        make_response(field, handle_add_value_to_existing_list), fields
    )

    assert field.id in fields.extracted_fields


def test_append_rows_to_table(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    initial_table = Table(headers=["Name", "Quantity"], rows=[["Widget A", "5"]])
    new_rows = Table(headers=["Name", "Quantity"], rows=[["Widget B", "3"]])

    initial = make_field(
        name="Line Items",
        data_type="table",
        value=initial_table,
        entity_name="invoice",
    )
    additional = make_field(
        name="Line Items",
        data_type="table",
        value=new_rows,
        entity_name="invoice",
        confidence=0.95,
    )

    handle_add_new_field(make_response(initial, handle_add_new_field), fields)
    handle_add_row_to_existing_table_field(
        make_response(additional, handle_add_row_to_existing_table_field),
        fields,
    )

    stored = fields.extracted_fields[initial.id]
    assert isinstance(stored.value, Table)
    table_value = stored.value
    assert table_value.rows == [["Widget A", "5"], ["Widget B", "3"]]
    assert stored.confidence == pytest.approx(0.95)


def test_table_rows_add_when_missing(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    table_field = make_field(
        name="Data Table",
        data_type="table",
        value=Table(headers=["Col1", "Col2"], rows=[["A", "B"]]),
        entity_name="report",
    )

    handle_add_row_to_existing_table_field(
        make_response(table_field, handle_add_row_to_existing_table_field), fields
    )

    assert table_field.id in fields.extracted_fields


def test_table_rows_ignore_header_mismatch(make_field: Callable[..., ExtractedField]):
    fields = FieldRepository()
    original = make_field(
        name="Items",
        data_type="table",
        value=Table(headers=["Name", "Price"], rows=[["Item1", "10"]]),
        entity_name="invoice",
    )
    mismatched = make_field(
        name="Items",
        data_type="table",
        value=Table(headers=["Name", "Quantity"], rows=[["Item2", "5"]]),
        entity_name="invoice",
    )

    handle_add_new_field(make_response(original, handle_add_new_field), fields)
    handle_add_row_to_existing_table_field(
        make_response(mismatched, handle_add_row_to_existing_table_field),
        fields,
    )

    stored = fields.extracted_fields[original.id]
    assert isinstance(stored.value, Table)
    table_value = stored.value
    assert table_value.rows == [["Item1", "10"]]
