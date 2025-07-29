# Contributing to Translation Notes Scripture Links Tool

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Translation Notes Scripture Links Tool.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone git@github.com:your-username/tn_add_scripture_links.git
   cd tn_add_scripture_links
   ```
3. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

This project uses only Python standard library modules, so no additional dependencies are required.

### Requirements

- Python 3.6 or higher
- Git

### Testing Your Changes

1. Test the script with the provided examples:

   ```bash
   python add_scripture_links.py examples/tn_GEN_sample.tsv
   ```

2. Test with your own TN TSV files to ensure compatibility

3. Check that the generated markdown links are correctly formatted

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and relatively small

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Input file format and sample content (if possible)
- Expected behavior vs. actual behavior
- Complete error messages

### Feature Requests

When suggesting new features:

- Explain the use case and problem it solves
- Provide examples of how it would work
- Consider backward compatibility

### Code Contributions

1. **Bug fixes**: Include a test case that reproduces the bug
2. **New features**: Update documentation and add examples
3. **Performance improvements**: Include benchmarks showing the improvement

## Submitting Changes

1. Make sure your code follows the project's style guidelines
2. Test your changes thoroughly
3. Update documentation if needed
4. Update the CHANGELOG.md file
5. Commit your changes with a clear, descriptive commit message
6. Push to your fork and submit a pull request

### Commit Message Format

Use clear, descriptive commit messages:

```
Add support for detecting cross-chapter verse ranges

- Handle references like "1:1–6:7" that span multiple chapters
- Update regex patterns to capture complex ranges
- Add test cases for cross-chapter references
```

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include test results and examples
- Keep pull requests focused on a single feature or fix

## Testing

While this project doesn't have a formal test suite yet, please test your changes by:

1. Running the script on various TN TSV files
2. Checking that generated links are correctly formatted
3. Verifying that existing functionality still works
4. Testing edge cases and error conditions

## Documentation

When adding new features or changing existing behavior:

1. Update the README.md with usage examples
2. Add entries to CHANGELOG.md
3. Update help text and command-line documentation
4. Consider adding examples to the examples/ directory

## Questions or Need Help?

Feel free to:

- Open an issue for questions about contributing
- Ask for clarification on existing code
- Suggest improvements to this contributing guide

## Code of Conduct

Please be respectful and professional in all interactions. This project welcomes contributions from everyone, regardless of experience level.

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.
