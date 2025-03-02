import pytest
from src.code_processing.code_execution import CodeExecutionManager

@pytest.fixture
def code_execution_manager():
    return CodeExecutionManager()

def test_valid_code_execution(code_execution_manager: CodeExecutionManager) -> None:
    code_snippet = """
x = 10
y = 20
z = x + y
print(z)
"""
    result = code_execution_manager.execute_code(code_snippet)
    assert result["locals"]["z"] == 30
    assert result["output"] == '30'
    assert result["error"] is None
    assert result["exception"] is None

def test_runtime_error(code_execution_manager: CodeExecutionManager) -> None:
    code_snippet = "x = 1 / 0"
    result = code_execution_manager.execute_code(code_snippet)
    assert result["output"] is None
    assert 'ZeroDivisionError' in result["error"]
    assert result["exception"] is not None
    assert result["locals"] == {}


def test_syntax_error(code_execution_manager: CodeExecutionManager) -> None:
    code_snippet = "x ="
    result = code_execution_manager.execute_code(code_snippet)
    assert result["output"] is None
    assert 'SyntaxError' in result["error"]
    assert result["exception"] is not None
    assert result["locals"] == {}

def test_valid_code_with_multiple_prints(code_execution_manager: CodeExecutionManager) -> None:
    code_snippet = """
print('Hello, World!')
print('This is a test.')
"""
    result = code_execution_manager.execute_code(code_snippet)
    expected_output = "Hello, World!\nThis is a test."
    assert result["output"] == expected_output, f"Expected output: {expected_output}, Actual output: {result['output']}"
    assert result["locals"] == {}
    assert result["error"] is None
    assert result["exception"] is None

def test_multiple_assignments(code_execution_manager: CodeExecutionManager) -> None:
    code_snippet = """
x = 42
y = 'hello'
z = [1, 2, 3]
a = {'key': 'value'}
"""
    result = code_execution_manager.execute_code(code_snippet)
    assert result["locals"]["x"] == 42
    assert isinstance(result["locals"]["x"], int)
    assert result["locals"]["y"] == 'hello'
    assert isinstance(result["locals"]["y"], str)
    assert result["locals"]["z"] == [1, 2, 3]
    assert isinstance(result["locals"]["z"], list)
    assert result["locals"]["a"] == {'key': 'value'}
    assert isinstance(result["locals"]["a"], dict)
    assert result["output"] is None
    assert result["error"] is None
    assert result["exception"] is None