#!/usr/bin/env python3
"""
Test script for the Translation Notes Scripture Links Tool.

This script runs the add_scripture_links.py tool on test cases and compares
the output with expected results for validation.
"""

import os
import sys
import subprocess
import csv
import difflib
from pathlib import Path

# Test configuration
TEST_BOOKS = ['PSA', 'MAT', 'JUD']
TEST_DIR = 'test_cases'
SCRIPT_NAME = 'add_scripture_links.py'

class TestResult:
    """Class to store and format test results."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.details = []
    
    def add_pass(self, message):
        """Record a passing test."""
        self.passed += 1
        self.details.append(f"✓ PASS: {message}")
        print(f"✓ PASS: {message}")
    
    def add_fail(self, message, details=None):
        """Record a failing test."""
        self.failed += 1
        error_msg = f"✗ FAIL: {message}"
        if details:
            error_msg += f"\n  Details: {details}"
        self.errors.append(error_msg)
        self.details.append(error_msg)
        print(error_msg)
    
    def add_error(self, message, exception=None):
        """Record an error during testing."""
        self.failed += 1
        error_msg = f"✗ ERROR: {message}"
        if exception:
            error_msg += f"\n  Exception: {str(exception)}"
        self.errors.append(error_msg)
        self.details.append(error_msg)
        print(error_msg)
    
    def summary(self):
        """Return a summary of test results."""
        total = self.passed + self.failed
        return f"\nTest Results: {self.passed}/{total} passed"


def read_tsv_file(filepath):
    """Read a TSV file and return rows as a list."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            return list(reader)
    except FileNotFoundError:
        return None
    except Exception as e:
        raise Exception(f"Error reading {filepath}: {e}")


def compare_tsv_files(actual_file, expected_file, test_result, test_name):
    """Compare two TSV files and report differences."""
    actual_rows = read_tsv_file(actual_file)
    expected_rows = read_tsv_file(expected_file)
    
    if actual_rows is None:
        test_result.add_error(f"{test_name}: Actual file not found: {actual_file}")
        return False
    
    if expected_rows is None:
        test_result.add_error(f"{test_name}: Expected file not found: {expected_file}")
        return False
    
    # Compare number of rows
    if len(actual_rows) != len(expected_rows):
        test_result.add_fail(
            f"{test_name}: Row count mismatch",
            f"Expected {len(expected_rows)} rows, got {len(actual_rows)} rows"
        )
        return False
    
    # Compare each row
    differences = []
    for i, (actual_row, expected_row) in enumerate(zip(actual_rows, expected_rows)):
        if len(actual_row) != len(expected_row):
            differences.append(f"Row {i+1}: Column count mismatch (expected {len(expected_row)}, got {len(actual_row)})")
            continue
        
        for j, (actual_cell, expected_cell) in enumerate(zip(actual_row, expected_row)):
            if actual_cell != expected_cell:
                differences.append(f"Row {i+1}, Column {j+1}:")
                differences.append(f"  Expected: {repr(expected_cell)}")
                differences.append(f"  Actual:   {repr(actual_cell)}")
    
    if differences:
        diff_summary = "\n".join(differences[:10])  # Show first 10 differences
        if len(differences) > 10:
            diff_summary += f"\n... and {len(differences) - 10} more differences"
        
        test_result.add_fail(f"{test_name}: Content differences found", diff_summary)
        return False
    
    test_result.add_pass(f"{test_name}: Files match perfectly")
    return True


