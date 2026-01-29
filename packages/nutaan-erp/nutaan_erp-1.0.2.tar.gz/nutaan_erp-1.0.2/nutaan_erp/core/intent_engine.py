"""Intent Engine for AI Agent SDK

This module handles intent analysis, clarity checking, and "psychological" intent understanding.
It acts as a pre-processor before the main agent execution to ensure requests are
actionable and well-formed.
"""

import json
from typing import Dict, Any, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from .config import AgentConfig

class IntentEngine:
    """
    Analyzes user messages to determine intent and clarity.
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = ChatGoogleGenerativeAI(
            model=config.model_name,
            google_api_key=config.api_key,
            temperature=0.1,
            max_tokens=1000
        )
        
    def analyze(
        self, 
        message: str, 
        context: Dict[str, Any],
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the user message for intent and clarity.
        
        Args:
            message: The latest user message
            context: System context (user, roles, current page, etc.)
            history: Conversation history
            
        Returns:
            Dict containing:
            - is_clear (bool): Is the request clear enough to proceed?
            - intent (str): The identified classification of intent
            - reasoning (str): Why it was classified this way
            - suggested_response (str): If unclear, what to ask the user. 
                                      If clear, a refined version of the request.
            - missing_info (List[str]): What information is missing
        """
        
        # Build context string
        user_context = f"""
        User: {context.get('user_name', 'Unknown')}
        Roles: {', '.join(context.get('user_roles', []))}
        Current Page: {context.get('current_path', 'Unknown')}
        Available Routes: {json.dumps(context.get('routes_map', {}), indent=2)}
        """
        
        # Build history string
        history_str = ""
        if history:
            history_str = "\n".join([
                f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" 
                for msg in history[-5:]  # Last 5 messages for context
            ])
            
        system_prompt = f"""You are an advanced 'Psychological Intent Engine' for an ERPNext AI Agent.
Your goal is to understand what the non-technical user REALLY wants, even if they spoke specifically or vaguely.

CONTEXT:
{user_context}

CONVERSATION HISTORY:
{history_str}

YOUR TASK:
Analyze the latest user message: "{message}"

Determine:
1. Is the request CLEAR and ACTIONABLE? (Can the agent likely perform this with available tools like creating docs, listing docs, navigating?)
2. What is the underlying INTENT? (e.g., "User wants to create a Sales Order", "User is greeting", "User is frustrated")
3. If unclear, what information is missing?

RULES:
- If the user says "help" or "what can you do", the intent is "Help".
- FOR CREATION TASKS (e.g. "Create Sales Order", "New Invoice"): 
    - Check if CRITICAL parameters are provided (e.g., Customer Name, Item Code, Employee Name, **Delivery Date** for orders).
    - If parameters are MISSING: Return `is_clear: false`, `missing_info: ["Customer", "Item", "Delivery Date"...]` and ask for them in `fallback_response`.
    - DO NOT assume or guess names (like "Test Customer") unless the user explicitly says "create a test order" or "use random data".
- If the user is vague (e.g., "I want to sell stuff"): infer the technical action (Create Sales Order) BUT mark `is_clear: false` because parameters are missing.
- IF the request is fully actionable (e.g. "Create sales order for Customer X"), return `is_clear: true`.
- REJECT OUT-OF-SCOPE requests:
    - Image editing, video processing, or media transformation (e.g. "Transform this photo", "Edit this video") -> Return `is_clear: false` and explain you are an ERP automation agent, not a media editor.
    - Nonsensical or completely ambiguous requests (e.g. "blue sky") -> Return `is_clear: false`.
- IF the user is asking to "check behavior" or "test", implies they want to run a test or verification.
- FOR UI INTERACTIONS (scroll, click button, navigate, analyze screen):
    - These are DIRECT COMMANDS.
    - Mark `is_clear: true`.
    - `refined_request` should be the direct command (e.g. "Scroll down the page").
    - Do NOT ask for more info unless the specific button name or page is completely missing.

OUTPUT FORMAT:
Return a JSON object with these keys:
- is_clear: boolean (true/false)
- intent: string (short description)
- reasoning: string (brief explanation)
- refined_request: string (The technical translation of what the user wants. e.g. "Create a Sales Order for customer 'John'")
- missing_info: used if is_clear is false. List of missing pieces.
- fallback_response: string (A helpful, natural language response to guide the user if needed. If is_clear is true, this can be empty).

Example JSON:
{{
  "is_clear": false,
  "intent": "Create Sales Order",
  "reasoning": "User matches 'Create Sales Order' intent but did not specify 'Customer' or 'Item'.",
  "refined_request": "Create Sales Order",
  "missing_info": ["Customer Name", "Item Code"],
  "fallback_response": "I can help you create a Sales Order. However, I need to know which Customer and Item you would like to include."
}}
"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            response = self.llm.invoke(messages)
            content = response.content.strip()
            
            # Clean up json block if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].strip()
                
            return json.loads(content)
            
        except Exception as e:
            # Fallback if analysis fails - assume clear and let main agent handle it
            # Returning is_clear=True ensures the system continues functioning even if intent analysis fails
            return {
                "is_clear": True, # Let the main agent try if we fail to analyze
                "intent": "Unknown",
                "reasoning": f"Analysis failed: {str(e)}",
                "refined_request": message,
                "missing_info": [],
                "fallback_response": ""
            }
