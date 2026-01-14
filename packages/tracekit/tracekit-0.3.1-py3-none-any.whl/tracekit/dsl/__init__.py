"""TraceKit DSL - Domain-Specific Language for trace analysis.

Provides a simple, declarative language for defining trace analysis workflows.

Example usage:
    ```python
    from tracekit.dsl import execute_dsl

    # Execute DSL script
    script = '''
    $data = load "capture.csv"
    $filtered = $data | filter lowpass 1000
    $rise = $filtered | measure rise_time
    '''

    env = execute_dsl(script)
    print(f"Rise time: {env['$rise']}")
    ```

    Or start interactive REPL:
    ```python
    from tracekit.dsl import start_repl
    start_repl()
    ```
"""

from tracekit.dsl.commands import BUILTIN_COMMANDS
from tracekit.dsl.interpreter import Interpreter, InterpreterError, execute_dsl
from tracekit.dsl.parser import (
    Assignment,
    Command,
    Expression,
    ForLoop,
    FunctionCall,
    Lexer,
    Literal,
    Parser,
    Pipeline,
    Statement,
    Token,
    TokenType,
    Variable,
    parse_dsl,
)
from tracekit.dsl.repl import REPL, start_repl

__all__ = [
    # Commands
    "BUILTIN_COMMANDS",
    # REPL
    "REPL",
    # AST nodes
    "Assignment",
    "Command",
    "Expression",
    "ForLoop",
    "FunctionCall",
    # Interpreter
    "Interpreter",
    "InterpreterError",
    # Parser
    "Lexer",
    "Literal",
    "Parser",
    "Pipeline",
    "Statement",
    "Token",
    "TokenType",
    "Variable",
    "execute_dsl",
    "parse_dsl",
    "start_repl",
]
