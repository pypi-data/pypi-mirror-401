# Test Suite Documentation

This directory contains the comprehensive test suite for the Synteles Platform MCP Server.

## 📁 Test Structure

```
tests/
├── __init__.py                 # Test package marker
├── conftest.py                 # Pytest fixtures and configuration
├── test_helpers.py             # Shared test utilities and mocks
├── test_init.py               # Package initialization tests
├── test_token_store.py        # TokenStore unit tests
├── test_oauth_client.py       # OAuthClient unit tests
├── test_main.py               # MCP server tools unit tests
├── test_integration.py        # Integration tests
└── README.md                  # This file
```

## 🧪 Test Categories

### Unit Tests

**test_token_store.py** (150+ lines)
- Token storage and retrieval
- Keychain operations
- Token clearing
- Error handling

**test_oauth_client.py** (250+ lines)
- PKCE code generation
- OAuth login flow
- Token refresh
- Logout functionality
- Callback handler

**test_main.py** (400+ lines)
- Authentication tools (login, logout, auth_status)
- User management tools
- Organization tools
- Agentlet CRUD operations
- API key management
- HTTP request handling
- Error propagation

**test_init.py** (50+ lines)
- Package version validation
- Module imports
- Package structure

### Integration Tests

**test_integration.py** (250+ lines)
- Full authentication flow
- Token refresh during API calls
- Token lifecycle management
- End-to-end scenarios
- Cross-component interactions

### Test Utilities

**conftest.py**
- Pytest fixtures for common test data
- Automatic test setup/teardown
- Logging configuration

**test_helpers.py**
- Mock object creation utilities
- Response builders
- Assertion helpers

## 🚀 Running Tests

### Run All Tests

```bash
# Using make
make test

# Using unittest directly
python -m unittest discover tests -v

# Using pytest (if installed)
pytest tests/ -v
```

### Run Specific Test Files

```bash
# Run only TokenStore tests
python -m unittest tests.test_token_store -v

# Run only OAuth client tests
python -m unittest tests.test_oauth_client -v

# Run only integration tests
python -m unittest tests.test_integration -v
```

### Run Specific Test Classes

```bash
# Run only TestTokenStore class
python -m unittest tests.test_token_store.TestTokenStore -v

# Run only authentication flow integration tests
python -m unittest tests.test_integration.TestAuthenticationFlow -v
```

### Run Specific Test Methods

```bash
# Run single test method
python -m unittest tests.test_token_store.TestTokenStore.test_save_tokens_with_id_token -v
```

## 📊 Test Coverage

### Generate Coverage Report

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests

# Generate report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

### Expected Coverage

- **TokenStore**: 100% coverage
- **OAuthClient**: ~95% coverage (some edge cases in HTTP server)
- **Main MCP Tools**: ~90% coverage
- **Overall**: Target 90%+ coverage

## 🏗️ Test Architecture

### Mocking Strategy

All tests use mocking to avoid:
- ❌ Real network requests
- ❌ Real OAuth flows
- ❌ Real keychain access
- ❌ Browser interactions

Key mocked components:
- `requests` library → Mock HTTP calls
- `keyring` library → Mock secure storage
- `webbrowser` → Mock browser opening
- `HTTPServer` → Mock OAuth callback server

### Test Isolation

Each test is fully isolated:
- No shared state between tests
- Automatic cleanup via fixtures
- Independent mock objects per test

### Test Naming Convention

```python
def test_<what>_<scenario>():
    """Test <description>."""
```

Examples:
- `test_save_tokens_with_id_token()` - Tests saving tokens including ID token
- `test_login_auth_timeout()` - Tests login timeout scenario
- `test_make_request_401_triggers_refresh()` - Tests automatic token refresh

## 🔍 Test Quality Guidelines

### Assertions

Each test should verify:
1. **Expected outcomes** - Function returns/raises correctly
2. **Side effects** - Mocks called with correct parameters
3. **State changes** - Objects in expected state

### Test Structure (AAA Pattern)

```python
def test_example(self):
    """Test description."""
    # Arrange - Set up test data and mocks
    mock_data = {...}

    # Act - Execute the code under test
    result = function_under_test(mock_data)

    # Assert - Verify outcomes
    assert result == expected_value
    mock_function.assert_called_once()
```

