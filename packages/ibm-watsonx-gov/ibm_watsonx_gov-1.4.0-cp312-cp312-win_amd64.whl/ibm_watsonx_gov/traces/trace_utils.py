# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import json
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

from ibm_watsonx_gov.clients.api_client import APIClient
from ibm_watsonx_gov.config.agentic_ai_configuration import \
    AgenticAIConfiguration
from ibm_watsonx_gov.entities.agentic_app import (AgenticApp,
                                                  MetricsConfiguration, Node)
from ibm_watsonx_gov.entities.enums import (EvaluatorFields, MessageStatus,
                                            MetricGroup)
from ibm_watsonx_gov.entities.evaluation_result import (AgentMetricResult,
                                                        MessageData,
                                                        MetricMapping,
                                                        MetricsMappingData,
                                                        NodeData)
from ibm_watsonx_gov.entities.foundation_model import FoundationModelInfo
from ibm_watsonx_gov.entities.metric import Mapping, MappingItem
from ibm_watsonx_gov.entities.utils import \
    build_configuration_from_metric_mappings
from ibm_watsonx_gov.evaluators.impl.evaluate_metrics_impl import \
    _evaluate_metrics_async
from ibm_watsonx_gov.metrics.utils import (COST_METADATA, ONE_M,
                                           TARGETED_USAGE_TRACE_NAMES,
                                           calculate_cost, mapping_to_df)
from ibm_watsonx_gov.traces.span_node import SpanNode
from ibm_watsonx_gov.traces.span_util import (get_attributes,
                                              get_span_nodes_from_json)
from ibm_watsonx_gov.utils.async_util import (gather_with_concurrency,
                                              run_in_event_loop)
from ibm_watsonx_gov.utils.python_utils import add_if_unique
from jsonpath_ng import parse as parse_jsonpath

try:
    from opentelemetry.proto.trace.v1.trace_pb2 import Span, Status
except:
    pass


STATUS_MAP = {
    Status.STATUS_CODE_OK: MessageStatus.SUCCESSFUL,
    Status.STATUS_CODE_ERROR: MessageStatus.FAILURE,
    Status.STATUS_CODE_UNSET: MessageStatus.UNKNOWN
}


