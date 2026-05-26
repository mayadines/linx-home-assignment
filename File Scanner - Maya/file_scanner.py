import os
import re
import sys

from readers import READERS


def run_scan() -> None:
    folder_path, sensitive_word = prompt_scan_inputs()
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        sys.exit(1)
    scan_folder(folder_path, sensitive_word)


def prompt_scan_inputs() -> tuple[str, str]:
    folder_path = input("Enter folder path to scan: ").strip()
    sensitive_word = ""
    while not sensitive_word:
        sensitive_word = input("Enter sensitive word to search for: ").strip()
        if not sensitive_word:
            print("Sensitive word cannot be empty. Please try again.")
    return folder_path, sensitive_word


def scan_folder(folder_path: str, sensitive_word: str) -> None:
    # \w covers letters/digits/underscore; also exclude apostrophe to reject "word's"
    pattern = re.compile(
        r"(?<!\w)" + re.escape(sensitive_word) + r"(?![\w'])",
        re.IGNORECASE,
    )
    sensitive_word_lower = sensitive_word.lower()
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            scan_file(os.path.join(dirpath, filename), pattern, sensitive_word_lower)


def scan_file(file_path: str, pattern: re.Pattern, sensitive_word_lower: str) -> None:
    _, ext = os.path.splitext(file_path)
    reader = READERS.get(ext.lower())
    if reader is None:
        return

    try:
        for line in reader(file_path):
            if sensitive_word_lower in line.lower() and pattern.search(line):
                print(file_path)
                return
    except Exception as e:
        print(f"Warning: could not read '{file_path}': {e}")
