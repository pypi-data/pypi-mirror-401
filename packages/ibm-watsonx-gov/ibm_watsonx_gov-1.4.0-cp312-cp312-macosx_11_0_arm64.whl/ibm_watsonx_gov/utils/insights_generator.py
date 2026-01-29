# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

"""
Insights Generator Module

This module provides utilities for generating insights from evaluation metrics.
It includes functionality to:
- Select the most significant metrics using relevance scoring and MMR (Maximal Marginal Relevance)
- Generate natural language insights report for metrics using LLM models
- Calculate severity and relevance scores for metrics
"""

import math
from typing import Any, Dict, List, Optional, Union

from ibm_watsonx_gov.entities.enums import ModelProviderType
from ibm_watsonx_gov.entities.foundation_model import (
    AWSBedrockFoundationModel, AzureOpenAIFoundationModel,
    CustomFoundationModel, GoogleAIStudioFoundationModel,
    OpenAIFoundationModel, PortKeyGateway, RITSFoundationModel,
    VertexAIFoundationModel, WxAIFoundationModel)
from ibm_watsonx_gov.entities.llm_judge import LLMJudge
from ibm_watsonx_gov.utils.gov_sdk_logger import GovSDKLogger


class InsightsReport:
    """
    A wrapper class for insights reports that displays properly in Jupyter notebooks.

    This class ensures that text reports with newlines are rendered correctly
    when displayed in Jupyter notebooks, rather than showing escaped \\n characters.
    """

    def __init__(self, content: str, format_type: str = "text"):
        """
        Initialize the InsightsReport.

        Args:
            content: The report content (text, HTML, or JSON string)
            format_type: The format type ("text", "html", or "json")
        """
        self.content = content
        self.format_type = format_type

    def __str__(self) -> str:
        """Return the content as a string."""
        return self.content

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"InsightsReport(format_type='{self.format_type}', length={len(self.content)})"

    def _repr_html_(self) -> Optional[str]:
        """
        Return HTML representation for Jupyter notebooks.

        This method is called by Jupyter to render the object.
        For HTML format, return the HTML directly.
        For text format, wrap in <pre> tags to preserve formatting.
        """
        if self.format_type == "html":
            return self.content
        elif self.format_type == "text":
            # Wrap text in <pre> tags to preserve formatting and newlines
            import html as pyhtml
            return f"<pre>{pyhtml.escape(self.content)}</pre>"
        return None


# Lazy import for LangChain dependencies
try:
    from langchain_ibm import ChatWatsonx
    from langchain_openai import AzureChatOpenAI, ChatOpenAI
except ImportError:
    ChatWatsonx = None
    AzureChatOpenAI = None
    ChatOpenAI = None

logger = GovSDKLogger.get_logger(__name__)

# Metric group weights define the relative importance of different metric categories
# Higher weights indicate more critical metric groups
default_metric_group_weights: Dict[str, float] = {
    "business": 4.0,              # Business outcome metrics (highest priority)
    "answer_quality": 3.0,        # Quality of generated answers
    "content_safety": 3.0,        # Safety and ethical considerations
    "retrieval_quality": 2.0,     # Quality of retrieved information
    "system_reliability": 2.0,    # System reliability and availability
    "performance": 1.75,          # Performance and latency metrics
    "usage": 1.0,                 # Resource usage metrics
    "cost": 1.0,                  # Cost-related metrics
    "other": 1.0                  # Miscellaneous metrics
}

# Metric weights define the relative importance of individual metrics within their groups
# Higher weights indicate more critical individual metrics
default_metric_weights: Dict[str, float] = {
    # Business Outcome Metrics
    "thumbs_up_rate": 4.0,
    "thumbs_down_rate": 4.0,

    # Answer Quality
    "answer_relevance": 4.0,
    "faithfulness": 4.0,
    "answer_similarity": 1.5,

    # Content Safety
    "evasiveness": 2.0,
    "hap": 4.0,
    "harm": 4.0,
    "harm_engagement": 4.0,
    "jailbreak": 4.0,
    "pii": 4.0,
    "profanity": 4.0,
    "sexual_content": 4.0,
    "social_bias": 4.0,
    "unethical_behavior": 2.0,
    "violence": 4.0,

    # Retrieval Quality
    "ndcg": 3.0,
    "context_relevance": 2.5,
    "average_precision": 2.5,
    "retrieval_precision": 2.0,
    "hit_rate": 1.5,
    "reciprocal_rank": 1.5,

    # Cost
    "input_tokens": 2.0,
    "output_tokens": 2.0,
    "tool_calls_count": 2.0,
    "total_tokens": 2.0,
    "total_tool_calls": 2.0,
    "cost": 2.0,
    "input_token_count": 2.0,
    "output_token_count": 2.0,

    # Performance
    "latency": 3.5,
    "duration": 3.5,

    # System Reliability
    "unsuccessful_requests": 4.0,
}


