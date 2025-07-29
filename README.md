# Translation Notes Scripture Links Tool

This Python script automatically adds markdown links to scripture references found in translationNotes (TN) TSV files. It converts plain text Bible references into clickable markdown links that follow the unfoldingWord file structure conventions.

## Features

- **Automatic Scripture Reference Detection**: Identifies various formats of Bible references including:

  - Book names with chapters/verses (e.g., "Gen 1:1", "Psalms 2, 8, 16")
  - Chapter references (e.g., "chapter 5", "chapters 2-8")
  - Verse references (e.g., "verse 12", "verses 5-7")
  - Chapter:verse notation (e.g., "5:12", "1:1–6:7")

- **Smart Link Generation**: Creates appropriate relative paths based on:

  - Current book context
  - Target book (same or different)
  - Chapter and verse formatting (Psalms uses 3-digit padding, others use 2-digit)

- **Batch Processing**: Can process single files, directories, or multiple files at once

- **Change Tracking**: Generates diff files showing exactly what changes were made

- **Flexible Output**: Option to modify files in-place or create new converted versions

## Installation

This script requires Python 3.6+ with the following standard library modules:

- `re` (regular expressions)
- `csv` (CSV file handling)
- `difflib` (text difference calculations)
- `sys` (system functions)
- `glob` (file pattern matching)
- `os` (operating system interface)
- `argparse` (command line argument parsing)

No additional dependencies are required.

## Usage

### Basic Usage

Process all TN TSV files in the current directory:

```bash
python add_scripture_links.py
```

### Process Specific Files

Process a single file:

```bash
python add_scripture_links.py tn_GEN.tsv
```

Process multiple files:

```bash
python add_scripture_links.py tn_GEN.tsv tn_EXO.tsv tn_LEV.tsv
```

### Process Directory

Process all TN TSV files in a specific directory:

```bash
python add_scripture_links.py /path/to/tn/files/
```

### In-place Modification

Modify files directly instead of creating `_converted` versions:

```bash
python add_scripture_links.py -i tn_GEN.tsv
```

### Command Line Options

```
usage: add_scripture_links.py [-h] [-i] [files ...]

Process TSV files to add verse links

positional arguments:
  files          Files or directories to process. If a directory, all tn_???.tsv files will be processed. Can be a relative path.

options:
  -h, --help     show this help message and exit
  -i, --inplace  Modify files in place instead of creating _converted versions
```

## How It Works

### Input File Format

The script expects TSV (Tab-Separated Values) files with the translationNotes format where:

- Column 0: Reference (e.g., "1:1", "2:5")
- Column 5 or 6: Note text containing scripture references

### Reference Detection

The script uses sophisticated regular expressions to detect:

1. **Book References**: Full book names followed by chapter/verse

   - Examples: "Genesis 1:1", "1 Samuel 2:3", "Psalms 23, 27, 46"

2. **Chapter References**: References to chapters without book names

   - Examples: "chapter 5", "chapters 2-8", "chapters 1, 3, and 5"

3. **Verse References**: References to verses within the current chapter

   - Examples: "verse 12", "verses 5-7", "verses 1, 3, and 8"

4. **Chapter:Verse Notation**: Direct chapter:verse references
   - Examples: "5:12", "1:1–6:7"

### Link Generation

The script generates markdown links with appropriate relative paths:

- **Same book, different chapter**: `../[chapter]/[verse].md`
- **Different book**: `../../[book]/[chapter]/[verse].md`
- **Psalms**: Uses 3-digit padding (e.g., `../001/001.md`)
- **Other books**: Uses 2-digit padding (e.g., `../01/01.md`)

### Special Handling

- **Single-chapter books** (Obadiah, Philemon, 2 John, 3 John, Jude): Treats numeric references as verses
- **Existing markdown links**: Skips references already inside markdown links
- **Context awareness**: Avoids creating links to the current verse/chapter
- **Range handling**: Links ranges to the first chapter/verse in the range

### Output Files

For each processed file, the script generates:

1. **Converted file** (unless using `-i` flag): `tn_[BOOK]_converted.tsv`
2. **Diff file**: `tn_[BOOK]_diff.tsv` showing all changes made

### Book Code Mapping

The script includes a comprehensive mapping of book names to USFM codes:

- Old Testament: Genesis (GEN), Exodus (EXO), Leviticus (LEV), etc.
- New Testament: Matthew (MAT), Mark (MRK), Luke (LUK), etc.
- Supports both full names and common abbreviations

## Examples

### Input Text

```
See Genesis 1:1 and chapter 2 for more context. Also refer to verses 5-7.
```

### Output Text

```
See [Genesis 1:1](../../gen/01/01.md) and [chapter 2](../02/01.md) for more context. Also refer to [verses 5-7](./05.md).
```

## File Structure

```
tn_add_scripture_links/
├── add_scripture_links.py    # Main script
├── test_script.py            # Test validation script
├── README.md                 # This documentation
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies (empty - uses stdlib only)
├── test_cases/              # Test files and validation
│   ├── README.md           # Test documentation
│   ├── tn_PSA.tsv          # Psalms test file
│   ├── tn_MAT.tsv          # Matthew test file
│   ├── tn_JUD.tsv          # Jude test file
│   └── tn_*_expected*.tsv  # Expected output files
└── examples/               # Example TN TSV files (optional)
```

## Testing

The project includes a comprehensive test suite to validate functionality:

```bash
# Run all tests
python3 test_script.py

# Create sample test files (for development)
python3 test_script.py --create-samples
```

The test suite validates:

- Scripture reference detection accuracy
- Proper markdown link generation
- Correct relative path creation
- Handling of various reference formats
- Special cases (Psalms formatting, single-chapter books, etc.)

See `test_cases/README.md` for detailed testing documentation.

## Error Handling

The script includes robust error handling:

- Skips non-existent files with warnings
- Continues processing other files if one fails
- Logs errors without stopping the entire batch

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample TN files
5. Submit a pull request

## License

This project is open source. Please check the repository for license information.

## Support

For issues or questions, please create an issue in the repository or contact the development team.
