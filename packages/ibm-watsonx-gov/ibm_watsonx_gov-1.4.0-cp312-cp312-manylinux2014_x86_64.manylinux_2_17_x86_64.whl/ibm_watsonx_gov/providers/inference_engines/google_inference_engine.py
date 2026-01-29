# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADP Schedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Any, Dict, List, Union

from datasets import Dataset
from unitxt.inference import (InferenceEngine, PackageRequirementsMixin,
                              StandardAPIParamsMixin,
                              TextGenerationInferenceOutput,
                              get_model_and_label_id)

try:
    from google.genai import types
except:
    pass


class GoogleStudioInferenceEngine(
    InferenceEngine, StandardAPIParamsMixin, PackageRequirementsMixin
):
    label: str = "google"
    _requirements_list = {
        "google-genai": (
            "Install Google GenAI client using: "
            "'pip install --upgrade google-genai'"
        )
    }
    model: str = None
    credentials: Dict[str, str] = {}

    def get_engine_id(self):
        return get_model_and_label_id(self.model, self.label)

    def to_google_messages(self, instance):
        msg = self.to_messages(instance)
        return [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=msg[0]["content"]),
                ],
            ),
        ]

    def prepare_engine(self):
        from google import genai

        if "api_key" not in self.credentials:
            raise ValueError(
                "api_key is missing from the credentials. Please set the GOOGLE_API_KEY environment variable to provide the API key.")

        self.client = genai.Client(
            api_key=self.credentials["api_key"],
        )

    def _infer(
        self,
        dataset: Union[List[Dict[str, Any]], Dataset],
        return_meta_data: bool = False,
    ) -> Union[List[str], List[TextGenerationInferenceOutput]]:
        args = self.to_dict([StandardAPIParamsMixin])
        results = []
        for instance in dataset:
            messages = self.to_google_messages(instance)
            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=messages,
            )
            # Extract text from response
            text = ""
            for chunk in response:
                if chunk.text:
                    text += chunk.text
            results.append(text)

        return results
