"""
Case Data Extractor Module

Extracts display-relevant fields from the upstream context based on case configuration.
This creates the lightweight case_data stored in pipeline_cases table.
"""

import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from topaz_agent_kit.utils.logger import Logger


class CaseDataExtractor:
    """
    Extracts case data from upstream context based on case configuration.
    
    The case config defines which fields to extract using dot-notation paths
    like "agent_id.field_name" or "agent_id.nested.field".
    """
    
    def __init__(self):
        self.logger = Logger("CaseDataExtractor")
    
    def extract_case_id(
        self,
        upstream: Dict[str, Any],
        case_config: Dict[str, Any],
        fallback_id: Optional[str] = None,
    ) -> str:
        """
        Extract the case ID from upstream context based on config.
        
        Returns a unique case_id in format: PREFIX-UUID (e.g., BATCH-ABC12345)
        The expression/data is stored in case_data, not in the ID.
        
        Args:
            upstream: The upstream context containing all agent outputs
            case_config: The case configuration with identity settings
            fallback_id: Fallback ID to use if extraction fails (unused now, kept for compatibility)
            
        Returns:
            Unique case_id string
        """
        identity_config = case_config.get("identity", {})
        prefix = identity_config.get("prefix", "")
        uniqueness = identity_config.get("uniqueness", "uuid_suffix")
        
        # Simplified: Just use prefix + UUID (no id_source needed)
        # The expression/data is already stored in case_data, so we don't need it in the ID
        # This keeps IDs simple, URL-safe, and database-friendly: BATCH-ABC12345
        if prefix:
            base_id = prefix
        else:
            base_id = "CASE"  # Default prefix if none provided
        
        # Generate unique case_id based on uniqueness strategy
        # For uuid_suffix, this will add UUID suffix: BATCH-ABC12345
        case_id = self._make_unique(base_id, uniqueness)
        
        self.logger.debug(
            "Extracted case ID: {} (strategy: {})",
            case_id, uniqueness
        )
        
        return case_id
    
    def _make_unique(self, display_id: str, uniqueness: str) -> str:
        """
        Make the display_id unique based on the uniqueness strategy.
        
        Args:
            display_id: The human-readable display ID
            uniqueness: Strategy - "uuid_suffix", "timestamp", "none"
            
        Returns:
            Unique case_id (stored in uppercase)
        """
        # Convert display_id to uppercase for case_id
        display_id_upper = display_id.upper()
        
        if uniqueness == "uuid_suffix":
            suffix = uuid.uuid4().hex[:8].upper()
            return f"{display_id_upper}-{suffix}"
        elif uniqueness == "timestamp":
            suffix = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:20].upper()  # Include microseconds for uniqueness
            return f"{display_id_upper}-{suffix}"
        elif uniqueness == "none":
            # No uniqueness guarantee - use at your own risk
            return display_id_upper
        else:
            # Default to uuid_suffix
            suffix = uuid.uuid4().hex[:8].upper()
            return f"{display_id_upper}-{suffix}"
    
    def _sanitize_id(self, raw_id: str) -> str:
        """
        Sanitize an ID to make it URL-safe and database-friendly.
        
        Replaces special characters with safe alternatives:
        - Spaces → underscores
        - Special chars (*, +, /, etc.) → underscores
        - Multiple underscores → single underscore
        - Trims underscores from start/end
        
        Args:
            raw_id: The raw ID string (e.g., "((4+5)* 2-5)/2 + 9** 2")
            
        Returns:
            Sanitized ID (e.g., "__4_5__2_5__2__9__2")
        """
        if not raw_id:
            return raw_id
        
        # Replace spaces with underscores
        sanitized = raw_id.replace(" ", "_")
        
        # Replace common special characters with underscores
        # Keep alphanumeric, underscores, and hyphens
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', sanitized)
        
        # Collapse multiple underscores into one
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        # If result is empty or too short, use a hash
        if not sanitized or len(sanitized) < 3:
            # Use first 8 chars of hash as fallback
            import hashlib
            hash_id = hashlib.md5(raw_id.encode()).hexdigest()[:8].upper()
            return hash_id
        
        return sanitized
    
    def _generate_fallback_display_id(self, prefix: str = "") -> str:
        """Generate a fallback display ID when extraction fails"""
        short_id = uuid.uuid4().hex[:6].upper()
        if prefix:
            return f"{prefix}-{short_id}"
        return f"CASE-{short_id}"
    
    def extract_case_data(
        self,
        upstream: Dict[str, Any],
        case_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract display-relevant data from upstream context.
        
        Args:
            upstream: The upstream context containing all agent outputs
            case_config: The case configuration defining what to extract
            
        Returns:
            Dictionary of extracted case data for display
        """
        case_data = {}
        
        # Extract detail view fields (primary - used in case detail modal)
        detail_view = case_config.get("detail_view", {})
        if detail_view:
            case_data["_detail_view"] = self._extract_detail_view_data(upstream, detail_view)
        
        # Note: list_view and hitl_preview are no longer used - removed to simplify configuration
        
        # Also store raw agent outputs for flexibility
        # Only include agents that are referenced in the config
        referenced_agents = self._get_referenced_agents(case_config)
        for agent_id in referenced_agents:
            if agent_id in upstream:
                case_data[agent_id] = upstream[agent_id]
        
        return case_data
    
    def extract_field(
        self,
        upstream: Dict[str, Any],
        source_path: str,
    ) -> Any:
        """
        Extract a single field from upstream using dot-notation path.
        
        Args:
            upstream: The upstream context
            source_path: Dot-notation path like "agent_id.field" or "agent_id.nested.field"
            
        Returns:
            The extracted value or None if not found
        """
        return self._get_nested_value(upstream, source_path)
    
    def _extract_list_view_data(
        self,
        upstream: Dict[str, Any],
        list_view_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Extract fields for list view display"""
        data = {}
        
        # Support both "fields" array and "primary"/"secondary" structure
        fields = list_view_config.get("fields", [])
        if fields:
            # Simple fields array structure
            data["fields"] = []
            for field_config in fields:
                # Support both "source" and "field" keys
                source = field_config.get("source") or field_config.get("field")
                if source:
                    data["fields"].append({
                        "value": self._get_nested_value(upstream, source),
                        "label": field_config.get("label", ""),
                        "type": field_config.get("type", "text"),
                        "key": field_config.get("key", source.split(".")[-1]),
                    })
        else:
            # Legacy primary/secondary structure
            # Primary field
            primary = list_view_config.get("primary", {})
            if primary:
                # Support both "source" and "field" keys
                source = primary.get("source") or primary.get("field")
                if source:
                    data["primary"] = {
                        "value": self._get_nested_value(upstream, source),
                        "label": primary.get("label", ""),
                        "type": primary.get("type", "text"),
                    }
            
            # Secondary fields
            secondary = list_view_config.get("secondary", [])
            data["secondary"] = []
            for field_config in secondary:
                # Support both "source" and "field" keys
                source = field_config.get("source") or field_config.get("field")
                if source:
                    data["secondary"].append({
                        "value": self._get_nested_value(upstream, source),
                        "label": field_config.get("label", ""),
                        "type": field_config.get("type", "text"),
                        "key": field_config.get("key", source.split(".")[-1]),
                    })
        
        return data
    
    def _extract_detail_view_data(
        self,
        upstream: Dict[str, Any],
        detail_view_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Extract fields for detail view display"""
        from topaz_agent_kit.utils.expression_evaluator import evaluate_expression
        
        data = {"sections": []}
        
        sections = detail_view_config.get("sections", [])
        for section_config in sections:
            # Evaluate condition if present - skip section if condition is false
            condition = section_config.get("condition")
            if condition:
                try:
                    # Log available agents in upstream for debugging
                    available_agents = [k for k in upstream.keys() if not k.startswith("_")]
                    self.logger.info(
                        "Evaluating condition '{}' for section '{}'. Available agents in upstream: {}",
                        condition,
                        section_config.get("id") or section_config.get("title"),
                        available_agents
                    )
                    condition_result = evaluate_expression(condition, upstream)
                    if not condition_result:
                        self.logger.info(
                            "Skipping section '{}' - condition '{}' evaluated to False. Available agents: {}",
                            section_config.get("id") or section_config.get("title"),
                            condition,
                            available_agents
                        )
                        continue
                    else:
                        self.logger.info(
                            "Condition '{}' for section '{}' evaluated to True",
                            condition,
                            section_config.get("id") or section_config.get("title")
                        )
                except Exception as e:
                    self.logger.warning(
                        "Failed to evaluate condition '{}' for section '{}': {}. Skipping section.",
                        condition,
                        section_config.get("id") or section_config.get("title"),
                        e
                    )
                    continue
            
            section = {
                "id": section_config.get("id", ""),
                "title": section_config.get("title") or section_config.get("name", ""),  # Support both "title" and "name"
                "fields": [],
            }
            
            # Only use explicit fields - don't include all source_agent fields
            # source_agent is just for reference/documentation, explicit fields define what to show
            explicit_fields = section_config.get("fields", [])
            
            # If no explicit fields but source_agent is specified, include all outputs from that agent
            # (fallback for backwards compatibility)
            if not explicit_fields:
                source_agent = section_config.get("source_agent")
                if source_agent and source_agent in upstream:
                    agent_output = upstream[source_agent]
                    if isinstance(agent_output, dict):
                        for key, value in agent_output.items():
                            section["fields"].append({
                                "key": key,
                                "value": value,
                                "label": self._format_label(key),
                                "type": "auto",
                            })
            else:
                # Use only explicit fields
                for field_config in explicit_fields:
                    # Support both "source" and "field" keys for field path
                    source = field_config.get("source") or field_config.get("field")
                    if source:
                        key = field_config.get("key", source.split(".")[-1])
                        value = self._get_nested_value(upstream, source)
                        section["fields"].append({
                            "key": key,
                            "value": value,
                            "label": field_config.get("label", self._format_label(key)),
                            "type": field_config.get("type", "text"),
                        })
            
            data["sections"].append(section)
        
        return data
    
    def _get_nested_value(
        self,
        data: Dict[str, Any],
        path: str,
    ) -> Any:
        """
        Get a nested value from a dictionary using dot-notation path.
        
        Handles agent outputs that may be wrapped in "parsed" or "result" keys.
        For paths like "agent_id.field", tries:
        1. data["agent_id"]["field"] (direct)
        2. data["agent_id"]["parsed"]["field"] (parsed wrapper)
        3. data["agent_id"]["result"]["field"] (result wrapper)
        
        Args:
            data: The dictionary to extract from
            path: Dot-notation path like "agent_id.field" or "agent_id.nested.field"
            
        Returns:
            The value at the path or None if not found
        """
        if not path or not data:
            return None
        
        parts = path.split(".")
        if len(parts) < 2:
            return None
        
        agent_id = parts[0]
        field_path = parts[1:]
        
        # Get agent output from upstream
        agent_output = data.get(agent_id)
        if agent_output is None:
            return None
        
        # IMPORTANT: Try "parsed" wrapper FIRST, as it contains the normalized agent output
        # The "result" wrapper contains raw output and should only be used as fallback
        # This ensures we get the correct extracted value (e.g., math_calculator.result from parsed.result)
        # instead of the raw result wrapper
        if isinstance(agent_output, dict) and "parsed" in agent_output:
            current = agent_output["parsed"]
            for part in field_path:
                if isinstance(current, dict):
                    current = current.get(part)
                elif isinstance(current, list) and part.isdigit():
                    index = int(part)
                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        current = None
                else:
                    current = None
                
                if current is None:
                    break
            
            if current is not None:
                return current
        
        # If not found in parsed, try direct path (for backwards compatibility)
        current = agent_output
        for part in field_path:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list) and part.isdigit():
                index = int(part)
                if 0 <= index < len(current):
                    current = current[index]
                else:
                    current = None
            else:
                current = None
            
            if current is None:
                break
        
        if current is not None:
            return current
        
        # If still not found, try "result" wrapper
        if isinstance(agent_output, dict) and "result" in agent_output:
            current = agent_output["result"]
            for part in field_path:
                if isinstance(current, dict):
                    current = current.get(part)
                elif isinstance(current, list) and part.isdigit():
                    index = int(part)
                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        current = None
                else:
                    current = None
                
                if current is None:
                    break
            
            if current is not None:
                return current
        
        # Special case: if field_path is just a single field name and agent_output is a dict,
        # check if that field exists as a top-level key (handles cases where parsed wrapper doesn't exist)
        # BUT only if we haven't already found it in parsed/result wrappers above
        # This is a fallback for edge cases where agent output structure is different
        if isinstance(agent_output, dict) and len(field_path) == 1:
            field_name = field_path[0]
            # Only check top-level if field_name exists and we haven't found it yet
            # This prevents returning wrong values when parsed wrapper exists
            if field_name in agent_output:
                # Double-check: if parsed exists and contains the field, we should have found it above
                # This is just a safety fallback
                if "parsed" not in agent_output or field_name not in agent_output.get("parsed", {}):
                    return agent_output[field_name]
        
        return None
    
    def _get_referenced_agents(
        self,
        case_config: Dict[str, Any],
    ) -> set:
        """Get all agent IDs referenced in the case config"""
        agents = set()
        
        def extract_from_source(source: str):
            if source and "." in source:
                agents.add(source.split(".")[0])
        
        # Identity
        identity = case_config.get("identity", {})
        extract_from_source(identity.get("id_source", ""))
        
        # Detail view
        detail_view = case_config.get("detail_view", {})
        for section in detail_view.get("sections", []):
            if section.get("source_agent"):
                agents.add(section["source_agent"])
            for field in section.get("fields", []):
                # Support both "field" and "source" keys (field is used in case configs)
                source = field.get("field", "") or field.get("source", "")
                extract_from_source(source)
        
        return agents
    
    def _format_label(self, key: str) -> str:
        """Convert snake_case or camelCase to Title Case label"""
        # Handle snake_case
        if "_" in key:
            words = key.split("_")
        # Handle camelCase
        elif any(c.isupper() for c in key):
            words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', key)
        else:
            words = [key]
        
        return " ".join(word.capitalize() for word in words)
