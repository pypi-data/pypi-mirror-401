import importlib.metadata

from dotenv import load_dotenv

from .actions.schemas import Action
from .extractor import Extractor
from .ocr import OCR
from .schemas import DefaultActionsT, FieldResponse, Table

try:
    __version__ = importlib.metadata.version("extract")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

_ = load_dotenv()


__all__ = [
    "OCR",
    "Extractor",
    "Action",
    "FieldResponse",
    "Table",
    "DefaultActionsT",
    "__version__",
]
