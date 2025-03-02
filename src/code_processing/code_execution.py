import subprocess
import traceback
import io, sys
from typing import Any, Dict, Optional


class CodeExecutionManager:
    def __init__(self):
        """
        Initialize the CodeExecutionManager.
        """
        self.context = {
            'output': None,
            'error': None,
            'exception': None,
            'locals': {}
        }

    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute the given Python code in a separate subprocess and return the result.
        """
        try:
            # 0. Redirect stdout to capture print statements and define local scope
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            local_scope = {}

            # 1. Execute the code using a subprocess
            exec(code, {}, local_scope)
        
            # 2. Restore stdout and capture the output and error
            sys.stdout = sys.__stdout__
            captured_output = output_buffer.getvalue().strip()
            self.context["locals"] = local_scope
            self.context["output"] = captured_output if captured_output else None
            self.context["error"] = None
            self.context["exception"] = None
        except Exception as e:
            sys.stdout = sys.__stdout__ # Restore stdout
            self.context["error"] = traceback.format_exc()
            self.context["output"] = None
            self.context["exception"] = str(e)
            self.context["locals"] = {}
    
        return self.context

    def compare_output(self, variable_name: str, expected_value: str) -> bool:
        """
        Compare the output of the code execution with the expected output.
        """
        return self.context["locals"].get(variable_name, None) == expected_value

    def reset_context(self):
        """
        Reset the context to its initial state.
        """
        self.context = {
            "output": None,
            "error": None,
            "exception": None,
            "locals": {}
        }

if __name__ == "__main__":
    manager = CodeExecutionManager()
    code = "print('Hello, World!')"
    result = manager.execute_code(code)
    print(result)