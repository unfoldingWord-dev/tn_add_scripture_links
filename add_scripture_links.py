import re
import csv
import difflib
import sys
import glob
import os
import argparse

def extract_chapter_verse_pairs(reference_string, starting_chapter=None):
    results = []
    current_chapter = starting_chapter
    split_refs = [ref.strip() for ref in reference_string.split(';')]
    for ref in split_refs:
        parts = [r.strip() for r in ref.split(',')]
        for part in parts:
            if ':' in part:
                chapter, verse = part.split(':', 1)
                chapter = chapter.strip()
                verse = verse.strip()
                if chapter and verse:
                    current_chapter = chapter
                    results.append((current_chapter, verse))
            elif current_chapter and part:
                results.append((current_chapter, part))
    return results

def get_diff_excerpt(a, b):
    sm = difflib.SequenceMatcher(None, a, b)
    diffs_orig = []
    diffs_repl = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            diffs_orig.append(a[i1:i2])
            diffs_repl.append(b[j1:j2])
    return ("".join(diffs_orig), "".join(diffs_repl))



def add_verse_codes_to_column(rows, book_code):
    usfm_book_codes = {
        "Genesis": "GEN", "Gen": "GEN", "Exodus": "EXO", "Exo": "EXO", "Leviticus": "LEV", "Lev": "LEV", "Numbers": "NUM", "Num": "NUM",
        "Deuteronomy": "DEU", "Deut": "DEU", "Joshua": "JOS", "Josh": "JOS", "Judges": "JDG", "Judg": "JDG", "Ruth": "RUT",
        "1 Samuel": "1SA", "1 Sam": "1SA", "2 Samuel": "2SA", "2 Sam": "2SA", "1 Kings": "1KI", "1 Kgs": "1KI", "2 Kings": "2KI", "2 Kgs": "2KI",
        "1 Chronicles": "1CH", "1 Chr": "1CH", "2 Chronicles": "2CH", "2 Chr": "2CH", "Ezra": "EZR", "Nehemiah": "NEH", "Neh": "NEH",
        "Esther": "EST", "Job": "JOB", "Psalms": "PSA", "Psalm": "PSA", "Psa": "PSA", "Proverbs": "PRO", "Prov": "PRO",
        "Ecclesiastes": "ECC", "Eccl": "ECC", "Song of Songs": "SNG", "Song": "SNG", "Isaiah": "ISA", "Isa": "ISA",
        "Jeremiah": "JER", "Jer": "JER", "Lamentations": "LAM", "Lam": "LAM", "Ezekiel": "EZK", "Ezek": "EZK", "Daniel": "DAN", "Dan": "DAN",
        "Hosea": "HOS", "Joel": "JOL", "Amos": "AMO", "Obadiah": "OBA", "Obad": "OBA",
        "Jonah": "JON", "Micah": "MIC", "Nahum": "NAM", "Habakkuk": "HAB", "Hab": "HAB",
        "Zephaniah": "ZEP", "Zeph": "ZEP", "Haggai": "HAG", "Hag": "HAG", "Zechariah": "ZEC", "Zech": "ZEC", "Malachi": "MAL", "Mal": "MAL",
        "Matthew": "MAT", "Matt": "MAT", "Mat": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN",
        "Acts": "ACT", "Act": "ACT", "Romans": "ROM", "Rom": "ROM", "1 Corinthians": "1CO", "1 Cor": "1CO", "2 Corinthians": "2CO", "2 Cor": "2CO",
        "Galatians": "GAL", "Gal": "GAL", "Ephesians": "EPH", "Eph": "EPH", "Philippians": "PHP", "Phil": "PHP", "Colossians": "COL", "Col": "COL",
        "1 Thessalonians": "1TH", "1 Thess": "1TH", "2 Thessalonians": "2TH", "2 Thess": "2TH", "1 Timothy": "1TI", "1 Tim": "1TI",
        "2 Timothy": "2TI", "2 Tim": "2TI", "Titus": "TIT", "Philemon": "PHM", "Phlm": "PHM", "Hebrews": "HEB", "Heb": "HEB",
        "James": "JAS", "Jas": "JAS", "1 Peter": "1PE", "1 Pet": "1PE", "2 Peter": "2PE", "2 Pet": "2PE", "1 John": "1JN", "1 Jn": "1JN",
        "2 John": "2JN", "2 Jn": "2JN", "3 John": "3JN", "3 Jn": "3JN", "Jude": "JUD", "Revelation": "REV", "Rev": "REV"
    }
    
    # Books with only one chapter
    single_chapter_books = {"OBA", "PHM", "2JN", "3JN", "JUD"}

    processed = []
    changes = []  # To store (ID, original_text, replaced_text)

    for i, row in enumerate(rows):
        # Skip header row
        if i == 0:
            processed.append(row)
            continue
            
        original = row[6] if len(row) > 6 else (row[5] if len(row) > 5 else "")
        updated = original

        # Parse current context from reference column (column 0)
        current_book = book_code
        current_chapter = None
        current_verse = None
        
        if len(row) > 0 and row[0]:
            reference = row[0].strip()
            if ':' in reference:
                # Format like "118:12" or "front:intro"
                current_chapter, current_verse = reference.split(':', 1)
                current_chapter = current_chapter.strip()
                current_verse = current_verse.strip()
            else:
                # Just chapter or special reference
                current_chapter = reference

        if original:
            # Find all Bible references in the text
            # Pattern 1: Book name followed by chapter/verse (e.g., "Gen 1:1", "Psalms 2, 8, 16")
            book_refs = re.finditer(r'\b((?:[1-3] )?(?:Genesis|Gen|Exodus|Exo|Leviticus|Lev|Numbers|Num|Deuteronomy|Deut|Joshua|Josh|Judges|Judg|Ruth|1 Samuel|1 Sam|2 Samuel|2 Sam|1 Kings|1 Kgs|2 Kings|2 Kgs|1 Chronicles|1 Chr|2 Chronicles|2 Chr|Ezra|Nehemiah|Neh|Esther|Job|Psalms|Psalm|Psa|Proverbs|Prov|Ecclesiastes|Eccl|Song of Songs|Song|Isaiah|Isa|Jeremiah|Jer|Lamentations|Lam|Ezekiel|Ezek|Daniel|Dan|Hosea|Joel|Amos|Obadiah|Obad|Jonah|Micah|Nahum|Habakkuk|Hab|Zephaniah|Zeph|Haggai|Hag|Zechariah|Zech|Malachi|Mal|Matthew|Matt|Mat|Mark|Luke|John|Acts|Act|Romans|Rom|1 Corinthians|1 Cor|2 Corinthians|2 Cor|Galatians|Gal|Ephesians|Eph|Philippians|Phil|Colossians|Col|1 Thessalonians|1 Thess|2 Thessalonians|2 Thess|1 Timothy|1 Tim|2 Timothy|2 Tim|Titus|Philemon|Phlm|Hebrews|Heb|James|Jas|1 Peter|1 Pet|2 Peter|2 Pet|1 John|1 Jn|2 John|2 Jn|3 John|3 Jn|Jude|Revelation|Rev))\s+(\d+(?::\d+(?:[-–]\d+)?)?(?:[,;]\s*\d+(?::\d+(?:[-–]\d+)?)?)*)', original)
            
            # Pattern 2: Chapter/verse references (e.g., "chapter 5", "verses 12-15", "5:12", "1:1–6:7")
            chapter_verse_refs = re.finditer(r'\b(?:(chapters?)\s+(\d+(?:[-–]\d+)?(?:[,;]\s*(?:and\s+|or\s+)?\d+(?:[-–]\d+)?)*(?:\s+(?:and|or)\s+\d+(?:[-–]\d+)?)?)|(verses?)\s+(\d+(?:[-–]\d+)?(?:[,;]\s*(?:and\s+|or\s+)?\d+(?:[-–]\d+)?)*(?:\s+(?:and|or)\s+\d+(?:[-–]\d+)?)?)|(\d+):(\d+(?:[-–]\d+(?::\d+)?)?))\b', original)
            
            all_matches = []
            
            # Collect all matches with their types
            for match in book_refs:
                all_matches.append(('book', match))
            
            for match in chapter_verse_refs:
                all_matches.append(('ref', match))
            
            # Sort by position in text
            all_matches.sort(key=lambda x: x[1].start())
            
            # Filter out matches that are already inside markdown links
            def is_inside_markdown_link(text, start, end):
                """Check if a position range is inside an existing markdown link."""
                # Find all markdown links in the text
                link_pattern = r'\[([^\]]+)\]\([^)]+\)'
                for link_match in re.finditer(link_pattern, text):
                    link_start = link_match.start()
                    link_end = link_match.end()
                    # Check if our match is completely inside this link
                    if link_start <= start and end <= link_end:
                        return True
                return False
            
            filtered_matches = []
            
            # Process book references first (higher priority)
            book_matches = [(match_type, match) for match_type, match in all_matches if match_type == 'book']
            ref_matches = [(match_type, match) for match_type, match in all_matches if match_type == 'ref']
            
            # First pass: add all book references (they have priority)
            for match_type, match in book_matches:
                start_idx = match.start()
                end_idx = match.end()
                
                # Skip if inside existing markdown link
                if is_inside_markdown_link(original, start_idx, end_idx):
                    continue
                    
                filtered_matches.append((match_type, match))
            
            # Second pass: add ref matches that don't conflict with book matches
            for match_type, match in ref_matches:
                start_idx = match.start()
                end_idx = match.end()
                
                # Skip if inside existing markdown link
                if is_inside_markdown_link(original, start_idx, end_idx):
                    continue
                
                # Skip if this overlaps with any book match
                conflicts = False
                for _, book_match in book_matches:
                    book_start = book_match.start()
                    book_end = book_match.end()
                    # Check if there's any overlap
                    if not (end_idx <= book_start or start_idx >= book_end):
                        conflicts = True
                        break
                
                if not conflicts:
                    filtered_matches.append((match_type, match))
            
            # Sort all filtered matches by position for processing in reverse order
            filtered_matches.sort(key=lambda x: x[1].start())
            
            replacements = []
            changes_local = []

            for match_type, match in reversed(filtered_matches):
                start, end = match.start(), match.end()
                original_text = match.group(0)
                
                if match_type == 'book':
                    # Handle book references (e.g., "Gen 1:1", "Psalms 2, 8, 16")
                    book_name = match.group(1).strip()
                    references = match.group(2).strip()
                    
                    # Get the book code for this reference
                    ref_book_code = None
                    for name, code in usfm_book_codes.items():
                        if book_name.lower() == name.lower():
                            ref_book_code = code
                            break
                    
                    if ref_book_code:
                        new_text = process_book_reference(original_text, book_name, references, ref_book_code, current_book, current_chapter, current_verse, single_chapter_books)
                    else:
                        new_text = original_text  # Keep original if book not found
                
                elif match_type == 'ref':
                    # Handle chapter/verse references without book name
                    if match.group(1):  # chapters
                        new_text = process_chapter_reference(original_text, match.group(1), match.group(2), current_book, current_chapter, current_verse, single_chapter_books)
                    elif match.group(3):  # verses
                        new_text = process_verse_reference(original_text, match.group(3), match.group(4), current_book, current_chapter, current_verse, single_chapter_books)
                    elif match.group(5) and match.group(6):  # chapter:verse
                        new_text = process_chapter_verse_reference(original_text, match.group(5), match.group(6), current_book, current_chapter, current_verse, single_chapter_books)
                    else:
                        new_text = original_text
                
                # Only add replacement if text changed
                if new_text != original_text:
                    changes_local.append((original_text, new_text))
                    replacements.append((start, end, new_text))

            # Apply replacements by offset (from end to start to avoid shifting)
            for start, end, replacement in sorted(replacements, reverse=True):
                updated = updated[:start] + replacement + updated[end:]

            # Only record changes if text actually changed
            if updated != original:
                for orig_text, new_text in changes_local:
                    changes.append((row[0] if len(row) > 0 else '', row[1] if len(row) > 1 else '', orig_text, new_text))

            if len(row) > 6:
                row[6] = updated
            elif len(row) > 5:
                row[5] = updated

        processed.append(row)

    return processed, changes


