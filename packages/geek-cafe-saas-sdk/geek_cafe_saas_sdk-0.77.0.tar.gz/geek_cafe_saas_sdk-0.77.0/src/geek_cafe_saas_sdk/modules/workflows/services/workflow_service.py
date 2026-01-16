"""
Execution service for async task/workflow execution tracking.

Provides CRUD operations and query methods for tracking executions.

Geek Cafe, LLC
MIT License. See Project Root for the license information.
"""

import time
import uuid
from datetime import datetime, UTC, timedelta
from typing import Optional, Dict, Any, List

from aws_lambda_powertools import Logger
from boto3_assist.dynamodb.dynamodb import DynamoDB

from geek_cafe_saas_sdk.core.services.database_service import DatabaseService
from geek_cafe_saas_sdk.core.service_result import ServiceResult
from geek_cafe_saas_sdk.core.error_codes import ErrorCode
from geek_cafe_saas_sdk.core.request_context import RequestContext
from geek_cafe_saas_sdk.lambda_handlers._base.decorators import service_method
from geek_cafe_saas_sdk.core.services.resource_meta_entry_service import (
    ResourceMetaEntryService,
)
from ..models.execution import Workflow, WorkflowStatus, ExecutionType
from .workflow_history_service import WorkflowHistoryService
from .workflow_metrics_service import WorkflowMetricsService

logger = Logger()


