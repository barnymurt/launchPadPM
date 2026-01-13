# Testing Guide

## Overview

This project uses pytest for testing with a target coverage of 80%+. Tests are organized into unit tests and integration tests.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_base_agent.py       # Unit tests for BaseAgent
├── test_agent_registry.py  # Unit tests for AgentRegistry
├── test_product_owner_agent.py  # Unit tests for ProductOwnerAgent
└── test_integration_agents.py   # Integration tests for agent interactions
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=agents --cov=config --cov=governance --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_base_agent.py -v
```

### Run Specific Test
```bash
pytest tests/test_base_agent.py::TestBaseAgent::test_base_agent_initialization -v
```

## Test Coverage

Current coverage target: **80%**

View coverage report:
```bash
# Generate HTML report
pytest --cov=agents --cov=config --cov=governance --cov-report=html

# Open htmlcov/index.html in browser
```

## Automated Testing

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

Hooks will run automatically on commit:
- Code formatting (black)
- Linting (flake8)
- Type checking (mypy)
- Tests (pytest)

### CI/CD

GitHub Actions workflow runs tests on:
- Push to main/develop branches
- Pull requests to main/develop branches

See `.github/workflows/tests.yml` for configuration.

## Writing Tests

### Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Test

```python
def test_agent_initialization(agent_context):
    """Test that agent initializes correctly"""
    agent = ProductOwnerAgent(context=agent_context)
    assert agent.role == "Product Owner"
    assert agent.context == agent_context
```

### Fixtures

Common fixtures available in `conftest.py`:
- `agent_context`: Creates a test AgentContext
- `clean_registry`: Clears agent registry before/after test

## Test Categories

### Unit Tests
- Test individual components in isolation
- Fast execution (< 1 second each)
- High coverage target (80%+)

### Integration Tests
- Test component interactions
- Test cross-functional collaboration
- Verify agent coordination

## Best Practices

1. **One assertion per test** (when possible)
2. **Descriptive test names** that explain what is being tested
3. **Use fixtures** for common setup
4. **Test edge cases** and error conditions
5. **Keep tests independent** - no test should depend on another
6. **Mock external dependencies** when appropriate

## Continuous Improvement

- Review test coverage regularly
- Add tests for new features
- Refactor tests when code changes
- Update test documentation
