# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import ast
import re
from typing import Annotated, Literal

import pandas as pd
from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.metrics.utils import calculate_cost
from ibm_watsonx_gov.utils.validation_util import validate_field
from pydantic import Field

COST = "cost"
COST_DISPLAY_NAME = "Cost"


class CostResult(RecordMetricResult):
    name: str = COST
    display_name: str = COST_DISPLAY_NAME


class CostMetric(GenAIMetric):
    """
    Defines the Cost metric class.

    The Cost metric keep track of LLM usage cost for provided token count.

    Examples:
        1. Create Cost metric with default parameters and compute using metrics evaluator.
            .. code-block:: python

                metric = CostMetric()
                result = MetricsEvaluator().evaluate(data={"model": "...", "input_tokens": "...", "output_tokens": "..."},
                                                    metrics=[metric])
    """
    name: Annotated[Literal["cost"],
                    Field(title="name",
                          description="The cost metric name.",
                          default=COST, frozen=True)]
    display_name: Annotated[Literal["Cost"],
                            Field(title="Display Name",
                                  description="The cost metric display name.",
                                  default=COST_DISPLAY_NAME, frozen=True)]
    tasks: Annotated[list[TaskType],
                     Field(title="Tasks",
                           description="The list of supported tasks.",
                           default=TaskType.values(), frozen=True)]
    group: Annotated[MetricGroup,
                     Field(title="Group",
                           description="The metric group.",
                           default=MetricGroup.USAGE, frozen=True)]

    def evaluate(
            self,
            data: pd.DataFrame,
            configuration: GenAIConfiguration | AgenticAIConfiguration,
            **kwargs,
    ) -> list[AggregateMetricResult]:
        from ibm_watsonx_gov.utils.aggregation_util import get_summaries

        validate_field("model_usage_detail_fields", configuration)
        meta_data = self._extract_required_dtls(data, configuration)
        record_ids = data[configuration.record_id_field].to_list()
        costs = self._evaluate(meta_data)
        record_level_metrics = [
            CostResult(record_id=record_id, value=cost,
                       group=MetricGroup.USAGE.value)
            for cost, record_id in zip(costs, record_ids)
        ]
        summary = get_summaries(costs)
        aggregate_metric_scores = AggregateMetricResult(
            name=self.name,
            display_name=self.display_name,
            group=self.group,
            min=summary.get("min"),
            max=summary.get("max"),
            mean=summary.get("mean"),
            value=summary.get("mean"),
            total_records=len(record_level_metrics),
            record_level_metrics=record_level_metrics,
        )

        return aggregate_metric_scores

    def _extract_required_dtls(self, data: pd.DataFrame, configuration: GenAIConfiguration | AgenticAIConfiguration):
        """
        Convert the dataframe to a consumable structure for calculate_cost function.
        Structure:
            [
                {
                    "model": "<model_name>",
                    "total_prompt_tokens": <token_count>,           # optional
                    "total_completion_tokens": <token_count>        # optional
                },
                ...
            ]
        """
        patterns = configuration.model_usage_detail_fields
        all_matching_cols = set()

        for pattern in patterns:
            regex = re.compile(pattern)
            for col in data.columns:
                if regex.fullmatch(col):
                    all_matching_cols.add(col)

        # Early exit if no matches
        if not all_matching_cols:
            return [[] for _ in range(len(data))]

        consolidated_data = []
        for _, row in data.iterrows():
            cost_meta_data = []

            for col in all_matching_cols:
                model_data = getattr(row, col, None)
                if isinstance(model_data, str):
                    try:
                        model_data = ast.literal_eval(model_data)
                    except (ValueError, SyntaxError):
                        model_data = None  # not a valid dict string

                if not isinstance(model_data, dict):
                    continue

                model = model_data.get("model")
                if not model or pd.isna(model):
                    continue

                cost_meta_data.append(model_data)

            consolidated_data.append(cost_meta_data)

        return consolidated_data

    def _evaluate(self, usage_data: list[list[dict]]) -> list:
        """
        Compute cost from associated properties
        """
        costs = []
        for data in usage_data:
            costs.append(calculate_cost(data))
        return costs