def process_book_reference(original_text, book_name, references, ref_book_code, current_book, current_chapter, current_verse, single_chapter_books):
    """Process a reference like 'Gen 1:1' or 'Psalms 2, 8, 16' or 'Jude 20'"""
    # Parse individual references
    ref_parts = parse_reference_list(references)
    
    links = []
    for i, ref in enumerate(ref_parts):
        if ':' in ref:
            # Chapter:verse format (e.g., "Jude 1:20" or "Gen 1:1")
            chap, verse_range = ref.split(':', 1)
            chap = chap.strip()
            verse = verse_range.split('–')[0].split('-')[0]  # Get first verse if range
        else:
            # Just a number - could be chapter or verse depending on the book
            if ref_book_code in single_chapter_books:
                # For single-chapter books, assume it's a verse reference
                chap = '1'
                verse = ref.split('–')[0].split('-')[0]  # Get first verse if range
            else:
                # For multi-chapter books, assume it's a chapter reference
                chap = ref.split('–')[0].split('-')[0]  # Get first chapter if range
                verse = '1'
        
        # Skip if this is the same book and same chapter (no verse specified) for multi-chapter books
        if ref_book_code == current_book and chap == current_chapter and ':' not in ref and ref_book_code not in single_chapter_books:
            continue
        
        # Skip if this is the exact same reference for single-chapter books
        if ref_book_code == current_book and ref_book_code in single_chapter_books and verse == current_verse and ':' not in ref:
            continue
        
        # Create the link
        target = create_target_path(ref_book_code, chap, verse, current_book)
        
        if i == 0:
            # First reference includes book name
            display_text = f"{book_name} {ref}"
        else:
            # Subsequent references
            display_text = ref
        
        links.append(f"[{display_text}]({target})")
    
    if links:
        if len(links) == 1:
            return links[0]
        else:
            # Join multiple links with commas and "and"
            if len(links) == 2:
                return f"{links[0]} and {links[1]}"
            else:
                return ", ".join(links[:-1]) + f", and {links[-1]}"
    
    return original_text


