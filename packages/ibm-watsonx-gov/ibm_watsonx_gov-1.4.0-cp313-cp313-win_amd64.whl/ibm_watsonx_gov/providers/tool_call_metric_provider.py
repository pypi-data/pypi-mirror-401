# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------
import json
from functools import lru_cache

import pandas as pd
from llmevalkit.function_calling.pipeline.pipeline import ReflectionPipeline
from llmevalkit.function_calling.pipeline.types import ToolCall, ToolSpec

from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.base_classes import Error
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.utils.python_utils import (
    get, parse_functions_to_openai_schema)


class ToolCallMetricProvider():
    """
    Base class for Tool Call Metrics Computation.
    """

    def __init__(self, configuration: GenAIConfiguration | AgenticAIConfiguration, metric: GenAIMetric):
        """
        Initialize the ToolCallMetricProvider with the configuration.

        Args:
            configuration (GenAIConfiguration | AgenticAIConfiguration): The configuration for the metric computation.
            metric (GenAIMetric): The metric to be computed.
        """
        self.configuration = configuration
        self.metric = metric

    def pre_process(self, data: pd.DataFrame):
        """
        Preprocess the dataframe and tool list for metrics computation

        Args:
            data (pd.DataFrame): Input dataframe

        Returns:
            pd.Dataframe: Processed dataframe
        """
        # Get the specification of tools used in the application
        # in proper format if it is a list of Callable
        if isinstance(self.configuration.tools, list) and all(callable(item) for item in self.configuration.tools):
            self.configuration.tools = self.get_tools_list_schema(
                self.configuration.tools)

        if self.configuration.available_tools_field and self.configuration.available_tools_field in data.columns:
            data[self.configuration.available_tools_field] = data[self.configuration.available_tools_field].apply(
                lambda x: json.loads(x) if isinstance(x, str) else x)

        # TODO: Add validation for the tool_call_field data schema
        tool_call_field = self.configuration.tool_calls_field
        if tool_call_field:
            data[tool_call_field] = data[tool_call_field].apply(
                lambda x: json.loads(x) if isinstance(x, str) else x)
        return data

    @staticmethod
    def get_tools_list_schema(tools: list) -> list:
        """
        Convert the list of callable objects to the
        format needed for the TCH computation

        Args:
            tools (list): List of Callable objects

        Returns:
            list: List of dictionary containing the tool
            specifications
        """
        tools_specifications = []
        for func in tools:
            tool_schema = parse_functions_to_openai_schema(func)
            if not tool_schema:
                continue
            tools_specifications.append(ToolSpec.model_validate(tool_schema))

        return tools_specifications

    async def compute_metrics(self, data: pd.DataFrame, syntactic_only: bool = True, metric_result_mapping_name: str = None, **kwargs):
        """
        Compute the Tool Call Metrics for the given data

        Args:
            data (pd.DataFrame): Input data including the tools used for the application
            syntactic_only (bool): If True, compute only syntactic metrics.
            metric_result_mapping_name (str): The mapping name for the metric result with the llmevalkit
            kwargs: Additional keyword arguments for the pipeline

        Returns:
            list: List of metrics calculated for each record
        """
        try:

            data = self.pre_process(data)
            tool_calls_field = self.configuration.tool_calls_field
            record_id_field = self.configuration.record_id_field
            record_level_metrics = []

            # Do not compute metrics if llm_judge is not set
            # and trying to compute a non syntactic metrics
            if not getattr(self.metric, "llm_judge", None) and not syntactic_only:
                return []

            for _, row in data.iterrows():

                available_tools = self.configuration.tools or row.get(
                    self.configuration.available_tools_field, [])
                if not all(isinstance(t, ToolSpec) for t in available_tools):
                    available_tools = [ToolSpec.model_validate(
                        func) for func in available_tools]

                tool_calls = self.extract_tool_calls_from_response(
                    row[tool_calls_field])

                if not available_tools:
                    record_level_metrics.append({
                        "value": None,  # Treat no available tools as None score as we are not able to compute a score
                        "record_id": row[record_id_field],
                        "errors": [Error(code="BAD_REQUEST", message_en="The list of available tools is empty.")]
                    })
                    continue

                if not tool_calls:
                    record_level_metrics.append({
                        "value": None,  # Treat no tool calls as None score as we are not able to compute a score
                        "record_id": row[record_id_field],
                        "errors": [Error(code="BAD_REQUEST", message_en="The list of tool calls made by LLM is empty.")]
                    })
                    continue

                if syntactic_only:
                    tool_call_level_explanation = self.compute_syntactic_metrics(
                        data=row, tool_calls=tool_calls, available_tools=available_tools)
                    record_level_metrics.append({
                        "value": 0.0 if tool_call_level_explanation else 1.0,
                        "record_id": row[record_id_field],
                        "explanations": tool_call_level_explanation
                    })
                else:
                    tool_call_level_explanation = await self.compute_semantic_metrics(
                        data=row, tool_calls=tool_calls, available_tools=available_tools, metric_result_mapping_name=metric_result_mapping_name, **kwargs)
                    record_level_metrics.append({
                        "value": min(entry.get("value") for entry in tool_call_level_explanation),
                        "errors": [Error(code="REQUEST_FAILED", message_en=entry.get("error")) for entry in
                                   tool_call_level_explanation if entry.get("error")],
                        "record_id": row[record_id_field],
                        "explanations": tool_call_level_explanation
                    })

            metric_result = self.post_process(
                record_level_metrics, syntactic_only=syntactic_only)

            return metric_result
        except Exception as ex:
            raise Exception(
                f"Error while computing metrics: '{self.metric.name}' using '{self.metric.method}'. Reason: {str(ex)}") from ex

    def compute_syntactic_metrics(self, data: pd.DataFrame, tool_calls: list, available_tools: list):
        """
        Compute the Tool Call Metrics for the given data
        in static mode

        Args:
            data (pd.DataFrame): Input data including the tools used for the application
            tool_calls (list): List of tool calls made by the LLM

        Returns:
            list: List of metrics calculated for each record
        """
        tool_call_level_explanation = []
        for call in tool_calls:
            explanations = ReflectionPipeline.static_only(
                inventory=available_tools, call=ToolCall.model_validate(call))
            explanations = explanations.model_dump()
            if explanations.get("final_decision") is False:
                tool_call_level_explanation.append({
                    "tool_name": call.get("function").get("name"),
                    "hallucinations": {
                        key: val for key, val in explanations["metrics"].items() if not val["valid"]
                    }
                })
        return tool_call_level_explanation

    async def compute_semantic_metrics(self, data: pd.DataFrame, tool_calls: list, available_tools: list, metric_result_mapping_name: str, **kwargs):
        """
        Compute the Tool Call Metrics for the given data
        in semantic mode

        Args:
            data (pd.DataFrame): Input data including the tools used for the application
            configuration (GenAIConfiguration | AgenticAIConfiguration): Metrics configuration
            metric_result_mapping_name (str): The mapping name for the metric result with the llmevalkit
            kwargs: Additional keyword arguments for the pipeline

        Returns:
            list: List of metrics calculated for each record
        """
        tool_call_level_explanation = []
        metrics_client = self.get_llm_metric_client()
        pipeline = ReflectionPipeline(
            metrics_client=metrics_client,
            **kwargs
        )
        for call in tool_calls:
            result = await pipeline.semantic_async(
                conversation=data[self.configuration.input_fields[0]],
                inventory=available_tools,
                call=ToolCall.model_validate(call),
                retries=2
            )

            explanations = get(
                result.model_dump(), f"{metric_result_mapping_name}.metrics.{self.metric.metric_mapping_name}")

            error = get(explanations, "error")
            if explanations:
                tool_call_level_explanation.append({
                    "tool_name": get(call, "function.name"),
                    "value": float(get(explanations, "raw_response.output", 0.0))/5 if not error else None,
                    "error": error,
                    "explanation": get(explanations, "raw_response.explanation"),
                    "evidence": get(explanations, "raw_response.evidence"),
                    "correction": get(explanations, "raw_response.correction")
                })
        return tool_call_level_explanation

    @staticmethod
    def extract_tool_calls_from_response(tool_calls_response) -> list:
        """
        Extracts the tool calls from the response

        Args:
            tool_calls_response (Any): The tool calls response
            can be a list of dictionary, an AIMessage object
            or a dictionary

        Returns:
            list: List of openai formatted tool call
        """
        if isinstance(tool_calls_response, dict):
            tool_calls = get(tool_calls_response, "kwargs.tool_calls")
        elif hasattr(tool_calls_response, "tool_calls"):
            tool_calls = tool_calls_response.tool_calls
        else:
            tool_calls = tool_calls_response

        if tool_calls is None:
            tool_calls = []
        converted = []
        for call in tool_calls:
            # check if tool call is already in the required format, else convert it
            if (isinstance(call, dict) and
                "id" in call and
                call.get("type") == "function" and
                isinstance(call.get("function"), dict) and
                "name" in call["function"] and
                    "arguments" in call["function"]):
                converted.append(call)
            else:
                converted.append({
                    "id": call["id"],
                    "type": "function",
                    "function": {
                        "name": call["name"],
                        "arguments": json.dumps(call["args"])
                    }
                })
        return converted

    def post_process(self, results: pd.DataFrame, syntactic_only: bool = True):
        """
        Post process the computed metrics to get the Aggregated Result and
        Record level metric result in the proper format

        Args:
            results (pd.DataFrame): Computed metric results
            configuration (GenAIConfiguration | AgenticAIConfiguration): Metric configuration

        Returns:
            AggregateMetricResult: The AggregateMetricResult object containing the calculated
            metrics information
        """

        # Preparing the record level metrics
        record_level_metrics: list[RecordMetricResult] = []

        for row in results:
            value = row.get("value")
            rounded_value = round(value, 4) if value is not None else None
            record_level_metrics.append(
                RecordMetricResult(
                    name=self.metric.name,
                    display_name=self.metric.display_name,
                    method=self.metric.method,
                    value=rounded_value,
                    provider="ibm",
                    errors=row.get("errors", []),
                    group=self.metric.group,
                    record_id=row["record_id"],
                    thresholds=self.metric.thresholds,
                    additional_info={"explanations": row.get("explanations")}
                )
            )

        # Get the number of records are violated, min, max
        values = [item.get("value") or 0.0 for item in results]
        min_value = min(values, default=0.0)
        max_value = max(values, default=0.0)
        if syntactic_only:
            count_invalid = sum(val == 0.0 for val in values)
            value = int(count_invalid)/int(len(results))
        else:
            value = sum(values)/len(values) if values else 0.0
        value = round(value, 4)

        # creating AggregateMetricResult
        aggregated_result = AggregateMetricResult(
            name=self.metric.name,
            display_name=self.metric.display_name,
            method=self.metric.method,
            provider="ibm",
            group=self.metric.group,
            value=value,
            total_records=len(results),
            record_level_metrics=record_level_metrics,
            min=min_value,
            max=max_value,
            thresholds=self.metric.thresholds
        )

        # return the aggregated result
        return aggregated_result

    @staticmethod
    @lru_cache(maxsize=128)
    def _create_client_impl(
        provider: str,
        model_id: str,
        project_id: str,
        space_id: str,
        credentials_json: str
    ):
        """
        Cached instance method for creating LLM clients.


        Args:
            provider: Provider name
            model_id: Model identifier
            project_id: Project ID (empty string if None)
            space_id: Space ID (empty string if None)
            credentials_json: JSON string of credentials

        Returns:
            Configured LLM client
        """
        from llmevalkit.llm import get_llm

        if provider == "ibm_watsonx.ai":
            from llmevalkit.llm.providers.ibm_watsonx_ai.ibm_watsonx_ai import \
                WatsonxLLMClientOutputVal

            provider_kwargs = json.loads(credentials_json)
            provider_kwargs["model_id"] = model_id

            if project_id:
                provider_kwargs["project_id"] = project_id
            if space_id:
                provider_kwargs["space_id"] = space_id

            return WatsonxLLMClientOutputVal(**provider_kwargs)

        elif provider == "openai":
            MetricsClientCls = get_llm("openai.async")
            return MetricsClientCls(model_name=model_id)

        elif provider == "wxo_ai_gateway":
            from llmevalkit.llm.providers.wxo_ai_gateway.wxo_ai_gateway import \
                WxoAIGatewayClientOutputVal

            provider_kwargs = json.loads(credentials_json)
            return WxoAIGatewayClientOutputVal(**provider_kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_llm_metric_client(self):
        """
        Get or create cached LLM metrics client.

        Returns:
            Cached or newly created LLM client
        """
        llm_judge = self.metric.llm_judge

        # Extract hashable parameters
        provider = llm_judge.get_model_provider()
        model_id = getattr(llm_judge.model, 'model_id', None) or ""
        project_id = getattr(llm_judge.model, 'project_id', None) or ""
        space_id = getattr(llm_judge.model, 'space_id', None) or ""

        credentials = llm_judge.model.provider.credentials.model_dump(
            exclude_none=True, exclude_unset=True
        )
        credentials_json = json.dumps(credentials, sort_keys=True)

        # Call cached method with hashable parameters
        return ToolCallMetricProvider._create_client_impl(
            provider, model_id, project_id, space_id, credentials_json
        )

    def extract_parameter_info(self, data, metric_mapping_name):
        """
        Extract parameter metrics into a list

        Args:
            data (dict): Response data to be extracted
            metric_mapping_name (str): Metric mapping name

        Returns:
            List: List of Parameter based explanation
        """
        result = {
            "is_issue": False,
            "raw_response": []
        }

        for param_name, param_data in data.get("parameter", {}).items():
            metrics = get(param_data, f"metrics.{metric_mapping_name}")
            raw_response = metrics['raw_response']
            is_issue = metrics.get('is_issue', False)

            if is_issue:
                result["is_issue"] = True

            param_info = {
                "parameter": param_name,
                "explanation": raw_response['explanation'],
                "evidence": raw_response['evidence'],
                "output": raw_response['output'],
                "confidence": raw_response['confidence'],
                "correction": raw_response['correction'],
                "is_issue": is_issue
            }

            result["raw_response"].append(param_info)

        return result
