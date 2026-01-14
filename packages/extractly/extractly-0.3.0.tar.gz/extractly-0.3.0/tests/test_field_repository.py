from typing import Callable

from extractly.fields import FieldRepository
from extractly.schemas import ExtractedField, Schema


def test_field_repository_tracks_fields(make_field: Callable[..., ExtractedField]):
    repository = FieldRepository()

    assert repository.extracted_fields == {}
    assert repository.extracted_field_ids == []

    field = make_field(
        name="Customer Name",
        data_type="string",
        value="John Doe",
        entity_name="customer",
    )
    repository.upsert_extracted_field(field)

    assert repository.extracted_field_ids == [field.id]
    stored = repository.get_extracted_field(field.id)
    assert stored is not None
    assert stored.value == "John Doe"
    assert repository.get_extracted_field("missing") is None


def test_build_extracted_schema_includes_entities(
    make_field: Callable[..., ExtractedField], sample_schema: Schema
):
    repository = FieldRepository(schema=sample_schema)

    field = make_field(
        name="Invoice Number",
        data_type="string",
        value="INV-123",
        entity_name="invoice",
    )
    repository.upsert_extracted_field(field)

    extracted_schema = repository.build_extracted_schema()

    assert extracted_schema.name == sample_schema.name
    assert extracted_schema.description == sample_schema.description
    assert [f.id for entity in extracted_schema.entities for f in entity.fields] == [
        field.id
    ]
    assert len(extracted_schema.entities) == 1
    entity = extracted_schema.entities[0]
    assert entity.name == field.entity_name
    assert entity.description == "Invoice data"
    stored_field = next(
        (f for e in extracted_schema.entities for f in e.fields if f.id == field.id),
        None,
    )
    assert stored_field is not None
    assert stored_field.value == "INV-123"
