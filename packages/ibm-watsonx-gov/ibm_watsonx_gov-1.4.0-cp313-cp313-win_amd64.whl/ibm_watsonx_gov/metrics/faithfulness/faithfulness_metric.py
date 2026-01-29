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
from lazy_imports import LazyModule, load
from pydantic import Field, model_validator
from typing_extensions import Self

from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.base_classes import Error
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.llm_judge import LLMJudge
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.entities.metric_threshold import MetricThreshold
from ibm_watsonx_gov.providers.detectors_provider import DetectorsProvider
from ibm_watsonx_gov.utils.async_util import run_in_event_loop
from ibm_watsonx_gov.utils.gov_sdk_logger import GovSDKLogger
from ibm_watsonx_gov.utils.validation_util import (validate_context,
                                                   validate_input,
                                                   validate_llm_as_judge,
                                                   validate_output,
                                                   validate_small_model_method,
                                                   validate_unitxt_method)

unitxt_provider = LazyModule(
    "from ibm_watsonx_gov.providers.unitxt_provider import UnitxtProvider",
    name="lazy_unitxt_provider"
)
load(unitxt_provider)
UnitxtProvider = unitxt_provider.UnitxtProvider

logger = GovSDKLogger.get_logger(__name__)
FAITHFULNESS = "faithfulness"

unitxt_methods = [
    "token_k_precision",
    "sentence_bert_mini_lm",
    "llm_as_judge",
    "granite_guardian",
    "faithfulness_model"
]