class WorkflowService(DatabaseService[Workflow]):
    """
    Service for managing execution tracking.
    
    Provides methods for creating, updating, and querying executions
    with support for hierarchical tracking (root_id, parent_id).
    """

    def __init__(
        self,
        *,
        dynamodb: Optional[DynamoDB] = None,
        table_name: Optional[str] = None,
        request_context: Optional[RequestContext] = None,
        record_history: bool = True,
        **kwargs
    ):
        super().__init__(
            dynamodb=dynamodb,
            table_name=table_name,
            request_context=request_context,
            **kwargs
        )

        self._resource_meta_entry_service: Optional[ResourceMetaEntryService] = None
        self._execution_history_service: Optional[WorkflowHistoryService] = None
        self._record_history: bool = record_history
    # =========================================================================
    # Create Operations
    # =========================================================================

    @service_method("create_execution")
    def create(
        self,
        name: str,
        execution_type: str = ExecutionType.CUSTOM,
        parent_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        description: Optional[str] = None,
        resource_arn: Optional[str] = None,
        execution_arn: Optional[str] = None,
        triggered_by: Optional[str] = None,
        triggered_by_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        input_payload: Optional[Dict[str, Any]] = None,
        total_steps: Optional[int] = None,
        max_retries: int = 3,
        ttl_days: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ServiceResult[Workflow]:
        """
        Create a new execution record.
        
        Args:
            name: Human-readable name for the execution
            execution_type: Type of execution (step_function, lambda, sqs, etc.)
            parent_id: Parent execution ID (for child executions)
            correlation_id: Correlation ID for cross-service tracking
            idempotency_key: Key to prevent duplicate processing
            description: Optional description
            resource_arn: AWS ARN of the resource (Step Function ARN, etc.)
            execution_arn: Specific execution ARN
            triggered_by: What initiated this (s3_event, api_call, schedule, etc.)
            triggered_by_id: ID of the trigger
            resource_id: ID of the resource being processed
            resource_type: Type of resource (file, directory, etc.)
            input_payload: Input data for the execution
            total_steps: Total number of steps if known
            max_retries: Maximum retry attempts (default: 3)
            ttl_days: Days until auto-expiration (None = no TTL)
            metadata: Additional metadata
            
        Returns:
            ServiceResult with created Execution
        """
        try:
            # Check for duplicate via idempotency key
            if idempotency_key:
                existing = self._find_by_idempotency_key(idempotency_key)
                if existing:
                    logger.info(f"Returning existing execution for idempotency_key: {idempotency_key}")
                    return ServiceResult.success_result(existing)
            
            execution = Workflow()
            execution.id = str(uuid.uuid4())
            execution.name = name
            execution.execution_type = execution_type
            execution.description = description
            execution.status = WorkflowStatus.PENDING
            
            # Hierarchy
            if parent_id:
                # Get parent to inherit root_id
                parent = self._get_by_id(parent_id, Workflow)
                if parent:
                    execution.parent_id = parent_id
                    execution.root_id = parent.root_id  # Inherit root from parent
                    # Update parent's child count
                    self._increment_child_count(parent_id)
                else:
                    logger.warning(f"Parent execution {parent_id} not found, creating as root")
                    execution.root_id = execution.id
            else:
                # This is a root execution
                execution.root_id = execution.id
            
            # Correlation
            execution.correlation_id = correlation_id or str(uuid.uuid4())
            execution.idempotency_key = idempotency_key
            
            # AWS resources
            execution.resource_arn = resource_arn
            execution.execution_arn = execution_arn
            
            # Context
            execution.triggered_by = triggered_by
            execution.triggered_by_id = triggered_by_id
            
            # Linked resource
            execution.resource_id = resource_id
            execution.resource_type = resource_type
            
            # Input/Output
            execution.input_payload = input_payload
            
            # Progress
            execution.total_steps = total_steps
            execution.progress_percent = 0
            
            # Retries
            execution.max_retries = max_retries
            execution.retry_count = 0
            
            # TTL (optional)
            if ttl_days:
                ttl_timestamp = int((datetime.now(UTC) + timedelta(days=ttl_days)).timestamp())
                execution.ttl = ttl_timestamp
            
            # Metadata
            execution.metadata = metadata
            
            # Inject security context from request
            if self.request_context:
                execution.tenant_id = self.request_context.authenticated_tenant_id
                execution.owner_id = self.request_context.authenticated_user_id
                execution.user_id = self.request_context.authenticated_user_id
            
            # Save
            execution.prep_for_save()
            result = self._save_model(execution)
            
            if result.success:
                self._emit_execution_event("execution.created", execution)
                self._record_history_event(
                    execution=execution,
                    event_type="created",
                    to_status=WorkflowStatus.PENDING,
                    message=f"Execution '{name}' created",
                    metadata={"name": name, "execution_type": execution_type},
                )
            
            return result
            
        except Exception as e:
            logger.exception(f"Error creating execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    # =========================================================================
    # Status Update Operations
    # =========================================================================

    @service_method("start_execution")
    def start(self, execution_id: str) -> ServiceResult[Workflow]:
        """
        Mark an execution as started (RUNNING).
        
        Args:
            execution_id: ID of the execution to start
            
        Returns:
            ServiceResult with updated Execution
        """
        try:
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            if not WorkflowStatus.can_transition(execution.status, WorkflowStatus.RUNNING):
                return ServiceResult.error_result(
                    message=f"Cannot start execution in status '{execution.status}'",
                    error_code=ErrorCode.VALIDATION_ERROR
                )
            
            now = datetime.now(UTC)
            execution.status = WorkflowStatus.RUNNING
            execution.started_utc = now.isoformat()
            execution.started_utc_ts = now.timestamp()
            
            # If execution was throttled, mark it as released now that it's running
            if execution.queue_state == "throttled":
                execution.queue_state = "released"
            
            execution.prep_for_save()
            result = self._save_model(execution)
            
            if result.success:
                self._emit_execution_event("execution.started", execution)
                self._record_history_event(
                    execution=execution,
                    event_type="started",
                    from_status=WorkflowStatus.PENDING,
                    to_status=WorkflowStatus.RUNNING,
                    message="Execution started",
                )
            
            return result
            
        except Exception as e:
            logger.exception(f"Error starting execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("update_progress")
    def update_progress(
        self,
        execution_id: str,
        progress_percent: Optional[int] = None,
        current_step: Optional[str] = None,
        current_step_index: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ServiceResult[Workflow]:
        """
        Update execution progress.
        
        Args:
            execution_id: ID of the execution
            progress_percent: Progress percentage (0-100)
            current_step: Current step name
            current_step_index: Current step index (0-based)
            metadata: Additional metadata to merge
            
        Returns:
            ServiceResult with updated Execution
        """
        try:
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            if execution.is_terminal():
                return ServiceResult.error_result(
                    message=f"Cannot update progress for terminal execution (status: {execution.status})",
                    error_code=ErrorCode.VALIDATION_ERROR
                )
            
            if progress_percent is not None:
                execution.progress_percent = progress_percent
            if current_step is not None:
                execution.current_step = current_step
            if current_step_index is not None:
                execution.current_step_index = current_step_index
            if metadata:
                existing = execution.metadata or {}
                existing.update(metadata)
                execution.metadata = existing
            
            execution.prep_for_save()
            result = self._save_model(execution)
            
            if result.success:
                self._emit_execution_event("execution.progress", execution)
            
            return result
            
        except Exception as e:
            logger.exception(f"Error updating execution progress: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("complete_execution")
    def complete(
        self,
        execution_id: str,
        output_payload: Optional[Dict[str, Any]] = None,
    ) -> ServiceResult[Workflow]:
        """
        Mark an execution as successfully completed.
        
        Args:
            execution_id: ID of the execution
            output_payload: Result data from the execution
            
        Returns:
            ServiceResult with updated Execution
        """
        try:
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            if not WorkflowStatus.can_transition(execution.status, WorkflowStatus.SUCCEEDED):
                return ServiceResult.error_result(
                    message=f"Cannot complete execution in status '{execution.status}'",
                    error_code=ErrorCode.VALIDATION_ERROR
                )
            
            now = datetime.now(UTC)
            execution.status = WorkflowStatus.SUCCEEDED
            execution.completed_utc = now.isoformat()
            execution.completed_utc_ts = now.timestamp()
            execution.progress_percent = 100
            execution.output_payload = output_payload
            
            # Calculate duration
            if execution.started_utc_ts:
                execution.duration_ms = int((now.timestamp() - execution.started_utc_ts) * 1000)
            
            execution.prep_for_save()
            result = self._save_model(execution)
            
            if result.success:
                self._emit_execution_event("execution.succeeded", execution)
                self._record_history_event(
                    execution=execution,
                    event_type="succeeded",
                    from_status=WorkflowStatus.RUNNING,
                    to_status=WorkflowStatus.SUCCEEDED,
                    message="Execution completed successfully",
                    duration_ms=execution.duration_ms,
                )
                # Update parent's completed child count
                if execution.parent_id:
                    self._increment_completed_child_count(execution.parent_id)
                
                # Decrement metrics counters
                self._cleanup_execution_metrics(
                    execution=execution,
                    success=True,
                )
            
            return result
            
        except Exception as e:
            logger.exception(f"Error completing execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("fail_execution")
    def fail(
        self,
        execution_id: str,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        error_details: Optional[Dict[str, Any]] = None,
    ) -> ServiceResult[Workflow]:
        """
        Mark an execution as failed.
        
        Args:
            execution_id: ID of the execution
            error_code: Error code
            error_message: Error message
            error_details: Additional error details
            
        Returns:
            ServiceResult with updated Execution
        """
        try:
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            if not WorkflowStatus.can_transition(execution.status, WorkflowStatus.FAILED):
                return ServiceResult.error_result(
                    message=f"Cannot fail execution in status '{execution.status}'",
                    error_code=ErrorCode.VALIDATION_ERROR
                )
            
            now = datetime.now(UTC)
            execution.status = WorkflowStatus.FAILED
            execution.completed_utc = now.isoformat()
            execution.completed_utc_ts = now.timestamp()
            execution.error_code = error_code
            execution.error_message = error_message
            execution.error_details = error_details
            
            execution.set_error_key(
                "workflow_failure",
                {
                    "error_code": error_code,
                    "error_message": error_message,
                    "error_details": error_details,
                }
            )
            # Calculate duration
            if execution.started_utc_ts:
                execution.duration_ms = int((now.timestamp() - execution.started_utc_ts) * 1000)
            
            execution.prep_for_save()
            result = self._save_model(execution)
            
            if result.success:
                self._emit_execution_event("execution.failed", execution)
                self._record_history_event(
                    execution=execution,
                    event_type="failed",
                    from_status=WorkflowStatus.RUNNING,
                    to_status=WorkflowStatus.FAILED,
                    message=f"Execution failed: {error_message or 'Unknown error'}",
                    duration_ms=execution.duration_ms,
                    error_code=error_code,
                    error_message=error_message,
                    error_details=error_details,
                )
                # Update parent's failed child count
                if execution.parent_id:
                    self._increment_failed_child_count(execution.parent_id)
                
                # Decrement metrics counters
                self._cleanup_execution_metrics(
                    execution=execution,
                    success=False,
                )
            
            return result
            
        except Exception as e:
            logger.exception(f"Error failing execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("cancel_execution")
    def cancel(self, execution_id: str) -> ServiceResult[Workflow]:
        """
        Cancel an execution.
        
        Args:
            execution_id: ID of the execution to cancel
            
        Returns:
            ServiceResult with updated Execution
        """
        try:
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            if not WorkflowStatus.can_transition(execution.status, WorkflowStatus.CANCELLED):
                return ServiceResult.error_result(
                    message=f"Cannot cancel execution in status '{execution.status}'",
                    error_code=ErrorCode.VALIDATION_ERROR
                )
            
            now = datetime.now(UTC)
            execution.status = WorkflowStatus.CANCELLED
            execution.completed_utc = now.isoformat()
            execution.completed_utc_ts = now.timestamp()
            
            # Calculate duration
            if execution.started_utc_ts:
                execution.duration_ms = int((now.timestamp() - execution.started_utc_ts) * 1000)
            
            execution.prep_for_save()
            result = self._save_model(execution)
            
            if result.success:
                self._emit_execution_event("execution.cancelled", execution)
                self._record_history_event(
                    execution=execution,
                    event_type="cancelled",
                    from_status=WorkflowStatus.RUNNING,
                    to_status=WorkflowStatus.CANCELLED,
                    message="Execution cancelled",
                    duration_ms=execution.duration_ms,
                )
                
                # Decrement metrics counters (treat as failure)
                self._cleanup_execution_metrics(
                    execution=execution,
                    success=False,
                )
            
            return result
            
        except Exception as e:
            logger.exception(f"Error cancelling execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("retry_execution")
    def retry(self, execution_id: str) -> ServiceResult[Workflow]:
        """
        Retry a failed or timed-out execution.
        
        Args:
            execution_id: ID of the execution to retry
            
        Returns:
            ServiceResult with updated Execution (reset to PENDING)
        """
        try:
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            if not execution.can_retry():
                return ServiceResult.error_result(
                    message=f"Cannot retry execution (status: {execution.status}, retries: {execution.retry_count}/{execution.max_retries})",
                    error_code=ErrorCode.VALIDATION_ERROR
                )
            
            # Reset for retry
            execution.status = WorkflowStatus.PENDING
            execution.retry_count += 1
            execution.started_utc = None
            execution.started_utc_ts = None
            execution.completed_utc = None
            execution.completed_utc_ts = None
            execution.duration_ms = None
            execution.progress_percent = 0
            execution.current_step = None
            execution.current_step_index = None
            execution.error_code = None
            execution.error_message = None
            execution.error_details = None
            execution.output_payload = None
            
            execution.prep_for_save()
            result = self._save_model(execution)
            
            if result.success:
                self._emit_execution_event("execution.retried", execution)
                self._record_history_event(
                    execution=execution,
                    event_type="retried",
                    from_status=WorkflowStatus.FAILED,
                    to_status=WorkflowStatus.PENDING,
                    message=f"Execution retried (attempt {execution.retry_count})",
                    metadata={"retry_count": execution.retry_count},
                )
            
            return result
            
        except Exception as e:
            logger.exception(f"Error retrying execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    # =========================================================================
    # Read Operations
    # =========================================================================

    @service_method("get_execution")
    def get(self, execution_id: str) -> ServiceResult[Workflow]:
        """
        Get an execution by ID.
        
        Args:
            execution_id: ID of the execution
            
        Returns:
            ServiceResult with Execution
        """
        try:
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            return ServiceResult.success_result(execution)
        except Exception as e:
            logger.exception(f"Error getting execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    # =========================================================================
    # Abstract Method Implementations (required by DatabaseService)
    # =========================================================================

    def get_by_id(self, **kwargs) -> ServiceResult[Workflow]:
        """
        Get execution by ID (abstract method implementation).
        
        Args:
            execution_id: ID of the execution
            
        Returns:
            ServiceResult with Execution
        """
        execution_id = kwargs.get("execution_id") or kwargs.get("id")
        return self.get(execution_id)

    def update(self, **kwargs) -> ServiceResult[Workflow]:
        """
        Update execution (abstract method implementation).
        
        For executions, use specific methods like start(), complete(), fail(), etc.
        This generic update is provided for interface compliance.
        
        Args:
            execution_id: ID of the execution
            **kwargs: Fields to update
            
        Returns:
            ServiceResult with updated Execution
        """
        try:
            execution_id = kwargs.get("execution_id") or kwargs.get("id")
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            # Update allowed fields
            if "metadata" in kwargs:
                existing = execution.metadata or {}
                existing.update(kwargs["metadata"])
                execution.metadata = existing
            
            execution.prep_for_save()
            return self._save_model(execution)
            
        except Exception as e:
            logger.exception(f"Error updating execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    def delete(self, **kwargs) -> ServiceResult[bool]:
        """
        Delete execution (abstract method implementation).
        
        Args:
            execution_id: ID of the execution to delete
            
        Returns:
            ServiceResult with boolean success
        """
        try:
            execution_id = kwargs.get("execution_id") or kwargs.get("id")
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            return self._delete_model(execution)
            
        except Exception as e:
            logger.exception(f"Error deleting execution: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("list_by_root")
    def list_by_root(
        self,
        root_id: str,
        limit: int = 50,
        ascending: bool = False,
    ) -> ServiceResult[List[Workflow]]:
        """
        List all executions in a chain by root_id.
        
        Args:
            root_id: Root execution ID
            limit: Maximum results
            ascending: Sort order by started_utc
            
        Returns:
            ServiceResult with list of Executions
        """
        try:
            user_id = self.request_context.authenticated_user_id
            tenant_id = self.request_context.authenticated_tenant_id
            
            query_model = Workflow()
            query_model.tenant_id = tenant_id
            query_model.owner_id = user_id
            query_model.root_id = root_id
            
            return self._query_by_index(
                query_model, "gsi1", limit=limit, ascending=ascending
            )
            
        except Exception as e:
            logger.exception(f"Error listing executions by root: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("list_children")
    def list_children(
        self,
        parent_id: str,
        limit: int = 50,
        ascending: bool = False,
    ) -> ServiceResult[List[Workflow]]:
        """
        List direct children of an execution.
        
        Args:
            parent_id: Parent execution ID
            limit: Maximum results
            ascending: Sort order by started_utc
            
        Returns:
            ServiceResult with list of child Executions
        """
        try:
            user_id = self.request_context.authenticated_user_id
            tenant_id = self.request_context.authenticated_tenant_id
            
            query_model = Workflow()
            query_model.tenant_id = tenant_id
            query_model.owner_id = user_id
            query_model.parent_id = parent_id
            
            return self._query_by_index(
                query_model, "gsi2", limit=limit, ascending=ascending
            )
            
        except Exception as e:
            logger.exception(f"Error listing child executions: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("list_by_status")
    def list_by_status(
        self,
        status: str,
        limit: int = 50,
        ascending: bool = False,
    ) -> ServiceResult[List[Workflow]]:
        """
        List executions by status.
        
        Args:
            status: Execution status to filter by
            limit: Maximum results
            ascending: Sort order by started_utc
            
        Returns:
            ServiceResult with list of Executions
        """
        try:
            user_id = self.request_context.authenticated_user_id
            tenant_id = self.request_context.authenticated_tenant_id
            
            query_model = Workflow()
            query_model.tenant_id = tenant_id
            query_model.owner_id = user_id
            query_model.status = status
            
            return self._query_by_index(
                query_model, "gsi3", limit=limit, ascending=ascending
            )
            
        except Exception as e:
            logger.exception(f"Error listing executions by status: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("list_by_correlation")
    def list_by_correlation(
        self,
        correlation_id: str,
        limit: int = 50,
        ascending: bool = False,
    ) -> ServiceResult[List[Workflow]]:
        """
        List executions by correlation ID (cross-service tracking).
        
        Args:
            correlation_id: Correlation ID
            limit: Maximum results
            ascending: Sort order by started_utc
            
        Returns:
            ServiceResult with list of Executions
        """
        try:
            tenant_id = self.request_context.authenticated_tenant_id
            
            query_model = Workflow()
            query_model.tenant_id = tenant_id
            query_model.correlation_id = correlation_id
            
            return self._query_by_index(
                query_model, "gsi4", limit=limit, ascending=ascending
            )
            
        except Exception as e:
            logger.exception(f"Error listing executions by correlation: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("list_by_execution_type")
    def list_by_execution_type(
        self,
        execution_type: str,
        status: Optional[str] = None,
        limit: int = 50,
        ascending: bool = False,
    ) -> ServiceResult[List[Workflow]]:
        """
        List executions by execution type with optional status filter.
        
        Uses GSI5: tenant/owner + execution_type + status + timestamp
        
        Args:
            execution_type: Type of execution (step_function, lambda, etc.)
            status: Optional status filter (pending, running, succeeded, etc.)
            limit: Maximum results
            ascending: Sort order by started_utc timestamp
            
        Returns:
            ServiceResult with list of Executions
            
        Examples:
            # All lambda executions
            service.list_by_execution_type("lambda")
            
            # Only running lambda executions
            service.list_by_execution_type("lambda", status="running")
        """
        try:
            user_id = self.request_context.authenticated_user_id
            tenant_id = self.request_context.authenticated_tenant_id
            
            query_model = Workflow()
            query_model.tenant_id = tenant_id
            query_model.owner_id = user_id
            query_model.execution_type = execution_type
            query_model.status = status
            index_name = "gsi4"
            # Set status gsi5 if provided for filtering
            if status:
                index_name = "gsi5"
            # Leave status empty for begins_with query on execution_type only
            
            return self._query_by_index(
                query_model, index_name, limit=limit, ascending=ascending
            )
            
        except Exception as e:
            logger.exception(f"Error listing executions by type: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )

    @service_method("get_execution_status")
    def get_status(
        self,
        execution_id: str,
        include_steps: bool = True,
    ) -> ServiceResult[Dict[str, Any]]:
        """
        Get execution status with all WorkflowStep records and summary.
        
        Returns the execution along with all its WorkflowStep records and an
        aggregated summary of step progress.
        
        Note: This queries WorkflowStep records (1...n steps per workflow).
        For parent-child workflow chains, use get_lineage() instead.
        
        Args:
            execution_id: ID of the execution
            include_steps: If True, include all WorkflowStep records (default: True)
            
        Returns:
            ServiceResult with dict containing:
            - execution: The execution
            - steps: List of WorkflowStep records (if include_steps=True)
            - summary: Aggregated status counts and progress from steps
        """
        try:
            # Get the execution
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            # Get WorkflowStep records for this execution
            from .workflow_step_service import WorkflowStepService
            
            step_service = WorkflowStepService(
                dynamodb=self.dynamodb,
                table_name=self.table_name,
                request_context=self.request_context
            )
            
            steps_result = step_service.get_steps_for_execution(execution_id)
            if not steps_result.success:
                return ServiceResult.error_result(
                    message=f"Failed to fetch steps: {steps_result.message}",
                    error_code=steps_result.error_code
                )
            
            steps = steps_result.data or []
            
            # Calculate summary from WorkflowStep records
            summary = self._calculate_status_summary_from_workflow_steps(steps)
            
            # Use execution's progress_percent if it's higher than calculated
            # This handles cases where workflow orchestration sets progress before steps complete
            if execution.progress_percent is not None and execution.progress_percent > summary["progress_percent"]:
                summary["progress_percent"] = execution.progress_percent
            
            # Build response
            response = {
                "execution": execution.to_api_dict() if hasattr(execution, 'to_api_dict') else execution.to_dict(),
                "summary": summary,
            }
            
            if include_steps:
                response["steps"] = [
                    step.to_api_dict() if hasattr(step, 'to_api_dict') else step.to_dict()
                    for step in steps
                ]
            
            return ServiceResult.success_result(response)
            
        except Exception as e:
            logger.exception(f"Error getting execution status: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )
    
    @service_method("get_execution_lineage")
    def get_lineage(
        self,
        execution_id: str,
        include_children: bool = True,
    ) -> ServiceResult[Dict[str, Any]]:
        """
        Get execution lineage (parent-child workflow chain).
        
        Returns the execution along with all child workflow executions in the chain.
        This does NOT include WorkflowStep records - use get_status() for that.
        
        Args:
            execution_id: ID of the execution
            include_children: If True, include child workflow executions (default: True)
            
        Returns:
            ServiceResult with dict containing:
            - execution: The root execution
            - children: List of child Workflow executions (if include_children=True)
            - summary: Aggregated status counts from child workflows
        """
        try:
            # Get the execution
            execution = self._get_by_id(execution_id, Workflow)
            if not execution:
                return ServiceResult.error_result(
                    message=f"Execution {execution_id} not found",
                    error_code=ErrorCode.NOT_FOUND
                )
            
            # Determine root_id (execution might be a child)
            root_id = execution.root_id or execution_id
            
            # Get all executions in the chain
            children_result = self.list_by_root(root_id, limit=500)
            if not children_result.success:
                return ServiceResult.error_result(
                    message=f"Failed to fetch child workflows: {children_result.message}",
                    error_code=children_result.error_code
                )
            
            all_executions = children_result.data or []
            
            # Separate root from children
            root_execution = None
            children = []
            for exec in all_executions:
                if exec.id == root_id:
                    root_execution = exec
                else:
                    children.append(exec)
            
            # If we didn't find root in list, use original
            if root_execution is None:
                root_execution = execution
            
            # Calculate summary from child Workflow executions
            summary = self._calculate_status_summary_from_workflows(children)
            
            # Build response
            response = {
                "execution": root_execution.to_api_dict() if hasattr(root_execution, 'to_api_dict') else root_execution.to_dict(),
                "summary": summary,
            }
            
            if include_children:
                response["children"] = [
                    child.to_api_dict() if hasattr(child, 'to_api_dict') else child.to_dict()
                    for child in children
                ]
            
            return ServiceResult.success_result(response)
            
        except Exception as e:
            logger.exception(f"Error getting execution lineage: {e}")
            return ServiceResult.error_result(
                message=str(e),
                error_code=ErrorCode.INTERNAL_ERROR
            )
    
    def _calculate_status_summary_from_workflow_steps(self, steps: List) -> Dict[str, Any]:
        """
        Calculate aggregated status summary from WorkflowStep records.
        
        Args:
            steps: List of WorkflowStep objects
            
        Returns:
            Summary dict with counts and progress percentage
        """
        from .workflow_step_service import StepStatus
        
        total = len(steps)
        
        status_counts = {
            "pending": 0,
            "running": 0,
            "succeeded": 0,  # Maps to StepStatus.COMPLETED
            "failed": 0,
            "cancelled": 0,
            "timed_out": 0,
        }
        
        for step in steps:
            status = step.status or StepStatus.PENDING
            
            # Map WorkflowStep statuses to summary statuses
            if status == StepStatus.COMPLETED:
                status_counts["succeeded"] += 1
            elif status == StepStatus.PENDING:
                status_counts["pending"] += 1
            elif status == StepStatus.RUNNING or status == StepStatus.DISPATCHED:
                status_counts["running"] += 1
            elif status == StepStatus.FAILED:
                status_counts["failed"] += 1
            elif status == StepStatus.CANCELLED:
                status_counts["cancelled"] += 1
            elif status == StepStatus.TIMED_OUT:
                status_counts["timed_out"] += 1
            # SKIPPED steps are not counted in any category
        
        # Calculate progress percentage
        completed = status_counts["succeeded"]
        failed = status_counts["failed"] + status_counts["cancelled"] + status_counts["timed_out"]
        in_progress = status_counts["running"]
        pending = status_counts["pending"]
        
        progress_percent = 0
        if total > 0:
            # Count completed + failed as "done" for progress
            done = completed + failed
            progress_percent = int((done / total) * 100)
        
        return {
            "total_steps": total,
            "completed": completed,
            "failed": failed,
            "running": in_progress,
            "pending": pending,
            "progress_percent": progress_percent,
            "status_counts": status_counts,
        }
    
    def _calculate_status_summary_from_workflows(self, workflows: List[Workflow]) -> Dict[str, Any]:
        """
        Calculate aggregated status summary from child Workflow executions.
        
        Args:
            workflows: List of Workflow objects
            
        Returns:
            Summary dict with counts and progress percentage
        """
        total = len(workflows)
        
        status_counts = {
            "pending": 0,
            "running": 0,
            "succeeded": 0,
            "failed": 0,
            "cancelled": 0,
            "timed_out": 0,
        }
        
        for workflow in workflows:
            status = workflow.status or "pending"
            if status in status_counts:
                status_counts[status] += 1
        
        # Calculate progress percentage
        completed = status_counts["succeeded"]
        failed = status_counts["failed"] + status_counts["cancelled"] + status_counts["timed_out"]
        in_progress = status_counts["running"]
        pending = status_counts["pending"]
        
        progress_percent = 0
        if total > 0:
            # Count completed + failed as "done" for progress
            done = completed + failed
            progress_percent = int((done / total) * 100)
        
        return {
            "total_steps": total,
            "completed": completed,
            "failed": failed,
            "running": in_progress,
            "pending": pending,
            "progress_percent": progress_percent,
            "status_counts": status_counts,
        }

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _find_by_idempotency_key(self, idempotency_key: str) -> Optional[Workflow]:
        """Find an execution by idempotency key (scan - use sparingly)."""
        # Note: For production, consider adding a GSI for idempotency_key
        # For now, this is a simple scan with filter
        # This should be rare since idempotency is typically checked on creation
        return None  # TODO: Implement if needed

    def _increment_child_count(self, parent_id: str) -> None:
        """Increment the child_count of a parent execution."""
        try:
            parent = self._get_by_id(parent_id, Workflow)
            if parent:
                parent.child_count += 1
                parent.prep_for_save()
                self._save_model(parent)
        except Exception as e:
            logger.warning(f"Failed to increment child count for {parent_id}: {e}")

    def _increment_completed_child_count(self, parent_id: str) -> None:
        """Increment the completed_child_count of a parent execution."""
        try:
            parent = self._get_by_id(parent_id, Workflow)
            if parent:
                parent.completed_child_count += 1
                parent.prep_for_save()
                self._save_model(parent)
        except Exception as e:
            logger.warning(f"Failed to increment completed child count for {parent_id}: {e}")

    def _increment_failed_child_count(self, parent_id: str) -> None:
        """Increment the failed_child_count of a parent execution."""
        try:
            parent = self._get_by_id(parent_id, Workflow)
            if parent:
                parent.failed_child_count += 1
                parent.prep_for_save()
                self._save_model(parent)
        except Exception as e:
            logger.warning(f"Failed to increment failed child count for {parent_id}: {e}")

    def _emit_execution_event(self, event_type: str, execution: Workflow) -> None:
        """
        Emit an execution event (placeholder for future implementation).
        
        This will eventually publish to SNS/EventBridge for downstream consumers.
        
        Args:
            event_type: Type of event (execution.created, execution.started, etc.)
            execution: The execution that triggered the event
        """
        # TODO: Implement event emission to SNS/EventBridge
        logger.info(
            f"[EVENT NOT IMPLEMENTED] Would emit event: {event_type}",
            extra={
                "event_type": event_type,
                "execution_id": execution.id,
                "status": execution.status,
                "correlation_id": execution.correlation_id,
            }
        )

    @property
    def resource_meta_entry_service(self) -> ResourceMetaEntryService:
        """Lazy-loaded resource meta entry service."""
        if self._resource_meta_entry_service is None:
            self._resource_meta_entry_service = ResourceMetaEntryService(
                dynamodb=self.dynamodb,
                table_name=self.table_name,
                request_context=self.request_context,
                resource_type="execution",
            )
        return self._resource_meta_entry_service

    @property
    def history_service(self) -> WorkflowHistoryService:
        """Lazy-loaded execution history service."""
        if self._execution_history_service is None:
            self._execution_history_service = WorkflowHistoryService(
                dynamodb=self.dynamodb,
                table_name=self.table_name,
                request_context=self.request_context,
            )
        return self._execution_history_service

    def _cleanup_execution_metrics(
        self,
        execution: Workflow,
        success: bool,
    ) -> None:
        """
        Cleanup execution metrics when execution completes or fails.
        
        Decrements active count and increments completed/failed totals.
        This prevents metric counters from accumulating forever.
        
        Args:
            execution: The completed/failed execution
            success: True if execution succeeded, False if failed
        """
        try:
            # Only cleanup metrics for root executions (not child executions)
            # Child executions don't increment metrics, so shouldn't decrement
            if execution.parent_id:
                return
            
            # Get execution type for metric_type
            metric_type = execution.execution_type or "execution"
            
            # Get user_id from execution
            user_id = execution.user_id
            if not user_id:
                logger.warning(f"No user_id on execution {execution.id}, skipping metrics cleanup")
                return
            
            # Create metrics service
            metrics_service = WorkflowMetricsService(
                dynamodb=self.dynamodb,
                table_name=self.table_name,
                request_context=self.request_context,
            )
            
            # Calculate profile count if available
            profile_count = 0
            if execution.output_payload:
                profile_count = execution.output_payload.get("profile_count", 0)
            
            # Decrement active count and update totals
            result = metrics_service.complete_execution(
                user_id=user_id,
                metric_type=metric_type,
                success=success,
                profile_count=profile_count,
                duration_ms=execution.duration_ms or 0,
            )
            
            if not result.success:
                logger.warning(
                    f"Failed to cleanup metrics for execution {execution.id}: {result.message}"
                )
            else:
                logger.info(
                    f"Cleaned up metrics for execution {execution.id}: "
                    f"user={user_id}, type={metric_type}, success={success}"
                )
                
        except Exception as e:
            # Log but don't fail the completion/failure operation
            logger.warning(f"Error cleaning up metrics for execution {execution.id}: {e}")

    def _record_history_event(
        self,
        execution: Workflow,
        event_type: str,
        from_status: Optional[str] = None,
        to_status: Optional[str] = None,
        message: Optional[str] = None,
        duration_ms: Optional[int] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        error_details: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record a history event for an execution.
        
        This is called automatically by state-changing methods when record_history is True.
        Failures are logged but do not fail the parent operation.
        """
        if not self._record_history:
            return
        
        try:
            self.history_service.create(
                execution_id=execution.id,
                event_type=event_type,
                from_status=from_status,
                to_status=to_status,
                message=message,
                duration_ms=duration_ms,
                error_code=error_code,
                error_message=error_message,
                error_details=error_details,
                metadata=metadata,
            )
        except Exception as e:
            logger.warning(f"Failed to record history event for {execution.id}: {e}")