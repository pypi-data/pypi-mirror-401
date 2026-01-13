from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import urllib.request
import json


@dataclass
class AngelQClient:
    """
    Minimal client skeleton for the AngelQ API.

    This initial release exists to establish the 'angelq-client' name on PyPI.
    The API surface will expand in future releases.
    """
    base_url: str
    api_key: Optional[str] = None
    timeout_s: float = 30.0

    def get_json(self, path: str) -> Dict[str, Any]:
        """Very small helper to GET a JSON endpoint."""
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        req = urllib.request.Request(url, method="GET")
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")

        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            data = resp.read().decode("utf-8")
        return json.loads(data)
