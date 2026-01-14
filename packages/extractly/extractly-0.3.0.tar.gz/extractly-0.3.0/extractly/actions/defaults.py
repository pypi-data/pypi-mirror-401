import logging

from ..fields import FieldRepository
from ..schemas import FieldResponse, Table, valueT
from .schemas import Action

logger = logging.getLogger(__name__)


def _ensure_list(value: valueT | list[valueT] | Table) -> list[valueT]:
    """Normalize a field value to a list."""
    if value is None:
        return []
    if isinstance(value, Table):
        raise ValueError("Table values are not supported for list operations")

    if isinstance(value, list):
        return value

    return [value]


def handle_add_new_field(
    field_response: FieldResponse,
    fields: FieldRepository,
) -> None:
    """Add or replace the field with the new value."""
    field = field_response.field
    if field.id in fields.extracted_field_ids:
        logger.info(
            "Field '%s' already exists; overwriting with new value due to add_new_field action",
            field.id,
        )
    fields.upsert_extracted_field(field)


def handle_replace_value_in_existing_field(
    field_response: FieldResponse,
    fields: FieldRepository,
) -> None:
    """Replace the value of an existing field with the new one."""
    field = field_response.field
    existing = fields.get_extracted_field(field.id)

    if existing is None:
        logger.warning(
            "Received replace_value_in_existing_field for unknown field '%s'; treating as add_new_field",
            field.id,
        )
        handle_add_new_field(
            field_response=field_response,
            fields=fields,
        )
        return

    fields.upsert_extracted_field(field)


def handle_add_value_to_existing_list(
    field_response: FieldResponse,
    fields: FieldRepository,
) -> None:
    """Append a value to an existing list field if it is not already present."""
    field = field_response.field
    existing = fields.get_extracted_field(field.id)

    if existing is None:
        logger.warning(
            "Received add_value_to_existing_list for unknown field '%s'; treating as add_new_field",
            field.id,
        )
        handle_add_new_field(
            field_response=field_response,
            fields=fields,
        )
        return

    current_values = _ensure_list(existing.value)
    new_values = _ensure_list(field.value)

    deduped = set(current_values)
    added = False
    for value in new_values:
        if value not in deduped:
            current_values.append(value)
            deduped.add(value)
            added = True

    if not added:
        logger.info(
            "No new values to add for field '%s'; incoming values already present",
            field.id,
        )
        return

    existing.value = current_values
    existing.confidence = max(existing.confidence, field.confidence)
    fields.upsert_extracted_field(existing)
    return


def handle_add_row_to_existing_table_field(
    field_response: FieldResponse,
    fields: FieldRepository,
) -> None:
    """
    Append new rows to a table field while avoiding duplicates.
    Table is expected to be a Table object with "headers" and "rows" attributes.
    """
    field = field_response.field
    existing = fields.get_extracted_field(field.id)

    if existing is None:
        logger.warning(
            "Received add_row_to_existing_table_field for unknown field '%s'; treating as add_new_field",
            field.id,
        )
        handle_add_new_field(
            field_response=field_response,
            fields=fields,
        )
        return

    existing_value = existing.value

    if not isinstance(existing_value, Table):
        logger.warning(
            "Existing field '%s' does not contain a valid table (headers and rows must be present in the Table object); treating as add_new_field",
            field.id,
        )
        handle_add_new_field(
            field_response=field_response,
            fields=fields,
        )
        return

    incoming_value = field.value
    if not isinstance(incoming_value, Table):
        logger.warning(
            "Incoming field '%s' does not contain a valid table (headers and rows must be present in the dict); ignoring action",
            field.id,
        )
        return
    if existing_value.headers != incoming_value.headers:
        logger.warning(
            "Header mismatch for table field '%s'; keeping original table",
            field.id,
        )
        return

    new_rows = incoming_value.rows
    existing_rows = existing_value.rows
    existing_rows.extend(new_rows)
    existing_value.rows = existing_rows
    existing.value = existing_value
    existing.confidence = max(existing.confidence, field.confidence)
    fields.upsert_extracted_field(existing)
    return


DEFAULT_ACTIONS: list[Action] = [
    Action(
        handler=handle_add_new_field,
        description="if the field is not identified under <extracted_fields>, identify it and add it to the list of fields.",
    ),
    Action(
        handler=handle_replace_value_in_existing_field,
        description='if the field is a single value, and the new value is different from the existing one, replace the existing value with the new one. In this case, the field response should have the same name and data_type as the existing field, but with the "value" attribute replaced with the new value.',
    ),
    Action(
        handler=handle_add_value_to_existing_list,
        description='if the field is a list, and the new value is different from the existing ones, add the new value to the list. In this case, the field response should have the same name and data_type as the existing field, but with a single value in the "value" attribute. No need to fill the description.',
    ),
    Action(
        handler=handle_add_row_to_existing_table_field,
        description="if the field is a table, and the new rows are not in the existing table, return a field with the same name, data_type and headers but with the new table rows.",
    ),
]
