# File Scanner

Scans a file or folder tree for a sensitive word and reports every file that contains it.

## Setup

```bash
pip install -r requirements.txt
```

Python 3.10+ is required.

## Running

```bash
python main.py
```

The program will prompt for two inputs:

| Prompt | What to enter |
|---|---|
| `Enter file or folder path to scan:` | Absolute or relative path to a single file **or** a directory. If a directory is given, all supported files inside it are scanned recursively. |
| `Enter sensitive word to search for:` | The word to look for. Cannot be empty. |

### Example session

```
Enter file or folder path to scan: root_folder
Enter sensitive word to search for: goat
```

## Supported file types

| Extension | Reader |
|---|---|
| `.txt` | Plain-text line reader |
| `.json` | Plain-text line reader |
| `.csv` | Plain-text line reader |
| `.docx` | `python-docx` - reads paragraphs and table cells |
| `.pdf` | `pypdf` - reads extracted text per page |

Files with any other extension are silently skipped.

## Matching rules

- **Case-insensitive** - `Secret`, `SECRET`, and `secret` all match.
- **Whole-word only** - the word must not be bordered by a letter, digit, underscore, or apostrophe. For example, searching for `secret` will not flag `secrets` or `top-secret's`.

## Key architectural decisions

### Lazy, streaming reads (`Iterator[str]`)
Each reader is a generator that yields one line/paragraph/page at a time. The scanner stops and reports the file as soon as the first match is found, without reading the rest. This keeps memory usage constant regardless of file size.

### Reader registry (`READERS` dict)
Format support is centralised in a single `dict[str, Callable]` in [readers.py](readers.py). Adding a new format means adding one entry to that dict and one small reader function - no changes are needed anywhere else in the codebase.

### Two-stage matching (substring pre-filter + regex)
A fast `in` substring check runs first; the compiled regex (`re.Pattern`) is only applied when the substring check passes. This avoids regex overhead on lines that clearly cannot match.

### Recursive traversal with `os.walk`
`scan_folder` uses `os.walk`, which traverses the entire directory tree depth-first without loading the full structure into memory. It yields `(dirpath, subdirs, filenames)` tuples one directory at a time, so deeply nested trees (like `folder4/my_folder44/1/2/3/4/5/6/7/8/`) are handled with no extra code and no recursion limit concerns.
