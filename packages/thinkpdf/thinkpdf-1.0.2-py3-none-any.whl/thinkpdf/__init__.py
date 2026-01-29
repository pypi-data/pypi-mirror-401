"""thinkpdf - PDF to Markdown converter."""

__version__ = "1.0.2"
__author__ = "thinkpdf Team"

from .engine import convert
from .core.extractor import PDFExtractor
from .core.converter import PDFConverter

__all__ = [
    "convert",
    "PDFExtractor",
    "PDFConverter",
    "__version__",
]
