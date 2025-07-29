# Test Cases for Translation Notes Scripture Links Tool

This directory contains test cases to validate the functionality of the Translation Notes Scripture Links Tool.

## Test Files

The test suite includes three test books:

### PSA (Psalms)

- `tn_PSA.tsv` - Input file with Psalms translation notes
- `tn_PSA_expected.tsv` - Expected output with scripture links
- `tn_PSA_expected_diff.tsv` - Expected diff file showing changes

### MAT (Matthew)

- `tn_MAT.tsv` - Input file with Matthew translation notes
- `tn_MAT_expected.tsv` - Expected output with scripture links
- `tn_MAT_expected_diff.tsv` - Expected diff file showing changes

### JUD (Jude)

- `tn_JUD.tsv` - Input file with Jude translation notes
- `tn_JUD_expected.tsv` - Expected output with scripture links
- `tn_JUD_expected_diff.tsv` - Expected diff file showing changes

## Test Content

The test files include various types of scripture references to validate:

### Reference Types Tested

- **Cross-book references**: References to other books (e.g., "Genesis 1:1", "2 Peter 3:3")
- **Chapter references**: References to chapters within the same book (e.g., "chapter 2", "chapters 2-8")
- **Verse references**: References to verses within the same chapter (e.g., "verses 2-4", "verse 3")
- **Mixed references**: Multiple references in one note (e.g., "Psalms 104 and 136")
- **Range references**: References spanning multiple chapters/verses (e.g., "Genesis 1:1–2:3")

### Special Cases Tested

- **Psalms formatting**: 3-digit padding for Psalms (e.g., `../001/001.md`)
- **Single-chapter books**: Jude references treated as verses (e.g., "verse 6")
- **Multi-book references**: References combining different books in one note
- **Context awareness**: Avoiding self-references to current chapter/verse

## Running Tests

From the project root directory, run:

```bash
python3 test_script.py
```

This will:

1. Check that all required test files exist
2. Run the add_scripture_links.py script on the test_cases directory
3. Compare the generated output files with the expected results
4. Report any differences found

## Expected Output

When all tests pass, you should see:

```
============================================================
Translation Notes Scripture Links Tool - Test Suite
============================================================

1. Checking test files...
✓ PASS: All required test files found

2. Running script on test cases...
✓ PASS: Script executed successfully

3. Comparing output files with expected results...

Testing PSA...
✓ PASS: PSA converted file: Files match perfectly
✓ PASS: PSA diff file: Files match perfectly

Testing MAT...
✓ PASS: MAT converted file: Files match perfectly
✓ PASS: MAT diff file: Files match perfectly

Testing JUD...
✓ PASS: JUD converted file: Files match perfectly
✓ PASS: JUD diff file: Files match perfectly

============================================================

Test Results: 8/8 passed
============================================================
```

## Creating New Test Cases

To add new test cases:

1. Create a new `tn_BOOK.tsv` file in this directory with the book code (e.g., `tn_GEN.tsv`)
2. Add the book code to the `TEST_BOOKS` list in `test_script.py`
3. Run the script manually on your test file to generate the output
4. Copy the `_converted.tsv` file to `_expected.tsv`
5. Copy the `_diff.tsv` file to `_expected_diff.tsv`
6. Run the test script to validate

## Test File Format

Test input files should follow the standard TN TSV format:

```
Reference	ID	Tags	SupportReference	Quote	Occurrence	Note
1:1	abc1		rc://*/ta/man/translate/translate-names	word	1	Note text with scripture references.
```

The scripture references should be in the "Note" column (column 6, or column 5 if there are only 6 columns total).

## Troubleshooting

If tests fail:

1. **Missing files**: Ensure all `tn_BOOK.tsv`, `tn_BOOK_expected.tsv`, and `tn_BOOK_expected_diff.tsv` files exist
2. **Content differences**: Check the detailed diff output to see what changed
3. **Script errors**: Check that the main script runs without errors on the test files

The test script provides detailed output showing exactly what differences were found when tests fail.
