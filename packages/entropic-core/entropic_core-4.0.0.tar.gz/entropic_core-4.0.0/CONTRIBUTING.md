# Contributing to Entropic Core

Thank you for considering contributing to Entropic Core! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, package version)
- **Code samples** or error messages
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** explaining why this would be useful
- **Possible implementation** if you have ideas
- **Examples** from other projects if relevant

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Install development dependencies**:
   ```bash
   pip install -e .[dev]
   ```
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Run the test suite**:
   ```bash
   pytest tests/ -v
   ```
6. **Run linting**:
   ```bash
   black entropic_core/ tests/
   flake8 entropic_core/ tests/
   isort entropic_core/ tests/
   ```
7. **Update documentation** if needed
8. **Commit your changes** with clear commit messages
9. **Push to your fork** and submit a pull request

## Development Setup

### Prerequisites

- Python 3.9+
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/entropic-core.git
cd entropic-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .[dev,advanced,enterprise]

# Run tests to verify setup
pytest tests/
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters maximum
- **Imports**: Organized using `isort`
- **Formatting**: Use `black` for automatic formatting
- **Type hints**: Required for public APIs
- **Docstrings**: Google style for all public functions/classes

### Example

```python
from typing import Dict, List, Optional

def calculate_entropy(
    agents: List[Agent],
    window_size: int = 100,
    normalize: bool = True
) -> Dict[str, float]:
    """Calculate entropy metrics for agent system.
    
    Args:
        agents: List of agent instances to analyze
        window_size: Number of recent events to consider
        normalize: Whether to normalize values to [0, 1]
    
    Returns:
        Dictionary containing entropy metrics:
        - 'decision': Decision entropy value
        - 'state': State dispersion value
        - 'communication': Communication complexity value
    
    Raises:
        ValueError: If agents list is empty
    
    Example:
        >>> agents = [Agent(), Agent()]
        >>> metrics = calculate_entropy(agents)
        >>> print(metrics['decision'])
        0.65
    """
    if not agents:
        raise ValueError("agents list cannot be empty")
    
    # Implementation here
    pass
```

## Testing Guidelines

### Writing Tests

- **Location**: Tests go in `tests/` directory
- **Naming**: Test files match source files (`test_entropy_monitor.py`)
- **Coverage**: Aim for >85% code coverage
- **Types**: Unit tests, integration tests, and end-to-end tests

### Test Structure

```python
import pytest
from entropic_core import EntropyBrain

class TestEntropyMonitor:
    """Tests for entropy monitoring functionality."""
    
    def test_basic_entropy_calculation(self):
        """Test basic entropy calculation with simple agents."""
        # Arrange
        brain = EntropyBrain()
        agents = [MockAgent(), MockAgent()]
        
        # Act
        entropy = brain.measure_entropy(agents)
        
        # Assert
        assert 0.0 <= entropy <= 1.0
        assert 'decision' in brain.last_metrics
    
    @pytest.mark.parametrize("agent_count", [1, 10, 100])
    def test_scalability(self, agent_count):
        """Test entropy calculation scales with agent count."""
        # Test implementation
        pass
```

## Documentation

### Docstring Guidelines

All public APIs must have docstrings following Google style:

```python
def function_name(param1: str, param2: int) -> bool:
    """One-line summary.
    
    Longer description if needed, explaining the purpose
    and any important details.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When and why this is raised
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
```

### README and Guides

When updating documentation:

- Keep examples simple and runnable
- Explain the "why" not just the "what"
- Include common pitfalls and solutions
- Update the table of contents if adding sections

## Commit Message Guidelines

We follow conventional commits format:

```
type(scope): short description

Longer explanation if needed

Fixes #123
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(monitor): add support for custom entropy metrics

This allows users to define their own entropy calculation
methods by subclassing EntropyMetric.

Closes #42
```

```
fix(regulator): prevent infinite loop in chaos reduction

The regulator could enter an infinite loop when entropy
oscillated rapidly. Added dampening factor to prevent this.

Fixes #156
```

## Release Process

Releases are automated through GitHub Actions:

1. Update `VERSION` file
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions will build and publish to PyPI

## Getting Help

- **Questions**: Open a discussion on GitHub Discussions
- **Bugs**: Open an issue with the bug report template
- **Chat**: Join our community Discord (link in README)
- **Email**: maintainers@entropic-core.org

## Recognition

Contributors will be:

- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Given credit in documentation

Thank you for contributing to Entropic Core!
