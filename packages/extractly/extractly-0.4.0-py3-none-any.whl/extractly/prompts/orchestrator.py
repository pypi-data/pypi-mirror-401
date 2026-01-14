from ..fields import FieldRepository
from ..schemas import ExtractedField, Schema, Table
from .defaults import (
    EXTRACTED_FIELD_TEMPLATE,
    FIELD_TO_EXTRACT_TEMPLATE,
    FIND_AND_USE_REQUESTED_FIELDS_SYSTEM_PROMPT,
    FIND_FIELDS_SYSTEM_PROMPT,
    STRICT_FIELDS_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    USER_PROMPT_WITH_REQUESTED_FIELDS_TEMPLATE,
    SCHEMA_IDENTIFICATION_SYSTEM_PROMPT,
    SCHEMA_IDENTIFICATION_USER_PROMPT,
)


class PromptService:
    """Central manager and orchestrator for prompts."""

    def __init__(
        self,
        identify_fields: bool,
        schema: Schema | None = None,
        system_prompt: str | None = None,
        user_prompt_template: str | None = None,
        field_to_extract_template: str = FIELD_TO_EXTRACT_TEMPLATE,
        extracted_field_template: str = EXTRACTED_FIELD_TEMPLATE,
    ) -> None:
        self.identify_fields: bool = identify_fields
        self.schema: Schema | None = schema

        self.provided_system_prompt: str | None = system_prompt
        self.provided_user_prompt_template: str | None = user_prompt_template
        self.field_to_extract_template: str = field_to_extract_template
        self.extracted_field_template: str = extracted_field_template

    def get_table_field_prompt(self, value: Table) -> str:
        return f"table with headers {value.headers} and {len(value.rows)} rows"

    def build_requested_fields_prompt(
        self,
        extracted_field_ids: list[str],
        field_to_extract_template: str = FIELD_TO_EXTRACT_TEMPLATE,
    ) -> str:
        if self.schema is None:
            return ""
        fields_str = ""

        for entity in self.schema.entities:
            for field in entity.fields:
                field_id = f"{entity.name}.{field.name}"
                if field_id in extracted_field_ids:
                    # no need to duplicate field information that has already been extracted
                    continue

                example = (
                    self.get_table_field_prompt(field.example)
                    if isinstance(field.example, Table)
                    else str(field.example)
                )
                fields_str += field_to_extract_template.format(
                    name=field.name,
                    entity=entity.name,
                    data_type=field.data_type,
                    description=field.description,
                    example=example,
                )
        return fields_str

    def build_extracted_fields_prompt(
        self,
        extracted_fields: dict[str, ExtractedField],
        extracted_field_template: str = EXTRACTED_FIELD_TEMPLATE,
    ) -> str:
        fields_str = ""
        for field in extracted_fields.values():
            if field.data_type == "table" and isinstance(field.value, Table):
                value = self.get_table_field_prompt(field.value)
            elif isinstance(field.value, list):
                value = ",".join(str(value) for value in field.value)
            else:
                value = field.value
            fields_str += extracted_field_template.format(
                name=field.name,
                data_type=field.data_type,
                description=field.description,
                value=value,
            )

        return fields_str

    @property
    def system_prompt(self) -> str:
        if self.provided_system_prompt:
            # user passed in a system prompt
            return self.provided_system_prompt
        if self.identify_fields and self.schema is not None:
            # user passed in requested fields and wants to identify other new fields
            return FIND_AND_USE_REQUESTED_FIELDS_SYSTEM_PROMPT

        elif self.identify_fields:
            # user didn't pass requested fields and wants to identify and extract new fields in the content
            return FIND_FIELDS_SYSTEM_PROMPT

        elif self.schema is not None:
            # user passed in requested fields and doesn't want to find more fields
            return STRICT_FIELDS_SYSTEM_PROMPT

        return FIND_FIELDS_SYSTEM_PROMPT

    @property
    def schema_identification_system_prompt(self) -> str:
        return SCHEMA_IDENTIFICATION_SYSTEM_PROMPT

    @property
    def user_prompt_template(self) -> str:
        if self.provided_user_prompt_template is not None:
            return self.provided_user_prompt_template
        if self.identify_fields or self.schema is not None:
            return USER_PROMPT_WITH_REQUESTED_FIELDS_TEMPLATE
        return USER_PROMPT_TEMPLATE

    def get_user_message(
        self,
        fields: FieldRepository,
        chunk: str,
        actions: str,
    ) -> str:
        requested_fields_prompt = self.build_requested_fields_prompt(
            extracted_field_ids=fields.extracted_field_ids,
            field_to_extract_template=self.field_to_extract_template,
        )
        extracted_fields_prompt = self.build_extracted_fields_prompt(
            extracted_fields=fields.extracted_fields,
            extracted_field_template=self.extracted_field_template,
        )
        user_prompt_template = self.user_prompt_template
        message = user_prompt_template.format(
            actions=actions,
            requested_fields=requested_fields_prompt,
            extracted_fields=extracted_fields_prompt,
            text=chunk,
        )
        message = user_prompt_template.format(
            actions=actions,
            requested_fields=requested_fields_prompt,
            extracted_fields=extracted_fields_prompt,
            text=chunk,
        )
        return message

    def get_schema_identification_message(
        self,
        schemas: list[Schema],
        content: str,
    ) -> str:
        schemas_desc = "\n".join(
            f'- Name: "{s.name}"\n  Description: {s.description}' for s in schemas
        )
        return SCHEMA_IDENTIFICATION_USER_PROMPT.format(
            schemas=schemas_desc,
            content=content,
        )