class TraceUtils:

    @staticmethod
    def build_span_trees(spans: list[dict], agentic_app: AgenticApp | None = None) -> List[SpanNode]:
        root_spans: list[SpanNode] = []

        span_nodes: dict[bytes, SpanNode] = {}
        for span in spans:
            span_nodes.update(get_span_nodes_from_json(span, agentic_app))

        # Create tree
        for _, node in span_nodes.items():
            parent_id = node.span.parent_span_id
            if not parent_id:
                root_spans.append(node)  # Root span which will not have parent
            else:
                # Use composite key of trace_id + parent_span_id to handle spans with same span_id across different traces
                parent_composite_key = node.span.trace_id + parent_id
                parent_node = span_nodes.get(parent_composite_key)
                if parent_node:
                    parent_node.add_child(node)
                else:
                    # Orphan span where parent is not found
                    root_spans.append(node)

        return root_spans

    @staticmethod
    def convert_array_value(array_obj: Dict) -> List:
        """Convert OTEL array value to Python list"""
        return [
            item.get("stringValue")
            or int(item.get("intValue", ""))
            or float(item.get("doubleValue", ""))
            or bool(item.get("boolValue", ""))
            for item in array_obj.get("values", [])
        ]

    @staticmethod
    def stream_trace_data(file_path: Path) -> Generator:
        """Generator that yields spans one at a time."""
        with open(file_path) as f:
            for line in f:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse line: {line}\nError: {e}")

    @staticmethod
    def __extract_usage_meta_data(attributes: dict) -> dict:
        """
        Extract meta data required to calculate usage metrics from spans
        """
        meta_data = {}
        model = attributes.get("gen_ai.request.model")

        if not model:
            return meta_data

        prompt_token = attributes.get("gen_ai.usage.input_tokens") or attributes.get(
            "gen_ai.usage.prompt_tokens") or 0
        completion_token = attributes.get("gen_ai.usage.output_tokens") or attributes.get(
            "gen_ai.usage.completion_tokens") or 0
        meta_data["cost"] = {
            "model": model,
            "total_prompt_tokens": prompt_token,
            "total_completion_tokens": completion_token,
            "total_tokens": attributes.get("llm.usage.total_tokens", 0),
        }
        meta_data["input_token_count"] = prompt_token

        meta_data["output_token_count"] = completion_token
        return meta_data

    @staticmethod
    async def compute_metrics_from_trace_async(span_tree: SpanNode, api_client: APIClient = None, **kwargs) -> tuple[list[AgentMetricResult], list[Node], list]:
        metric_results, edges = [], []

        # Add Interaction level metrics
        metric_results.extend(await TraceUtils.__compute_message_level_metrics(
            span_tree, api_client, **kwargs))

        # Add node level metrics result
        node_metric_results, nodes_list, experiment_run_metadata = await TraceUtils.__compute_node_level_metrics(
            span_tree, api_client, **kwargs)
        metric_results.extend(node_metric_results)

        for node in nodes_list:
            if node.name in experiment_run_metadata:
                node.foundation_models = list(
                    experiment_run_metadata[node.name]["foundation_models"])

        return metric_results, nodes_list, edges

    @staticmethod
    def compute_metrics_from_trace(span_tree: SpanNode, api_client: APIClient = None) -> tuple[
            list[AgentMetricResult], list[Node], list]:
        return run_in_event_loop(
            TraceUtils.compute_metrics_from_trace_async, span_tree, api_client)

    @staticmethod
    async def __compute_node_level_metrics(span_tree: SpanNode, api_client: APIClient | None, **kwargs):
        metric_results = []
        trace_metadata = defaultdict(list)
        experiment_run_metadata = defaultdict(lambda: defaultdict(set))
        nodes_list = []
        node_stack = list(span_tree.children)
        child_stack = list()
        node_execution_count = {}
        while node_stack or child_stack:
            is_parent = not child_stack
            node = child_stack.pop() if child_stack else node_stack.pop()
            if is_parent:
                parent_span: Span = node.span
                node_name, metrics_config_from_decorators, code_id, events, execution_order = None, [], "", [], None
                data = {}
                # inputs = get_nested_attribute_values(
                #     [node], "traceloop.entity.input")
                # outputs = get_nested_attribute_values(
                #     [node], "traceloop.entity.output")
            span: Span = node.span
            attributes = get_attributes(span.attributes)
            if is_parent:
                node_name = attributes.get("traceloop.entity.name")
                code_id = attributes.get("gen_ai.runnable.code_id")
                execution_order = int(attributes.get("traceloop.association.properties.langgraph_step")) if attributes.get(
                    "traceloop.association.properties.langgraph_step") else None
                for key in ("traceloop.entity.input", "traceloop.entity.output"):
                    try:
                        attr_value = attributes.get(key)
                        content = attr_value if isinstance(
                            attr_value, dict) else json.loads(attr_value)

                        inputs_outputs = content.get(
                            "inputs" if key.endswith("input") else "outputs")
                        if isinstance(inputs_outputs, str):
                            inputs_outputs = json.loads(inputs_outputs)
                        if data:
                            data.update(inputs_outputs)
                        else:
                            data = inputs_outputs
                    except (json.JSONDecodeError, AttributeError) as e:
                        raise Exception(
                            "Unable to parse json string") from e

            if attributes.get("wxgov.config.metrics"):
                metrics_config_from_decorators.append(
                    json.loads(attributes.get("wxgov.config.metrics")))

            if span.events:
                events.extend(span.events)

            if (not node_name) or (node_name == "__start__"):
                continue

            if span.name in TARGETED_USAGE_TRACE_NAMES:
                # Extract required details to calculate usage metrics from each span
                for k, v in TraceUtils.__extract_usage_meta_data(attributes).items():
                    trace_metadata[k].append(v)

            for k, v in TraceUtils.__get_run_metadata_from_span(attributes).items():
                experiment_run_metadata[node_name][k].add(v)

            child_stack.extend(node.children)

            if not child_stack:
                metrics_to_compute, all_metrics_config = TraceUtils.__get_metrics_to_compute(
                    span_tree.get_nodes_configuration(), node_name, metrics_config_from_decorators)

                add_if_unique(Node(name=node_name, func_name=code_id.split(":")[-1] if code_id else node_name, metrics_configurations=all_metrics_config), nodes_list,
                              ["name", "func_name"])

                if node_name in node_execution_count:
                    node_execution_count[node_name] += node_execution_count.get(
                        node_name)
                else:
                    node_execution_count[node_name] = 1

                coros = []
                for mc in metrics_to_compute:
                    coros.append(_evaluate_metrics_async(
                        configuration=mc.configuration,
                        data=data,
                        metrics=mc.metrics,
                        metric_groups=mc.metric_groups,
                        api_client=api_client,
                        **kwargs))

                results = await gather_with_concurrency(coros, max_concurrency=kwargs.get("max_concurrency", 10))
                for metric_result in results:
                    for mr in metric_result.to_dict():
                        node_result = {
                            "applies_to": "node",
                            "message_id": span_tree.get_message_id(),
                            "node_name": node_name,
                            "conversation_id": span_tree.get_conversation_id(),
                            "execution_count": node_execution_count.get(node_name),
                            "execution_order": execution_order,
                            **mr
                        }
                        metric_results.append(AgentMetricResult(**node_result))

                # Add node latency metric result
                latency = round((int(parent_span.end_time_unix_nano) -
                                int(parent_span.start_time_unix_nano))/1e9, 4)
                metric_results.append(AgentMetricResult(name="latency",
                                                        display_name="Latency",
                                                        value=latency,
                                                        group=MetricGroup.PERFORMANCE,
                                                        applies_to="node",
                                                        message_id=span_tree.get_message_id(),
                                                        conversation_id=span_tree.get_conversation_id(),
                                                        node_name=node_name,
                                                        execution_count=node_execution_count.get(
                                                            node_name),
                                                        execution_order=execution_order))

                # Get the node level metrics computed online during graph invocation from events
                metric_results.extend(TraceUtils.__get_metrics_results_from_events(
                    events=events,
                    message_id=span_tree.get_message_id(),
                    conversation_id=span_tree.get_conversation_id(),
                    node_name=node_name,
                    execution_count=node_execution_count.get(node_name),
                    execution_order=execution_order))

        metric_results.extend(
            TraceUtils.__compute_usage_metrics_from_trace_metadata(trace_metadata, span_tree.get_message_id(), span_tree.get_conversation_id()))

        return metric_results, nodes_list, experiment_run_metadata

    @staticmethod
    async def __compute_message_level_metrics(span_tree: SpanNode, api_client: APIClient | None, **kwargs) -> list[AgentMetricResult]:
        metric_results = []
        span = span_tree.span
        duration = round((int(span.end_time_unix_nano) -
                         int(span.start_time_unix_nano)) / 1e9, 4)
        metric_results.append(AgentMetricResult(name="duration",
                                                display_name="Duration",
                                                value=duration,
                                                group=MetricGroup.PERFORMANCE,
                                                applies_to="message",
                                                message_id=span_tree.get_message_id(),
                                                conversation_id=span_tree.get_conversation_id()))

        if not span_tree.agentic_app:
            return metric_results

        data = TraceUtils.__get_data_from_default_mapping(span_tree)

        metric_result = await _evaluate_metrics_async(configuration=span_tree.agentic_app.metrics_configuration.configuration,
                                                      data=data,
                                                      metrics=span_tree.agentic_app.metrics_configuration.metrics,
                                                      metric_groups=span_tree.agentic_app.metrics_configuration.metric_groups,
                                                      api_client=api_client,
                                                      **kwargs)
        metric_result = metric_result.to_dict()
        for mr in metric_result:
            node_result = {
                "applies_to": "message",
                "message_id": span_tree.get_message_id(),
                "conversation_id": span_tree.get_conversation_id(),
                **mr
            }

            metric_results.append(AgentMetricResult(**node_result))

        return metric_results

    @staticmethod
    def __get_data_from_default_mapping(span_tree: SpanNode) -> Dict[str, Any]:
        data = {}

        span = span_tree.span
        attrs = get_attributes(
            span.attributes, ["traceloop.entity.input", "traceloop.entity.output"])
        inputs = attrs.get("traceloop.entity.input", "{}")
        if isinstance(inputs, str):
            inputs = json.loads(inputs).get("inputs", {})
        elif isinstance(inputs, dict):
            inputs = inputs.get("inputs", {})

        if "messages" in inputs:
            for message in reversed(inputs["messages"]):
                if "kwargs" in message and "type" in message["kwargs"] and message["kwargs"]["type"].upper() == "HUMAN":
                    data["input_text"] = message["kwargs"]["content"]
                    break
        else:
            data.update(inputs)

        outputs = attrs.get("traceloop.entity.output", "{}")
        if isinstance(outputs, str):
            outputs = json.loads(outputs).get("outputs", {})
        elif isinstance(outputs, dict):
            outputs = outputs.get("outputs", {})

        if "messages" in outputs:
            # The messages is a list depicting the history of messages with the agent.
            # It need NOT be the whole list of messages in the conversation though.
            # We will traverse the list from the end to find the human input of the message,
            # and the AI output.

            # If there was no input_text so far, find first human message
            if "input_text" not in data:
                for message in reversed(outputs["messages"]):
                    if "kwargs" in message and "type" in message["kwargs"] and message["kwargs"]["type"].upper() == "HUMAN":
                        data["input_text"] = message["kwargs"]["content"]
                        break

            # Find last AI message
            for message in reversed(outputs["messages"]):
                if "kwargs" in message and "type" in message["kwargs"] and message["kwargs"]["type"].upper() == "AI":
                    data["generated_text"] = message["kwargs"]["content"]
                    break
        else:
            data.update(outputs)

        mapping = EvaluatorFields.get_default_fields_mapping()
        data.update(
            {mapping[EvaluatorFields.STATUS_FIELD]: span_tree.get_message_status()})

        return data

    @staticmethod
    def __get_metrics_to_compute(nodes_config, node_name, metrics_configurations):
        metrics_to_compute, all_metrics_config = [], []

        if nodes_config.get(node_name):
            metrics_config = nodes_config.get(node_name)
            for mc in metrics_config:
                mc_obj = MetricsConfiguration(configuration=mc.configuration,
                                              metrics=mc.metrics,
                                              metric_groups=mc.metric_groups)
                metrics_to_compute.append(mc_obj)
                all_metrics_config.append(mc_obj)

        for mc in metrics_configurations:
            mc_obj = MetricsConfiguration.model_validate(
                mc.get("metrics_configuration"))

            all_metrics_config.append(mc_obj)
            if mc.get("compute_real_time") == "false":
                metrics_to_compute.append(mc_obj)

        return metrics_to_compute, all_metrics_config

    @staticmethod
    def __get_metrics_results_from_events(events, message_id, conversation_id, node_name, execution_count, execution_order):
        results = []
        if not events:
            return results

        for event in events:
            for attr in event.attributes:
                if attr.key == "attr_wxgov.result.metric":
                    val = attr.value.string_value
                    if val:
                        mr = json.loads(val)
                        mr.update({
                            "node_name": node_name,
                            "message_id": message_id,
                            "conversation_id": conversation_id,
                            "execution_count": execution_count,
                            "execution_order": execution_order
                        })
                        results.append(AgentMetricResult(**mr))

        return results

    @staticmethod
    def __compute_usage_metrics_from_trace_metadata(trace_metadata: dict, message_id: str, conversation_id: str) -> list:
        metrics_result = []

        for metric, data in trace_metadata.items():
            if metric == "cost":
                metric_value = calculate_cost(data)
            elif metric == "input_token_count":
                metric_value = sum(data)
            elif metric == "output_token_count":
                metric_value = sum(data)
            else:
                continue
            agent_mr = {
                "name": metric,
                "value": metric_value,
                "display_name": metric,
                "message_id": message_id,
                "applies_to": "message",
                "conversation_id": conversation_id,
                "group": MetricGroup.USAGE.value
            }

            metrics_result.append(AgentMetricResult(**agent_mr))

        return metrics_result

    @staticmethod
    def __get_run_metadata_from_span(attributes: dict) -> dict:
        """
        Extract run specific metadata from traces
        1. Foundation model involved in run
        2. Tools involved in run
        """
        metadata = {}
        provider = attributes.get(
            "traceloop.association.properties.ls_provider", attributes.get("gen_ai.system"))
        llm_type = attributes.get("llm.request.type")
        model_name = attributes.get("gen_ai.request.model")

        if model_name:
            metadata["foundation_models"] = FoundationModelInfo(
                model_name=model_name, provider=provider, type=llm_type
            )

        return metadata

    @staticmethod
    async def __process_span_and_extract_data(span_tree: SpanNode,
                                              metric_mappings: List[MetricMapping],
                                              target_component_mapping: List[MappingItem],
                                              message_io_mapping: Optional[Mapping],
                                              **kwargs) -> Tuple[MessageData, Dict[str, List[NodeData]], MetricsMappingData, Dict[str, Node], Dict]:
        """
        Extract and process span tree data to generate metrics, node information, and mapping data.

        This method traverses a span tree extracting:
        - Node information and I/O data
        - Experiment run metadata
        - Metric mapping data
        - Application I/O data
        """
        root_span = span_tree.span
        conversation_id = str(span_tree.get_conversation_id())
        message_id = str(span_tree.get_message_id())

        app_io_start_time = TraceUtils._timestamp_to_iso(
            root_span.start_time_unix_nano)
        app_io_end_time = TraceUtils._timestamp_to_iso(
            root_span.end_time_unix_nano)

        app_io_data = TraceUtils._extract_app_io_from_attributes(
            root_span.attributes, message_io_mapping)

        # Initialize data structures
        experiment_run_metadata = defaultdict(lambda: defaultdict(set))
        nodes_list = []
        node_execution_count = {}
        nodes_data: Dict[str, List[NodeData]] = {}

        # Build quick index for span name to mapping items lookup
        span_mapping_items = defaultdict(list)
        metrics_without_mapping = list()
        for metric_mapping in metric_mappings:
            if metric_mapping.mapping:
                for mapping_item in metric_mapping.mapping.items:
                    if mapping_item.span_name and (mapping_item not in span_mapping_items[mapping_item.span_name]):
                        span_mapping_items[mapping_item.span_name].append(
                            mapping_item)
            else:
                metrics_without_mapping.append(metric_mapping.name)

        for mapping_item in target_component_mapping:
            if mapping_item.span_name:
                span_mapping_items[mapping_item.span_name].append(
                    mapping_item)

        metric_map_data = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))

        # Process span tree using iterative DFS
        TraceUtils._process_span_tree(
            span_tree=span_tree,
            root_span=root_span,
            conversation_id=conversation_id,
            message_id=message_id,
            app_io_data=app_io_data,
            span_mapping_items=span_mapping_items,
            experiment_run_metadata=experiment_run_metadata,
            nodes_list=nodes_list,
            node_execution_count=node_execution_count,
            nodes_data=nodes_data,
            metric_map_data=metric_map_data,
            metrics_without_mapping=metrics_without_mapping,
        )

        # Prepare message data
        messages_data = MessageData(
            message_id=message_id,
            message_timestamp=app_io_end_time,
            conversation_id=conversation_id,
            start_time=app_io_start_time,
            end_time=app_io_end_time,
            input=TraceUtils._string_to_bytes(app_io_data["input"]),
            output=TraceUtils._string_to_bytes(app_io_data["output"]),
            num_loops=sum(node_execution_count.values()) -
            len(node_execution_count)
        )

        metric_mapping_data = MetricsMappingData(
            message_id=message_id,
            metric_mappings=metric_mappings,
            data=metric_map_data
        )

        return (
            messages_data,
            nodes_data,
            metric_mapping_data,
            nodes_list,
            experiment_run_metadata,
        )

    @staticmethod
    def _timestamp_to_iso(timestamp_ns: int) -> str:
        """Convert nanosecond timestamp to ISO format string."""
        return datetime.fromtimestamp(timestamp_ns / 1e9).isoformat()

    @staticmethod
    def _iso_to_timestamp(iso_str: str) -> int:
        """Convert ISO format string to nanosecond timestamp."""
        dt = datetime.fromisoformat(iso_str)
        return int(dt.timestamp() * 1e9)

    @staticmethod
    def _extract_app_io_from_attributes(attributes: List, message_io_mapping: Optional[Mapping]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract application input and output from span attributes.
        """
        app_input = None
        app_output = None
        input_key = "traceloop.entity.input"
        output_key = "traceloop.entity.output"
        input_json_path, output_json_path = None, None

        # If message_io_mapping is provided, use it to extract the input and output from the attributes
        if message_io_mapping is not None:
            for item in message_io_mapping.items:
                if item.type_ == "input":
                    input_key = item.attribute_name if item.attribute_name else input_key
                    input_json_path = item.json_path
                elif item.type_ == "output":
                    output_key = item.attribute_name if item.attribute_name else output_key
                    output_json_path = item.json_path

        for attribute in attributes:
            att_key = attribute.key
            att_val = attribute.value.string_value

            if att_key == input_key:
                if input_json_path:
                    app_input = TraceUtils._extract_with_jsonpath(
                        json.loads(att_val), input_json_path)
                else:
                    app_input = TraceUtils._safe_json_dumps(att_val)
            elif att_key == output_key:
                if output_json_path:
                    app_output = TraceUtils._extract_with_jsonpath(
                        json.loads(att_val), output_json_path)
                else:
                    app_output = TraceUtils._safe_json_dumps(att_val)

        return {"input": app_input, "output": app_output}

    @staticmethod
    def _safe_json_dumps(value: str) -> str:
        """
        Safely JSON dump a string value only if it's not already JSON-formatted.
        """
        if value and '\\"' not in value:
            try:
                return json.dumps(value)
            except (TypeError, ValueError):
                return value
        return value

    @staticmethod
    def _string_to_bytes(text: Optional[str]) -> Optional[bytes]:
        """Convert string to bytes if not None."""
        return bytes(text, "utf-8") if text is not None else None

    @staticmethod
    def _process_span_tree(span_tree: SpanNode, root_span: Span, conversation_id: str, message_id: str,
                           app_io_data: Dict, span_mapping_items: defaultdict[str, list[MappingItem]], experiment_run_metadata: defaultdict[str, defaultdict[str, set]],
                           nodes_list: List[Node], node_execution_count: Dict[str, int], nodes_data: Dict[str, List[NodeData]], metric_map_data: defaultdict,
                           metrics_without_mapping: list) -> None:
        """
        Process the span tree using iterative depth-first search in correct order.
        """
        current_parent_context = TraceUtils._initialize_parent_context(
            span_tree)
        root_span_status = root_span.status.code

        # Process root span attributes for message I/O data
        TraceUtils._process_span_attributes(
            current_span=root_span,
            is_parent=True,
            parent_context=current_parent_context,
            span_mapping_items=span_mapping_items,
            metric_map_data=metric_map_data,
            experiment_run_metadata=experiment_run_metadata,
            metrics_without_mapping=metrics_without_mapping,
        )

        # Reverse the initial children to process in correct order
        node_stack: List[SpanNode] = list(reversed(span_tree.children))
        child_stack: List[SpanNode] = []
        while node_stack or child_stack:
            is_parent = not child_stack
            node = child_stack.pop() if child_stack else node_stack.pop()
            current_span = node.span

            if not current_span.name:
                # No data to extract from current span
                continue
            if is_parent:
                current_parent_context = TraceUtils._initialize_parent_context(
                    node)

            # Process span attributes for node I/O data and metric mappings
            TraceUtils._process_span_attributes(
                current_span=current_span,
                is_parent=is_parent,
                parent_context=current_parent_context,
                span_mapping_items=span_mapping_items,
                metric_map_data=metric_map_data,
                experiment_run_metadata=experiment_run_metadata,
                metrics_without_mapping=metrics_without_mapping,
            )

            if current_parent_context.get("name") == "__start__":
                if app_io_data["input"] is None:
                    # Reading the application input from `__start__` node
                    app_io_data["input"] = current_parent_context["input"]
                    # No data to extract from current span
                    continue

            # Add children to stack for processing
            child_stack.extend(node.children)

            # All node span process completed when all children are processed
            if not child_stack:
                TraceUtils._finalize_node_processing(
                    parent_context=current_parent_context,
                    conversation_id=conversation_id,
                    message_id=message_id,
                    node_execution_count=node_execution_count,
                    nodes_list=nodes_list,
                    nodes_data=nodes_data,
                )

        # If status is extracted from default paths
        if "status" in metrics_without_mapping:
            # Once process all child spans, finalize the message status
            metric_map_data["status"] = metric_map_data["status"] if metric_map_data["status"] else STATUS_MAP[root_span_status]

    @staticmethod
    def _initialize_parent_context(node: SpanNode) -> Dict:
        """
        Initialize context for a parent node.
        """
        parent_span = node.span
        return {
            "span": parent_span,
            "txn_id": str(uuid.uuid4()),
            "execution_order": None,
            "name": None,
            "input": None,
            "output": None,
            "metrics_config": [],
            "code_id": "",
            "start_time": TraceUtils._timestamp_to_iso(parent_span.start_time_unix_nano),
            "end_time": TraceUtils._timestamp_to_iso(parent_span.end_time_unix_nano)
        }

    @staticmethod
    def _process_span_attributes(current_span: Span, is_parent: bool, parent_context: Dict, span_mapping_items: defaultdict[str, list[MappingItem]], metric_map_data: defaultdict,
                                 experiment_run_metadata: defaultdict, metrics_without_mapping: list
                                 ) -> None:
        """
        Need to process all spans to extract FM details
        Process attributes of the current span for I/O data and metric mappings.
        """
        has_metric_mapping = current_span.name in span_mapping_items
        attributes = get_attributes(current_span.attributes)

        if is_parent:
            TraceUtils._process_parent_attribute(
                attributes, parent_context)
            # Extract required details to calculate duration metrics from each parent span
            if any(
                metric in metrics_without_mapping
                for metric in ("duration", "latency")
            ):
                # Process only non `__start__` span
                if "__start__" not in current_span.name:
                    # Initialize span start end time
                    span_data = metric_map_data[current_span.name]
                    if "start_time" not in span_data:
                        span_data["start_time"] = []
                    if "end_time" not in span_data:
                        span_data["end_time"] = []

                    span_data["start_time"].append(TraceUtils._iso_to_timestamp(
                        parent_context["start_time"]))
                    span_data["end_time"].append(TraceUtils._iso_to_timestamp(
                        parent_context["end_time"]))

        if has_metric_mapping:
            TraceUtils._process_metric_mapping(
                current_span.name, attributes,
                span_mapping_items[current_span.name],
                metric_map_data,
            )

        # Extract required details to calculate usage and duration metrics from each span, in case mapping is not provided in metric configuration
        if current_span.name in TARGETED_USAGE_TRACE_NAMES:
            cost_meta_data = TraceUtils.__extract_usage_meta_data(
                attributes)["cost"]
            # Aggregate total input and output token
            model_key = cost_meta_data["model"]
            inner_map = metric_map_data.get(current_span.name)
            if inner_map and model_key in inner_map:
                prev_cost_meta_data = metric_map_data[current_span.name][model_key]["model_usage_details"]
                cost_meta_data["total_prompt_tokens"] += prev_cost_meta_data.get(
                    "total_prompt_tokens", 0)
                cost_meta_data["total_completion_tokens"] += prev_cost_meta_data.get(
                    "total_completion_tokens", 0)

            # Cost
            if "cost" in metrics_without_mapping:
                metric_map_data[current_span.name][model_key]["model_usage_details"] = cost_meta_data
            # Token count
            if "input_token_count" in metrics_without_mapping:
                metric_map_data[current_span.name][model_key]["prompt_tokens_count"] = cost_meta_data["total_prompt_tokens"]
            if "output_token_count" in metrics_without_mapping:
                metric_map_data[current_span.name][model_key]["completion_tokens_count"] = cost_meta_data["total_completion_tokens"]

        # Extract FM details to store it node details
        for k, v in TraceUtils.__get_run_metadata_from_span(attributes).items():
            experiment_run_metadata[parent_context.get("name")][k].add(v)

        # Extract failed status if any
        if "status" in metrics_without_mapping:
            if current_span.status.code == Status.STATUS_CODE_ERROR:
                metric_map_data["status"] = MessageStatus.FAILURE

    @staticmethod
    def _process_parent_attribute(attributes: dict, parent_context: Dict) -> None:
        """
        Process an attribute for a parent node.
        """
        parent_context["name"] = attributes.get("traceloop.entity.name")
        parent_context["code_id"] = attributes.get("gen_ai.runnable.code_id")
        parent_context["execution_order"] = int(attributes.get("traceloop.association.properties.langgraph_step")) if attributes.get(
            "traceloop.association.properties.langgraph_step") else None
        parent_context["input"] = TraceUtils._safe_json_dumps(
            attributes.get("traceloop.entity.input"))
        parent_context["output"] = TraceUtils._safe_json_dumps(
            attributes.get("traceloop.entity.output"))

    @staticmethod
    def _process_metric_mapping(span_name: str, attribute: dict, mapping_items: List[MappingItem], metric_map_data: defaultdict
                                ) -> None:
        """
        Process metric mapping for a span attribute.
        """
        for mapping_item in mapping_items:
            try:
                content = attribute.get(mapping_item.attribute_name)
                content = TraceUtils._parse_nested_json_fields(content)
                if mapping_item.json_path:
                    extracted_value = TraceUtils._extract_with_jsonpath(
                        content, mapping_item.json_path)
                else:
                    extracted_value = content
            except (json.JSONDecodeError, AttributeError):
                # Fallback to string value if JSON parsing fails
                extracted_value = attribute.get(mapping_item.attribute_name)

            if mapping_item.type_ == "target_component":
                metric_map_data[span_name][mapping_item.attribute_name][mapping_item.json_path] = extracted_value
            else:
                span_data = metric_map_data[span_name][mapping_item.attribute_name]
                json_path_data = span_data[mapping_item.json_path]
                # The defaultdict should create a list here, but ensure it's actually a list
                if not isinstance(json_path_data, list):
                    span_data[mapping_item.json_path] = []
                    json_path_data = span_data[mapping_item.json_path]
                json_path_data.append(extracted_value)

    @staticmethod
    def _parse_nested_json_fields(content) -> Dict:
        """
        Recursively parse a value that might be a JSON string.
        """
        if isinstance(content, str):
            try:
                # Try to parse as JSON
                parsed = json.loads(content)
                # Recursively parse the result in case it contains more JSON strings
                return TraceUtils._parse_nested_json_fields(parsed)
            except (json.JSONDecodeError, ValueError):
                # Not a JSON string, return as-is
                return content
        elif isinstance(content, dict):
            # Recursively parse all values in the dictionary
            return {k: TraceUtils._parse_nested_json_fields(v) for k, v in content.items()}
        elif isinstance(content, list):
            # Recursively parse all items in the list
            return [TraceUtils._parse_nested_json_fields(item) for item in content]
        else:
            # Return other types as-is (int, float, bool, None, etc.)
            return content

    @staticmethod
    def _extract_with_jsonpath(content: Dict, json_path: str) -> Any:
        """
        Extract value from content using JSONPath expression.
        """
        try:
            jsonpath_expr = parse_jsonpath(json_path)
            matches = [match.value for match in jsonpath_expr.find(content)]

            if matches:
                return matches[0] if len(matches) == 1 else matches
            return None
        except Exception:
            return None

    @staticmethod
    def _finalize_node_processing(parent_context: Dict, conversation_id: str, message_id: str, node_execution_count: Dict[str, int],
                                  nodes_list: List[Node], nodes_data: Dict[str, List[NodeData]]) -> None:
        """
        Finalize processing for a completed node.
        """
        node_name = parent_context["name"]

        # Update execution count
        node_execution_count[node_name] = node_execution_count.get(
            node_name, 0) + 1

        # Add unique node to nodes list
        func_name = parent_context["code_id"].split(
            ":")[-1] if parent_context["code_id"] else node_name
        add_if_unique(
            Node(
                name=node_name,
                func_name=func_name,
            ),
            nodes_list,
            ["name", "func_name"]
        )

        # Add node I/O data
        if node_name not in nodes_data:
            nodes_data[node_name] = []

        nodes_data[node_name].append(NodeData(
            message_id=message_id,
            message_timestamp=parent_context["end_time"],
            conversation_id=conversation_id,
            node_name=node_name,
            start_time=parent_context["start_time"],
            end_time=parent_context["end_time"],
            input=TraceUtils._string_to_bytes(parent_context["input"]),
            output=TraceUtils._string_to_bytes(parent_context["output"]),
            execution_order=parent_context["execution_order"],
            execution_count=node_execution_count[node_name],
            node_txn_id=parent_context["txn_id"],
            node_txn_timestamp=parent_context["end_time"]
        ))

    @staticmethod
    async def __compute_metrics_from_maps(metrics_configuration: MetricsConfiguration,
                                          mapping_data: Dict,
                                          api_client: APIClient,
                                          message_id: str,
                                          conversation_id: str,
                                          message_timestamp: str,
                                          nodes_data: Dict[str, List[NodeData]],
                                          **kwargs) -> List[AgentMetricResult]:
        """
        Process all configured metrics by:
        1. Extracting required data from mapping data
        2. Computing metrics asynchronously
        """
        metric_results = []
        coros = []
        execution_map = defaultdict(lambda: defaultdict())
        metric_count = 0
        msg_data = mapping_to_df(mapping_data)
        for metric in metrics_configuration.metrics:
            target_component = None
            if metric.target_component:
                if metric.target_component.type == "mapping":
                    target_component = mapping_data[metric.target_component.value.span_name][
                        metric.target_component.value.attribute_name][metric.target_component.value.json_path]
                else:
                    target_component = metric.target_component.value
            configuration = AgenticAIConfiguration(
                **build_configuration_from_metric_mappings(metric, target_component))
            if metric.applies_to == "message":
                coros.append(_evaluate_metrics_async(
                    configuration=configuration,
                    data=msg_data,
                    metrics=[metric],
                    api_client=api_client,
                    **kwargs))
                metric_count += 1
                execution_map[metric_count]["applies_to"] = metric.applies_to
            else:  # Node level
                node_data_list = nodes_data.get(target_component)
                if node_data_list is None:
                    # Skip this metric if the target component doesn't exist in nodes_data
                    continue
                for i in range(len(node_data_list)):
                    coros.append(_evaluate_metrics_async(
                        configuration=configuration,
                        # Extract data specific to execution order <i>
                        data=mapping_to_df(mapping_data, i),
                        metrics=[metric],
                        api_client=api_client,
                        **kwargs))
                    metric_count += 1
                    execution_map[metric_count]["target_component"] = target_component
                    execution_map[metric_count]["applies_to"] = metric.applies_to
                    execution_map[metric_count]["execution_count"] = node_data_list[i].execution_count
                    execution_map[metric_count]["execution_order"] = node_data_list[i].execution_order

        results = await gather_with_concurrency(coros, max_concurrency=kwargs.get("max_concurrency", 10))
        for i, result in enumerate(results, start=1):
            for mr in result.to_dict():
                result = {
                    "applies_to": execution_map[i].get("applies_to"),
                    "message_id": message_id,
                    "conversation_id": conversation_id,
                    "message_timestamp": message_timestamp,
                    **mr
                }
                if execution_map[i].get("target_component"):
                    result.update({
                        "node_name": execution_map[i].get("target_component"),
                        "execution_count": execution_map[i].get("execution_count"),
                        "execution_order": execution_map[i].get("execution_order"),
                    })
                metric_results.append(AgentMetricResult(**result))

        return metric_results

    @staticmethod
    async def compute_metrics_from_trace_async_v2(span_tree: SpanNode,
                                                  metrics_configuration: MetricsConfiguration,
                                                  message_io_mapping: Mapping | None = None,
                                                  api_client: APIClient | None = None,
                                                  **kwargs
                                                  ) -> Tuple[List[AgentMetricResult], MessageData, List[NodeData], MetricsMappingData, List[Node]]:
        """
        Process span tree data to compute comprehensive metrics and extract execution artifacts.

        This method orchestrates the end-to-end metrics computation pipeline by:
        1. Extracting and processing raw data from span traces
        2. Computing metrics from the extracted trace data  
        3. Calculating additional metrics based on mapping configurations
        """

        # Assuming both the message and node level mappings are available in `agentic_app.metrics_configuration`
        metric_mappings = []
        target_component_mapping = []
        for m in metrics_configuration.metrics:
            metric_mappings.append(MetricMapping(
                name=m.name, method=m.method, applies_to=m.applies_to, mapping=m.mapping))
            if m.target_component and m.target_component.type == "mapping":
                target_component_mapping.append(m.target_component.value)

        # Extract and process core data components from span tree
        (
            message_data, nodes_data, metric_mapping_data,
            nodes, experiment_run_metadata) = await TraceUtils.__process_span_and_extract_data(span_tree,
                                                                                               metric_mappings,
                                                                                               target_component_mapping,
                                                                                               message_io_mapping,
                                                                                               **kwargs)

        # Compute metrics using mapping configurations
        metric_results = await TraceUtils.__compute_metrics_from_maps(metrics_configuration=metrics_configuration,
                                                                      mapping_data=metric_mapping_data.data,
                                                                      api_client=api_client,
                                                                      message_id=message_data.message_id,
                                                                      conversation_id=message_data.conversation_id,
                                                                      message_timestamp=message_data.message_timestamp,
                                                                      nodes_data=nodes_data,
                                                                      **kwargs)

        # Add foundation model details to node
        for node in nodes:
            if node.name in experiment_run_metadata:
                node.foundation_models = list(
                    experiment_run_metadata[node.name]["foundation_models"])

        return metric_results, message_data, [item for sublist in nodes_data.values() for item in sublist], metric_mapping_data, nodes
