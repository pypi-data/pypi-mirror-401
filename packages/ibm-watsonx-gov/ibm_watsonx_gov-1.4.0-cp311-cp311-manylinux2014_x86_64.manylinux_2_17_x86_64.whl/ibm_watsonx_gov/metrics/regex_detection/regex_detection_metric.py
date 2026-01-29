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
from ibm_watsonx_gov.utils.validation_util import validate_input

REGEX = "regex"


class RegexDetectionMetric(GenAIMetric):
    """
    Defines the Regex Detection metric class.

    The Regex detection metric detects specific regex pattern(s) when they are mentioned explicitly in natural language.

    Examples:
        1. Create regex detection metric with default parameters and compute using metrics evaluator.
            .. code-block:: python

                metric = RegexDetectionMetric(case_sensitive=True, regex_patterns=["..."])
                result = MetricsEvaluator().evaluate(data={"input_text": "..."}, metrics=[metric])

        2. Create regex detection metric with a custom threshold.
            .. code-block:: python

                threshold  = MetricThreshold(type="upper_limit", value=0)
                metric = RegexDetectionMetric(threshold=threshold, regex_patterns=["..."])
    """
    name: Annotated[Literal["regex_detection"],
                    Field(title="Name",
                          description="The regex detectionmetric name.",
                          default="regex_detection", frozen=True)]
    display_name: Annotated[Literal["Regex Detection"],
                            Field(title="Display Name",
                                  description="The regex detection metric display name.",
                                  default="Regex Detection", frozen=True)]
    tasks: Annotated[list[TaskType],
                     Field(title="Tasks",
                           description="The list of supported tasks.",
                           default=TaskType.values(), frozen=True)]
    thresholds: Annotated[list[MetricThreshold],
                          Field(title="Thresholds",
                                description="The metric thresholds.",
                                default=[MetricThreshold(type="upper_limit", value=0)])]
    # group: Annotated[MetricGroup,
    #                  Field(title="Group",
    #                        description="The metric group.",
    #                        default=MetricGroup.CONTENT_SAFETY, frozen=True)]

    regex_patterns: Annotated[list[str], Field(title="Regex Patterns",
                                               default=None,
                                               description=f"List of regex patterns to match against the input text.")]

    async def evaluate_async(
            self,
            data: pd.DataFrame,
            configuration: GenAIConfiguration,
            **kwargs
    ) -> list[AggregateMetricResult]:
        if not self.regex_patterns:
            raise AssertionError(
                f"The regex_patterns field is required, but was missing from the input.")

        validate_input(data.columns.to_list(), configuration)
        kwargs["detector_params"] = {"regex_patterns": self.regex_patterns}

        provider = DetectorsProvider(configuration=configuration,
                                     metric_name=REGEX,
                                     metric_display_name=self.display_name,
                                     metric_method=self.method,
                                     metric_group=MetricGroup.CONTENT_SAFETY,
                                     thresholds=self.thresholds,
                                     **kwargs)
        aggregated_metric_result = await provider.evaluate_async(data=data)
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
