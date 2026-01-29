# Nutaan ERP AI Agent SDK

**Autonomous AI agent for ERPNext/Frappe automation** with 14 built-in tools.

[![PyPI version](https://badge.fury.io/py/nutaan-erp.svg)](https://badge.fury.io/py/nutaan-erp)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Core SDK for autonomous AI agent functionality. This package provides:

- **Agent Management**: Create and manage AI agents with Google Gemini
- **14 Built-in Tools**: Navigate, create documents, fill forms, and more
- **LangChain Integration**: Built on LangChain for robust agent orchestration
- **Intent Engine**: Smart clarification for vague requests
- **Action Tracking**: Automatic session tracking and reporting
- **Context Building**: Utilities for ERPNext/Frappe context

## Installation

### From PyPI (Recommended)
```bash
pip install nutaan-erp
```

### For Development (Local)
```bash
pip install -e /path/to/nutaan-erp/sdk
```

### For Production (Git)
```bash
pip install git+https://github.com/tecosys/nutaan-erp.git#subdirectory=sdk
```

## Quick Start

```python
from nutaan_erp import AgentManager, AgentConfig

# Create configuration
config = AgentConfig(
    api_key="your-gemini-api-key",
    model_name="gemini-2.0-flash-exp",
    temperature=0.1,
    max_tokens=4000
)

# Create agent manager
manager = AgentManager(config)

# Build context (example for Frappe/ERPNext)
from nutaan_erp.utils import build_frappe_context

context = build_frappe_context(
    user="john@example.com",
    current_path="/app/sales-order",
    roles=["Sales User", "Sales Manager"],
    user_full_name="John Doe"
)

# Execute agent
result = manager.execute(
    message="Create a new Sales Order for customer ABC Corp",
    context=context,
    history=[]
)

print(result)
```

## Features

### Tools
The SDK includes 14 tools:
1. `navigate` - Navigate to doctypes/forms
2. `create_doc` - Create new documents
3. `set_field` - Set form field values
4. `click_button` - Click buttons on page
5. `analyze_screen` - Analyze current page state
6. `scroll_page` - Scroll page up/down
7. `add_table_row` - Add rows to child tables
8. `set_table_field` - Set child table field values
9. `get_field_value` - Get field values
10. `select_option` - Select dropdown options
11. `get_validation_errors` - Check validation errors
12. `search_doctype` - Search for records in a DocType
13. `get_doctype_list` - Get list of available records
14. `validate_doctype_exists` - Check if a specific record exists

### Configuration
```python
config = AgentConfig(
    api_key="...",              # Required
    model_name="...",           # Default: gemini-2.0-flash-exp
    temperature=0.1,            # Default: 0.1
    max_tokens=4000,            # Default: 4000
    max_iterations=10,          # Default: 10
    timeout=300                 # Default: 300 seconds
)
```

## Architecture

```
nutaan_erp/
├── core/
│   ├── agent.py       # AgentManager
│   ├── config.py      # AgentConfig
│   └── tools.py       # Tool definitions
├── integrations/
│   └── langchain.py   # LangChain wrapper
└── utils/
    └── context.py     # Context building
```

## Requirements

- Python >= 3.8
- langchain >= 0.3.0
- langchain-google-genai >= 2.0.0
- langchain-core >= 0.3.0

## License

MIT
