from ..schemas import (
    ExtractedEntity,
    ExtractedField,
    ExtractedSchema,
    Schema,
)


class FieldRepository:
    _extracted_fields: dict[str, ExtractedField]
    _schema: Schema | None

    def __init__(self, schema: Schema | None = None):
        self._schema = schema
        self._extracted_fields = {}

    def upsert_extracted_field(self, field: ExtractedField):
        self._extracted_fields[field.id] = field

    def get_extracted_field(self, id: str) -> ExtractedField | None:
        return self._extracted_fields.get(id)

    @property
    def extracted_fields(self) -> dict[str, ExtractedField]:
        return self._extracted_fields

    @property
    def extracted_field_ids(self) -> list[str]:
        return [field.id for field in self._extracted_fields.values()]

    def build_extracted_schema(self) -> ExtractedSchema:
        schema_entities = (
            {entity.name: entity for entity in self._schema.entities}
            if self._schema
            else {}
        )

        extracted_entities: dict[str, ExtractedEntity] = {}
        for field in self._extracted_fields.values():
            entity = extracted_entities.get(field.entity_name)
            if entity is None:
                schema_entity = schema_entities.get(field.entity_name)
                entity = ExtractedEntity(
                    name=field.entity_name,
                    description=schema_entity.description if schema_entity else None,
                )
                extracted_entities[field.entity_name] = entity
            entity.fields.append(field)

        schema_name = self._schema.name if self._schema else "Extracted Schema"
        schema_description = self._schema.description if self._schema else None

        return ExtractedSchema(
            name=schema_name,
            description=schema_description,
            entities=list(extracted_entities.values()),
        )
