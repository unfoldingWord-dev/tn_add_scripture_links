# Examples

This directory contains example files to demonstrate the functionality of the Translation Notes Scripture Links Tool.

## Sample Files

### `tn_GEN_sample.tsv`

A small sample of Genesis translation notes with various types of scripture references:

- Direct book references (Genesis 1:1)
- Verse references (verses 3-5)
- Cross-references to other books (John 1:5)
- Chapter references (chapter 1)
- Range references (Genesis 1:1–2:3)
- Multiple references (Psalms 104 and 136)

## Running the Example

To test the tool with the sample file:

```bash
# From the project root directory
python add_scripture_links.py examples/tn_GEN_sample.tsv
```

This will create:

- `examples/tn_GEN_sample_converted.tsv` - The processed file with scripture links
- `tn_GEN_diff.tsv` - A diff file showing all the changes made

## Expected Output

The tool will convert references like:

- `Genesis 1:1` → `[Genesis 1:1](../../gen/01/01.md)`
- `verses 3-5` → `[verses 3-5](./03.md)`
- `John 1:5` → `[John 1:5](../../jhn/01/05.md)`
- `chapter 1` → `[chapter 1](../01/01.md)`
- And more...

The processed notes will have clickable markdown links that follow the unfoldingWord file structure conventions.
