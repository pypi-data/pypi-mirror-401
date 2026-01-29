"""Context building utilities"""

import json
from typing import Dict, Any, List


def build_system_prompt(context: Dict[str, Any]) -> str:
    """
    Build system prompt for the agent based on context
    
    Args:
        context: Context dictionary containing:
            - user_name: User's full name
            - user_roles: List of user roles
            - current_path: Current page path
            - routes_map: Available routes/doctypes
    
    Returns:
        System prompt string
    """
    user_name = context.get("user_name", "User")
    user_roles = context.get("user_roles", [])
    current_path = context.get("current_path", "/")
    
    # Format roles
    roles_str = ', '.join(user_roles) if user_roles else 'Guest'
    
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    system_prompt = f"""You are Nutaan AI, an intelligent automation assistant for ERPNext.
    **CURRENT SYSTEM TIME**: {current_time}
    
 CORE PRINCIPLES:
 1. ACCURACY FIRST: Prioritize correctness over speed. Do not guess.
 2. NO HALLUCINATION: If you do not know a Customer Name, Item Code, or Document ID, do NOT invent one. Search for it or ask.
 3. Use demo/default data ONLY if the user explicitly requests a "test", "demo", or "random" data.
 4. Handle errors gracefully: analyze the error, adjust your approach, and retry.
 5. Execute tasks through tool calls, never just describe.
 
 TOOL USAGE GUIDELINES:
 - When searching for records (Customers, Items, etc.), use `get_doctype_list`.
 - ALWAYS use the EXACT name string returned by `get_doctype_list` (e.g. "Test Customer ABC"). Do not guess or approximate.
 - If a specific record is not found, look for reasonable alternatives using `search_doctype`. If still not found, report this to the user.
 - For `create_doc`, ensure you have the necessary mandatory fields. If missing, do not proceed; explain what is missing.
 - **DATE HANDLING**: 
   - Always reference the **CURRENT SYSTEM TIME** ({current_time}) for relative dates.
   - For "Delivery Date" or deadlines, ALWAYS assume the **FUTURE** occurrence. Example: If today is 2026-01-15 and user says "2 Feb", use "2026-02-02". If user says "1 Jan", use "2027-01-01". Never pick a past date for a deadline.
   - For `delivery_date` and `transaction_date`, if not specified, ASK the user.
 
 ERROR RECOVERY:
 - Validation errors: Read the error message carefully, identify the missing/incorrect field, fix the arguments, and retry.
 - **Payment Schedule Errors**: If you encounter "Missing Payment Amount" or related Payment Schedule errors, the system failed to auto-calculate. Fix this by:
   1. Searching for a `Payment Terms Template` (e.g., search for "Default").
   2. Setting the `payment_terms_template` field to a valid template name.
   3. Retrying the Save.
 - Data missing: Use search tools to find valid data.
 - Screen Interaction: You CAN scroll the page using `scroll_page`. Do NOT say you cannot scroll. Use the tool to reveal more content.
 
 Context:
 - User: {user_name} ({roles_str})
 - Current page: {current_path}
 
 You are an intelligent agent. Use your reasoning capabilities to map the user's intent to the correct sequence of tools. Do not rely on hardcoded scripts. Verify your actions."""
    
    return system_prompt


def build_frappe_context(
    user: str,
    current_path: str,
    roles: List[str],
    user_full_name: str = None
) -> Dict[str, Any]:
    """
    Build context dictionary from Frappe-specific information
    
    Args:
        user: Username
        current_path: Current route/path
        roles: List of user roles
        user_full_name: User's full name (optional)
    
    Returns:
        Context dictionary for agent
    """
    # Build routes map based on roles
    routes_map = get_frappe_routes(roles)
    
    return {
        "user_name": user_full_name or user,
        "user_roles": roles,
        "current_path": current_path,
        "routes_map": routes_map
    }


def get_frappe_routes(roles: List[str]) -> Dict[str, List[str]]:
    """
    Get available routes based on user roles
    
    Args:
        roles: List of user role names
    
    Returns:
        Dictionary mapping module names to available doctypes
    """
    routes = {}
    
    # Core doctypes
    common_doctypes = ["ToDo", "Note", "Event", "Task"]
    
    # Sales module
    if "Sales User" in roles or "Sales Manager" in roles or "System Manager" in roles:
        routes["Sales"] = ["Sales Order", "Sales Invoice", "Quotation", "Customer"]
    
    # Purchase module
    if "Purchase User" in roles or "Purchase Manager" in roles or "System Manager" in roles:
        routes["Purchase"] = ["Purchase Order", "Purchase Invoice", "Supplier"]
    
    # Stock module
    if "Stock User" in roles or "Stock Manager" in roles or "System Manager" in roles:
        routes["Stock"] = ["Stock Entry", "Item", "Warehouse", "Delivery Note"]
    
    # Accounts module
    if "Accounts User" in roles or "Accounts Manager" in roles or "System Manager" in roles:
        routes["Accounts"] = ["Journal Entry", "Payment Entry", "Bank Account"]
    
    # HR module
    if "HR User" in roles or "HR Manager" in roles or "System Manager" in roles:
        routes["HR"] = ["Employee", "Attendance", "Leave Application", "Salary Slip"]
    
    # Manufacturing
    if "Manufacturing User" in roles or "Manufacturing Manager" in roles or "System Manager" in roles:
        routes["Manufacturing"] = ["Work Order", "BOM", "Job Card"]
    
    # System Manager has access to everything
    if "System Manager" in roles:
        routes["System"] = ["User", "Role", "DocType", "Custom Field"]
    
    routes["Common"] = common_doctypes
    
    return routes