def process_chapter_reference(original_text, chapter_word, references, current_book, current_chapter, current_verse, single_chapter_books):
    """Process references like 'chapter 5', 'chapters 2, 8, 16', or 'chapters 8-10'"""
    ref_parts = parse_reference_list(references)
    
    links = []
    for i, ref in enumerate(ref_parts):
        # Check if this is a range like "8-10"
        if '-' in ref or '–' in ref:
            # For ranges, link the entire range to the first chapter
            chap = ref.split('–')[0].split('-')[0]  # Get first chapter of range
            
            # For ranges, always create link (don't skip based on current chapter)
            
            target = create_target_path(current_book, chap, '1', current_book)
            
            if i == 0:
                display_text = f"{chapter_word} {ref}"
            else:
                display_text = ref
            
            # Link the entire range text to the first chapter
            links.append(f"[{display_text}]({target})")
        else:
            # Single chapter reference
            chap = ref
            
            # Skip if this is the same chapter
            if chap == current_chapter:
                continue
            
            target = create_target_path(current_book, chap, '1', current_book)
            
            if i == 0:
                display_text = f"{chapter_word} {ref}"
            else:
                display_text = ref
            
            links.append(f"[{display_text}]({target})")
    
    if links:
        if len(links) == 1:
            return links[0]
        else:
            if len(links) == 2:
                return f"{links[0]} and {links[1]}"
            else:
                return ", ".join(links[:-1]) + f", and {links[-1]}"
    
    return original_text


