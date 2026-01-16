"""
SQS Lambda handler for batch message processing.

Provides a handler specifically designed for SQS-triggered Lambda functions
that need to return batchItemFailures for partial batch failure reporting.
"""

from typing import Dict, Any, Callable, Optional, List, Type, TypeVar
from aws_lambda_powertools import Logger

from .service_pool import ServicePool
from .lambda_event import LambdaEvent

logger = Logger()

T = TypeVar('T')  # Service type


class SqsLambdaHandler:
    """
    Handler for SQS-triggered Lambda functions with batch failure reporting.
    
    Unlike API Gateway handlers, SQS handlers:
    - Process batches of messages from SQS
    - Return batchItemFailures for partial batch failure reporting
    - Don't wrap responses in API Gateway format
    - Don't require requestContext or authentication headers
    
    Example:
        handler = SqsLambdaHandler(
            service_class=DataCleaningHandler,
        )
        
        def lambda_handler(event, context):
            return handler.execute(event, context, process_messages)
        
        def process_messages(event: LambdaEvent, service: DataCleaningHandler) -> Dict:
            # service.handle() should return {"batchItemFailures": [...]}
            return service.handle(event.raw, context=None)
    """
    
    def __init__(
        self,
        service_class: Optional[Type[T]] = None,
        service_kwargs: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize SQS handler.
        
        Args:
            service_class: Service class to instantiate for processing
            service_kwargs: Additional kwargs for service instantiation
            config: Optional configuration dict passed to LambdaEvent
        """
        self.service_class = service_class
        self.service_kwargs = service_kwargs or {}
        self.config = config or {}
        
        # Initialize service pool if a class is provided
        self._service_pool = ServicePool(service_class, **self.service_kwargs) if service_class else None

    def _get_service(self, injected_service: Optional[T] = None) -> Optional[T]:
        """
        Get service instance (injected or from pool).
        
        Args:
            injected_service: Injected service for testing
            
        Returns:
            Service instance
        """
        if injected_service:
            return injected_service
        
        if self._service_pool:
            return self._service_pool.get()
        
        if self.service_class:
            return self.service_class(**self.service_kwargs)

        return None

    def execute(
        self,
        event: Dict[str, Any],
        context: Any,
        business_logic: Callable,
        injected_service: Optional[T] = None
    ) -> Dict[str, Any]:
        """
        Execute the SQS Lambda handler with the given business logic.
        
        Args:
            event: Lambda event dictionary containing SQS Records
            context: Lambda context object
            business_logic: Callable(event: LambdaEvent, service) that returns 
                           {"batchItemFailures": [...]} or similar dict
            injected_service: Optional service instance for testing
            
        Returns:
            Dict with batchItemFailures for partial batch failure reporting
        """
        records = event.get("Records", [])
        logger.info(f"Processing SQS batch with {len(records)} records")
        
        try:
            # Get service instance
            service = self._get_service(injected_service)
            
            # Wrap event in LambdaEvent for convenient access
            lambda_event = LambdaEvent(event, config=self.config)
            
            # Execute business logic - expects dict with batchItemFailures
            result = business_logic(lambda_event, service)
            
            # Validate result format
            if not isinstance(result, dict):
                logger.error(f"Business logic returned {type(result)}, expected dict")
                # Return all messages as failures
                return {
                    "batchItemFailures": [
                        {"itemIdentifier": r.get("messageId", f"unknown-{i}")}
                        for i, r in enumerate(records)
                    ]
                }
            
            # Log results
            failures = result.get("batchItemFailures", [])
            if failures:
                logger.warning(f"Batch processing completed with {len(failures)} failures")
            else:
                logger.info(f"Batch processing completed successfully ({len(records)} messages)")
            
            return result
            
        except Exception as e:
            logger.exception(f"SQS handler execution error: {e}")
            # Return all messages as failures so they can be retried
            return {
                "batchItemFailures": [
                    {"itemIdentifier": r.get("messageId", f"unknown-{i}")}
                    for i, r in enumerate(records)
                ]
            }


def create_sqs_handler(
    service_class: Optional[Type[T]] = None,
    **kwargs
) -> SqsLambdaHandler:
    """
    Convenience function for creating SQS handlers.
    
    Example:
        from geek_cafe_saas_sdk.lambda_handlers import create_sqs_handler
        
        handler = create_sqs_handler(
            service_class=DataCleaningHandler,
        )
        
        def lambda_handler(event, context):
            return handler.execute(event, context, process_batch)
    """
    return SqsLambdaHandler(service_class=service_class, **kwargs)
