"""Tool definitions for AI Agent SDK"""

import json
from typing import List
from langchain_core.tools import tool


@tool
def navigate(doctype: str, name: str = None) -> str:
    """Navigate to a doctype list or form in ERPNext.
    
    Args:
        doctype: The doctype to navigate to (e.g., 'Sales Order', 'Customer')
        name: Specific document name to open (optional)
    """
    if name:
        return json.dumps({"action": "navigate", "doctype": doctype, "name": name})
    return json.dumps({"action": "navigate", "doctype": doctype})


@tool
def create_doc(doctype: str) -> str:
    """Create a new document of specified doctype.
    
    Args:
        doctype: The doctype to create (e.g., 'Customer', 'Sales Order')
    """
    return json.dumps({"action": "create_doc", "doctype": doctype})


@tool
def set_field(fieldname: str, value: str) -> str:
    """Set value of a field in the current form.
    
    Args:
        fieldname: The field name to set
        value: The value to set
    """
    return json.dumps({"action": "set_field", "fieldname": fieldname, "value": value})


@tool
def click_button(button_text: str) -> str:
    """Click a button on the page.
    
    Args:
        button_text: Text of the button to click (e.g., 'Save', 'Submit')
    """
    return json.dumps({"action": "click_button", "button_text": button_text})


@tool
def analyze_screen(purpose: str) -> str:
    """Analyze current screen to understand page state.
    
    Args:
        purpose: What you want to understand about the current page
    """
    return json.dumps({"action": "analyze_screen", "purpose": purpose})


@tool
def scroll_page(direction: str, amount: int = 300) -> str:
    """Scroll the page up or down.
    
    Args:
        direction: 'up' or 'down'
        amount: Pixels to scroll (default 300)
    """
    return json.dumps({"action": "scroll_page", "direction": direction, "amount": amount})


@tool
def add_table_row(table_fieldname: str) -> str:
    """Add a new row to a child table (e.g., 'items' in Sales Order).
    
    Args:
        table_fieldname: The fieldname of the child table (e.g., 'items', 'taxes')
    """
    return json.dumps({"action": "add_table_row", "table_fieldname": table_fieldname})


@tool
def set_table_field(table_fieldname: str, row_idx: int, fieldname: str, value: str) -> str:
    """Set a field value in a child table row.
    
    Args:
        table_fieldname: The child table fieldname (e.g., 'items')
        row_idx: Row index (1-based)
        fieldname: Field name within the row (e.g., 'item_code', 'qty')
        value: Value to set
    """
    return json.dumps({
        "action": "set_table_field",
        "table_fieldname": table_fieldname,
        "row_idx": row_idx,
        "fieldname": fieldname,
        "value": value
    })


@tool
def get_field_value(fieldname: str) -> str:
    """Get the current value of a form field.
    
    Args:
        fieldname: The field name to read
    """
    return json.dumps({"action": "get_field_value", "fieldname": fieldname})


@tool
def select_option(fieldname: str, value: str) -> str:
    """Select an option from a dropdown or link field.
    
    Args:
        fieldname: The field name (e.g., 'customer', 'item_code')
        value: The value to select
    """
    return json.dumps({"action": "select_option", "fieldname": fieldname, "value": value})


@tool
def get_validation_errors() -> str:
    """Check for any validation errors on the current form.
    Use this after clicking Save/Submit to see what fields need to be filled.
    
    Returns:
        List of validation errors or confirmation that there are none
    """
    return json.dumps({"action": "get_validation_errors"})


@tool
def search_doctype(doctype: str, search_text: str, limit: int = 20) -> str:
    """Search for records in a DocType that match the search text.
    Use this to find existing customers, items, or other records before using them.
    
    Args:
        doctype: The DocType to search (e.g., 'Customer', 'Item', 'Supplier')
        search_text: Text to search for (searches in name and common fields)
        limit: Maximum number of results to return (default 20)
    
    Returns:
        List of matching records with their names
    """
    return json.dumps({
        "action": "search_doctype",
        "doctype": doctype,
        "search_text": search_text,
        "limit": limit
    })


@tool
def get_doctype_list(doctype: str, limit: int = 50) -> str:
    """Get a list of available records from a DocType.
    Use this to see what customers, items, or other records are available in the system.
    
    Args:
        doctype: The DocType to list (e.g., 'Customer', 'Item', 'Supplier')
        limit: Maximum number of records to return (default 50)
    
    Returns:
        List of available records with their names
    """
    return json.dumps({
        "action": "get_doctype_list",
        "doctype": doctype,
        "limit": limit
    })


@tool
def validate_doctype_exists(doctype: str, name: str) -> str:
    """Check if a specific record exists in a DocType.
    Use this before setting a link field to verify the record exists.
    
    Args:
        doctype: The DocType to check (e.g., 'Customer', 'Item')
        name: The name/ID of the record to check
    
    Returns:
        Confirmation whether the record exists or not
    """
    return json.dumps({
        "action": "validate_doctype_exists",
        "doctype": doctype,
        "name": name
    })


def get_all_tools() -> List:
    """Return list of all available tools"""
    return [
        navigate,
        create_doc,
        set_field,
        click_button,
        analyze_screen,
        scroll_page,
        add_table_row,
        set_table_field,
        get_field_value,
        select_option,
        get_validation_errors,
        search_doctype,
        get_doctype_list,
        validate_doctype_exists
    ]
