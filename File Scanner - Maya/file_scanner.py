import os
import re
from readers import READERS

def run_scan() -> None:
    folder_path, sensitive_word = prompt_scan_inputs()
    scan_folder(folder_path, sensitive_word)

def prompt_scan_inputs() -> tuple[str, str]:
    folder_path = input("Enter folder path to scan: ").strip()
    sensitive_word = input("Enter sensitive word to search for: ").strip()
    return folder_path, sensitive_word

def scan_folder(folder_path: str, sensitive_word: str) -> None:
    for entry in os.scandir(folder_path):
        if entry.is_file():
            scan_file(entry.path, sensitive_word)
        elif entry.is_dir():
            scan_folder(entry.path, sensitive_word)

def scan_file(file_path: str, sensitive_word: str) -> None:
    _, ext = os.path.splitext(file_path)
    reader = READERS.get(ext.lower())
    if reader is None:
        return

    # \w covers letters/digits/underscore; also exclude apostrophe to reject "word's"
    pattern = re.compile(
        r"(?<!\w)" + re.escape(sensitive_word) + r"(?![\w'])",
        re.IGNORECASE,
    )

    for line in reader(file_path):
        if pattern.search(line):
            print(file_path)
            return