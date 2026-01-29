"""Action Tracking Module for AI Agent SDK

This module provides session tracking and action recording capabilities
for AI agent executions. It captures all tool calls, arguments, results,
and timing information for later analysis and report generation.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class ActionRecord:
    """Record of a single action/tool execution"""
    action_number: int
    timestamp: str
    tool_name: str
    tool_arguments: Dict[str, Any]
    result: Any = None
    target_doctype: Optional[str] = None
    target_document: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class SessionData:
    """Complete session data with all actions and metadata"""
    session_id: str
    user: str = ""
    start_time: str = ""
    end_time: str = ""
    initial_message: str = ""
    final_outcome: str = ""
    total_actions: int = 0
    actions: List[ActionRecord] = field(default_factory=list)
    created_documents: List[Dict[str, str]] = field(default_factory=list)
    modified_documents: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Convert ActionRecord objects to dicts
        data['actions'] = [action.to_dict() if isinstance(action, ActionRecord) else action 
                          for action in self.actions]
        return data


class ActionTracker:
    """
    Tracks AI agent actions during a session.
    
    Records all tool calls with their arguments, results, and timing information.
    Generates session summaries suitable for reporting and PDF generation.
    """
    
    def __init__(self):
        """Initialize a new action tracker"""
        self.session_data: Optional[SessionData] = None
        self.action_counter: int = 0
    
    def start_session(self, session_id: Optional[str] = None, user: str = "", initial_message: str = "") -> str:
        """
        Start a new tracking session
        
        Args:
            session_id: Optional session ID (auto-generated if not provided)
            user: User who initiated the session
            initial_message: Initial user message that started the session
            
        Returns:
            Session ID
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        self.session_data = SessionData(
            session_id=session_id,
            user=user,
            start_time=datetime.utcnow().isoformat(),
            initial_message=initial_message
        )
        self.action_counter = 0
        
        return session_id
    
    def record_action(
        self,
        tool_name: str,
        tool_arguments: Dict[str, Any],
        result: Any = None
    ) -> ActionRecord:
        """
        Record a single action/tool execution
        
        Args:
            tool_name: Name of the tool that was executed
            tool_arguments: Arguments passed to the tool
            result: Result returned by the tool
            
        Returns:
            ActionRecord instance
        """
        if self.session_data is None:
            raise RuntimeError("Session not started. Call start_session() first.")
        
        self.action_counter += 1
        
        # Extract target doctype and document from arguments if available
        target_doctype = tool_arguments.get('doctype')
        target_document = tool_arguments.get('name')
        
        action = ActionRecord(
            action_number=self.action_counter,
            timestamp=datetime.utcnow().isoformat(),
            tool_name=tool_name,
            tool_arguments=tool_arguments,
            result=result,
            target_doctype=target_doctype,
            target_document=target_document
        )
        
        self.session_data.actions.append(action)
        
        # Track created/modified documents
        self._track_document_changes(action)
        
        return action
    
    def _track_document_changes(self, action: ActionRecord):
        """
        Track documents that were created or modified
        
        Args:
            action: Action record to analyze
        """
        if self.session_data is None:
            return
        
        # Track document creation
        if action.tool_name == 'create_doc' and action.target_doctype:
            doc_info = {
                'doctype': action.target_doctype,
                'name': action.target_document or 'New',
                'action_number': action.action_number
            }
            if doc_info not in self.session_data.created_documents:
                self.session_data.created_documents.append(doc_info)
        
        # Track document modifications (navigate, set_field, etc.)
        elif action.tool_name in ['navigate', 'set_field', 'set_table_field', 'click_button']:
            if action.target_doctype:
                doc_info = {
                    'doctype': action.target_doctype,
                    'name': action.target_document or 'Unknown',
                    'action_number': action.action_number
                }
                # Only add if not already tracked
                if doc_info not in self.session_data.modified_documents:
                    # Also don't add if it's in created_documents
                    is_created = any(
                        d['doctype'] == doc_info['doctype'] and d.get('name') == doc_info.get('name')
                        for d in self.session_data.created_documents
                    )
                    if not is_created:
                        self.session_data.modified_documents.append(doc_info)
    
    def end_session(self, final_outcome: str = "") -> SessionData:
        """
        End the current session and finalize data
        
        Args:
            final_outcome: Description of the final outcome/result
            
        Returns:
            Complete SessionData
        """
        if self.session_data is None:
            raise RuntimeError("No active session to end.")
        
        self.session_data.end_time = datetime.utcnow().isoformat()
        self.session_data.final_outcome = final_outcome
        self.session_data.total_actions = self.action_counter
        
        return self.session_data
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session
        
        Returns:
            Dictionary with session summary information
        """
        if self.session_data is None:
            return {
                'active': False,
                'message': 'No active session'
            }
        
        # Calculate duration
        duration_seconds = 0
        if self.session_data.start_time and self.session_data.end_time:
            start = datetime.fromisoformat(self.session_data.start_time)
            end = datetime.fromisoformat(self.session_data.end_time)
            duration_seconds = int((end - start).total_seconds())
        
        # Count actions by tool
        tool_counts = {}
        for action in self.session_data.actions:
            tool_counts[action.tool_name] = tool_counts.get(action.tool_name, 0) + 1
        
        return {
            'active': True,
            'session_id': self.session_data.session_id,
            'user': self.session_data.user,
            'initial_message': self.session_data.initial_message,
            'total_actions': self.session_data.total_actions,
            'duration_seconds': duration_seconds,
            'created_documents': self.session_data.created_documents,
            'modified_documents': self.session_data.modified_documents,
            'tool_usage': tool_counts,
            'start_time': self.session_data.start_time,
            'end_time': self.session_data.end_time
        }
    
    def get_full_session_data(self) -> Optional[Dict[str, Any]]:
        """
        Get complete session data including all actions
        
        Returns:
            Complete session data as dictionary, or None if no active session
        """
        if self.session_data is None:
            return None
        
        return self.session_data.to_dict()
