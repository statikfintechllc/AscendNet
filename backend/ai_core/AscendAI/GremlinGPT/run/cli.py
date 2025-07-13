#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Fair-Use License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Unified CLI (NLP+Chat/Session)

import readline
import sys
import os

# --- Set project root and sys.path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# --- Core Imports ---
import nltk
from utils.nltk_setup import setup_nltk_data
from nlp_engine.parser import parse_nlp
from loguru import logger
from backend.api.chat_handler import chat
from nlp_engine.chat_session import ChatSession

# --- Ensure NLTK Paths and Resources (centralized) ---
NLTK_DATA_DIR = setup_nltk_data()
if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_DIR)

BANNER = """
🌩️  GremlinGPT Terminal v1.0.3 [NLP+Chat Mode]
Type your command. Type 'exit' to leave.
Type '/session' to enter session chat mode (with memory).
Type '/nlp' to return to NLP+chat mode.
"""

MODE_NLP = "nlp"
MODE_SESSION = "session"


def main():
    print(BANNER)
    mode = MODE_NLP
    session = ChatSession(user_id="cli_user")
    while True:
        try:
            user_input = input("👤 > ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("GremlinGPT going dark.")
                break
            if user_input.lower() == "/session":
                mode = MODE_SESSION
                print("[Switched to session chat mode]")
                continue
            if user_input.lower() == "/nlp":
                mode = MODE_NLP
                print("[Switched to NLP+chat mode]")
                continue
            if mode == MODE_NLP:
                logger.info(f"[CLI] Received input: {user_input}")
                result = parse_nlp(user_input)
                print("\n🧠 NLP Engine Output:")
                print(f"- Intent route: {result['route']}")
                print(f"- Tokens: {result['tokens'][:10]}...")
                print(f"- POS tags: {result['pos'][:5]}...")
                print(f"- Entities: {result['entities']}")
                print(f"- Financial terms: {result['financial_hits']}")
                print(f"- Code structures: {result['code_entities']}")
                response = chat(user_input)
                # Normalize response
                if isinstance(response, str):
                    msg = response
                elif isinstance(response, dict):
                    msg = response.get("response", next(iter(response.values()), ""))
                elif isinstance(response, tuple):
                    val = response[0]
                    if isinstance(val, dict):
                        msg = val.get("response", next(iter(val.values()), ""))
                    else:
                        msg = str(val)
                else:
                    msg = str(response)
                print("🤖 GremlinGPT:", msg)
                print("-" * 40)
            elif mode == MODE_SESSION:
                result = session.process_input(user_input)
                print(f"Gremlin: {result['response']}")
                if result.get("explanation"):
                    print(f"[Reasoning] {result['explanation']}")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Shutting down.")
            break
        except EOFError:
            print("\nEOF detected (Ctrl-D). Exiting CLI.")
            break
        except Exception as e:
            logger.exception(f"[CLI] Error during input handling: {e}")
            print(
                "An error occurred while handling your input. Please check the logs for details."
            )


if __name__ == "__main__":
    main()
