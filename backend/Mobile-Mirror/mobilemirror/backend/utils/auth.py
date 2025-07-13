#!/usr/bin/env python3
# auth.py — TouchCore lightweight token check

import os

# Default secret token (could be replaced with env var or file-based secret)
DEFAULT_TOKEN = "touchcore-access"

def verify_token(token: str) -> bool:
    expected = os.getenv("TOUCHCORE_TOKEN", DEFAULT_TOKEN)
    return token == expected