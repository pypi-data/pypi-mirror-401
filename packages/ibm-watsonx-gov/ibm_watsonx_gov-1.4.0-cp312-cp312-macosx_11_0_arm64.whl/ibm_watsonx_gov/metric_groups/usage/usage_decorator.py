# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------
from functools import partial
from typing import Callable, Optional

from wrapt import decorator

from ibm_watsonx_gov.config.agentic_ai_configuration import \
    AgenticAIConfiguration
from ibm_watsonx_gov.entities.enums import EvaluatorFields, MetricGroup
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.metrics.base_metric_decorator import BaseMetricDecorator
from ibm_watsonx_gov.metrics import CostMetric, InputTokenCountMetric, OutputTokenCountMetric


class UsageDecorator(BaseMetricDecorator):
    def evaluate_usage(self,
                       func: Optional[Callable] = None,
                       *,
                       configuration: Optional[AgenticAIConfiguration] = None,
                       metrics: list[GenAIMetric] = []
                       ) -> dict:
        """
        An evaluation decorator for computing usage metric on an agent invocation.
        """
        if func is None:
            return partial(self.evaluate_usage, configuration=configuration, metrics=metrics)

        if not metrics:
            metrics = MetricGroup.USAGE.get_metrics()

        @decorator
        def wrapper(func, instance, args, kwargs):

            try:
                self.validate(func=func, metrics=metrics,
                              valid_metric_types=(CostMetric, InputTokenCountMetric, OutputTokenCountMetric))

                metric_inputs = [EvaluatorFields.MODEL_USAGE_DETAIL_FIELDS,
                                 EvaluatorFields.INPUT_TOKEN_COUNT_FIELDS, EvaluatorFields.OUTPUT_TOKEN_COUNT_FIELDS]

                original_result = self.compute_helper(func=func, args=args, kwargs=kwargs,
                                                      configuration=configuration,
                                                      metrics=metrics,
                                                      metric_inputs=metric_inputs)

                return original_result
            except Exception as ex:
                raise Exception(
                    f"There was an error while evaluating usage metric on {func.__name__},") from ex

        return wrapper(func)
