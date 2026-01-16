# AGENTS.md

This file provides guidance for agentic coding assistants working in this repository.

## Build/Install/Run

```bash
# Install in editable mode (recommended)
uv pip install -e .

# Run directly without installation
uvx treesitter-mcp

# Run MCP server in stdio mode (default, for Claude Desktop)
treesitter-mcp

# Run in HTTP mode for testing/development
treesitter-mcp --http --port 8000 --host 127.0.0.1

# Run specific tools only
treesitter-mcp --http --tools treesitter_analyze_file,treesitter_get_ast
```

## Testing

```bash
# Run all tests
pytest

# Run a single test file
pytest test_file.py

# Run a specific test
pytest test_file.py::test_function_name

# Run with verbose output
pytest -v
```

## Code Style

### Imports
- Use `from typing import List, Optional, Dict, Any` for type hints
- Group imports: standard library, third-party, local (each separated by blank line)
- Relative imports for local modules: `from ..core.analyzer import BaseAnalyzer`

### Formatting
- 4 spaces for indentation (no tabs)
- Line length: reasonable, no strict limit observed
- No trailing whitespace

### Type Hints
- Always add type hints to function signatures
- Use `typing` module: `List[str]`, `Optional[str]`, `Dict[str, Any]`, `-> str`
- Return types required for all functions
- Pydantic models for structured data: `BaseModel` from `pydantic`

### Naming Conventions
- **Classes**: PascalCase (`CAnalyzer`, `BaseAnalyzer`, `ASTNode`)
- **Functions/Variables**: snake_case (`get_language_name`, `extract_symbols`)
- **Constants**: UPPER_SNAKE_CASE (when applicable)
- **Private methods**: prefix with underscore (`_build_ast`, `_field_name_for_child`)
- **Protected methods**: prefix with underscore

### Error Handling
- Use try/except for error handling in MCP tool functions
- Return dictionaries with `"error"` key: `{"error": "message"}`
- Check file existence before analysis: `os.path.exists(file_path)`
- Normalize paths: `os.path.abspath(os.path.expanduser(file_path))`

### Docstrings
- Google-style docstrings for functions and classes
- Include `Args:` and `Returns:` sections
- Keep descriptions concise and clear

### Tree-sitter Queries
- Use S-expression format in triple-quoted strings
- Pattern: `(node_type field: (child_type) @capture_name) @capture`
- Use `Query` and `QueryCursor` for execution
- Decode node text: `node.text.decode("utf8")`

### Architecture Patterns
- Inherit language analyzers from `BaseAnalyzer`
- Implement all abstract methods from `BaseAnalyzer`
- Use `LanguageManager` to get parsers/languages
- MCP tools decorated with `@mcp_tool_if_enabled("tool_name")`
- Use `model_dump()` for Pydantic serialization

### Important Notes
- Tree-sitter version: `>=0.22.0` (pinned minimum in pyproject.toml)
- Ruby analyzer exists but is NOT registered in `analyzers` dict (server.py)
- File extension mapping in `get_analyzer()` function (server.py)
- AST nodes can be large; use `max_depth` parameter for control
- Imports use `uv` package manager (per `.claude/CLAUDE.md`)
