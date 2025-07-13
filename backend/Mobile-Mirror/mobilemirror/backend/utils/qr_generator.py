#!/usr/bin/env python3
# qr_generator.py — Renders QR code for mobile broadcast access

import subprocess
import base64
from io import BytesIO
from PIL import Image


def generate_qr(url: str) -> dict:
    """
    Returns a dict with base64-encoded PNG of QR code for the given URL
    """
    try:
        qr_img = subprocess.check_output(["qrencode", "-t", "PNG", "-o", "-", url])
        b64img = base64.b64encode(qr_img).decode()
        return {"url": url, "qr_base64": f"data:image/png;base64,{b64img}"}
    except Exception as e:
        return {"error": str(e)}
