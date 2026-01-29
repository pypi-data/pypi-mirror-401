# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import re
from typing import Annotated, Literal

import pandas as pd
from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.utils.validation_util import validate_field
from pydantic import Field

INPUT_TOKEN_COUNT = "input_token_count"
INPUT_TOKEN_COUNT_DISPLAY_NAME = "Input Token Count"


class InputTokenCountResult(RecordMetricResult):
    name: str = INPUT_TOKEN_COUNT
    display_name: str = INPUT_TOKEN_COUNT_DISPLAY_NAME


class InputTokenCountMetric(GenAIMetric):
    """
    Defines the Input token count metric class.

    The Input token count metric keep track of LLM input token count.

    Examples:
        1. Create Cost metric with default parameters and compute using metrics evaluator.
            .. code-block:: python

                metric = InputTokenCountMetric()
                result = MetricsEvaluator().evaluate(data={"input_tokens": "..."},
                                                    metrics=[metric])
    """
    name: Annotated[Literal["input_token_count"],
                    Field(title="name",
                          description="The input token count metric name.",
                          default=INPUT_TOKEN_COUNT, frozen=True)]
    display_name: Annotated[Literal["Input Token Count"],
                            Field(title="Display Name",
                                  description="The input token count metric display name.",
                                  default=INPUT_TOKEN_COUNT_DISPLAY_NAME, frozen=True)]
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

        validate_field("input_token_count_fields", configuration)
        record_ids = data[configuration.record_id_field].to_list()
        data = data.fillna(0)
        input_tokens = self._evaluate(data, configuration)
        record_level_metrics = [
            InputTokenCountResult(record_id=record_id,
                                  value=token, group=MetricGroup.USAGE.value)
            for token, record_id in zip(input_tokens, record_ids)
        ]
        summary = get_summaries(input_tokens)
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

    def _evaluate(self, data: pd.DataFrame, config: GenAIConfiguration | AgenticAIConfiguration) -> list:
        """
        Track total input token.
        """
        matched_cols = []

        for pattern in config.input_token_count_fields:
            # Compile regex pattern for safety and performance
            regex = re.compile(pattern)
            # Filter columns matching this pattern
            matched = [col for col in data.columns if regex.fullmatch(col)]
            matched_cols.extend(matched)

        # Remove duplicates in case multiple patterns match the same column
        matched_cols = list(set(matched_cols))

        # Sum across these columns row-wise
        return data[matched_cols].sum(axis=1).tolist()
