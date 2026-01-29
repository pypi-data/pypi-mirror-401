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
from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration
from ibm_watsonx_gov.entities.enums import (CategoryClassificationType,
                                            MessageStatus, MetricGroup,
                                            MetricValueType, TaskType)
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.utils.async_util import run_in_event_loop
from pydantic import Field

STATUS = "status"


class StatusMetric(GenAIMetric):
    """
    Defines the Status metric class.

    The Status metric measures the status of the message processing, which can be one of the following values:
    - successful
    - failure
    - unknown
    Examples:
        1. Create Status metric with default parameters and compute using metrics AgenticEvaluator.
            .. code-block:: python

                agent_app = AgenticApp(name="Rag agent",
                       metrics_configuration=MetricsConfiguration(metrics=[
                           StatusMetric()]))

                evaluator = AgenticEvaluator(agentic_app=agent_app)
                evaluator.start_run()
                result = rag_app.invoke({"input_text": "What is concept drift?", "ground_truth": "Concept drift occurs when the statistical properties of the target variable change over time, causing a machine learning model’s predictions to become less accurate."})
                evaluator.end_run()
    """
    name: Annotated[Literal["status"],
                    Field(title="Name",
                          description="The status metric name.",
                          default=STATUS, frozen=True)]
    display_name: Annotated[Literal["Status"],
                            Field(title="Display Name",
                                  description="The status metric display name.",
                                  default="Status", frozen=True)]
    tasks: Annotated[list[TaskType],
                     Field(title="Tasks",
                           description="The list of supported tasks.",
                           default=TaskType.values(), frozen=True)]
    group: Annotated[MetricGroup,
                     Field(title="Group",
                           description="The metric group.",
                           default=MetricGroup.MESSAGE_COMPLETION, frozen=True)]
    category_classification: Annotated[dict[str, list[str]], Field(
        title="Category Classification",
        description="The category classification of the metrics values.",
        default={
            CategoryClassificationType.FAVOURABLE.value: [MessageStatus.SUCCESSFUL.value],
            CategoryClassificationType.UNFAVOURABLE.value: [MessageStatus.FAILURE.value],
            CategoryClassificationType.NEUTRAL.value: [
                MessageStatus.UNKNOWN.value]
        },
    )]

    async def evaluate_async(
            self,
            data: pd.DataFrame | dict,
            configuration: GenAIConfiguration,
            **kwargs
    ) -> list[AggregateMetricResult]:

        record_level_metrics: list[RecordMetricResult] = []
        for _, row in data.iterrows():
            record_level_metrics.append(
                RecordMetricResult(
                    name=self.name,
                    display_name=self.display_name,
                    method=self.method,
                    label=row.get(
                        configuration.status_field) or MessageStatus.UNKNOWN.value,
                    value=None,
                    category_classification=self.category_classification,
                    group=self.group,
                    record_id=row[configuration.record_id_field],
                    value_type=MetricValueType.CATEGORICAL.value)
            )

        aggregated_metric_result = AggregateMetricResult.create(
            record_level_metrics)
        return aggregated_metric_result

    def evaluate(
        self,
        data: pd.DataFrame | dict,
        configuration: GenAIConfiguration,
        **kwargs,
    ):
        # If ran in sync mode, block until it is done
        return run_in_event_loop(
            self.evaluate_async,
            data=data,
            configuration=configuration,
            **kwargs,
        )
