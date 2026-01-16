from __future__ import annotations

import os

SERVER_NAME      = "boostspace-mcp"
API_BASE: str | None = os.getenv("BOOSTSPACE_API_BASE")
TOKEN:    str | None = os.getenv("BOOSTSPACE_TOKEN")

ALLOWED_ENDPOINTS: list[str] = [] # Empty list  ⇒  allow every endpoint
# EXAMPLE of ALLOWED_ENDPOINTS values:
#    [
#        "GET    /custom-module",
#        "GET    /custom-module-item",
#    ]

# For testing purposes, provide default values if environment variables are not set
if API_BASE is None:
    API_BASE = "https://app.boost.space/api"
    print("[WARNING] BOOSTSPACE_API_BASE not set, using default for testing: https://app.boost.space/api")

if TOKEN is None:
    TOKEN = "test_token_for_testing"
    print("[WARNING] BOOSTSPACE_TOKEN not set, using default for testing: test_token_for_testing")