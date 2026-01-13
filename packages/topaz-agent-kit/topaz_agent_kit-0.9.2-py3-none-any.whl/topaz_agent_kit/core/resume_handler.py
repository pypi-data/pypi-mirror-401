"""
Pipeline Resume Handler Module

Handles resuming pipeline execution from checkpoints after HITL response.
Reconstructs context, injects HITL response, and executes remaining steps.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from topaz_agent_kit.core.checkpoint_manager import CheckpointManager, PipelineCheckpoint
from topaz_agent_kit.core.case_manager import CaseManager
from topaz_agent_kit.core.hitl_queue_manager import HITLQueueManager
from topaz_agent_kit.core.chat_database import ChatDatabase
from topaz_agent_kit.utils.logger import Logger


class ResumeHandler:
    """
    Handles pipeline resumption from checkpoints.
    
    Responsibilities:
    - Load and validate checkpoints
    - Reconstruct execution context with HITL response
    - Trigger pipeline execution from resume point
    - Update case and checkpoint status
    """
    
    def __init__(
        self,
        database: ChatDatabase,
        checkpoint_manager: Optional[CheckpointManager] = None,
        case_manager: Optional[CaseManager] = None,
        hitl_queue_manager: Optional[HITLQueueManager] = None,
    ):
        """
        Initialize ResumeHandler.
        
        Args:
            database: ChatDatabase instance
            checkpoint_manager: Optional pre-initialized CheckpointManager
            case_manager: Optional pre-initialized CaseManager
            hitl_queue_manager: Optional pre-initialized HITLQueueManager
        """
        self.database = database
        self.checkpoint_manager = checkpoint_manager or CheckpointManager(database)
        self.case_manager = case_manager or CaseManager(database)
        self.hitl_queue_manager = hitl_queue_manager or HITLQueueManager(database)
        self.logger = Logger("ResumeHandler")
        
        # Callback for pipeline execution (will be set by orchestrator)
        self._execute_resume_callback = None
    
    def set_execute_callback(self, callback):
        """
        Set the callback function for executing resumed pipelines.
        
        The callback should have signature:
            async def callback(
                pipeline_id: str,
                context: Dict[str, Any],
                resume_point: str,
            ) -> Any
        
        Args:
            callback: Async function to execute resumed pipeline
        """
        self._execute_resume_callback = callback
    
    async def resume_from_queue_response(
        self,
        queue_item_id: str,
        decision: str,
        response_data: Optional[Dict[str, Any]] = None,
        responded_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Resume pipeline execution from a queue response.
        
        This is the main entry point for resuming after HITL response.
        
        Args:
            queue_item_id: The HITL queue item ID
            decision: User's decision (e.g., "approve", "reject", action ID)
            response_data: Additional response data
            responded_by: User who responded
            
        Returns:
            Dictionary with resume result
        """
        self.logger.info(
            "Resuming from queue response: queue_item={}, decision={}",
            queue_item_id, decision
        )
        
        # 1. Get queue item to retrieve gate_id before submitting response
        queue_item = self.hitl_queue_manager.get_queue_item(queue_item_id)
        if not queue_item:
            self.logger.error("Queue item not found: {}", queue_item_id)
            return {
                "success": False,
                "error": "Queue item not found",
                "queue_item_id": queue_item_id,
            }
        
        gate_id = queue_item.get("gate_id")
        case_id = queue_item.get("case_id")
        
        # 2. Submit the response to queue
        response_result = self.hitl_queue_manager.submit_response(
            queue_item_id=queue_item_id,
            decision=decision,
            response_data=response_data,
            responded_by=responded_by,
        )
        
        if not response_result.get("success"):
            return response_result
        
        checkpoint_id = response_result["checkpoint_id"]
        
        # 3. Add timeline entry for HITL response
        # Include all response data (selection, input fields, notes, etc.)
        event_data = {
            "gate_id": gate_id,
            "decision": decision,
            "responded_at": datetime.now().isoformat(),
            "responded_by": responded_by,
        }
        
        # Include all response data (for selection gates, input gates, etc.)
        if response_data:
            # For selection gates, include the selected option
            if "selection" in response_data:
                event_data["selection"] = response_data["selection"]
            # For input gates, include all field values
            # Filter out internal fields like "notes" and "selection" which we handle separately
            input_fields = {
                k: v for k, v in response_data.items()
                if k not in ("notes", "selection")
            }
            if input_fields:
                event_data["input_fields"] = input_fields
            # Include notes if present
            if "notes" in response_data:
                event_data["notes"] = response_data["notes"]
        
        self.case_manager._add_timeline_entry(
            case_id=case_id,
            event_type="hitl_response",
            event_data=event_data,
        )
        
        # 4. Resume from checkpoint
        return await self.resume_from_checkpoint(
            checkpoint_id=checkpoint_id,
            decision=decision,
            response_data=response_data,
        )
    
    async def resume_from_checkpoint(
        self,
        checkpoint_id: str,
        decision: str,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Resume pipeline execution from a checkpoint.
        
        Args:
            checkpoint_id: The checkpoint ID
            decision: User's decision
            response_data: Additional response data
            
        Returns:
            Dictionary with resume result
        """
        self.logger.info(
            "Resuming from checkpoint: checkpoint_id={}, decision={}",
            checkpoint_id, decision
        )
        
        # 1. Load the checkpoint
        checkpoint = self.checkpoint_manager.get_checkpoint(checkpoint_id)
        
        if not checkpoint:
            self.logger.error("Checkpoint not found or expired: {}", checkpoint_id)
            return {
                "success": False,
                "error": "Checkpoint not found or expired",
                "checkpoint_id": checkpoint_id,
            }
        
        # 2. Reconstruct context with HITL response
        context = self._reconstruct_context(
            checkpoint=checkpoint,
            decision=decision,
            response_data=response_data,
        )
        
        # 2.5. Log resume summary for debugging
        resume_info = context.get("_resume", {})
        is_resumed = resume_info.get("is_resumed", False)
        if is_resumed:
            loop_index = context.get("loop_index")
            loop_total = context.get("loop_total")
            if loop_index is not None and loop_total is not None:
                self.logger.info(
                    "Resume summary: Processing loop iteration {}/{} only (other iterations have separate checkpoints)",
                    loop_index + 1, loop_total
                )
            
            # Log agents that will be skipped (already in upstream)
            upstream = context.get("upstream", {})
            skipped_agents = [agent_id for agent_id in upstream.keys() if agent_id]
            if skipped_agents:
                self.logger.info(
                    "Resume summary: {} agents already executed and will be skipped: {}",
                    len(skipped_agents), ", ".join(skipped_agents[:10])  # Limit to first 10 for readability
                )
        
        # 3. Update case status to processing
        self.case_manager.update_case_status(
            case_id=checkpoint.case_id,
            status=CaseManager.STATUS_PROCESSING,
            current_step=checkpoint.resume_point,
        )
        
        # 4. Mark checkpoint as resumed
        self.checkpoint_manager.mark_resumed(checkpoint_id)
        
        # 5. Execute resumed pipeline
        if self._execute_resume_callback:
            try:
                start_time = datetime.now()
                
                result = await self._execute_resume_callback(
                    pipeline_id=checkpoint.pipeline_id,
                    context=context,
                    resume_point=checkpoint.resume_point,
                    checkpoint=checkpoint,
                )
                
                # Calculate processing time
                processing_time_ms = int(
                    (datetime.now() - start_time).total_seconds() * 1000
                )
                
                # Extract final upstream context from result to update case_data
                # The execute_resume_callback returns {"result": result, "upstream": context.get("upstream", {}), "context": context}
                # We should prioritize result["upstream"] as it contains the final state after all agents have run
                final_upstream = context.get("upstream", {})  # Fallback to original context
                
                # Priority: result["upstream"] > result["context"]["upstream"] > context["upstream"]
                if isinstance(result, dict):
                    if "upstream" in result:
                        # This is the final upstream from the callback, includes all post-HITL agents
                        final_upstream = result["upstream"]
                        self.logger.debug(
                            "Using upstream from result: {} agents",
                            len(final_upstream)
                        )
                    elif "context" in result and isinstance(result["context"], dict):
                        final_upstream = result["context"].get("upstream", final_upstream)
                        self.logger.debug(
                            "Using upstream from result.context: {} agents",
                            len(final_upstream)
                        )
                    else:
                        # Fallback: context is passed by reference and should be updated
                        # But prefer result if available
                        self.logger.debug(
                            "Using upstream from context: {} agents",
                            len(final_upstream)
                        )
                
                # Get case_config from context (loaded during resume)
                case_config = context.get("case_config", {})
                if case_config:
                    # CRITICAL: Extract nested agents from sub-pipeline nodes before updating case data
                    # Sub-pipelines store results in structure: pipeline_id.nodes.agent_id
                    # But case YAML expects agents directly accessible (e.g., math_auditor.parsed.final_answer)
                    # So we need to extract agents from sub-pipeline nodes and add them to final_upstream
                    import copy
                    upstream_for_case = copy.deepcopy(final_upstream)
                    
                    for pipeline_id, pipeline_data in list(upstream_for_case.items()):
                        # Handle accumulated sub-pipeline results (list)
                        if isinstance(pipeline_data, list) and len(pipeline_data) > 0:
                            # For resume, use the last element (most recent iteration)
                            pipeline_data = pipeline_data[-1]
                        
                        if isinstance(pipeline_data, dict) and "nodes" in pipeline_data:
                            nodes = pipeline_data.get("nodes", {})
                            self.logger.info(
                                "Extracting {} nodes from sub-pipeline '{}' for case data update after resume",
                                len(nodes), pipeline_id
                            )
                            for node_id, node_data in nodes.items():
                                # Store the full node_data structure (with parsed/result wrappers) so CaseDataExtractor
                                # can properly access fields using _get_nested_value which expects parsed/result wrappers
                                if isinstance(node_data, dict):
                                    # Only add if not already present (don't overwrite direct agent outputs)
                                    if node_id not in upstream_for_case:
                                        # Store the full node_data structure (has parsed/result wrappers)
                                        upstream_for_case[node_id] = copy.deepcopy(node_data)
                                        self.logger.info(
                                            "Extracted node '{}' from sub-pipeline '{}' for case data update (has parsed: {}, has result: {})",
                                            node_id, pipeline_id,
                                            "parsed" in node_data, "result" in node_data
                                        )
                                    elif isinstance(upstream_for_case[node_id], dict):
                                        # If it exists, check if it has the parsed/result wrapper structure
                                        if "parsed" not in upstream_for_case[node_id] and "result" not in upstream_for_case[node_id]:
                                            # Existing entry doesn't have wrapper structure, replace with full node_data
                                            upstream_for_case[node_id] = copy.deepcopy(node_data)
                                            self.logger.info(
                                                "Replaced node '{}' from sub-pipeline '{}' with full structure for case data update",
                                                node_id, pipeline_id
                                            )
                                        elif "parsed" in node_data and "parsed" not in upstream_for_case[node_id]:
                                            # New node_data has parsed wrapper but existing doesn't, update it
                                            upstream_for_case[node_id] = copy.deepcopy(node_data)
                                            self.logger.info(
                                                "Updated node '{}' from sub-pipeline '{}' with parsed wrapper for case data update",
                                                node_id, pipeline_id
                                            )
                    
                    # Update case_data with final upstream context (now includes extracted nested agents)
                    # This ensures the case detail view shows all agent outputs including post-HITL agents
                    self.case_manager.update_case_data(
                        case_id=checkpoint.case_id,
                        upstream=upstream_for_case,
                        case_config=case_config,
                    )
                
                # Clean result of non-serializable objects (like AGUIEventEmitter) before storing/returning
                cleaned_result = self._clean_result_for_serialization(result)
                
                # Update case as completed
                self.case_manager.mark_completed(
                    case_id=checkpoint.case_id,
                    final_output=cleaned_result if isinstance(cleaned_result, dict) else {"result": cleaned_result},
                    processing_time_ms=processing_time_ms,
                )
                
                self.logger.info(
                    "Successfully resumed and completed case: {} ({}ms)",
                    checkpoint.case_id, processing_time_ms
                )
                
                return {
                    "success": True,
                    "case_id": checkpoint.case_id,
                    "checkpoint_id": checkpoint_id,
                    "result": cleaned_result,
                    "processing_time_ms": processing_time_ms,
                }
                
            except Exception as e:
                # Check if this is a graceful stop (PipelineStoppedByUser), not an error
                from topaz_agent_kit.core.exceptions import PipelineStoppedByUser
                
                if isinstance(e, PipelineStoppedByUser):
                    # Pipeline was stopped by user (e.g., HITL rejection) - this is graceful, not a failure
                    self.logger.info(
                        "Pipeline stopped by user for case {}: {}",
                        checkpoint.case_id, e
                    )
                    
                    # Mark case as completed (with note that it was stopped by user)
                    # The case completed successfully - user just chose to stop it
                    self.case_manager.mark_completed(
                        case_id=checkpoint.case_id,
                        final_output={"status": "stopped_by_user", "reason": str(e)},
                        processing_time_ms=0,  # Will be calculated if needed
                    )
                    
                    # Mark the queue item as responded (not failed)
                    queue_item = self.hitl_queue_manager.get_queue_item_by_checkpoint(checkpoint_id)
                    if queue_item:
                        queue_item_id = queue_item.get("queue_item_id") or queue_item.get("id")
                        if queue_item_id:
                            # Queue item was responded to (user rejected), mark as responded
                            self.hitl_queue_manager.database.update_hitl_queue_item_status(
                                queue_item_id=queue_item_id,
                                status=HITLQueueManager.STATUS_RESPONDED,
                            )
                            self.logger.info(
                                "Marked queue item {} as responded (stopped by user)",
                                queue_item_id
                            )
                    
                    return {
                        "success": True,  # Successfully stopped by user
                        "stopped_by_user": True,
                        "reason": str(e),
                        "case_id": checkpoint.case_id,
                        "checkpoint_id": checkpoint_id,
                    }
                else:
                    # Actual error - mark as failed
                    self.logger.error(
                        "Failed to execute resumed pipeline for case {}: {}",
                        checkpoint.case_id, e
                    )
                    
                    # Update case as failed
                    self.case_manager.mark_failed(
                        case_id=checkpoint.case_id,
                        error_message=str(e),
                    )
                    
                    # Mark the queue item as failed so it can be retried
                    # Find the queue item by checkpoint_id
                    failed_queue_item_id = None
                    queue_item = self.hitl_queue_manager.get_queue_item_by_checkpoint(checkpoint_id)
                    if queue_item:
                        queue_item_id = queue_item.get("queue_item_id") or queue_item.get("id")
                        if queue_item_id:
                            self.hitl_queue_manager.database.update_hitl_queue_item_status(
                                queue_item_id=queue_item_id,
                                status=HITLQueueManager.STATUS_FAILED,
                            )
                            self.logger.info(
                                "Marked queue item {} as failed for retry",
                                queue_item_id
                            )
                            failed_queue_item_id = queue_item_id
                    
                    return {
                        "success": False,
                        "error": str(e),
                        "case_id": checkpoint.case_id,
                        "checkpoint_id": checkpoint_id,
                        "queue_item_id": failed_queue_item_id,
                    }
        else:
            # No callback set - return context for manual execution
            self.logger.warning(
                "No execute callback set, returning reconstructed context"
            )
            return {
                "success": True,
                "case_id": checkpoint.case_id,
                "checkpoint_id": checkpoint_id,
                "context": context,
                "resume_point": checkpoint.resume_point,
                "requires_manual_execution": True,
            }
    
    def _reconstruct_context(
        self,
        checkpoint: PipelineCheckpoint,
        decision: str,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Reconstruct execution context from checkpoint with HITL response.
        
        Args:
            checkpoint: The pipeline checkpoint
            decision: User's decision
            response_data: Additional response data
            
        Returns:
            Reconstructed execution context
        """
        # Start with the checkpoint's upstream context
        context = {
            # Core identifiers
            "pipeline_id": checkpoint.pipeline_id,
            "run_id": checkpoint.run_id,
            "session_id": checkpoint.session_id,
            "case_id": checkpoint.case_id,
            
            # RESTORED: Full upstream context (all agent outputs)
            "upstream": checkpoint.upstream.copy(),
            
            # RESTORED + UPDATED: HITL context with new response
            "hitl": {
                **checkpoint.hitl,
                checkpoint.gate_id: {
                    "decision": decision,
                    "data": response_data or {},
                    "responded_at": datetime.now().isoformat(),
                },
            },
            
            # Resume metadata
            "_resume": {
                "checkpoint_id": checkpoint.checkpoint_id,
                "gate_id": checkpoint.gate_id,
                "resume_point": checkpoint.resume_point,
                "is_resumed": True,
                "loop_index": checkpoint.loop_index,  # Store in resume_info so it doesn't get overwritten
            },
        }
        
        # Add loop context if present
        if checkpoint.loop_index is not None:
            context["loop_index"] = checkpoint.loop_index
            context["loop_item"] = checkpoint.loop_item
            context["loop_total"] = checkpoint.loop_total
            context["loop_id"] = checkpoint.loop_id
            
            # Also set in upstream for template access
            context["upstream"]["_loop"] = {
                "index": checkpoint.loop_index,
                "item": checkpoint.loop_item,
                "total": checkpoint.loop_total,
            }
        
        # Add pattern stack if present
        if checkpoint.pattern_stack:
            context["_pattern_stack"] = checkpoint.pattern_stack
        
        self.logger.debug(
            "Reconstructed context for case {} with {} upstream keys, hitl gate: {}",
            checkpoint.case_id,
            len(checkpoint.upstream),
            checkpoint.gate_id,
        )
        
        return context
    
    def get_pending_resumes(
        self,
        pipeline_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of pending checkpoints that can be resumed.
        
        Args:
            pipeline_id: Optional filter by pipeline
            
        Returns:
            List of checkpoint metadata
        """
        return self.checkpoint_manager.list_pending_checkpoints(
            pipeline_id=pipeline_id
        )
    
    def get_resume_context_preview(
        self,
        checkpoint_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get a preview of what the resumed context would look like.
        
        Useful for debugging or UI display without actually resuming.
        
        Args:
            checkpoint_id: The checkpoint ID
            
        Returns:
            Preview of context or None if checkpoint not found
        """
        checkpoint = self.checkpoint_manager.get_checkpoint(checkpoint_id)
        
        if not checkpoint:
            return None
        
        return {
            "checkpoint_id": checkpoint_id,
            "case_id": checkpoint.case_id,
            "pipeline_id": checkpoint.pipeline_id,
            "gate_id": checkpoint.gate_id,
            "resume_point": checkpoint.resume_point,
            "upstream_keys": list(checkpoint.upstream.keys()),
            "hitl_keys": list(checkpoint.hitl.keys()),
            "loop_context": {
                "index": checkpoint.loop_index,
                "total": checkpoint.loop_total,
            } if checkpoint.loop_index is not None else None,
            "created_at": checkpoint.created_at,
        }
    
    def _clean_result_for_serialization(self, obj: Any) -> Any:
        """
        Recursively clean result of non-serializable objects (like AGUIEventEmitter).
        
        This ensures that results can be safely serialized to JSON for storage in the database
        or returned in API responses.
        
        Args:
            obj: The object to clean (can be dict, list, or any other type)
            
        Returns:
            Cleaned object with non-serializable objects removed or replaced
        """
        # Import here to avoid circular dependencies
        from topaz_agent_kit.core.ag_ui_event_emitter import AGUIEventEmitter
        
        # Handle None
        if obj is None:
            return None
        
        # Handle AGUIEventEmitter and other non-serializable objects
        if isinstance(obj, AGUIEventEmitter):
            # Replace emitter with a placeholder string
            return "<AGUIEventEmitter>"
        
        # Handle dict - recursively clean values
        if isinstance(obj, dict):
            cleaned = {}
            for key, value in obj.items():
                # Skip emitter key entirely
                if key == "emitter":
                    continue
                # Recursively clean the value
                cleaned[key] = self._clean_result_for_serialization(value)
            return cleaned
        
        # Handle list - recursively clean items
        if isinstance(obj, list):
            return [self._clean_result_for_serialization(item) for item in obj]
        
        # Handle other non-serializable types
        try:
            # Try to serialize to check if it's serializable
            import json
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            # Not serializable - return string representation
            return f"<{type(obj).__name__}>"