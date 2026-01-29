# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated, Callable, Dict, Optional, Union

from ibm_watsonx_gov.entities.base_classes import BaseConfiguration
from ibm_watsonx_gov.entities.enums import TaskType
from ibm_watsonx_gov.entities.llm_judge import LLMJudge
from ibm_watsonx_gov.entities.locale import Locale
from pydantic import Field, model_validator
from typing_extensions import Self


class GenAIConfiguration(BaseConfiguration):
    """
    Defines the GenAIConfiguration class.

    This is used to specify the fields mapping details in the data and other configuration parameters needed for evaluation.

    Examples:
        1. Create configuration with default parameters
            .. code-block:: python

                configuration = GenAIConfiguration()

        2. Create configuration with parameters
            .. code-block:: python

                configuration = GenAIConfiguration(input_fields=["input"], 
                                                   output_fields=["output"])

        2. Create configuration with dict parameters
            .. code-block:: python

                config = {"input_fields": ["input"],
                          "output_fields": ["output"],
                          "context_fields": ["contexts"],
                          "reference_fields": ["reference"]}
                configuration = GenAIConfiguration(**config)    
    """
    task_type: Annotated[TaskType | None, Field(title="Task Type",
                                                description="The generative task type. Default value is None.",
                                                default=None,
                                                examples=[TaskType.RAG])]
    input_fields: Annotated[list[str], Field(title="Input Fields",
                                             description="The list of model input fields in the data. Default value is ['input_text'].",
                                             examples=[
                                                 ["question"]],
                                             default=["input_text"])]
    context_fields: Annotated[list[str], Field(title="Context Fields",
                                               description="The list of context fields in the input fields. Default value is ['context'].",
                                               default=["context"],
                                               examples=[["context1", "context2"]])]
    output_fields: Annotated[list[str], Field(title="Output Fields",
                                              description="The list of model output fields in the data. Default value is ['generated_text'].",
                                              default=["generated_text"],
                                              examples=[["output"]])]
    reference_fields: Annotated[list[str], Field(title="Reference Fields",
                                                 description="The list of reference fields in the data. Default value is ['ground_truth'].",
                                                 default=["ground_truth"],
                                                 examples=[["reference"]])]
    locale: Annotated[Locale | None, Field(title="Locale",
                                           description="The language locale of the input, output and reference fields in the data.",
                                           default=None)]
    tools: Annotated[Union[list[Callable], list[Dict]], Field(title="Tools",
                                                              description="The list of tools used by the LLM.",
                                                              default=[],
                                                              examples=[["function1", "function2"]])]
    tool_calls_field: Annotated[Optional[str], Field(title="Tool Calls Field",
                                                     description="The tool calls field in the input fields. Default value is 'tool_calls'.",
                                                     default="tool_calls",
                                                     examples=["tool_calls"])]
    available_tools_field: Annotated[Optional[str], Field(title="Available Tools Field",
                                                          description="The tool inventory field in the data. Default value is 'available_tools'.",
                                                          default="available_tools",
                                                          examples=["available_tools"])]

    llm_judge: Annotated[LLMJudge | None, Field(title="LLM Judge",
                                                description="LLM as Judge Model details.",
                                                default=None)]
    prompt_field: Annotated[Optional[str], Field(title="Model Prompt Field",
                                                 description="The prompt field in the input fields. Default value is 'model_prompt'.",
                                                 default="model_prompt",
                                                 examples=["model_prompt"])]
    start_time_field: Annotated[Optional[str], Field(title="Span Start Time Field ",
                                                     description="The start time field in span attributes.",
                                                     default=None,
                                                     examples=["start_time"])]
    end_time_field: Annotated[Optional[str], Field(title="Span End Time Field",
                                                         description="The end time field in span attributes.",
                                                         default=None,
                                                         examples=["end_time"])]
    model_usage_detail_fields: Annotated[Optional[list[str]], Field(title="Model Usage Detail Field",
                                                                    description="The model usage detail field in span attributes.This field should provide information on model name, input_token_count and output_token_count",
                                                                    default=[])]
    input_token_count_fields: Annotated[Optional[list[str]], Field(title="Input Token Count Field",
                                                                   description="The input token count field in span attributes.",
                                                                   default=[],
                                                                   examples=[["input_tokens"]])]
    output_token_count_fields: Annotated[Optional[list[str]], Field(title="Output Token Count Field",
                                                                    description="The output token count field in span attributes.",
                                                                    default=[
                                                                        "output_tokens"],
                                                                    examples=[["output_tokens"]])]
    status_field: Annotated[Optional[str], Field(title="Span Status Field ",
                                                 description="The status field in span attributes.",
                                                 default="status",
                                                 examples=["status"])]
    user_id_field: Annotated[Optional[str], Field(title="User Id Field ",
                                                  description="The user id field in span attributes.",
                                                  default="user_id",
                                                  examples=["user_id"])]

    @model_validator(mode="after")
    def validate_fields(self) -> Self:

        if self.task_type == TaskType.RAG:
            if not self.input_fields or not self.context_fields:
                raise ValueError(
                    "input_fields and context_fields are required for RAG task type.")

        return self