class InsightsGenerator:
    """
    A utility class for generating insights from evaluation metrics.

    This class provides methods to analyze evaluation metrics and generate
    meaningful insights, including selecting the most significant metrics
    and optionally generating an insights report in natural language.

    The class uses a combination of relevance scoring and Maximal Marginal Relevance (MMR)
    to select diverse and significant metrics from a larger set of evaluation results.
    """

    # Metrics that should use percentile-based thresholds (cost and latency metrics)
    PERCENTILE_BASED_METRICS = {
        "duration", "latency",
        "cost", "input_token_count", "output_token_count",
        "input_tokens", "output_tokens", "total_tokens"
    }

    def __init__(self, metrics: List[Any], top_k: int = 3, applies_to: Optional[Union[str, List[str]]] = None,
                 percentile_threshold: float = 95.0,
                 llm_model: Union[LLMJudge, WxAIFoundationModel, OpenAIFoundationModel,
                                  AzureOpenAIFoundationModel, Any] = None,
                 metric_group_weights: Optional[Dict[str, float]] = None,
                 metric_weights: Optional[Dict[str, float]] = None):
        """
        Initialize the InsightsGenerator with the provided metrics, k, and applies_to.

        Args:
            metrics: List of metric dictionaries
            top_k: Number of top metrics to select
            applies_to: Filter by component level. Can be:
                - None: No filtering (default)
                - str: Single component level (e.g., "node", "message", "conversation")
                - List[str]: Multiple component levels (e.g., ["node", "message"])
            percentile_threshold: Percentile to use as threshold for cost/latency metrics (default: 95.0)
                Higher values indicate worse performance for these metrics.
            llm_model: LLM model for generating insights. Can be:
                - LLMJudge instance (wraps a FoundationModel)
                - FoundationModel instance directly (e.g., WxAIFoundationModel)
                - Any object with a generate() method
            metric_group_weights: Optional custom weights for metric groups.
                If provided, these will override the default weights for the specified groups.
                Each weight must be a float between 1.0 and 5.0 (inclusive).
            metric_weights: Optional custom weights for individual metrics.
                If provided, these will override the default weights for the specified metrics.
                Each weight must be a float between 1.0 and 5.0 (inclusive).

        Raises:
            ValueError: If any custom weight is not between 1.0 and 5.0

        Examples:
            >>> # Using WxAIFoundationModel directly
            >>> model = WxAIFoundationModel(
            ...     model_id="ibm/granite-3-3-8b-instruct",
            ...     project_id=PROJECT_ID
            ... )
            >>> generator = InsightsGenerator(metrics, top_k=3, llm_model=model)

            >>> # Using LLMJudge wrapper
            >>> llm_judge = LLMJudge(model=model)
            >>> generator = InsightsGenerator(metrics, top_k=3, llm_model=llm_judge)
        """
        self.metrics = metrics
        self.k = top_k
        self.percentile_threshold = percentile_threshold
        self.llm_model = llm_model

        # Validate and merge custom weights with default weights
        self.metric_group_weights = default_metric_group_weights.copy()
        if metric_group_weights:
            self._validate_weights(metric_group_weights, "metric group")
            self.metric_group_weights.update(metric_group_weights)
            logger.info(
                f"Applied custom metric group weights: {metric_group_weights}")

        self.metric_weights = default_metric_weights.copy()
        if metric_weights:
            self._validate_weights(metric_weights, "metric")
            self.metric_weights.update(metric_weights)
            logger.info(
                f"Applied custom metric weights: {metric_weights}")

        # Normalize applies_to to always be a list or None
        if applies_to is None:
            self.applies_to = None
        elif isinstance(applies_to, str):
            self.applies_to = [applies_to]
        elif isinstance(applies_to, list):
            self.applies_to = applies_to
        else:
            raise TypeError(
                f"applies_to must be None, str, or List[str], got {type(applies_to).__name__}")

    @staticmethod
    def _validate_weights(weights: Dict[str, float], weight_type: str) -> None:
        """
        Validate that all weights are between 1.0 and 5.0 (inclusive).

        Args:
            weights: Dictionary of weights to validate
            weight_type: Type of weight for error message (e.g., "metric", "metric group")

        Raises:
            ValueError: If any weight is not between 1.0 and 5.0
        """
        for name, weight in weights.items():
            if not isinstance(weight, (int, float)):
                raise ValueError(
                    f"Invalid {weight_type} weight for '{name}': {weight}. "
                    f"Weight must be a number between 1.0 and 5.0."
                )
            if weight < 1.0 or weight > 5.0:
                raise ValueError(
                    f"Invalid {weight_type} weight for '{name}': {weight}. "
                    f"Weight must be between 1.0 and 5.0 (inclusive). "
                    f"1.0 is the minimum weight and 5.0 is the maximum weight."
                )

    def select_top_k_metrics(self) -> List[Any]:
        """
        Select the top k most significant metrics from the provided list using MMR algorithm.

        This method uses a greedy selection approach that balances relevance and diversity:
        1. First metric is selected based purely on relevance score
        2. Subsequent metrics are selected using MMR to ensure diversity

        Returns:
            List[dict]: Top k metrics with their original data intact. The metrics are
                ordered by their selection order (most significant first).

        Raises:
            ValueError: If k is not a positive integer
            TypeError: If metrics is not a list

        Examples:
            >>> metrics = [
            ...     {"name": "faithfulness", "value": 0.85, "group": "answer_quality", "severity": 0.3},
            ...     {"name": "hap", "value": 0.95, "group": "content_safety", "severity": 0.1}
            ... ]
            >>> top_metrics = InsightsGenerator.select_top_k_metrics(metrics, k=2)
            >>> # Filter for node-level metrics only
            >>> node_metrics = InsightsGenerator.select_top_k_metrics(metrics, k=2, applies_to="node")
        """
        # Input validation
        if not isinstance(self.metrics, list):
            raise TypeError(
                f"metrics must be a list, got {type(self.metrics).__name__}")

        if not isinstance(self.k, int) or self.k <= 0:
            raise ValueError(f"k must be a positive integer, got {self.k}")

        if not self.metrics:
            logger.warning(
                "Empty metrics list provided to select_top_k_metrics")
            return []

        # Validate metric structure
        for i, metric in enumerate(self.metrics):
            if not isinstance(metric, dict):
                logger.warning(
                    f"Metric at index {i} is not a dictionary, skipping")
                continue
            if "name" not in metric or "group" not in metric:
                logger.warning(
                    f"Metric at index {i} missing required fields 'name' or 'group'")

            # Calculate severity if not already set
            if "severity" not in metric:
                # Check if metric has explicit thresholds
                if "thresholds" in metric and metric.get("thresholds"):
                    try:
                        sev = self._severity(
                            metric["value"],
                            metric["thresholds"][0]["value"],
                            metric["thresholds"][0]["type"]
                        )
                        metric["severity"] = sev
                    except (KeyError, IndexError, TypeError) as e:
                        logger.warning(
                            f"Could not calculate severity for metric {metric.get('name')}: {e}")
                        metric["severity"] = 0.0
                # For cost/latency metrics without thresholds, use percentile-based threshold
                elif metric.get("name") in self.PERCENTILE_BASED_METRICS:
                    try:
                        threshold_val, sev = self._compute_percentile_based_severity(
                            metric)
                        metric["severity"] = sev
                        metric["threshold"] = threshold_val
                        # Also compute violations_count from individual results
                        violations = self._compute_violations_count_from_individual_results(
                            metric)
                        if violations is not None:
                            metric["violations_count"] = violations
                        logger.debug(
                            f"Computed percentile-based severity {sev:.4f} and violations_count {metric.get('violations_count', 0)} for {metric.get('name')}")
                    except Exception as e:
                        logger.warning(
                            f"Could not calculate percentile-based severity for metric {metric.get('name')}: {e}")
                        metric["severity"] = 0.0
                else:
                    metric["severity"] = 0.0

        selected: List[Any] = []
        candidates: List[dict] = self.metrics[:]

        while candidates and len(selected) < self.k:
            if not selected:
                # First metric: select based on relevance score
                best = max(candidates, key=self._relevance_score)
                # Store the relevance score as MMR score for the first metric
                best["mmr_score"] = self._relevance_score(best)
            else:
                # Apply MMR (Maximal Marginal Relevance)
                best = max(
                    candidates,
                    key=lambda c: self._compute_mmr_score(
                        c,
                        selected))
                # Store the MMR score
                best["mmr_score"] = self._compute_mmr_score(
                    best, selected)

            selected.append(best)
            candidates.remove(best)

        # Sort selected metrics by MMR score in descending order
        selected.sort(key=lambda m: m.get("mmr_score", 0), reverse=True)

        # Remove individual_results from the returned metrics to avoid exposing unnecessary data
        for metric in selected:
            if "individual_results" in metric:
                del metric["individual_results"]

        return selected

    @staticmethod
    def _severity(value: float, threshold: float, direction: str) -> float:
        """
        Compute severity of threshold violation based on how far the value deviates from threshold.

        The severity score increases exponentially as the violation becomes more severe,
        using the formula: 1 - exp(-2 * relative_violation)

        Args:
            value (float): The actual metric value
            threshold (float): The threshold value to compare against
            direction (str): Direction of the threshold check:
                - "upper_limit": value should be below threshold
                - "lower_limit": value should be above threshold

        Returns:
            float: Severity score between 0.0 and 1.0, where:
                - 0.0 indicates no violation
                - 1.0 indicates severe violation

        Examples:
            >>> InsightsGenerator._severity(0.9, 0.8, "upper_limit")  # 12.5% over limit
            0.22  # Moderate severity
            >>> InsightsGenerator._severity(0.5, 0.8, "lower_limit")  # 37.5% below limit
            0.53  # Higher severity
        """
        if threshold == 0:
            return 0.0

        if direction == "upper_limit":
            rel = max(0.0, (value - threshold) / abs(threshold))
        else:
            rel = max(0.0, (threshold - value) / abs(threshold))

        return max(0.0, min(1.0, 1 - math.exp(-2 * rel)))

    def _compute_percentile_based_severity(self, metric: dict) -> tuple[float, float]:
        """
        Compute severity for cost/latency metrics using percentile-based thresholds.

        For metrics without explicit thresholds (like duration, cost, token counts),
        this method uses the specified percentile from the metric's percentiles data
        as a dynamic threshold. Values above this percentile are considered violations.

        Args:
            metric (dict): Metric dictionary containing:
                - value (float): The actual metric value
                - percentiles (dict, optional): Dictionary with percentile values
                - name (str): Metric name

        Returns:
            float: Severity score between 0.0 and 1.0, where:
                - 0.0 indicates value is at or below the percentile threshold
                - Higher values indicate increasingly severe violations

        Examples:
            >>> metric = {
            ...     "name": "duration",
            ...     "value": 8.5,
            ...     "percentiles": {"95": 5.0, "99": 7.0}
            ... }
            >>> generator = InsightsGenerator([], k=3, percentile_threshold=95.0)
            >>> generator._compute_percentile_based_severity(metric)
            0.53  # Value is 70% above 95th percentile
        """
        if not isinstance(metric, dict):
            return 0.0

        value = metric.get("value")
        if value is None:
            return 0.0

        # Get percentiles data
        percentiles = metric.get("percentiles")
        if not percentiles or not isinstance(percentiles, dict):
            logger.debug(
                f"No percentiles data available for {metric.get('name')}, severity set to 0.0")
            return 0.0

        # Get the threshold percentile value (e.g., 95th percentile)
        percentile_key = str(int(self.percentile_threshold))
        threshold_value = percentiles.get(percentile_key)

        if threshold_value is None:
            logger.debug(
                f"Percentile {percentile_key} not found for {metric.get('name')}, severity set to 0.0")
            return 0.0

        # For cost/latency metrics, higher values are worse (upper_limit behavior)
        # Calculate severity using the same formula as _severity method
        return threshold_value, self._severity(value, threshold_value, "upper_limit")

    def _compute_violations_count_from_individual_results(self, metric: dict) -> Optional[int]:
        """
        Compute violations_count for percentile-based metrics using individual results.
        Also updates the metric value to show the maximum violating value instead of the mean.

        For metrics with percentile-based thresholds, this method counts how many
        individual measurements exceeded the percentile threshold and replaces the
        aggregated value with the maximum violating value for better visibility.

        Args:
            metric (dict): Metric dictionary containing:
                - value (float): The aggregated metric value (will be replaced with max violating value)
                - percentiles (dict): Dictionary with percentile values
                - individual_results (list, optional): List of individual metric measurements
                - name (str): Metric name

        Returns:
            Optional[int]: Number of violations, or None if individual_results are not available

        Examples:
            >>> metric = {
            ...     "name": "duration",
            ...     "value": 8.5,
            ...     "percentiles": {"95": 5.0},
            ...     "individual_results": [
            ...         {"value": 3.0}, {"value": 6.0}, {"value": 9.0}, {"value": 4.0}
            ...     ]
            ... }
            >>> generator = InsightsGenerator([], k=3, percentile_threshold=95.0)
            >>> generator._compute_violations_count_from_individual_results(metric)
            2  # Two values (6.0 and 9.0) exceed the 95th percentile threshold of 5.0
            # metric["value"] is now 9.0 (the maximum violating value)
        """
        if not isinstance(metric, dict):
            return None

        # Get individual results
        individual_results = metric.get("individual_results")
        if not individual_results or not isinstance(individual_results, list):
            logger.debug(
                f"No individual_results available for {metric.get('name')}, cannot compute violations_count")
            return None

        threshold_value = metric.get("threshold")

        if threshold_value is None:
            return None

        # Find all individual results that exceed the threshold
        # For cost/latency metrics, higher values are worse (violations)
        violating_values = [
            result.get("value")
            for result in individual_results
            if isinstance(result, dict) and result.get("value") is not None
            and result.get("value") > threshold_value
        ]

        violations_count = len(violating_values)

        # If there are violations, replace the aggregated value with the maximum violating value
        if violations_count > 0:
            max_violating_value = max(violating_values)
            metric["value"] = max_violating_value
            logger.debug(
                f"Replaced aggregated value with max violating value {max_violating_value} for {metric.get('name')}")

        logger.debug(
            f"Computed violations_count={violations_count} for {metric.get('name')} "
            f"from {len(individual_results)} individual results with threshold={threshold_value}")

        return violations_count

    def _relevance_score(
            self,
            metric: dict,
            w_sev: float = 0.7,
            w_frq: float = 0.3) -> float:
        """
        Compute the relevance score for a metric based on severity, frequency, and importance weights.

        The relevance score combines:
        1. Severity of threshold violations (weighted by w_sev)
        2. Frequency of violations (weighted by w_frq)
        3. Metric group importance (from metric_group_weights)
        4. Individual metric importance (from metric_weights)

        Args:
            metric (dict): Metric dictionary containing:
                - name (str): Metric name
                - group (str): Metric group
                - severity (float, optional): Severity score (0-1)
                - violations_count (int, optional): Number of violations
            w_sev (float, optional): Weight for severity component. Defaults to 0.7.
            w_frq (float, optional): Weight for frequency component. Defaults to 0.3.

        Returns:
            float: Relevance score (higher values indicate more relevant/important metrics)

        Note:
            If violations_count is not present in the metric, it defaults to 0.
            Unknown metric groups default to weight 1.0.
            Unknown metric names default to weight 1.0.
        """
        if "violations_count" not in metric:
            metric["violations_count"] = 0

        base_score = (
            w_sev * metric.get("severity", 0.0) +
            w_frq * metric["violations_count"]
        )

        group_weight = self.metric_group_weights.get(
            metric.get("group", "other"), 1.0)
        metric_weight = self.metric_weights.get(metric.get("name", ""), 1.0)

        return base_score * group_weight * metric_weight

    @staticmethod
    def _similarity(
            metric_1: dict,
            metric_2: dict,
            method: str = "category") -> float:
        """
        Compute similarity between two metrics for diversity calculation in MMR.

        Args:
            metric_1 (dict): First metric dictionary
            metric_2 (dict): Second metric dictionary
            method (str, optional): Similarity calculation method. Defaults to "category".
                - "category": Returns 1.0 if metrics are in same group, 0.0 otherwise
                - "euclidean": Returns similarity based on Euclidean distance of
                  violations_count and severity

        Returns:
            float: Similarity score between 0.0 (completely different) and 1.0 (identical)

        Examples:
            >>> m1 = {"group": "answer_quality", "violations_count": 2, "severity": 0.5}
            >>> m2 = {"group": "answer_quality", "violations_count": 3, "severity": 0.6}
            >>> InsightsGenerator._similarity(m1, m2, "category")
            1.0  # Same group
            >>> m3 = {"group": "content_safety", "violations_count": 2, "severity": 0.5}
            >>> InsightsGenerator._similarity(m1, m3, "category")
            0.0  # Different group
        """
        if method == "euclidean":
            distance = ((metric_1.get("violations_count", 0) -
                         metric_2.get("violations_count", 0)) ** 2 +
                        (metric_1.get("severity", 0.0) -
                         metric_2.get("severity", 0.0)) ** 2)
            return 1.0 / (1.0 + math.sqrt(distance))
        elif method == "category":
            return 1.0 if metric_1.get(
                "group") == metric_2.get("group") else 0.0
        return 0.0

    def _compute_mmr_score(
            self,
            candidate: dict,
            selected: List[dict],
            lambda_val: float = 0.5) -> float:
        """
        Compute Maximal Marginal Relevance (MMR) score for a candidate metric.

        MMR balances relevance and diversity by penalizing candidates that are too similar
        to already selected metrics. The score is computed as:
        MMR = λ * relevance + (1-λ) * diversity

        Args:
            candidate (dict): Candidate metric to score
            selected (List[dict]): List of already selected metrics
            lambda_val (float, optional): Balance parameter between relevance and diversity.
                Defaults to 0.5.
                - Higher values (closer to 1.0) favor relevance
                - Lower values (closer to 0.0) favor diversity

        Returns:
            float: MMR score (higher values indicate better candidates considering both
                relevance and diversity)

        Raises:
            ValueError: If selected list is empty

        Note:
            This method is used internally by select_top_k_metrics to ensure diverse
            metric selection.
        """
        if not selected:
            raise ValueError(
                "selected list cannot be empty for MMR computation")

        rel = self._relevance_score(metric=candidate)
        max_sim = max(
            InsightsGenerator._similarity(
                metric_1=candidate,
                metric_2=s) for s in selected)
        diversity = 1.0 - max_sim
        score = lambda_val * rel + (1 - lambda_val) * diversity
        return score

    @staticmethod
    def _convert_to_langchain_model(
        llm_model: Union[WxAIFoundationModel, OpenAIFoundationModel,
                         AzureOpenAIFoundationModel, Any]
    ) -> Any:
        """
        Convert a foundation model to a LangChain-compatible model.

        Args:
            llm_model: A FoundationModel instance
                (e.g., WxAIFoundationModel, OpenAIFoundationModel, AzureOpenAIFoundationModel)

        Returns:
            LangChain-compatible model with invoke() method

        Raises:
            Exception: If the provider type is not supported

        Examples:
            >>> # Using WxAIFoundationModel directly
            >>> model = WxAIFoundationModel(model_id="ibm/granite-3-3-8b-instruct", project_id=PROJECT_ID)
            >>> langchain_model = InsightsGenerator._convert_to_langchain_model(model)

        """
        # Extract the foundation model from LLMJudge if needed

        foundation_model = llm_model

        provider_type = foundation_model.provider.type

        if provider_type == ModelProviderType.IBM_WATSONX_AI:
            if ChatWatsonx is None:
                raise ImportError(
                    "langchain_ibm is required for WatsonX models. Install it with: pip install langchain-ibm")

            parameters = {
                "decoding_method": "greedy",
                "max_new_tokens": 512,
                "min_new_tokens": 1,
                "stop_sequences": [".", "<|eom_id|>"]
            }
            return ChatWatsonx(
                model_id=foundation_model.model_id,
                url=foundation_model.provider.credentials.url,
                apikey=foundation_model.provider.credentials.api_key,
                project_id=foundation_model.project_id,
                params=parameters,
            )
        elif provider_type == ModelProviderType.AZURE_OPENAI:
            if AzureChatOpenAI is None:
                raise ImportError(
                    "langchain_openai is required for Azure OpenAI models. Install it with: pip install langchain-openai")

            credentials = foundation_model.provider.credentials
            model_id = foundation_model.model_name
            azure_openapi_host = credentials.url
            api_version = credentials.api_version
            model_base = model_id.split("/")[-1].replace(".", "-")
            azure_endpoint = \
                f'{azure_openapi_host}/openai/deployments/{model_base}/chat/completions?api-version={api_version}'
            parameters = {"temperature": 0}
            return AzureChatOpenAI(
                api_key=credentials.api_key,
                azure_endpoint=azure_endpoint,
                api_version=api_version,
                max_retries=2,
                **parameters
            )
        elif provider_type == ModelProviderType.OPENAI:
            if ChatOpenAI is None:
                raise ImportError(
                    "langchain_openai is required for OpenAI models. Install it with: pip install langchain-openai")

            model_name = foundation_model.model_name
            return ChatOpenAI(
                model=model_name,
                max_retries=2,
                temperature=0.0
            )
        else:
            raise Exception(
                f"Unsupported provider type: {provider_type}. Supported types are: IBM_WATSONX_AI, AZURE_OPENAI, RITS, OPENAI")

    def generate_structured_insights(self,
                                     top_metrics: List[Any],
                                     output_format: str = "html",
                                     top_k: int = 3
                                     ) -> Union[str, InsightsReport]:
        """
        Generate structured insights with top insights, root causes, and recommendations.

        This method analyzes metrics and generates a comprehensive report including:
        - Top K most significant insights
        - Likely root causes
        - Actionable recommendations

        Args:
            metrics (List[Any]): List of metric dictionaries or objects
            output_format (str, optional): Output format ("text", "json", or "html"). Defaults to "html".
        Returns:
            Union[str, InsightsReport]: For "text" format, returns InsightsReport object that displays
                properly in Jupyter notebooks. For "html" and "json" formats, returns formatted string.

        Note:
            For text format in Jupyter notebooks, the returned InsightsReport object will automatically
            render with proper formatting. If you need the raw string, use str(result) or result.content.

        Examples:
            >>> metrics = [
            ...     {"name": "latency", "value": 7.21, "group": "performance", "threshold": 3.0},
            ...     {"name": "average_precision", "value": 0.0, "group": "retrieval_quality", "threshold": 0.7}
            ... ]
            >>> insights = InsightsGenerator.generate_structured_insights(metrics, llm_judge)
            >>> # Filter for node-level metrics only
            >>> node_insights = InsightsGenerator.generate_structured_insights(metrics, llm_judge, applies_to="node")
            >>> # Filter for multiple component levels
            >>> multi_insights = InsightsGenerator.generate_structured_insights(metrics, llm_judge, applies_to=["node", "message"])
        """
        import json as json_module
        from datetime import datetime

        # Build structured input for LLM
        llm_input = {
            "top_metrics": [],
            "summary_stats": {
                "total_metrics": len(self.metrics),
                "metrics_by_group": {}
            }
        }

        # Process metrics
        for metric in top_metrics:
            if isinstance(metric, dict):
                metric_dict = metric
            elif hasattr(metric, '__dict__'):
                metric_dict = metric.__dict__
            else:
                continue

            # Get threshold value - either explicit or from percentiles
            threshold_value = metric_dict.get("threshold")
            if threshold_value is None and metric_dict.get("thresholds"):
                threshold_value = metric_dict.get(
                    "thresholds", [{}])[0].get("value")

            metric_info = {
                "name": metric_dict.get("name", "Unknown"),
                "value": metric_dict.get("value"),
                "group": metric_dict.get("group", "other"),
                "mmr_score": metric_dict.get("mmr_score"),
                "violations_count": metric_dict.get("violations_count", 0),
                "threshold": threshold_value,
                "applies_to": metric_dict.get("applies_to", "unknown"),
                "node_name": metric_dict.get("node_name", "")
            }
            llm_input["top_metrics"].append(metric_info)

            # Update group stats
            group = metric_info["group"]
            if group not in llm_input["summary_stats"]["metrics_by_group"]:
                llm_input["summary_stats"]["metrics_by_group"][group] = 0
            llm_input["summary_stats"]["metrics_by_group"][group] += 1

        # Create comprehensive prompt
        prompt = f"""
                        You are an analyst writing for engineering and product stakeholders (including business users).
                        Using ONLY the JSON below, produce a structured analysis with three sections:

                        1) Top {top_k} Insights:
                        - Provide exactly {top_k} key insights based on the top_metrics list, in the same order as provided
                        - Each insight should be 1-2 sentences, business-friendly (focus on user/customer impact)
                        - Mention the metric name, group, value, and threshold (if available)
                        - Explain the significance and potential impact on users
                        - Use specific numbers from the JSON

                        2) Likely Root Causes:
                        - Provide 3 concise bullet points of probable causes based on the metrics data
                        - Consider patterns across multiple metrics
                        - Be specific and actionable

                        3) Recommendations:
                        - Provide 4-6 actionable recommendations
                        - Prioritize by impact (first = highest priority)
                        - Be specific and include concrete next steps

                        DO NOT invent or change numbers — use only data present in the JSON.
                        Keep the analysis concise and actionable.

                        Structured data (do NOT modify):
                        {json_module.dumps(llm_input, indent=2)}
                        """

        try:
            # Generate insights using LLM
            if isinstance(self.llm_model, (WxAIFoundationModel, OpenAIFoundationModel,
                                           AzureOpenAIFoundationModel)):
                try:

                    from ibm_watsonx_gov.metrics.llm_validation.llm_validation_impl import \
                        generate_llm_response

                    # Convert foundation model to LangChain-compatible model
                    langchain_model = InsightsGenerator._convert_to_langchain_model(
                        self.llm_model)

                    system_message = "You are a helpful, concise system reliability analyst."
                    response = generate_llm_response(
                        langchain_model,
                        system_message,
                        prompt
                    )
                except Exception as e:
                    logger.warning(f"Error generating insights: {str(e)}")
                    response = InsightsGenerator._generate_fallback_insights(
                        llm_input, top_k)
            else:
                # For custom models with generate() method
                response = self.llm_model.generate(prompt).strip()

            if output_format == "html":
                return InsightsGenerator._format_structured_as_html(
                    response, llm_input)
            elif output_format == "json":
                return InsightsGenerator._format_structured_as_json(
                    response, llm_input)
            else:
                # Return InsightsReport object for proper Jupyter notebook display
                text_content = InsightsGenerator._format_structured_as_text(
                    response, llm_input)
                return InsightsReport(text_content, format_type="text")

        except Exception as e:
            logger.error(f"Failed to generate structured insights: {str(e)}")
            fallback_content = InsightsGenerator._generate_fallback_insights(
                llm_input, top_k)
            return InsightsReport(fallback_content, format_type="text")

    @staticmethod
    def _generate_fallback_insights(llm_input: dict, top_k: int) -> str:
        """Generate fallback insights when LLM generation fails."""
        fallback = f"Top {top_k} Insights (Fallback):\n\n"
        for i, m in enumerate(llm_input["top_metrics"], 1):
            threshold_text = f", threshold: {m['threshold']}" if m.get(
                'threshold') is not None else ""
            fallback += f"{i}. {m['name']} ({m['group']}): value={m['value']}{threshold_text}\n"
        return fallback

    @staticmethod
    def _extract_list_items(text: str) -> List[str]:
        """
        Extract list items from text by splitting on numbered items or bullet points.

        Args:
            text: Text containing numbered or bulleted list items

        Returns:
            List of cleaned text items without markers
        """
        import re

        items = re.split(
            r'\n\s*(?=\d+[\.\)]\s+|-\s+|\*\s+|•\s+)', text)
        cleaned_items = []
        for item in items:
            # Remove leading bullet/number markers
            cleaned = re.sub(
                r'^\s*(?:\d+[\.\)]\s*|-\s+|\*\s+|•\s+)', '', item.strip())
            if cleaned:
                cleaned_items.append(cleaned)
        return cleaned_items

    @staticmethod
    def _parse_insights_sections(text: str) -> dict:
        """
        Parse the insights text into structured sections.

        Args:
            text: Raw insights text from LLM

        Returns:
            Dictionary with keys: top_insights, root_causes, recommendations
        """
        import re

        sections = {
            "top_insights": [],
            "root_causes": [],
            "recommendations": []
        }

        # Split by common section headers
        top_insights_match = re.search(
            r'(?:Top \d+ Insights?:|1\)\s*Top \d+ Insights?:)(.*?)(?=(?:Likely Root Causes?:|2\)|$))',
            text, re.DOTALL | re.IGNORECASE)
        root_causes_match = re.search(
            r'(?:Likely Root Causes?:|2\)\s*Likely Root Causes?:)(.*?)(?=(?:Recommendations?:|3\)|$))',
            text, re.DOTALL | re.IGNORECASE)
        recommendations_match = re.search(
            r'(?:Recommendations?:|3\)\s*Recommendations?:)(.*?)$',
            text, re.DOTALL | re.IGNORECASE)

        # Extract top insights
        if top_insights_match:
            insights_text = top_insights_match.group(1).strip()
            sections["top_insights"] = InsightsGenerator._extract_list_items(
                insights_text)

        # Extract root causes
        if root_causes_match:
            causes_text = root_causes_match.group(1).strip()
            sections["root_causes"] = InsightsGenerator._extract_list_items(
                causes_text)

        # Extract recommendations
        if recommendations_match:
            recs_text = recommendations_match.group(1).strip()
            sections["recommendations"] = InsightsGenerator._extract_list_items(
                recs_text)

        return sections

    @staticmethod
    def _wrap_text(text: str, width: int = 76, indent: str = "") -> str:
        """
        Wrap text to a specified width with optional indentation for continuation lines.

        Args:
            text: Text to wrap
            width: Maximum line width (default: 76)
            indent: Indentation string for continuation lines (default: "")

        Returns:
            Wrapped text with proper line breaks
        """
        import textwrap

        # Use textwrap to handle the wrapping
        wrapper = textwrap.TextWrapper(
            width=width,
            subsequent_indent=indent,
            break_long_words=False,
            break_on_hyphens=False
        )

        return wrapper.fill(text)

    @staticmethod
    def _format_structured_as_html(insights_text: str, llm_input: dict) -> str:
        """Format structured insights as HTML report with proper bullet points."""
        import html as pyhtml
        from datetime import datetime, timezone

        # Parse the insights
        parsed = InsightsGenerator._parse_insights_sections(insights_text)

        html_lines = [
            "<html><head><meta charset='utf-8'><title>AI System Insights Report</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }",
            "h1 { color: #333; }",
            "h2 { color: #666; margin-top: 30px; }",
            "h3 { color: #888; margin-top: 20px; }",
            "ul, ol { line-height: 1.8; margin-left: 20px; }",
            "li { margin-bottom: 10px; }",
            "table { border-collapse: collapse; width: 100%; margin-top: 20px; }",
            "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "th { background-color: #f2f2f2; font-weight: bold; }",
            ".metric-value { font-weight: bold; color: #d9534f; }",
            ".metric-group { color: #5bc0de; font-style: italic; }",
            ".section { margin-bottom: 30px; }",
            "</style></head><body>",
            "<h1>AI System Insights Report</h1>",
            f"<p><em>Generated: {datetime.now(timezone.utc).isoformat()}</em></p>",
            "<hr>"
        ]

        # Add Top Insights section
        if parsed["top_insights"]:
            html_lines.append("<div class='section'>")
            html_lines.append(
                f"<h2>Top {len(parsed['top_insights'])} Insights</h2>")
            html_lines.append("<ol>")
            for insight in parsed["top_insights"]:
                html_lines.append(f"<li>{pyhtml.escape(insight)}</li>")
            html_lines.append("</ol>")
            html_lines.append("</div>")

        # Add Root Causes section
        if parsed["root_causes"]:
            html_lines.append("<div class='section'>")
            html_lines.append("<h2>Likely Root Causes</h2>")
            html_lines.append("<ul>")
            for cause in parsed["root_causes"]:
                html_lines.append(f"<li>{pyhtml.escape(cause)}</li>")
            html_lines.append("</ul>")
            html_lines.append("</div>")

        # Add Recommendations section
        if parsed["recommendations"]:
            html_lines.append("<div class='section'>")
            html_lines.append("<h2>Recommendations</h2>")
            html_lines.append("<ol>")
            for rec in parsed["recommendations"]:
                html_lines.append(f"<li>{pyhtml.escape(rec)}</li>")
            html_lines.append("</ol>")
            html_lines.append("</div>")

        # If parsing failed, fall back to raw text
        if not any([parsed["top_insights"], parsed["root_causes"], parsed["recommendations"]]):
            html_lines.append("<div class='section'>")
            html_lines.append("<pre>")
            html_lines.append(pyhtml.escape(insights_text))
            html_lines.append("</pre>")
            html_lines.append("</div>")

        html_lines.append("<hr>")
        html_lines.append("<h2>Summary Statistics</h2>")
        html_lines.append(
            f"<p>Total metrics analyzed: <strong>{llm_input['summary_stats']['total_metrics']}</strong></p>")
        html_lines.append("<h3>Metrics by Group</h3>")
        html_lines.append("<table><tr><th>Group</th><th>Count</th></tr>")

        for group, count in llm_input['summary_stats']['metrics_by_group'].items(
        ):
            html_lines.append(
                f"<tr><td>{pyhtml.escape(group)}</td><td>{count}</td></tr>")

        html_lines.append("</table>")
        html_lines.append("<h3>Top Metrics Details</h3>")

        # Check if any metrics have applies_to='node' to determine if we should show node_name column
        has_node_metrics = any(m.get('applies_to') ==
                               'node' for m in llm_input['top_metrics'])

        # Build table header based on whether we have node metrics
        if has_node_metrics:
            html_lines.append(
                "<table><tr><th>Metric</th><th>Group</th><th>Node Name</th><th>Value</th><th>Threshold</th><th>Violations</th></tr>")
        else:
            html_lines.append(
                "<table><tr><th>Metric</th><th>Group</th><th>Value</th><th>Threshold</th><th>Violations</th></tr>")

        for m in llm_input['top_metrics']:
            threshold_val = m.get('threshold', 'N/A')
            applies_to = m.get('applies_to', 'unknown')
            node_name = m.get('node_name', '')

            # Build row based on whether we're showing node_name column
            if has_node_metrics:
                # Only show node_name value if applies_to is 'node'
                node_name_display = pyhtml.escape(
                    node_name) if applies_to == 'node' and node_name else '-'
                html_lines.append(
                    f"<tr><td>{pyhtml.escape(str(m['name']))}</td>"
                    f"<td class='metric-group'>{pyhtml.escape(str(m['group']))}</td>"
                    f"<td>{node_name_display}</td>"
                    f"<td class='metric-value'>{pyhtml.escape(str(m['value']))}</td>"
                    f"<td>{pyhtml.escape(str(threshold_val))}</td>"
                    f"<td>{m.get('violations_count', 0)}</td></tr>")
            else:
                html_lines.append(
                    f"<tr><td>{pyhtml.escape(str(m['name']))}</td>"
                    f"<td class='metric-group'>{pyhtml.escape(str(m['group']))}</td>"
                    f"<td class='metric-value'>{pyhtml.escape(str(m['value']))}</td>"
                    f"<td>{pyhtml.escape(str(threshold_val))}</td>"
                    f"<td>{m.get('violations_count', 0)}</td></tr>")

        html_lines.append("</table></body></html>")
        return "\n".join(html_lines)

    @staticmethod
    def _format_structured_as_json(insights_text: str, llm_input: dict) -> str:
        """Format structured insights as JSON with cleaned formatting."""
        import json as json_module
        from datetime import datetime, timezone

        # Parse the insights
        parsed_insights = InsightsGenerator._parse_insights_sections(
            insights_text)

        # Clean up top_metrics by removing newlines from node_name
        cleaned_metrics = []
        for metric in llm_input["top_metrics"]:
            cleaned_metric = metric.copy()
            if "node_name" in cleaned_metric and cleaned_metric["node_name"]:
                # Replace newlines and multiple spaces with single space
                cleaned_metric["node_name"] = ' '.join(
                    cleaned_metric["node_name"].split())
            cleaned_metrics.append(cleaned_metric)

        # Create JSON structure with parsed insights
        output = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "insights": {
                "top_insights": parsed_insights["top_insights"],
                "root_causes": parsed_insights["root_causes"],
                "recommendations": parsed_insights["recommendations"]
            },
            "summary_stats": llm_input["summary_stats"],
            "top_metrics": cleaned_metrics
        }

        return json_module.dumps(output, indent=2, ensure_ascii=False)

    @staticmethod
    def _format_structured_as_text(insights_text: str, llm_input: dict) -> str:
        """Format structured insights as plain text with proper formatting for Jupyter notebooks."""
        from datetime import datetime, timezone

        # Parse the insights
        parsed = InsightsGenerator._parse_insights_sections(insights_text)

        lines = [
            "=" * 80,
            "AI System Insights Report",
            "=" * 80,
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            ""
        ]

        # Add Top Insights section
        if parsed["top_insights"]:
            lines.append(f"1) Top {len(parsed['top_insights'])} Insights:")
            lines.append("")
            for i, insight in enumerate(parsed["top_insights"], 1):
                # Wrap long lines for better readability
                wrapped_insight = InsightsGenerator._wrap_text(
                    insight, width=76, indent="   ")
                lines.append(f"   {i}. {wrapped_insight}")
                lines.append("")

        # Add Root Causes section
        if parsed["root_causes"]:
            lines.append("2) Likely Root Causes:")
            lines.append("")
            for cause in parsed["root_causes"]:
                wrapped_cause = InsightsGenerator._wrap_text(
                    cause, width=76, indent="      ")
                lines.append(f"   - {wrapped_cause}")
                lines.append("")

        # Add Recommendations section
        if parsed["recommendations"]:
            lines.append("3) Recommendations:")
            lines.append("")
            for i, rec in enumerate(parsed["recommendations"], 1):
                wrapped_rec = InsightsGenerator._wrap_text(
                    rec, width=76, indent="      ")
                lines.append(f"   {i}) {wrapped_rec}")
                lines.append("")

        # If parsing failed, fall back to raw text
        if not any([parsed["top_insights"], parsed["root_causes"], parsed["recommendations"]]):
            lines.append(insights_text)
            lines.append("")

        lines.extend([
            "=" * 80,
            "Summary Statistics",
            "=" * 80,
            f"Total metrics analyzed: {llm_input['summary_stats']['total_metrics']}",
            ""
        ])

        # Metrics by Group
        if llm_input['summary_stats']['metrics_by_group']:
            lines.append("Metrics by Group:")
            for group, count in llm_input['summary_stats']['metrics_by_group'].items():
                lines.append(f"  - {group}: {count}")
            lines.append("")

        # Top Metrics Details
        lines.extend([
            "Top Metrics Details:",
            "-" * 80
        ])

        for m in llm_input['top_metrics']:
            threshold_val = m.get('threshold', 'N/A')
            applies_to = m.get('applies_to', 'unknown')
            node_name = m.get('node_name', '')

            # Clean node name by replacing newlines and extra spaces
            if node_name:
                node_name = ' '.join(node_name.split())

            # Build metric line with node name if it's a node-level metric
            if applies_to == 'node' and node_name:
                lines.append(
                    f"  • {m['name']} ({m['group']}) [Node: {node_name}]:"
                )
                lines.append(
                    f"    value={m['value']}, threshold={threshold_val}, violations={m.get('violations_count', 0)}"
                )
            else:
                lines.append(
                    f"  • {m['name']} ({m['group']}):"
                )
                lines.append(
                    f"    value={m['value']}, threshold={threshold_val}, violations={m.get('violations_count', 0)}"
                )

        lines.append("=" * 80)
        return "\n".join(lines)
