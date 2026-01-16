# Contributing to GrandLight

Thank you for your interest in contributing to **GrandLight**! We appreciate your help in making this glassmorphism GUI library even better. 🎨✨

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. We expect all contributors to:

- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on constructive criticism
- Accept responsibility for mistakes
- Prioritize the community's best interests

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of GUI programming
- Familiarity with glassmorphism design principles

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Visit https://github.com/hslcrb/grandlight and click "Fork"
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/grandlight.git
   cd grandlight
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

5. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- **Clear title**: Brief description of the issue
- **Steps to reproduce**: Detailed steps to recreate the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, GrandLight version
- **Screenshots**: If applicable

### Suggesting Enhancements

We love new ideas! When suggesting enhancements:

- **Check existing issues**: Ensure it hasn't been suggested before
- **Describe the feature**: Explain what you want and why
- **Provide examples**: Show how it would work
- **Consider alternatives**: Mention other approaches you've considered

### Contributing Code

We welcome code contributions for:

- New glassmorphic components
- Bug fixes
- Performance improvements
- Documentation enhancements
- Example applications
- Tests

## Development Workflow

1. **Write your code**
   - Follow our coding standards (see below)
   - Add appropriate docstrings
   - Include type hints where applicable

2. **Test your changes**
   ```bash
   pytest tests/
   ```

3. **Format your code**
   ```bash
   black grandlight/
   flake8 grandlight/
   ```

4. **Update documentation**
   - Update README.md if adding features
   - Add docstrings to new functions/classes
   - Update examples if necessary

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add glassmorphic tooltip component"
   ```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use **Black** for code formatting (line length: 88)
- Use **type hints** for function signatures
- Write **descriptive variable names**

### Example

```python
from typing import Tuple, Optional

class GlassComponent:
    """Base class for all glassmorphic components.
    
    Args:
        blur: Blur intensity (0-100)
        opacity: Transparency level (0.0-1.0)
        background_color: RGBA color tuple
    """
    
    def __init__(
        self,
        blur: int = 20,
        opacity: float = 0.7,
        background_color: Tuple[int, int, int, int] = (255, 255, 255, 100)
    ) -> None:
        self.blur = blur
        self.opacity = opacity
        self.background_color = background_color
    
    def render(self) -> None:
        """Render the glassmorphic component."""
        pass
```

### Docstring Format

Use Google-style docstrings:

```python
def create_glass_effect(
    blur: int,
    opacity: float
) -> dict:
    """Create a glassmorphism effect configuration.
    
    Args:
        blur: Blur intensity from 0 to 100
        opacity: Transparency level from 0.0 to 1.0
    
    Returns:
        Dictionary containing effect parameters
    
    Raises:
        ValueError: If blur or opacity values are out of range
    
    Example:
        >>> effect = create_glass_effect(blur=20, opacity=0.8)
        >>> print(effect)
        {'blur': 20, 'opacity': 0.8}
    """
    if not 0 <= blur <= 100:
        raise ValueError("Blur must be between 0 and 100")
    if not 0.0 <= opacity <= 1.0:
        raise ValueError("Opacity must be between 0.0 and 1.0")
    
    return {"blur": blur, "opacity": opacity}
```

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test function names
- Test both success and failure cases
- Aim for high code coverage

### Example Test

```python
import pytest
from grandlight import GlassButton

def test_glass_button_creation():
    """Test that GlassButton is created with correct defaults."""
    button = GlassButton(text="Click Me")
    assert button.text == "Click Me"
    assert button.blur == 15
    assert button.opacity == 0.8

def test_glass_button_invalid_opacity():
    """Test that invalid opacity raises ValueError."""
    with pytest.raises(ValueError):
        GlassButton(text="Test", opacity=1.5)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=grandlight tests/

# Run specific test file
pytest tests/test_components.py
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat(components): add GlassTooltip component

Added a new glassmorphic tooltip component with customizable
blur and opacity settings.

Closes #123
```

```
fix(rendering): resolve transparency layering issue

Fixed bug where multiple glass panels would not layer correctly
when opacity values were very low.
```

## Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest tests/
   ```

2. **Update documentation**
   - Update README.md if needed
   - Add examples for new features

3. **Create a pull request**
   - Use a clear, descriptive title
   - Reference related issues
   - Describe your changes in detail
   - Add screenshots for UI changes

4. **Respond to feedback**
   - Address review comments
   - Update your PR as needed
   - Be patient and respectful

5. **Merge requirements**
   - All tests must pass
   - Code must be reviewed by maintainers
   - Documentation must be updated
   - Follows coding standards

## Questions?

If you have questions or need help:

- **GitHub Issues**: [Ask a question](https://github.com/hslcrb/grandlight/issues)
- **Discussions**: Use GitHub Discussions for general questions

## Recognition

All contributors will be recognized in our README.md file. Thank you for helping make GrandLight better! 🙏

---

**Happy coding! ✨**  
*Rhee Creative Team*