def process_verse_reference(original_text, verse_word, references, current_book, current_chapter, current_verse, single_chapter_books):
    """Process references like 'verse 12' or 'verses 5-7, 12'"""
    ref_parts = parse_reference_list(references)
    
    links = []
    for i, ref in enumerate(ref_parts):
        verse = ref.split('–')[0].split('-')[0]  # Get first verse if range
        
        # Create target for same chapter, different verse
        target = create_target_path(current_book, current_chapter or '1', verse, current_book)
        
        if i == 0:
            display_text = f"{verse_word} {ref}"
        else:
            display_text = ref
        
        links.append(f"[{display_text}]({target})")
    
    if links:
        if len(links) == 1:
            return links[0]
        else:
            if len(links) == 2:
                return f"{links[0]} and {links[1]}"
            else:
                return ", ".join(links[:-1]) + f", and {links[-1]}"
    
    return original_text


def process_chapter_verse_reference(original_text, chapter, verse_range, current_book, current_chapter, current_verse, single_chapter_books):
    """Process references like '5:12' or cross-chapter ranges like '1:1–6:7'"""
    
    # Check if this is a cross-chapter range (contains ':' in the range part)
    if ':' in verse_range:
        # This is a cross-chapter range like "1–6:7"
        # Just link the entire range to the first chapter
        target = create_target_path(current_book, chapter, '1', current_book)
        return f"[{original_text}]({target})"
    else:
        # Regular verse range within same chapter
        verse = verse_range.split('–')[0].split('-')[0]  # Get first verse if range
        
        # Skip if this is the exact same reference
        if chapter == current_chapter and verse == current_verse:
            return original_text
        
        if chapter == current_chapter:
            # Same chapter, different verse - link to ./verse.md
            target = create_target_path(current_book, chapter, verse, current_book)
        else:
            # Different chapter - link to ../chapter/verse.md
            target = create_target_path(current_book, chapter, verse, current_book)
        
        return f"[{original_text}]({target})"