### Error Testing

Always test both success and failure cases:

```python
def test_success_case(self):
    """Test successful operation."""
    # Test happy path

def test_failure_case(self):
    """Test operation failure."""
    # Test error handling
```

## 📝 Writing New Tests

### 1. Choose Test File

- **Unit tests** → Create/update `test_<module>.py`
- **Integration tests** → Add to `test_integration.py`
- **Helper functions** → Add to `test_helpers.py`

### 2. Use Fixtures

Leverage existing fixtures from `conftest.py`:

```python
def test_with_fixtures(self, mock_tokens, mock_org_id):
    """Test using pytest fixtures."""
    # Use mock_tokens and mock_org_id directly
```

### 3. Mock External Dependencies

```python
@patch('module.external_dependency')
def test_with_mock(self, mock_dependency):
    """Test with mocked dependency."""
    mock_dependency.return_value = expected_value
    # Test code
```

### 4. Add Docstrings

Every test must have a clear docstring:

```python
def test_example(self):
    """Test that function handles edge case correctly.

    This test verifies that when X happens, the function
    returns Y and calls Z with the correct parameters.
    """
```

## 🐛 Debugging Tests

### Run with Verbose Output

```bash
python -m unittest tests -v
```

### Show Print Statements

```bash
python -m unittest tests -v -b  # -b disables output capturing
```

### Run with Python Debugger

```python
import pdb; pdb.set_trace()  # Add to test code
```

### Check Mock Calls

```python
# Verify mock was called
mock_function.assert_called_once()

# Verify mock call arguments
mock_function.assert_called_with(expected_arg1, expected_arg2)

# See all calls
print(mock_function.call_args_list)
```

## ⚡ Performance

### Test Execution Time

All tests should complete in:
- Individual test: < 0.1 seconds
- Test file: < 5 seconds
- Full suite: < 30 seconds

### Slow Tests

If a test is slow, consider:
1. Reducing timeout values
2. Mocking more dependencies
3. Simplifying test data

## 🔄 CI/CD Integration

Tests run automatically on:
- Every push to main/develop
- Every pull request
- Pre-merge checks

CI configuration in `.github/workflows/ci.yml`

### CI Test Commands

```yaml
# Install dependencies
uv pip install --system -e .

# Run tests
python -m unittest discover tests -v

# Run with coverage
coverage run -m unittest discover tests
coverage report
```

## 📚 Additional Resources

### Python unittest Documentation
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [unittest.mock — Mock object library](https://docs.python.org/3/library/unittest.mock.html)

### Best Practices
- [Effective Python Testing](https://realpython.com/python-testing/)
- [Test-Driven Development](https://www.obeythetestinggoat.com/)

### Project-Specific
- [API Contracts](../docs/API_CONTRACTS.md)
- [Authentication Spec](../docs/AUTH_SPEC.md)
- [CLAUDE.md](../CLAUDE.md)

## 🆘 Common Issues

### Import Errors

```bash
# Ensure package is installed in development mode
uv pip install -e .
```

### Mock Not Working

```python
# Ensure you're patching the right location
# Patch where it's used, not where it's defined
@patch('synteles_platform_mcp.main.requests')  # ✅ Correct
@patch('requests')  # ❌ Wrong
```

### Keyring Errors

All keyring operations should be mocked:

```python
@patch('synteles_platform_mcp.auth.token_store.keyring')
```

## 📈 Test Metrics

Current test statistics:
- **Total tests**: 80+
- **Test files**: 6
- **Code coverage**: ~90%
- **Lines of test code**: 1,500+
- **Execution time**: ~10 seconds

## ✅ Test Checklist

Before committing:
- [ ] All tests pass locally
- [ ] New code has corresponding tests
- [ ] Coverage remains above 85%
- [ ] No mocked dependencies leak to other tests
- [ ] All test docstrings are clear
- [ ] No hardcoded credentials or tokens
- [ ] CI tests pass

## 🔮 Future Improvements

Potential enhancements:
1. Add property-based testing (hypothesis)
2. Add mutation testing (mutmut)
3. Add performance benchmarks
4. Add contract tests for API
5. Add end-to-end tests with test server