class FaithfulnessMetric(GenAIMetric):
    """
    Defines the Faithfulness metric class.

    The faithfulness metrics can be computed using the below methods:

    1. token_k_precision (default)
    2. sentence_bert_mini_lm
    3. llm_as_judge
    4. granite_guardian
    5. faithfulness_model

    Examples:
        1. Create Faithfulness metric with default parameters.
            .. code-block:: python

                metric = FaithfulnessMetric()
                result = MetricsEvaluator().evaluate(data={"input_text": "...", "context": "...", "generated_text": "..."}, 
                                                    metrics=[metric])
                # A list of contexts can also be passed as shown below
                result = MetricsEvaluator().evaluate(data={"input_text": "...", "context": ["...", "..."], "generated_text": "..."}, 
                                                    metrics=[metric])

        2. Create Faithfulness metric with a custom threshold and method.
            .. code-block:: python

                thresholds  = [MetricThreshold(type="lower_limit", value=0.5)]
                method = "sentence_bert_mini_lm"
                metric = FaithfulnessMetric(method=method, thresholds=thresholds)

        3. Create Faithfulness metric with llm_as_judge method.
            .. code-block:: python

                # Define LLM Judge using watsonx.ai
                # To use other frameworks and models as llm_judge, see :module:`ibm_watsonx_gov.entities.foundation_model`
                llm_judge = LLMJudge(model=WxAIFoundationModel(
                                            model_id="ibm/granite-3-3-8b-instruct",
                                            project_id="<PROJECT_ID>"
                                    ))
                metric = FaithfulnessMetric(llm_judge=llm_judge)

        4. Create Faithfulness metric with granite_guardian method.
            .. code-block:: python

                metric = FaithfulnessMetric(method="granite_guardian")

        5. Create Faithfulness metric with faithfulness_model method. Currently available only in On-Prem version.
            .. code-block:: python

                metric = FaithfulnessMetric(method="faithfulness_model")
    """
    name: Annotated[Literal["faithfulness"],
                    Field(title="Name",
                          description="The faithfulness metric name.",
                          default=FAITHFULNESS, frozen=True)]
    display_name: Annotated[Literal["Faithfulness"],
                            Field(title="Display Name",
                                  description="The faithfulness metric display name.",
                                  default="Faithfulness", frozen=True)]
    tasks: Annotated[list[TaskType],
                     Field(title="Tasks",
                           description="The list of supported tasks.",
                           default=[TaskType.RAG])]
    thresholds: Annotated[list[MetricThreshold],
                          Field(title="Thresholds",
                                description="The metric thresholds.",
                                default=[MetricThreshold(type="lower_limit", value=0.7)])]
    method: Annotated[Literal["token_k_precision", "sentence_bert_mini_lm", "llm_as_judge", "granite_guardian", "faithfulness_model"],
                      Field(title="Method",
                            description="The method used to compute the metric. This field is optional and when `llm_judge` is provided, the method would be set to `llm_as_judge`. The `faithfulness_model` method is currently available only in On-Prem version.",
                            default="token_k_precision")]
    group: Annotated[MetricGroup,
                     Field(title="Group",
                           description="The metric group.",
                           default=MetricGroup.ANSWER_QUALITY, frozen=True)]
    llm_judge: Annotated[LLMJudge | None,
                         Field(title="LLM Judge",
                               description="The LLM judge used to compute the metric.",
                               default=None)]

    @model_validator(mode="after")
    def set_llm_judge_default_method(self) -> Self:
        # If llm_judge is set, set the method to llm_as_judge
        if self.llm_judge:
            self.method = "llm_as_judge"
        return self

    def evaluate(self,
                 data: pd.DataFrame,
                 configuration: GenAIConfiguration | AgenticAIConfiguration,
                 **kwargs) -> AggregateMetricResult:
        # If ran in sync mode, block until it is done
        return run_in_event_loop(
            self.evaluate_async,
            data=data,
            configuration=configuration,
            **kwargs,
        )

    def __is_supported(self, **kwargs):
        # Currently supported only in CPD and ypqa
        return kwargs.get(
            "api_client").credentials.region == "ypqa" or kwargs.get("api_client").is_cpd

    async def evaluate_async(self,
                             data: pd.DataFrame,
                             configuration: GenAIConfiguration | AgenticAIConfiguration,
                             **kwargs) -> AggregateMetricResult:
        data_cols = data.columns.to_list()

        try:
            validate_input(data_cols, configuration)
            validate_output(data_cols, configuration)
            validate_context(data_cols, configuration)
            validate_unitxt_method(self.name, self.method, unitxt_methods)
            validate_llm_as_judge(self.name, self.method,
                                  self.llm_judge, configuration.llm_judge)
            validate_small_model_method(
                self.name, self.method, self.__is_supported(**kwargs), unitxt_methods)
        except ValueError as ve:
            if kwargs.get("ignore_validation_errors"):
                message = f"Skipping '{self.name}' computation because the validation failed. Details: {str(ve)}"
                logger.warning(message)
                return
            raise ve

        # Separate the data into a dataframe with no None values and a dataframe with None values
        input_output_has_none = data[configuration.input_fields +
                                     configuration.output_fields].isna().any(axis=1)
        all_contexts_none = data[configuration.context_fields].isna().all(
            axis=1)
        mask_has_none = input_output_has_none | all_contexts_none
        df_with_none = data[mask_has_none]
        df_without_none = data[mask_has_none == False]

        # Compute the metrics only for the dataframe with no None values
        aggregated_metric_result = None
        if not df_without_none.empty:
            if self.method in ["granite_guardian", "faithfulness_model"]:
                kwargs["detector_params"] = {
                    "method": self.method, "threshold": 0.001}
                provider = DetectorsProvider(configuration=configuration,
                                             metric_name=self.name,
                                             metric_display_name=self.display_name,
                                             metric_method=self.method,
                                             metric_group=self.group,
                                             thresholds=self.thresholds,
                                             **kwargs)
            else:
                provider = UnitxtProvider(configuration=configuration,
                                          metric_name=self.name,
                                          metric_display_name=self.display_name,
                                          metric_method=self.method,
                                          metric_prefix="metrics.rag.external_rag",
                                          metric_group=self.group,
                                          llm_judge=self.llm_judge,
                                          thresholds=self.thresholds,
                                          **kwargs)

            aggregated_metric_result = await provider.evaluate_async(data=df_without_none)

        # Update the metric result with record level metrics results for the records with missing values
        if not df_with_none.empty:
            # Create None results for records with missing values
            none_results = []
            for _, row in df_with_none.iterrows():
                record_result = RecordMetricResult(
                    name=self.name,
                    display_name=self.display_name,
                    method=self.method,
                    group=self.group,
                    value=None,
                    record_id=row[configuration.record_id_field],
                    thresholds=self.thresholds,
                    errors=[Error(
                        code="BAD_REQUEST", message_en="The value of required fields input, output or context is None.")]
                )
                none_results.append(record_result)

            # Merge the results
            if aggregated_metric_result:
                all_record_results = aggregated_metric_result.record_level_metrics + none_results
                aggregated_metric_result.record_level_metrics = all_record_results
                aggregated_metric_result.total_records = len(
                    all_record_results)
            else:
                aggregated_metric_result = AggregateMetricResult(
                    name=self.name,
                    display_name=self.display_name,
                    method=self.method,
                    group=self.group,
                    value=None,
                    total_records=len(none_results),
                    record_level_metrics=none_results,
                    min=None,
                    max=None,
                    mean=None,
                    thresholds=self.thresholds
                )

        return aggregated_metric_result
