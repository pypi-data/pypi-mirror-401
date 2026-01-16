from contextlib import asynccontextmanager
from opentelemetry.trace import SpanKind
from opentelemetry import context as otel_context_api
from opentelemetry.context import Context
from service_forge.workflow.trigger_event import TriggerEvent
from .execution_context import (
    ExecutionContext,
    get_current_context,
    reset_current_context,
    set_current_context,
)

class TraceScope:
    def __init__(self, tracer, service_name: str):
        self._tracer = tracer
        self._service_name = service_name

    def _resolve_parent_context(self, *, base_context, trigger_node, task_id) -> Context:
        if hasattr(trigger_node, "task_contexts"):
            ctx = trigger_node.task_contexts.pop(task_id, None)
            if ctx:
                return ctx

        if base_context and base_context.trace_context:
            return base_context.trace_context

        return otel_context_api.get_current()

    @asynccontextmanager
    async def workflow_span(
        self,
        *,
        workflow_name: str,
        event: TriggerEvent,
        base_context,
        span_kind=SpanKind.INTERNAL,
        extra_attributes: dict | None = None,
    ):
        parent_context = event.trace_context
        # parent_context = self._resolve_parent_context(
        #     base_context=base_context,
        #     trigger_node=trigger_node,
        #     task_id=task_id,
        # )

        span_name = f"Workflow {workflow_name}"
        token = None

        with self._tracer.start_as_current_span(
            span_name,
            context=parent_context,
            kind=span_kind,
        ) as span:
            span.set_attribute("workflow.name", workflow_name)
            span.set_attribute("workflow.task_id", str(event.task_id))
            span.set_attribute("service.name", self._service_name)

            if extra_attributes:
                for k, v in extra_attributes.items():
                    span.set_attribute(k, v)

            execution_context = ExecutionContext(
                trace_context=otel_context_api.get_current(),
                span=span,
                metadata={
                    **(base_context.metadata if base_context else {}),
                    "workflow_name": workflow_name,
                    "task_id": str(event.task_id),
                },
            )

            token = set_current_context(execution_context)
            try:
                yield execution_context
            finally:
                if token is not None:
                    reset_current_context(token)