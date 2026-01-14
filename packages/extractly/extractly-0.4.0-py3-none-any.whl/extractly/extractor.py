import logging
from pathlib import Path
from typing import Literal

from pydantic import create_model
from pydantic_ai import Agent, models

from .actions import ActionService
from .actions.schemas import Action
from .chunking import chunk_markdown
from .config import DEFAULT_MAX_CHUNK_SIZE, DEFAULT_MODEL
from .fields import FieldRepository
from .ocr import OCR
from .prompts import PromptService
from .schemas import (
    BatchExtractionResult,
    DocumentInput,
    DocumentResult,
    ExtractedSchema,
    FieldResponse,
    Schema,
)

logger = logging.getLogger(__name__)


class Extractor:
    def __init__(
        self,
        content: str | None = None,
        model: models.Model | str = DEFAULT_MODEL,
        max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
        schema: Schema | None = None,
        schemas: list[Schema] | None = None,
        actions: list[Action] | None = None,
        identify_fields: bool = True,
    ) -> None:
        self.content: str | None = content
        self.schemas: list[Schema] = schemas or []
        self.fields: FieldRepository = FieldRepository(schema=schema)
        self.identify_fields: bool = identify_fields
        self.model: models.Model | str = model
        self.max_chunk_size: int = max_chunk_size
        self.prompt_service: PromptService = PromptService(
            identify_fields=self.identify_fields, schema=schema
        )

        self.action_service: ActionService = ActionService()
        if actions:
            # explicit action handlers take precedence over the default ones
            self.action_service.register_many(actions)

        if self.content:
            self.agent: Agent[None, list[FieldResponse]] = self.create_agent()

    @classmethod
    def from_file(
        cls,
        input_file_path: Path | str,
        *,
        use_ocr: bool = False,
        ocr_service: OCR | None = None,
        ocr_output_file_path: Path | str | None = None,
        ocr_filename: str | None = None,
        ocr_is_image: bool | None = None,
        encoding: str = "utf-8",
        model: models.Model | str = DEFAULT_MODEL,
        max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
        schema: Schema | None = None,
        actions: list[Action] | None = None,
        identify_fields: bool = True,
    ) -> "Extractor":
        """Create an extractor from a file and optionally run OCR first."""

        input_path = Path(input_file_path)
        output_path = Path(ocr_output_file_path) if ocr_output_file_path else None

        if use_ocr:
            service = ocr_service or OCR()
            content = service.extract_text_from_file_path(
                input_file_path=input_path,
                output_file_path=output_path,
                filename=ocr_filename,
                is_image=ocr_is_image,
            )
        else:
            try:
                content = input_path.read_text(encoding=encoding)
            except UnicodeDecodeError as exc:
                raise ValueError(
                    f"Could not decode {input_path} with encoding {encoding}. Pass a different encoding or set use_ocr=True for images/PDFs."
                ) from exc

        return cls(
            content=content,
            model=model,
            max_chunk_size=max_chunk_size,
            schema=schema,
            actions=actions,
            identify_fields=identify_fields,
        )

    def create_agent(self) -> Agent[None, list[FieldResponse]]:
        # extend available actions with the action handler registry
        ActionType = Literal[tuple(self.action_service.available_actions())]

        FieldResponseWithAction = create_model(
            "Response",
            action=ActionType,
            __base__=FieldResponse,
        )
        return Agent(
            system_prompt=self.prompt_service.system_prompt,
            model=self.model,
            output_type=list[FieldResponseWithAction],
        )

    def process_chunk(self, chunk: str, dry_run: bool = False) -> list[FieldResponse]:
        """Send a chunk to the agent and return the structured field responses."""
        message = self.prompt_service.get_user_message(
            fields=self.fields,
            chunk=chunk,
            actions=self.action_service.available_actions_description(),
        )
        print("prompt:", message)
        if dry_run:
            logger.info(f"Dry run - would process chunk with user prompt: {message}")
            return []

        result = self.agent.run_sync(message)

        logger.info(f"token usage: {result.usage()}")
        return result.output or []

    def handle_field_response(self, field_response: FieldResponse) -> None:
        """Dispatch a field response to the appropriate action handler."""
        self.action_service.dispatch(
            field_response=field_response,
            fields=self.fields,
        )

    def identify_schema(self, content: str) -> str | None:
        """Identify the schema that best matches the provided content."""
        if not self.schemas:
            return None

        agent = Agent(
            system_prompt=self.prompt_service.schema_identification_system_prompt,
            model=self.model,
            output_type=str,
        )

        message = self.prompt_service.get_schema_identification_message(
            schemas=self.schemas,
            content=content,
        )

        try:
            result = agent.run_sync(message)
            schema_name: str | None = result.output
            if schema_name == "None" or schema_name not in [
                s.name for s in self.schemas
            ]:
                return None
            return schema_name
        except Exception:
            logger.exception("Failed to identify schema")
            return None

    def extract_fields(
        self, documents: list[DocumentInput] | None = None, dry_run: bool = False
    ) -> ExtractedSchema | BatchExtractionResult:
        """Extract fields from the provided content or batch of documents."""
        if documents is not None:
            results: list[DocumentResult] = []
            for doc in documents:
                if doc.infer_schema:
                    logger.info(f"Inferring schema for {doc.file_path}")
                    # Temporary extractor to get content. efficiency could be improved
                    # by separating content loading from extractor creation, but reusing logic for now.
                    # We don't know the schema yet, but we need content.
                    temp_extractor = Extractor.from_file(
                        input_file_path=doc.file_path,
                        use_ocr=doc.use_ocr,
                        ocr_filename=doc.ocr_filename,
                        ocr_is_image=doc.ocr_is_image,
                        model=self.model,
                        max_chunk_size=self.max_chunk_size,
                        identify_fields=False,  # Just loading content
                    )
                    # Use first chunk or reasonable amount of text for identification
                    # limit to first 2000 chars to save tokens? lets pass first chunk
                    chunks = chunk_markdown(
                        temp_extractor.content or "", max_chars=self.max_chunk_size
                    )
                    sample_content = chunks[0] if chunks else ""

                    identified_name = self.identify_schema(sample_content)
                    if identified_name:
                        schema = next(
                            (s for s in self.schemas if s.name == identified_name),
                            None,
                        )
                        logger.info(
                            f"Identified schema {identified_name} for {doc.file_path}"
                        )
                        # Update doc with identified schema for result reporting
                        doc.schema_name = identified_name
                    else:
                        schema = None

                elif doc.schema_name:
                    schema = next(
                        (s for s in self.schemas if s.name == doc.schema_name), None
                    )
                else:
                    results.append(
                        DocumentResult(
                            document_id=str(doc.file_path),
                            schema_name="Unknown",
                            error="Schema name not provided and infer_schema is False.",
                        )
                    )
                    continue

                if not schema:
                    results.append(
                        DocumentResult(
                            document_id=str(doc.file_path),
                            schema_name=doc.schema_name or "Unknown",
                            error=f"Schema '{doc.schema_name}' not found provided schemas.",
                        )
                    )
                    continue

                try:
                    # Create child extractor for this document
                    extractor = Extractor.from_file(
                        input_file_path=doc.file_path,
                        use_ocr=doc.use_ocr,
                        ocr_filename=doc.ocr_filename,
                        ocr_is_image=doc.ocr_is_image,
                        model=self.model,
                        max_chunk_size=self.max_chunk_size,
                        schema=schema,
                        identify_fields=self.identify_fields,
                        actions=self.action_service.actions,  # Pass along actions if any?
                    )
                    extracted = extractor.extract_fields(dry_run=dry_run)
                    if isinstance(extracted, ExtractedSchema):
                        results.append(
                            DocumentResult(
                                document_id=str(doc.file_path),
                                schema_name=doc.schema_name
                                or (schema.name if schema else "Unknown"),
                                extracted_schema=extracted,
                            )
                        )
                    else:
                        logger.error(
                            f"Unexpected return type from extract_fields for {doc.file_path}"
                        )

                except Exception as e:
                    logger.exception(f"Failed to process document {doc.file_path}")
                    results.append(
                        DocumentResult(
                            document_id=str(doc.file_path),
                            schema_name=doc.schema_name
                            or (schema.name if schema else "Unknown"),
                            error=str(e),
                        )
                    )

            return BatchExtractionResult(results=results)

        if self.content is None:
            raise ValueError("No content provided for extraction.")

        chunks = chunk_markdown(self.content, max_chars=self.max_chunk_size)
        chunk_count = len(chunks)
        logger.info(f"Identifying fields for {chunk_count} chunks of text")

        for i, chunk in enumerate(chunks):
            logger.info(
                f"identifying fields for text chunk {i + 1}/{chunk_count} with length {len(chunk)}"
            )
            field_responses = self.process_chunk(chunk, dry_run)
            if not field_responses:
                logger.info("No fields identified for chunk %s", i + 1)
                continue
            logger.info(f"Found {len(field_responses)} fields for chunk {i + 1}")
            for field_response in field_responses:
                self.handle_field_response(field_response)
        return self.fields.build_extracted_schema()
