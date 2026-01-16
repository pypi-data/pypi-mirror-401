from __future__ import annotations

import inspect
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, is_dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Optional,
    Union,
    cast,
)

from loguru import logger
from opentelemetry import context as otel_context_api
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from pydantic import BaseModel

from ..db.database import DatabaseManager, PostgresDatabase, MongoDatabase, RedisDatabase
from ..utils.workflow_clone import node_clone
from ..trace.execution_context import (
    ExecutionContext,
    get_current_context,
    reset_current_context,
    set_current_context,
)
from ..utils.register import Register
from .context import Context
from .edge import Edge
from .port import Port
from .workflow_callback import CallbackEvent

if TYPE_CHECKING:
    from .workflow import Workflow


class Node(ABC):
    DEFAULT_INPUT_PORTS: list[Port] = []
    DEFAULT_OUTPUT_PORTS: list[Port] = []

    CLASS_NOT_REQUIRED_TO_REGISTER = ["Node"]
    AUTO_FILL_INPUT_PORTS = []

    def __init__(
        self,
        name: str,
        context: Optional[Context] = None,
        input_edges: Optional[list[Edge]] = None,
        output_edges: Optional[list[Edge]] = None,
        input_ports: list[Port] = DEFAULT_INPUT_PORTS,
        output_ports: list[Port] = DEFAULT_OUTPUT_PORTS,
        query_user: Optional[Callable[[str, str], Awaitable[str]]] = None,
    ) -> None:
        from .workflow_group import WorkflowGroup

        self.name = name
        self.input_edges = [] if input_edges is None else input_edges
        self.output_edges = [] if output_edges is None else output_edges
        self.input_ports = input_ports
        self.output_ports = output_ports
        self.workflow: Optional[Workflow] = None
        self.query_user = query_user
        self.sub_workflows: Optional[WorkflowGroup] = None

        # runtime variables
        self.context = context
        self.input_variables: dict[Port, Any] = {}
        self.num_activated_input_edges = 0
        self._tracer = trace.get_tracer("service_forge.node")

    @property
    def default_postgres_database(self) -> PostgresDatabase | None:
        return self.database_manager.get_default_postgres_database()

    @property
    def default_mongo_database(self) -> MongoDatabase | None:
        return self.database_manager.get_default_mongo_database()

    @property
    def default_redis_database(self) -> RedisDatabase | None:
        return self.database_manager.get_default_redis_database()
    
    @property
    def database_manager(self) -> DatabaseManager:
        assert self.workflow
        return self.workflow.database_manager

    @property
    def global_context(self) -> Context:
        return self.workflow.global_context

    def __init_subclass__(cls) -> None:
        if cls.__name__ not in Node.CLASS_NOT_REQUIRED_TO_REGISTER:
            # TODO: Register currently stores class objects; clarify Register typing vs instance usage.
            node_register.register(cls.__name__, cls)
        return super().__init_subclass__()

    def _query_user(self, prompt: str) -> Awaitable[str]:
        assert self.query_user
        return self.query_user(self.name, prompt)

    def variables_to_params(self) -> dict[str, Any]:
        params = {port.name: self.input_variables[port] for port in self.input_variables.keys() if not port.is_extended_generated}
        for port in self.input_variables.keys():
            if port.is_extended_generated:
                if port.get_extended_name() not in params:
                    params[port.get_extended_name()] = []
                params[port.get_extended_name()].append((port.get_extended_index(), self.input_variables[port]))
                params[port.get_extended_name()].sort()
        return params

    def is_trigger(self) -> bool:
        from .trigger import Trigger
        return isinstance(self, Trigger)

    # TODO: maybe add a function before the run function?

    @abstractmethod
    async def _run(self, **kwargs) -> Union[None, AsyncIterator]:
        ...

    async def clear(self) -> None:
        ...
    
    def run(self) -> Union[None, AsyncIterator]:
        task_id: uuid.UUID | None = None
        for key in list(self.input_variables.keys()):
            if key and key.name[0].isupper():
                del self.input_variables[key]
        params = self.variables_to_params()
        if task_id is not None and "task_id" in self._run.__code__.co_varnames:
            params["task_id"] = task_id
        base_context = get_current_context()
        parent_context = (
            base_context.trace_context
            if base_context and base_context.trace_context
            else otel_context_api.get_current()
        )
        span_name = f"Node {self.name}"

        if inspect.isasyncgenfunction(self._run):
            return self._run_async_generator(
                params, task_id, base_context, parent_context, span_name
            )
        if inspect.iscoroutinefunction(self._run):
            return self._run_async(
                params, task_id, base_context, parent_context, span_name
            )

        return self._run_sync(params, task_id, base_context, parent_context, span_name)

    def _build_execution_context(
        self, base_context: ExecutionContext | None, span: trace.Span
    ) -> ExecutionContext:
        return ExecutionContext(
            trace_context=otel_context_api.get_current(),
            span=span,
            state=base_context.state if base_context else {},
            metadata={
                **(base_context.metadata if base_context else {}),
                "node": self.name,
                "workflow_name": getattr(self.workflow, "name", None),
            },
        )

    @staticmethod
    def _serialize_for_trace(value: Any, max_length: int = 4000) -> tuple[str, bool]:
        def _normalize(val: Any) -> Any:
            if isinstance(val, BaseModel):
                return val.model_dump()
            if hasattr(val, "model_dump"):
                try:
                    return val.model_dump()
                except Exception:
                    pass
            if hasattr(val, "dict"):
                try:
                    return val.dict()
                except Exception:
                    pass
            if is_dataclass is not None and is_dataclass(val):
                return asdict(val) if asdict else val
            if isinstance(val, dict):
                return {k: _normalize(v) for k, v in val.items()}
            if isinstance(val, (list, tuple)):
                return [_normalize(v) for v in val]
            return val

        normalized_value = _normalize(value)
        serialized = json.dumps(normalized_value, ensure_ascii=False, default=str)
        if len(serialized) > max_length:
            return serialized[:max_length], True
        return serialized, False

    def _set_span_attributes(
        self, span: trace.Span, params: dict[str, Any], task_id: uuid.UUID | None
    ) -> None:
        span.set_attribute("node.name", self.name)
        if self.workflow is not None:
            span.set_attribute("workflow.name", self.workflow.name)
        if task_id is not None:
            span.set_attribute("workflow.task_id", str(task_id))
        span.set_attribute("node.input_keys", ",".join(params.keys()))
        serialized_inputs, inputs_truncated = self._serialize_for_trace(params)
        span.set_attribute("node.inputs", serialized_inputs)
        if inputs_truncated:
            span.set_attribute("node.inputs_truncated", True)

    def _record_output(self, span: trace.Span, output: Any) -> None:
        span.set_attribute(
            "node.output_type", type(output).__name__ if output is not None else "None"
        )
        serialized_output, output_truncated = self._serialize_for_trace(output)
        span.set_attribute("node.output", serialized_output)
        if output_truncated:
            span.set_attribute("node.output_truncated", True)

    async def _run_async(
        self,
        params: dict[str, Any],
        task_id: uuid.UUID | None,
        base_context: ExecutionContext | None,
        parent_context: otel_context_api.Context,
        span_name: str,
    ) -> Any:
        with self._tracer.start_as_current_span(
            span_name,
            context=parent_context,
            kind=SpanKind.INTERNAL,
        ) as span:
            self._set_span_attributes(span, params, task_id)
            exec_ctx = self._build_execution_context(base_context, span)
            token = set_current_context(exec_ctx)
            try:
                result = self._run(**params)
                if inspect.isawaitable(result):
                    result = await result
                self._record_output(span, result)
                return result
            finally:
                reset_current_context(token)

    async def _run_async_generator(
        self,
        params: dict[str, Any],
        task_id: uuid.UUID | None,
        base_context: ExecutionContext | None,
        parent_context: otel_context_api.Context,
        span_name: str,
    ) -> AsyncIterator[Any]:
        # Trigger 节点是长期运行的 async generator，这里为每次触发单独生成/关闭 span，避免一个 span 挂载所有请求。
        if self.is_trigger():
            async for item in self._run(**params):
                trigger_parent_context = parent_context
                if hasattr(self, "task_contexts") and isinstance(item, uuid.UUID):
                    trigger_ctx = getattr(self, "task_contexts").get(item)
                    if trigger_ctx is not None:
                        trigger_parent_context = trigger_ctx
                with self._tracer.start_as_current_span(
                    span_name,
                    context=trigger_parent_context,
                    kind=SpanKind.INTERNAL,
                ) as span:
                    self._set_span_attributes(span, params, task_id)
                    span.set_attribute("node.output_type", "async_generator")
                    serialized_item, item_truncated = self._serialize_for_trace(item)
                    span.add_event(
                        "node.output_item",
                        {
                            "value": serialized_item,
                            "truncated": item_truncated,
                        },
                    )
                    exec_ctx = self._build_execution_context(base_context, span)
                    token = set_current_context(exec_ctx)
                    try:
                        yield item
                    finally:
                        reset_current_context(token)
        else:
            with self._tracer.start_as_current_span(
                span_name,
                context=parent_context,
                kind=SpanKind.INTERNAL,
            ) as span:
                self._set_span_attributes(span, params, task_id)
                span.set_attribute("node.output_type", "async_generator")
                exec_ctx = self._build_execution_context(base_context, span)
                token = set_current_context(exec_ctx)
                try:
                    async for item in self._run(**params):
                        serialized_item, item_truncated = self._serialize_for_trace(item)
                        span.add_event(
                            "node.output_item",
                            {
                                "value": serialized_item,
                                "truncated": item_truncated,
                            },
                        )
                        yield item
                finally:
                    reset_current_context(token)

    def _run_sync(
        self,
        params: dict[str, Any],
        task_id: uuid.UUID | None,
        base_context: ExecutionContext | None,
        parent_context: otel_context_api.Context,
        span_name: str,
    ) -> Any:
        with self._tracer.start_as_current_span(
            span_name,
            context=parent_context,
            kind=SpanKind.INTERNAL,
        ) as span:
            self._set_span_attributes(span, params, task_id)
            exec_ctx = self._build_execution_context(base_context, span)
            token = set_current_context(exec_ctx)
            try:
                result = self._run(**params)
                self._record_output(span, result)
                return result
            finally:
                reset_current_context(token)

    def get_input_port_by_name(self, name: str) -> Optional[Port]:
        for port in self.input_ports:
            if port.name == name:
                return port
        return None

    def get_output_port_by_name(self, name: str) -> Optional[Port]:
        for port in self.output_ports:
            if port.name == name:
                return port
        return None

    def try_create_extended_input_port(self, name: str) -> None:
        for port in self.input_ports:
            if port.is_extended and name.startswith(port.name + '_') and name[len(port.name + '_'):].isdigit():
                self.input_ports.append(Port(name=name, type=port.type, node=port.node, port=port.port, value=port.value, default=port.default, is_extended=False, is_extended_generated=True))

    def try_create_extended_output_port(self, name: str) -> None:
        for port in self.output_ports:
            if port.is_extended and name.startswith(port.name + '_') and name[len(port.name + '_'):].isdigit():
                self.output_ports.append(Port(name=name, type=port.type, node=port.node, port=port.port, value=port.value, default=port.default, is_extended=False, is_extended_generated=True))

    def num_input_ports(self) -> int:
        return sum(1 for port in self.input_ports if not port.is_extended)
    
    def is_ready(self) -> bool:
        return self.num_activated_input_edges == self.num_input_ports()

    def fill_input_by_name(self, port_name: str, value: Any) -> None:
        self.try_create_extended_input_port(port_name)
        port = self.get_input_port_by_name(port_name)
        if port is None:
            raise ValueError(f"{port_name} is not a valid input port.")
        self.fill_input(port, value)

    def fill_input(self, port: Port, value: Any) -> None:
        port.activate(value)

    def activate_output_edges(self, port: str | Port, data: Any) -> None:
        if isinstance(port, str):
            port = self.get_output_port_by_name(port)
        for output_edge in self.output_edges:
            if output_edge.start_port == port:
                output_edge.end_port.activate(data)

    # for trigger nodes
    def prepare_output_edges(self, port: Port, data: Any) -> None:
        if isinstance(port, str):
            port = self.get_output_port_by_name(port)
        for output_edge in self.output_edges:
            if output_edge.start_port == port:
                output_edge.end_port.prepare(data)

    def trigger_output_edges(self, port: Port) -> None:
        if isinstance(port, str):
            port = self.get_output_port_by_name(port)
        for output_edge in self.output_edges:
            if output_edge.start_port == port:
                output_edge.end_port.trigger()

    # TODO: the result is outputed to the trigger now, maybe we should add a new function to output the result to the workflow
    def output_to_workflow(self, data: Any) -> None:
        if self.workflow and hasattr(self.workflow, "_handle_workflow_output"):
            handler = cast(
                Callable[[str, Any], None],
                getattr(self.workflow, "_handle_workflow_output"),
            )
            handler(self.name, data)
        else:
            logger.warning("Workflow output handler not set; skipping output dispatch.")

    def extended_output_name(self, name: str, index: int) -> str:
        return name + '_' + str(index)

    def _clone(self, context: Context) -> Node:
        return node_clone(self, context)

    async def stream_output(self, data: Any) -> None:
         await self.workflow.call_callbacks(CallbackEvent.ON_NODE_STREAM_OUTPUT, node=self, output=data)


node_register = Register[Node]()
