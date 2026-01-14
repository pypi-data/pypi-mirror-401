import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, computed_field
from typing_extensions import override

DefaultActionsT = Literal[
    "add_new_field",
    "replace_value_in_existing_field",
    "add_value_to_existing_list",
    "add_row_to_existing_table_field",
]


valueT = (
    str | int | float | bool | datetime.date | datetime.time | datetime.datetime | None
)


class Table(BaseModel):
    headers: list[str]
    rows: list[list[valueT]]


FieldValue = valueT | list[valueT] | Table


def _generate_field_id(name: str, entity_name: str) -> str:
    return f"{entity_name}.{name}"


class SchemaField(BaseModel):
    name: str
    description: str | None = None
    data_type: str
    example: valueT | list[valueT] | Table


class SchemaEntity(BaseModel):
    name: str
    description: str
    fields: list[SchemaField]


class Schema(BaseModel):
    name: str
    description: str
    entities: list[SchemaEntity]
    fields_by_id: dict[str, SchemaField] = Field(default_factory=dict)

    @override
    def model_post_init(self, __context: object | None):
        self.fields_by_id = {}
        for entity in self.entities:
            for field in entity.fields:
                field_id = _generate_field_id(field.name, entity.name)
                self.fields_by_id[field_id] = field

    @computed_field
    @property
    def field_ids(self) -> list[str]:
        return [field_id for field_id in self.fields_by_id.keys()]

    def get_field(self, field_id: str) -> SchemaField | None:
        return self.fields_by_id.get(field_id)


class ExtractedField(BaseModel):
    name: str
    description: str
    data_type: str
    value: valueT | list[valueT] | Table
    entity_name: str
    confidence: float = Field(
        description="Confidence score for the field extraction",
        ge=0,
        le=1,
    )

    @computed_field
    @property
    def id(self) -> str:
        return _generate_field_id(self.name, self.entity_name)


class ExtractedEntity(BaseModel):
    name: str
    description: str | None = None
    fields: list[ExtractedField] = Field(default_factory=list)


class ExtractedSchema(BaseModel):
    name: str
    description: str | None = None
    entities: list[ExtractedEntity]


class FieldResponse(BaseModel):
    field: ExtractedField = Field(
        description="Field to extract",
    )
    action: DefaultActionsT = Field(
        description="Action to take for the extracted field",
    )


class FieldExtractorOutput(BaseModel):
    fields: list[FieldResponse]


class DocumentInput(BaseModel):
    file_path: str | Path
    schema_name: str | None = None
    infer_schema: bool = False
    use_ocr: bool = False
    ocr_filename: str | None = None
    ocr_is_image: bool | None = None


class DocumentResult(BaseModel):
    document_id: str
    schema_name: str
    extracted_schema: ExtractedSchema | None = None
    error: str | None = None


class BatchExtractionResult(BaseModel):
    results: list[DocumentResult]

    @property
    def successful_results(self) -> list[DocumentResult]:
        return [r for r in self.results if not r.error]

    @property
    def failed_results(self) -> list[DocumentResult]:
        return [r for r in self.results if r.error]
