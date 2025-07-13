#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: nlp_engine/chat_session.py :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# GremlinGPT v1.0.3 :: nlp_engine/chat_session.py
# Self-improving chat session manager for GremlinGPT.
# Handles dialog state, memory, feedback, and learning integration.


from datetime import datetime, timezone
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from memory.log_history import log_event
from nlp_engine.tokenizer import tokenize
from nlp_engine.semantic_score import reasoned_similarity
from agent_core.fsm import inject_task
from backend.api.chat_handler import chat as backend_chat

__all__ = ["ChatSession"]


class ChatSession:
    """
    ChatSession manages a dialog session, maintaining a history of turns.

    self.history: List of tuples in the format:
        (user_input: str, bot_response: str, meta: dict)
    where meta contains optional keys such as:
        - "explanation": str or None
        - "feedback": any feedback provided by the user
    """


    def __init__(self, user_id=None):
        self.user_id = user_id or "anon"
        self.history = []  # List of (user, bot, meta)
        self.created = datetime.utcnow().isoformat()
        safe_created = self.created.replace(":", "-")
        self.session_id = f"chat_{self.user_id}_{safe_created}"
        self.memory_trace = []


    def process_input(self, user_input, context=None, feedback=None):
        # Tokenize and embed
        tokens = tokenize(user_input)
        vector = embed_text(user_input)
        package_embedding(
            text=user_input,
            vector=vector,
            meta={
                "origin": "chat_session",
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": self.user_id,
                "session_id": self.session_id,
                "token_count": len(tokens),
            },
        )
        inject_watermark(origin="chat_session")
        # Call backend chat handler for response
        bot_response = backend_chat(user_input)
        # Ensure output is always a string
        if isinstance(bot_response, dict):
            # Prefer explicit "response" key; fallback to first value if not present
            if "response" in bot_response:
                bot_response = str(bot_response["response"])
            else:
                # Fallback: use the first value in the dict (documented behavior)
                bot_response = str(next(iter(bot_response.values()), ""))
        else:
            bot_response = str(bot_response)
        # Optionally, reason about similarity to previous turns
        explanation = None
        if self.history:
            prev_user, prev_bot, _ = self.history[-1]
            sim = reasoned_similarity(prev_user, user_input)
            explanation = sim.get("explanation")
        # Log event
        # Optionally, reason about similarity to previous turns
        # 'explanation' holds reasoning or similarity explanation for the current turn, if available
        explanation = None
        if self.history:
            prev_user, prev_bot, _ = self.history[-1]
            sim = reasoned_similarity(prev_user, user_input)
            explanation = sim.get("explanation")
        # Store in history
        self.history.append((user_input, bot_response, {"explanation": explanation, "feedback": feedback}))
        # Optionally inject feedback for learning
        if feedback:
            inject_task({"type": "feedback", "input": user_input, "feedback": feedback})
        return {
            "response": bot_response,
# For API/CLI usage
            "session_id": self.session_id,
        }


    def get_history(self):
        return self.history

# For API/CLI usage
__all__ = ["ChatSession"]
