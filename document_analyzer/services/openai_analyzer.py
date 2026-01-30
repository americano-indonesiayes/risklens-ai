import json
import os
from typing import Any, Dict, Optional

import requests
from django.conf import settings


class OpenAIAnalyzerError(Exception):
    pass


def analyze_text(text: str, model: Optional[str] = None, timeout: int = 60) -> Dict[str, Any]:
    api_key = getattr(settings, "OPENAI_API_KEY", None) or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIAnalyzerError("OPENAI_API_KEY is not set.")

    model_name = model or getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "risk_level": {
                "type": "string",
                "enum": ["SAFE", "MODERATE", "HIGH"],
            },
            "recommended_disclosure": {
                "type": "string",
                "enum": ["PUBLIC_SAFE", "INTERNAL_ONLY", "RESTRICTED"],
            },
            "flag_reasons": {
                "type": "array",
                "items": {"type": "string"},
            },
            "categories": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "PII",
                        "SECRETS",
                        "SOCIAL_ENGINEERING",
                        "CONFIDENTIAL_BUSINESS",
                    ],
                },
            },
            "safe_version": {"type": "string"},
        },
        "required": [
            "risk_level",
            "recommended_disclosure",
            "flag_reasons",
            "categories",
            "safe_version",
        ],
    }

    system_prompt = (
        "You are a governance layer for document risk analysis. "
        "Return ONLY valid JSON that matches the provided schema. "
        "Classify risk, suggest disclosure, list reasons, categorize, "
        "and provide a safe redacted version."
    )

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "document_analysis", "schema": schema, "strict": True},
        },
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise OpenAIAnalyzerError(f"OpenAI request failed: {exc}") from exc

    if response.status_code != 200:
        raise OpenAIAnalyzerError(
            f"OpenAI request failed ({response.status_code}): {response.text}"
        )

    try:
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)
    except (KeyError, json.JSONDecodeError) as exc:
        raise OpenAIAnalyzerError(f"Invalid OpenAI response: {exc}") from exc
