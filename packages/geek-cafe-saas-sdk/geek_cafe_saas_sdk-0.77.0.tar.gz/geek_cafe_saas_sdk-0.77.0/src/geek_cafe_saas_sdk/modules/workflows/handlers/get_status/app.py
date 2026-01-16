"""
Get Execution Status Lambda Handler.

GET /executions/{execution-id}/status

Returns the execution with all child steps and an aggregated summary.

Geek Cafe, LLC
MIT License. See Project Root for the license information.
"""

from typing import Any
from geek_cafe_saas_sdk.lambda_handlers import create_handler, LambdaEvent
from geek_cafe_saas_sdk.modules.workflows.services import WorkflowService

handler_wrapper = create_handler(
    service_class=WorkflowService,
    require_body=False,
    convert_request_case=True
)


def lambda_handler(event: dict, context: Any, injected_service=None) -> dict:
    """Lambda entry point."""
    return handler_wrapper.execute(event, context, get_execution_status, injected_service=injected_service)


def get_execution_status(
    event: LambdaEvent,
    service: WorkflowService
) -> Any:
    """
    Get execution status with all steps and summary.
    
    Path parameters:
        execution-id or executionId: Execution ID
        
    Query parameters:
        include_steps: Include child steps (default: true)
        
    Returns:
        {
            "execution": { ... root execution ... },
            "steps": [ ... child executions ... ],
            "summary": {
                "total_steps": 5,
                "completed": 2,
                "running": 1,
                "pending": 2,
                "failed": 0,
                "progress_percent": 40,
                "status_counts": { ... }
            }
        }
    """
    execution_id = event.path("executionId", "id")
    include_steps = event.query_bool("includeSteps", default=True)
    
    return service.get_status(
        execution_id=execution_id,
        include_steps=include_steps,
    )
