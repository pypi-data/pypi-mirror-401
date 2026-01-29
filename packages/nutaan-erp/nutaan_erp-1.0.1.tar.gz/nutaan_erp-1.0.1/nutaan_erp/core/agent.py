"""Main Agent Manager for AI Agent SDK"""

import json
import traceback
from typing import Dict, List, Any, Optional

from .config import AgentConfig
from .tools import get_all_tools
from .tracker import ActionTracker
from .intent_engine import IntentEngine
from ..integrations.langchain import create_langchain_agent
from ..utils.context import build_system_prompt


class AgentManager:
    """
    Main class for managing AI Agent lifecycle and execution
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize AgentManager with configuration
        
        Args:
            config: AgentConfig instance
        """
        self.config = config
        self.agent = None
        self.tracker = ActionTracker()
        self.intent_engine = IntentEngine(config)
    
    def _initialize_agent(self, context: Dict[str, Any]):
        """
        Initialize the LangChain agent with tools and configuration
        
        Args:
            context: Context information for system prompt
        """
        # Build system prompt
        system_prompt = build_system_prompt(context)
        
        # Get all tools
        tools = get_all_tools()
        
        # Create agent using LangChain integration
        self.agent = create_langchain_agent(
            api_key=self.config.api_key,
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            tools=tools,
            system_prompt=system_prompt
        )
    
    def execute(
        self,
        message: str,
        context: Dict[str, Any],
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Execute agent with a message and context
        
        Args:
            message: User message/command
            context: Context dictionary with user info, routes, etc.
            history: Conversation history
        
        Returns:
            Dictionary with execution results
        """
        try:
            # Start tracking session
            user = context.get('user', 'Unknown')
            session_id = self.tracker.start_session(user=user, initial_message=message)
            
            # Initialize agent with context
            self._initialize_agent(context)
            
            # Build messages
            messages = []
            if history:
                # Limit history to prevent context overflow (keep last 30 messages)
                recent_history = history[-30:] if len(history) > 30 else history
                for msg in recent_history:
                    messages.append({
                        "role": msg.get("role"),
                        "content": msg.get("content", "")
                    })
            
            # Analyze intent before proceeding
            intent_result = self.intent_engine.analyze(message, context, history)
            
            # If request is unclear, return fallback response immediately
            if not intent_result.get("is_clear", True):
                fallback_msg = intent_result.get("fallback_response", "Could you please clarify your request?")
                
                # Record this interaction
                self.tracker.record_action("intent_clarification", {"reason": intent_result.get("reasoning")}, fallback_msg)
                session_data = self.tracker.end_session(final_outcome="Clarification Requested")
                
                return {
                    "success": True,
                    "tool_calls": [],
                    "agent_steps": [{
                        "type": "response",
                        "content": fallback_msg
                    }],
                    "content": fallback_msg,
                    "agent_loop_complete": True,
                    "debug_events": [],
                    "session_data": session_data.to_dict(),
                    "session_id": session_id
                }

            # Use refined request if available, otherwise original
            effective_message = intent_result.get("refined_request", message)
            
            if effective_message:
                messages.append({"role": "user", "content": effective_message})
            
            # Stream agent events for step-by-step feedback
            tool_calls = []
            agent_steps = []
            final_content = ""
            
            # Debug: Log all events
            all_events = []
            
            # Use stream to get step-by-step updates
            for event in self.agent.stream({"messages": messages}, stream_mode="updates"):
                # Debug: capture raw event
                all_events.append(str(event)[:500])
                
                # Each event is a dict with node name as key
                for node_name, node_data in event.items():
                    if node_name == "model":  # LangGraph uses 'model' for AI responses
                        # Model node - contains AI responses
                        if "messages" in node_data:
                            for msg in node_data["messages"]:
                                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                    for tc in msg.tool_calls:
                                        tool_call_info = {
                                            "name": tc.get("name"),
                                            "args": tc.get("args", {}),
                                            "id": tc.get("id", "")
                                        }
                                        tool_calls.append(tool_call_info)
                                        agent_steps.append({
                                            "type": "tool_call",
                                            "tool": tc.get("name"),
                                            "args": tc.get("args", {})
                                        })
                                        
                                        # Record action in tracker
                                        self.tracker.record_action(
                                            tool_name=tc.get("name"),
                                            tool_arguments=tc.get("args", {})
                                        )
                                        
                                elif hasattr(msg, 'content') and msg.content:
                                    final_content = msg.content
                                    agent_steps.append({
                                        "type": "response",
                                        "content": msg.content
                                    })
                    
                    elif node_name == "tools":
                        # Tools node - contains tool execution results
                        if "messages" in node_data:
                            for msg in node_data["messages"]:
                                if hasattr(msg, 'content'):
                                    agent_steps.append({
                                        "type": "tool_result",
                                        "tool_call_id": getattr(msg, 'tool_call_id', ''),
                                        "result": msg.content
                                    })
            
            # End session and get session data
            session_data = self.tracker.end_session(final_outcome=final_content or "Done")
            
            return {
                "success": True,
                "tool_calls": tool_calls,
                "agent_steps": agent_steps,
                "content": final_content or "Done",
                "agent_loop_complete": True,
                "debug_events": all_events[:10],  # First 10 raw events for debugging
                "session_data": session_data.to_dict(),
                "session_id": session_id
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "success": False,
                "traceback": traceback.format_exc()
            }