def parse_reference_list(references):
    """Parse a list of references like '2, 8, 16' or '1:5, 2:3-7, and 5:12'"""
    # Split on commas and semicolons
    parts = re.split(r'[,;]\s*', references)
    ref_parts = []
    
    for part in parts:
        part = part.strip()
        # Handle "and" or "or" at the beginning or end
        part = re.sub(r'^(?:and\s+|or\s+)', '', part)
        
        # Check if this part has "and X" or "or X" at the end
        and_or_match = re.search(r'(.+?)\s+(?:and|or)\s+(.+)$', part)
        if and_or_match:
            ref_parts.append(and_or_match.group(1).strip())
            ref_parts.append(and_or_match.group(2).strip())
        elif part:
            ref_parts.append(part)
    
    return [ref for ref in ref_parts if ref]


def create_target_path(target_book, chapter, verse, current_book):
    """Create the appropriate target path based on context"""
    # Handle Psalms special formatting (3 digits) vs normal formatting (2 digits)
    if target_book == 'PSA':
        chap_padded = chapter.zfill(3)
        verse_padded = verse.zfill(3)
    else:
        chap_padded = chapter.zfill(2)
        verse_padded = verse.zfill(2)
    
    if target_book == current_book:
        # Same book
        return f"../{chap_padded}/{verse_padded}.md"
    else:
        # Different book
        return f"../../{target_book.lower()}/{chap_padded}/{verse_padded}.md"



def process_file(input_file, inplace=False):
    """Process a single TSV file and return the book code."""
    # Extract book code from filename (e.g., "tn_GEN.tsv" -> "GEN")
    basename = os.path.basename(input_file)
    if basename.startswith('tn_') and basename.endswith('.tsv'):
        book_code = basename[3:-4]  # Remove 'tn_' prefix and '.tsv' suffix
    else:
        # Fallback: use the base filename without extension
        book_code = os.path.splitext(basename)[0]
    
    print(f"Processing {input_file} (book: {book_code})")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        rows = list(reader)

    processed, changes = add_verse_codes_to_column(rows, book_code)
    input_base, input_ext = os.path.splitext(input_file)

    if inplace:
        # Overwrite the original file
        output_file = input_file
    else:
        # Write to converted file instead of overwriting
        # Create output filename by inserting "_converted" before the extension
        output_file = f"{input_base}_converted{input_ext}"

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, row in enumerate(processed):
            f.write('\t'.join(row))
            f.write('\n')

    # Write changes to a diff file
    changes_file = f"{input_base}_diff{input_ext}"
    with open(changes_file, 'w', encoding='utf-8') as f:
        f.write('\t'.join(["Reference", "ID", "Original", "Replaced"]) + '\n')
        for row in changes:
            f.write('\t'.join(row) + '\n')
    
    print(f"  Converted file: {output_file}")
    print(f"  Changes logged: {changes_file}")
    print(f"  Total changes: {len(changes)}")
    return book_code


def main():
    # Handle command line arguments
    parser = argparse.ArgumentParser(description='Process TSV files to add verse links')
    parser.add_argument('-i', '--inplace', action='store_true', 
                       help='Modify files in place instead of creating _converted versions')
    parser.add_argument('files', nargs='*', 
                       help='Files or directories to process. If a directory, all tn_???.tsv files will be processed. Can be a reatlive path.')
    args = parser.parse_args()
    
    inplace = args.inplace
    if len(sys.argv) > 1:
        # Use provided file(s) as arguments
        input_files = []
        for arg in sys.argv[1:]:
            if os.path.isdir(arg):
                # If it's a directory, find all tn_???.tsv files in it
                pattern = os.path.join(arg, 'tn_???.tsv')
                input_files.extend(sorted(glob.glob(pattern)))
            elif os.path.isfile(arg):
               # If it's a file, add it directly
                input_files.append(arg)
            else:
                print(f"Warning: {arg} is not a valid file or directory")
    else:
        # Find all .tsv files in current directory
        input_files = sorted(glob.glob('tn_???.tsv'))
        if not input_files:
            print("No .tsv files found in current directory")
            return
    
    print(f"Found {len(input_files)} file(s) to process")
    
    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"Warning: File {input_file} does not exist, skipping")
            continue
        
        try:
            process_file(input_file, inplace)
        except Exception as e:
            print(f"Error processing {input_file}: {e}")
            continue


if __name__ == "__main__":
    main()
