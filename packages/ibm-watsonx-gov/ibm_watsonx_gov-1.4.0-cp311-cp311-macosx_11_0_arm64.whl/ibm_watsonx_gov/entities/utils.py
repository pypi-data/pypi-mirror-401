# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


from typing import Dict, Optional

from ibm_watsonx_gov.entities.enums import EvaluatorFields
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.metrics import (CostMetric, DurationMetric,
                                     InputTokenCountMetric,
                                     OutputTokenCountMetric, StatusMetric)
from ibm_watsonx_gov.metrics.utils import TARGETED_USAGE_TRACE_NAMES


def build_configuration_from_metric_mappings(metric: GenAIMetric, target_component: Optional[str] = None) -> Dict[str, object]:
    """
    Build a configuration dict from a list of GenAIMetric instances by
    reading their mapping items.
    """
    kwargs: Dict[str, object] = {}
    if not getattr(metric, "mapping", None):
        # If no mapping_details provided, use the default values
        # When calculating metrics from spans, details are provided under below naming convention
        if isinstance(metric, CostMetric):
            # Regex patterns to match fields like: '<span_name>->...->model_usage_details'
            kwargs[EvaluatorFields.MODEL_USAGE_DETAIL_FIELDS.value] = [
                r"^" + span_name + r"->.*->model_usage_details$" for span_name in TARGETED_USAGE_TRACE_NAMES
            ]
        # Regex patterns to match fields like: '<span_name>->...->prompt_tokens_count'
        elif isinstance(metric, InputTokenCountMetric):
            kwargs[EvaluatorFields.INPUT_TOKEN_COUNT_FIELDS.value] = [
                r"^" + span_name + r"->.*->prompt_tokens_count$" for span_name in TARGETED_USAGE_TRACE_NAMES
            ]
        # Regex patterns to match fields like: '<span_name>->...->completion_tokens_count'
        elif isinstance(metric, OutputTokenCountMetric):
            kwargs[EvaluatorFields.OUTPUT_TOKEN_COUNT_FIELDS.value] = [
                r"^" + span_name + r"->.*->completion_tokens_count$" for span_name in TARGETED_USAGE_TRACE_NAMES
            ]

        elif isinstance(metric, DurationMetric):
            if target_component is None:
                # Message level, assuming root span is `LangGraph.workflow`
                kwargs[EvaluatorFields.START_TIME_FIELD.value] = "LangGraph.workflow->start_time"
                kwargs[EvaluatorFields.END_TIME_FIELD.value] = "LangGraph.workflow->end_time"
            else:  # Node level
                kwargs[EvaluatorFields.START_TIME_FIELD.value] = f"{target_component}.task->start_time"
                kwargs[EvaluatorFields.END_TIME_FIELD.value] = f"{target_component}.task->end_time"

        elif isinstance(metric, StatusMetric):
            kwargs[EvaluatorFields.STATUS_FIELD.value] = "status"

        # preserve original behavior: skip the whole process when mapping is missing
        return kwargs

    for item in metric.mapping.items:
        value = f"{item.span_name}->{item.attribute_name}->{item.json_path}"
        t = item.type_
        if t == "output":
            kwargs.setdefault(
                EvaluatorFields.OUTPUT_FIELDS.value, []).append(value)
        elif t == "context":
            kwargs.setdefault(
                EvaluatorFields.CONTEXT_FIELDS.value, []).append(value)
        elif t == "input":
            kwargs.setdefault(
                EvaluatorFields.INPUT_FIELDS.value, []).append(value)
        elif t == "reference":
            kwargs.setdefault(
                EvaluatorFields.REFERENCE_FIELDS.value, []).append(value)
        elif t == "start_time":
            kwargs[EvaluatorFields.START_TIME_FIELD.value] = value
        elif t == "end_time":
            kwargs[EvaluatorFields.END_TIME_FIELD.value] = value
        elif t == "input_token_count":
            kwargs.setdefault(
                EvaluatorFields.INPUT_TOKEN_COUNT_FIELDS.value, []).append(value)
        elif t == "output_token_count":
            kwargs.setdefault(
                EvaluatorFields.OUTPUT_TOKEN_COUNT_FIELDS.value, []).append(value)
        elif t == "model_usage_details":
            kwargs.setdefault(
                EvaluatorFields.MODEL_USAGE_DETAIL_FIELDS.value, []).append(value)
        elif t == "status":
            kwargs[EvaluatorFields.STATUS_FIELD.value] = value
        elif t == "user_id":
            kwargs[EvaluatorFields.USER_ID_FIELD.value] = value
        elif t == "tool_call":
            kwargs[EvaluatorFields.TOOL_CALLS_FIELD.value] = value
        elif t == "available_tools":
            kwargs[EvaluatorFields.AVAILABLE_TOOLS_FIELD.value] = value
        # add any other mapping types here if needed

    return kwargs