def run_script_on_test_cases(test_result):
    """Run the add_scripture_links.py script on the test_cases directory."""
    script_path = Path(SCRIPT_NAME)
    test_path = Path(TEST_DIR)
    
    if not script_path.exists():
        test_result.add_error(f"Script not found: {script_path}")
        return False
    
    if not test_path.exists():
        test_result.add_error(f"Test directory not found: {test_path}")
        return False
    
    # Run the script
    try:
        print(f"Running: python3 {script_path} {test_path}")
        result = subprocess.run(
            [sys.executable, str(script_path), str(test_path)],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode != 0:
            test_result.add_error(
                f"Script execution failed with return code {result.returncode}",
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )
            return False
        
        print("Script output:")
        print(result.stdout)
        if result.stderr:
            print("Script stderr:")
            print(result.stderr)
        
        test_result.add_pass("Script executed successfully")
        return True
        
    except Exception as e:
        test_result.add_error("Failed to execute script", e)
        return False


def check_test_files(test_result):
    """Check that all required test files exist."""
    missing_files = []
    
    for book in TEST_BOOKS:
        input_file = Path(TEST_DIR) / f"tn_{book}.tsv"
        expected_converted = Path(TEST_DIR) / f"tn_{book}_expected.tsv"
        expected_diff = Path(TEST_DIR) / f"tn_{book}_expected_diff.tsv"
        
        if not input_file.exists():
            missing_files.append(str(input_file))
        if not expected_converted.exists():
            missing_files.append(str(expected_converted))
        if not expected_diff.exists():
            missing_files.append(str(expected_diff))
    
    if missing_files:
        test_result.add_error(
            "Missing test files",
            f"Required files not found: {', '.join(missing_files)}"
        )
        return False
    
    test_result.add_pass("All required test files found")
    return True


def run_tests():
    """Run all tests and return the results."""
    test_result = TestResult()
    
    print("=" * 60)
    print("Translation Notes Scripture Links Tool - Test Suite")
    print("=" * 60)
    
    # Check if test files exist
    print("\n1. Checking test files...")
    if not check_test_files(test_result):
        return test_result
    
    # Run the script
    print("\n2. Running script on test cases...")
    if not run_script_on_test_cases(test_result):
        return test_result
    
    # Compare output files
    print("\n3. Comparing output files with expected results...")
    
    for book in TEST_BOOKS:
        print(f"\nTesting {book}...")
        
        # Compare converted TSV files
        actual_converted = Path(TEST_DIR) / f"tn_{book}_converted.tsv"
        expected_converted = Path(TEST_DIR) / f"tn_{book}_expected.tsv"
        
        compare_tsv_files(
            actual_converted, 
            expected_converted, 
            test_result, 
            f"{book} converted file"
        )
        
        # Compare diff files
        actual_diff = Path(TEST_DIR) / f"tn_{book}_diff.tsv"  # These are created in the test_cases directory
        expected_diff = Path(TEST_DIR) / f"tn_{book}_expected_diff.tsv"
        
        compare_tsv_files(
            actual_diff, 
            expected_diff, 
            test_result, 
            f"{book} diff file"
        )
    
    return test_result


def create_sample_test_files():
    """Create sample test files for demonstration purposes."""
    print("Creating sample test files...")
    
    # Sample PSA test file
    psa_content = [
        ["Reference", "ID", "Tags", "SupportReference", "Quote", "Occurrence", "Note"],
        ["1:1", "abc1", "", "rc://*/ta/man/translate/translate-names", "blessed", "1", "This refers to Psalms 2 and chapter 3. See verses 2-4."],
        ["1:2", "abc2", "", "rc://*/ta/man/translate/figs-metaphor", "meditate", "1", "Compare with Joshua 1:8 and see verse 3."],
        ["2:1", "abc3", "", "rc://*/ta/man/translate/figs-rquestion", "nations", "1", "This connects to Psalm 1:1 and Acts 4:25-26."]
    ]
    
    # Sample MAT test file  
    mat_content = [
        ["Reference", "ID", "Tags", "SupportReference", "Quote", "Occurrence", "Note"],
        ["1:1", "abc1", "", "rc://*/ta/man/translate/translate-names", "Jesus", "1", "This genealogy connects to Genesis 22:18 and 2 Samuel 7:12-16."],
        ["1:2", "abc2", "", "rc://*/ta/man/translate/translate-names", "Abraham", "1", "See Genesis 12:1-3 and compare chapter 2."],
        ["2:1", "abc3", "", "rc://*/ta/man/translate/translate-names", "Bethlehem", "1", "This fulfills Micah 5:2 and verses 4-6."]
    ]
    
    # Sample JUD test file
    jud_content = [
        ["Reference", "ID", "Tags", "SupportReference", "Quote", "Occurrence", "Note"],
        ["1:1", "abc1", "", "rc://*/ta/man/translate/translate-names", "Jude", "1", "Compare with 2 Peter 3:3 and see verses 17-18."],
        ["1:4", "abc2", "", "rc://*/ta/man/translate/figs-metaphor", "condemnation", "1", "This refers to 2 Peter 2:1-3 and verse 6."],
        ["1:9", "abc3", "", "rc://*/ta/man/translate/translate-unknown", "Michael", "1", "See Daniel 10:13 and Revelation 12:7."]
    ]
    
    # Write test files
    test_dir = Path(TEST_DIR)
    test_dir.mkdir(exist_ok=True)
    
    for book, content in [("PSA", psa_content), ("MAT", mat_content), ("JUD", jud_content)]:
        with open(test_dir / f"tn_{book}.tsv", 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(content)
        print(f"Created tn_{book}.tsv")
    
    print("\nSample test files created!")
    print("You need to:")
    print("1. Run the script manually on these files to generate expected output")
    print("2. Rename the _converted.tsv files to _expected.tsv")
    print("3. Rename the _diff.tsv files to _expected_diff.tsv")
    print("4. Move the expected diff files to the test_cases directory")


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--create-samples':
        create_sample_test_files()
        return
    
    # Run the actual tests
    result = run_tests()
    
    print("\n" + "=" * 60)
    print(result.summary())
    
    if result.errors:
        print(f"\nFailed tests:")
        for error in result.errors:
            print(error)
    
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if result.failed == 0 else 1)


if __name__ == "__main__":
    main()
