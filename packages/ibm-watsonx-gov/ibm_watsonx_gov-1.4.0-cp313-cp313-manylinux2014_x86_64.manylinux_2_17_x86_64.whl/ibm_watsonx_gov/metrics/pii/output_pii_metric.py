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

from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import AggregateMetricResult
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.entities.metric_threshold import MetricThreshold
from ibm_watsonx_gov.providers.detectors_provider import DetectorsProvider
from ibm_watsonx_gov.utils.async_util import run_in_event_loop

OUTPUT_PII = "output_pii"


class OutputPIIMetric(GenAIMetric):
    """
    Defines the Output PII metric class.

    The Output PII metric measures if your model output data contains any personally identifiable information.
    It is computed using the Watson Natural Language Processing entity extraction model on the output data.

    Examples:
        1. Create Output PII metric with default parameters and compute using metrics evaluator.
            .. code-block:: python

                metric = OutputPIIMetric()
                result = MetricsEvaluator().evaluate(data={"generated_text": "...", metrics=[metric])

        2. Create Output PII metric with a custom threshold.
            .. code-block:: python

                threshold  = MetricThreshold(type="lower_limit", value=0.5)
                metric = OutputPIIMetric(threshold=threshold)
    """
    name: Annotated[Literal["output_pii"],
                    Field(title="Name",
                          description="The output pii metric name.",
                          default=OUTPUT_PII, frozen=True)]
    display_name: Annotated[Literal["Output PII"],
                            Field(title="Display Name",
                                  description="The output pii metric display name.",
                                  default="Output PII", frozen=True)]
    tasks: Annotated[list[TaskType],
                     Field(title="Tasks",
                           description="The list of supported tasks.",
                           default=TaskType.values(), frozen=True)]
    thresholds: Annotated[list[MetricThreshold],
                          Field(title="Thresholds",
                                description="The metric thresholds.",
                                default=[MetricThreshold(type="upper_limit", value=0.1)])]
    group: Annotated[MetricGroup,
                     Field(title="Group",
                           description="The metric group.",
                           default=MetricGroup.CONTENT_SAFETY, frozen=True)]

    async def evaluate_async(
            self,
            data: pd.DataFrame | dict,
            configuration: GenAIConfiguration,
            **kwargs
    ) -> AggregateMetricResult:

        # Create a modified configuration that uses output_fields as input_fields
        # This allows DetectorsProvider to process output data
        modified_config = configuration.model_copy(deep=True)
        modified_config.input_fields = configuration.output_fields

        provider = DetectorsProvider(configuration=modified_config,
                                     metric_name="pii",
                                     metric_display_name=self.display_name,
                                     metric_method=self.method,
                                     metric_group=self.group,
                                     thresholds=self.thresholds,
                                     **kwargs)
        aggregated_metric_result = await provider.evaluate_async(data=data)
        # Update the metric name to output_pii
        aggregated_metric_result.name = self.name
        for record in aggregated_metric_result.record_level_metrics:
            record.name = self.name
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

# Made with Bob
