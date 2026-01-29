# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated, Literal, Optional

import pandas as pd
from pydantic import Field

from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration
from ibm_watsonx_gov.entities.enums import (MetricGroup, MetricValueType,
                                            TaskType)
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric, Mapping, MappingItem
from ibm_watsonx_gov.utils.async_util import run_in_event_loop

USER_ID = "user_id"


class UserIdMetric(GenAIMetric):
    """
    Defines the User Id metric class.
    The User Id metric identifies user identifiers from trace data or tabular data 
    and aggregates them to determine the count of distinct users
    Examples:
        1. Create UserId metric with default parameters and compute using metrics AgenticEvaluator.
            .. code-block:: python

                agent_app = AgenticApp(name="Rag agent",
                       metrics_configuration=MetricsConfiguration(metrics=[
                           UserIdMetric()]))

                evaluator = AgenticEvaluator(agentic_app=agent_app)
                evaluator.start_run()
                result = rag_app.invoke({"input_text": "What is concept drift?", "ground_truth": "Concept drift occurs when the statistical properties of the target variable change over time, causing a machine learning model’s predictions to become less accurate."})
                evaluator.end_run()
    """
    name: Annotated[Literal["user_id"],
                    Field(title="Name",
                          description="The user_id metric name.",
                          default=USER_ID, frozen=True)]
    display_name: Annotated[Literal["User Id"],
                            Field(title="Display Name",
                                  description="The user_id metric display name.",
                                  default="User Id", frozen=True)]
    tasks: Annotated[list[TaskType],
                     Field(title="Tasks",
                           description="The list of supported tasks.",
                           default=TaskType.values(), frozen=True)]
    group: Annotated[MetricGroup,
                     Field(title="Group",
                           description="The metric group.",
                           default=MetricGroup.MESSAGE_COMPLETION, frozen=True)]
    mapping: Annotated[Optional[Mapping],
                       Field(title="Mapping",
                             description="The data mapping details for the metric which are used to read the values needed to compute the metric.",
                             default_factory=lambda: Mapping(items=[MappingItem(name="user_id",
                                                                                type="user_id",
                                                                                span_name="LangGraph.workflow",
                                                                                attribute_name="user.id",
                                                                                json_path=None)])
                             )]

    async def evaluate_async(
            self,
            data: pd.DataFrame | dict,
            configuration: GenAIConfiguration,
            **kwargs
    ) -> list[AggregateMetricResult]:

        record_level_metrics: list[RecordMetricResult] = []

        for _, row in data.iterrows():
            if configuration.user_id_field not in row or not row[configuration.user_id_field]:
                continue

            record_level_metrics.append(
                RecordMetricResult(
                    name=self.name,
                    display_name=self.display_name,
                    method=self.method,
                    label=row.get(configuration.user_id_field),
                    value=None,
                    group=self.group,
                    record_id=row.get(configuration.record_id_field),
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
