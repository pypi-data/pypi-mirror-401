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
from .schemas import ExtractedSchema, FieldResponse, Schema

logger = logging.getLogger(__name__)


class Extractor:
    def __init__(
        self,
        content: str,
        model: models.Model | str = DEFAULT_MODEL,
        max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
        schema: Schema | None = None,
        actions: list[Action] | None = None,
        identify_fields: bool = True,
    ) -> None:
        self.content: str = content
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

    def extract_fields(self, dry_run: bool = False) -> ExtractedSchema:
        """Extract fields from the provided content and return them as an ExtractedSchema."""
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
