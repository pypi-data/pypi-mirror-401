# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated, Literal

import pandas as pd
from pydantic import Field

from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.utils.validation_util import validate_start_time, validate_end_time

DURATION = "duration"
DURATION_DISPLAY_NAME = "Duration"
LATENCY = "latency"
LATENCY_DISPLAY_NAME = "Latency"


class DurationMetric(GenAIMetric):
    """
    Defines the Duration metric class.

    The Duration metric measures how long it take to process the task.

    Examples:
        1. Create Duration metric with default parameters and compute using metrics evaluator.
            .. code-block:: python

                metric = DurationMetric()
                result = MetricsEvaluator().evaluate(data={"start_time": "...", "end_time": "..."},
                                                    metrics=[metric])
    """
    name: Annotated[Literal["duration", "latency"],
                    Field(title="name",
                          description="The duration metric name.",
                          default=DURATION, frozen=True)]
    display_name: Annotated[Literal["Duration", "Latency"],
                            Field(title="Display Name",
                                  description="The duration metric display name.",
                                  default=DURATION_DISPLAY_NAME, frozen=True)]
    tasks: Annotated[list[TaskType],
                     Field(title="Tasks",
                           description="The list of supported tasks.",
                           default=TaskType.values(), frozen=True)]
    group: Annotated[MetricGroup,
                     Field(title="Group",
                           description="The metric group.",
                           default=MetricGroup.PERFORMANCE, frozen=True)]

    def evaluate(
            self,
            data: pd.DataFrame,
            configuration: GenAIConfiguration | AgenticAIConfiguration,
            **kwargs,
    ) -> list[AggregateMetricResult]:
        from ibm_watsonx_gov.utils.aggregation_util import get_summaries

        data_cols = data.columns.to_list()
        validate_start_time(data_cols, configuration)
        validate_end_time(data_cols, configuration)
        record_ids = data[configuration.record_id_field].to_list()
        if self.applies_to == "message":
            metric_name = self.name
            metric_display_name = self.display_name
        else:  # node
            metric_name = LATENCY
            metric_display_name = LATENCY_DISPLAY_NAME

        durations = self._evaluate(data, configuration)
        record_level_metrics = [
            RecordMetricResult(record_id=record_id,
                               value=duration, name=metric_name, display_name=metric_display_name, group=MetricGroup.PERFORMANCE.value)
            for duration, record_id in zip(durations, record_ids)
        ]
        summary = get_summaries(durations)
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
        Compute durations from start_time and end_time columns.
        """
        # Convert to numeric, handling errors
        start_time = pd.to_numeric(
            data[config.start_time_field], errors="coerce")
        end_time = pd.to_numeric(
            data[config.end_time_field], errors="coerce")

        # Calculate duration in seconds (convert from nanoseconds to seconds)
        durations = round((end_time - start_time) / 1e9, 4).tolist()
        return durations
