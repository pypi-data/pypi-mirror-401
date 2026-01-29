# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration


def validate_input(data_columns: list, configuration: GenAIConfiguration):
    if not configuration.input_fields:
        raise ValueError(
            "The `input_fields` value is invalid. Please provide valid value for `input_fields` in the configuration.")

    if not all(field in data_columns for field in configuration.input_fields):
        raise ValueError(
            f"The input fields {configuration.input_fields} are not present in the data.")


def validate_context(data_columns: list, configuration: GenAIConfiguration):
    if not configuration.context_fields:
        raise ValueError(
            "The `context_fields` value is invalid. Please provide valid value for `context_fields` in the configuration.")

    if (not all(field in data_columns for field in configuration.context_fields)):
        raise ValueError(
            f"The context fields {configuration.context_fields} are not present in the data.")


def validate_output(data_columns: list, configuration: GenAIConfiguration):
    if not configuration.output_fields:
        raise ValueError(
            "The `output_fields` value is invalid. Please provide valid value for `output_fields` in the configuration.")

    if (not all(field in data_columns for field in configuration.output_fields)):
        raise ValueError(
            f"The output fields {configuration.output_fields} are not present in the data.")


def validate_reference(data_columns: list, configuration: GenAIConfiguration):
    if not configuration.reference_fields:
        raise ValueError(
            "The `reference_fields` value is invalid. Please provide valid value for `reference_fields` in the configuration."
        )

    if (not all(field in data_columns for field in configuration.reference_fields)):
        raise ValueError(
            f"The reference fields {configuration.reference_fields} are not present in the data.")


def validate_unitxt_method(name: str, method: str, unitxt_methods: list):
    if method not in unitxt_methods:
        raise ValueError(
            f"The provided method '{method}' for computing '{name}' metric is not supported.")


def validate_llm_as_judge(name, method, metric_llm_judge, config_llm_judge):
    if method == "llm_as_judge" and not metric_llm_judge and not config_llm_judge:
        raise ValueError(
            f"llm_judge is required for computing {name} using {method} method")


def validate_small_model_method(name, method, is_supported, unitxt_methods: list):
    if name == "faithfulness":
        if method == "faithfulness_model" and not is_supported:
            unitxt_methods.remove("faithfulness_model")
            raise ValueError(
                f"The 'faithfulness_model' method is supported only in On-Prem version. Please run your evaluation in On-Prem version or use one of the other available methods : {unitxt_methods}")
    if name == "context_relevance":
        if method == "context_relevance_model" and not is_supported:
            unitxt_methods.remove("context_relevance_model")
            raise ValueError(
                f"The 'context_relevance_model' method is supported only in On-Prem version. Please run your evaluation in On-Prem version or use one of the other available methods : {unitxt_methods}")
    if name == "answer_relevance":
        if method == "answer_relevance_model" and not is_supported:
            unitxt_methods.remove("answer_relevance_model")
            raise ValueError(
                f"The 'answer_relevance_model' method is supported only in On-Prem version. Please run your evaluation in On-Prem version or use one of the other available methods : {unitxt_methods}")


def validate_tool_calls(data_columns: list, configuration: GenAIConfiguration):

    if not configuration.tools:
        if not configuration.available_tools_field:
            raise ValueError(
                "The available_tools_field value is invalid. Please provide either the list of tools or the available_tools_field in the configuration.")
        elif configuration.available_tools_field and configuration.available_tools_field not in data_columns:
            raise ValueError(
                f"The available tools field {configuration.available_tools_field} is not present in the data.")

    if not configuration.tool_calls_field:
        raise ValueError(
            "The `tool_calls_field` value is invalid. Please provide valid value for `tool_calls_field` in the configuration.")

    if configuration.tool_calls_field not in data_columns:
        raise ValueError(
            f"The tool calls fields {configuration.tool_calls_field} are not present in the data.")


def validate_field(field: str, configuration: GenAIConfiguration):
    if not getattr(configuration, field, None):
        raise ValueError(
            f"The `{field}` value is invalid. Please provide valid value for `{field}` in the configuration.")


def validate_start_time(data_columns: list, configuration: GenAIConfiguration):
    if not configuration.start_time_field:
        raise ValueError(
            "The `start_time_field` value is invalid. Please provide valid value for `start_time_field` in the configuration.")

    if not configuration.start_time_field in data_columns:
        raise ValueError(
            f"The start time field {configuration.start_time_field} is not present in the data.")


def validate_end_time(data_columns: list, configuration: GenAIConfiguration):
    if not configuration.end_time_field:
        raise ValueError(
            "The `end_time_field` value is invalid. Please provide valid value for `end_time_field` in the configuration.")

    if not configuration.start_time_field in data_columns:
        raise ValueError(
            f"The start time field {configuration.end_time_field} is not present in the data.")
