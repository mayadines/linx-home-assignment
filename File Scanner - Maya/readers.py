from typing import Callable, Iterator
import pypdf
from docx import Document


def _read_text(file_path: str) -> Iterator[str]:
    with open(file_path, encoding="utf-8", errors="ignore") as f:
        yield from f


def _read_docx(file_path: str) -> Iterator[str]:
    for para in Document(file_path).paragraphs:
        yield para.text


def _read_pdf(file_path: str) -> Iterator[str]:
    for page in pypdf.PdfReader(file_path).pages:
        yield page.extract_text()


READERS: dict[str, Callable[[str], Iterator[str]]] = {
    ".txt": _read_text,
    ".json": _read_text,
    ".csv": _read_text,
    ".docx": _read_docx,
    ".pdf": _read_pdf,
}
