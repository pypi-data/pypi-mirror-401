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

KEYWORD = "keyword"


class KeywordDetectionMetric(GenAIMetric):
    """
    Defines the Keyword Detection metric class.

    The Keyword detection metric detects specific keyword(s) when they are mentioned explicitly in natural language.

    Examples:
        1. Create keyword detection metric with default parameters and compute using metrics evaluator.
            .. code-block:: python

                metric = KeywordDetectionMetric(case_sensitive=True, keywords=["..."])
                result = MetricsEvaluator().evaluate(data={"input_text": "..."}, metrics=[metric])

        2. Create Keyword detection metric with a custom threshold.
            .. code-block:: python

                threshold  = MetricThreshold(type="upper_limit", value=0)
                metric = KeywordDetectionMetric(threshold=threshold, keywords=["..."])
    """
    name: Annotated[Literal["keyword_detection"],
                    Field(title="Name",
                          description="The keyword detection metric name.",
                          default="keyword_detection", frozen=True)]
    display_name: Annotated[Literal["Keyword Detection"],
                            Field(title="Display Name",
                                  description="The keyword metric display name.",
                                  default="Keyword Detection", frozen=True)]
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

    case_sensitive: Annotated[bool, Field(title="Case Sensitive",
                                          default=False,
                                          description="Specifies whether keyword matching is case-sensitive. If enabled, matches will be case-sensitive.")]

    keywords: Annotated[list[str], Field(title="Keyword Strings",
                                         default=None,
                                         description=f"List of keywords to match against the input text.")]

    async def evaluate_async(
            self,
            data: pd.DataFrame,
            configuration: GenAIConfiguration,
            **kwargs
    ) -> list[AggregateMetricResult]:
        if not self.keywords:
            raise AssertionError(
                f"The keywords field is required, but was missing from the input.")

        validate_input(data.columns.to_list(), configuration)
        kwargs["detector_params"] = {"case_sensitive": self.case_sensitive,
                                     "keywords": self.keywords}

        provider = DetectorsProvider(configuration=configuration,
                                     metric_name=KEYWORD,
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
