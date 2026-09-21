from __future__ import annotations

import json
from urllib.parse import quote
from urllib.request import Request, urlopen


API_URL = "https://huggingface.co/api/models"


def search_public_models(query: str = "", limit: int = 8) -> list[dict[str, object]]:
    """Search the public Hugging Face Hub API on explicit user request."""
    params = f"?search={quote(query)}&pipeline_tag=text-generation&sort=downloads&direction=-1&limit={max(1, min(limit, 20))}"
    request = Request(API_URL + params, headers={"User-Agent": "GENESIS-model-onboarding/0.1"})
    with urlopen(request, timeout=8) as response:  # nosec B310 - fixed public HTTPS endpoint
        payload = json.loads(response.read().decode("utf-8"))
    return [
        {
            "id": item.get("id", ""),
            "downloads": item.get("downloads", 0),
            "likes": item.get("likes", 0),
            "pipeline_tag": item.get("pipeline_tag", "text-generation"),
        }
        for item in payload
        if isinstance(item, dict)
    ]
