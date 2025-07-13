#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: FSM Core & Module Integrity Directive

import numpy as np
from datetime import datetime
from memory.vector_store.embedder import package_embedding, embed_text
from memory.log_history import log_event
from self_training.feedback_loop import inject_feedback

WATERMARK = "source:GremlinGPT"
MODULE = "mini_attention"


class MiniMultiHeadAttention:
    """
    Production-grade, traceable, multi-head self-attention module, fully integrated with
    GremlinGPT system memory, feedback, and event logging.
    Now supports dropout, bias, per-head extraction, and attention visualization stub.
    """

    def __init__(self, embed_dim, num_heads=4, scale=True, seed=None, dropout=0.0, use_bias=True):
        assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = scale
        self.dropout = dropout
        self.use_bias = use_bias

        # Allow deterministic initialization for traceability/testing
        if seed is not None:
            np.random.seed(seed)

        # Initialize projection weights (Kaiming-like, small variance)
        self.W_q = np.random.randn(num_heads, embed_dim, self.head_dim) * (
            2.0 / np.sqrt(embed_dim)
        )
        self.W_k = np.random.randn(num_heads, embed_dim, self.head_dim) * (
            2.0 / np.sqrt(embed_dim)
        )
        self.W_v = np.random.randn(num_heads, embed_dim, self.head_dim) * (
            2.0 / np.sqrt(embed_dim)
        )
        self.W_out = np.random.randn(num_heads * self.head_dim, embed_dim) * (
            2.0 / np.sqrt(embed_dim)
        )
        if self.use_bias:
            self.b_q = np.zeros((num_heads, self.head_dim))
            self.b_k = np.zeros((num_heads, self.head_dim))
            self.b_v = np.zeros((num_heads, self.head_dim))
            self.b_out = np.zeros((embed_dim,))
        else:
            self.b_q = self.b_k = self.b_v = self.b_out = None

    def _softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)

    def _apply_mask(self, scores, mask=None):
        if mask is not None:
            # Set masked positions to a large negative value for softmax
            scores = np.where(mask, scores, -1e9)
        return scores

    def _apply_dropout(self, x):
        if self.dropout > 0.0:
            mask = np.random.binomial(1, 1 - self.dropout, size=x.shape)
            return x * mask / (1 - self.dropout)
        return x

    def _combine_heads(self, heads):
        # heads: (num_heads, seq_len, head_dim) -> (seq_len, num_heads * head_dim)
        return heads.transpose(1, 0, 2).reshape(heads.shape[1], -1)

    def forward(self, X, mask=None, return_qkv=False):
        """
        Args:
            X: (seq_len, embed_dim)
            mask: (seq_len, seq_len) boolean or None
            return_qkv: if True, also return Q, K, V for analysis
        Returns:
            output: (seq_len, embed_dim)
            weights: (num_heads, seq_len, seq_len)
            (optionally) Q, K, V: each (num_heads, seq_len, head_dim)
        """
        seq_len = X.shape[0]
        head_outputs = []
        all_weights = []
        Qs, Ks, Vs = [], [], []

        for h in range(self.num_heads):
            Q = X @ self.W_q[h]
            K = X @ self.W_k[h]
            V = X @ self.W_v[h]
            if self.use_bias and self.b_q is not None and self.b_k is not None and self.b_v is not None:
                Q = Q + self.b_q[h]
                K = K + self.b_k[h]
                V = V + self.b_v[h]
            Qs.append(Q)
            Ks.append(K)
            Vs.append(V)
            scores = Q @ K.T
            if self.scale:
                scores = scores / np.sqrt(self.head_dim)
            scores = self._apply_mask(scores, mask)
            weights = self._softmax(scores)
            weights = self._apply_dropout(weights)
            output = weights @ V
            head_outputs.append(output)
            all_weights.append(weights)

        # Stack heads: (num_heads, seq_len, head_dim)
        head_outputs = np.stack(head_outputs, axis=0)
        all_weights = np.stack(all_weights, axis=0)
        Qs = np.stack(Qs, axis=0)
        Ks = np.stack(Ks, axis=0)
        Vs = np.stack(Vs, axis=0)

        combined = self._combine_heads(head_outputs)  # (seq_len, embed_dim)
        final_output = combined @ self.W_out  # (seq_len, embed_dim)
        if self.use_bias:
            final_output = final_output + self.b_out

        self._log_attention_event(X, final_output, all_weights, mask)

        if return_qkv:
            return final_output, all_weights, Qs, Ks, Vs
        return final_output, all_weights

    def extract_attention(self, attn_weights, token_idx=None, head_idx=None):
        """
        Extract attention weights for a specific token or head.
        Args:
            attn_weights: (num_heads, seq_len, seq_len)
            token_idx: int or None (if None, return all tokens)
            head_idx: int or None (if None, return all heads)
        Returns:
            np.ndarray: selected attention weights
        """
        if head_idx is not None and token_idx is not None:
            return attn_weights[head_idx, token_idx]
        elif head_idx is not None:
            return attn_weights[head_idx]
        elif token_idx is not None:
            return attn_weights[:, token_idx]
        return attn_weights

    def visualize_attention(self, attn_weights, tokens=None):
        """
        Placeholder for attention visualization. In a real system, this could generate a heatmap.
        Args:
            attn_weights: (num_heads, seq_len, seq_len)
            tokens: list of str or None
        """
        print("[MiniAttention] Visualization stub: attention weights shape:", attn_weights.shape)
        if tokens is not None:
            print("Tokens:", tokens)
        # Visualization logic would go here (e.g., matplotlib, seaborn)

    def _log_attention_event(self, input_tensor, output_tensor, weights, mask):
        timestamp = datetime.utcnow().isoformat()
        info = {
            "origin": MODULE,
            "event": "forward_pass",
            "watermark": WATERMARK,
            "timestamp": timestamp,
            "shape_input": input_tensor.shape,
            "shape_output": output_tensor.shape,
            "num_heads": self.num_heads,
            "mask_applied": mask is not None,
        }
        # Log to system memory and logs
        log_event(MODULE, "attention_forward", info)
        summary = (
            f"MiniAttention: {self.num_heads} heads | "
            f"in={input_tensor.shape} out={output_tensor.shape} mask={mask is not None}"
        )
        vector = embed_text(summary)
        package_embedding(text=summary, vector=vector, meta=info)
        # Training signal hint
        inject_feedback()

    def repair_weights(self):
        """
        Reload/reinitialize weights in case of detection of corruption or failed shapes.
        """
        self.W_q = np.random.randn(self.num_heads, self.embed_dim, self.head_dim) * (
            2.0 / np.sqrt(self.embed_dim)
        )
        self.W_k = np.random.randn(self.num_heads, self.embed_dim, self.head_dim) * (
            2.0 / np.sqrt(self.embed_dim)
        )
        self.W_v = np.random.randn(self.num_heads, self.embed_dim, self.head_dim) * (
            2.0 / np.sqrt(self.embed_dim)
        )
        self.W_out = np.random.randn(self.num_heads * self.head_dim, self.embed_dim) * (
            2.0 / np.sqrt(self.embed_dim)
        )
        if self.use_bias:
            self.b_q = np.zeros((self.num_heads, self.head_dim))
            self.b_k = np.zeros((self.num_heads, self.head_dim))
            self.b_v = np.zeros((self.num_heads, self.head_dim))
            self.b_out = np.zeros((self.embed_dim,))
        log_event(
            MODULE,
            "weights_repair",
            {
                "origin": MODULE,
                "timestamp": datetime.utcnow().isoformat(),
                "event": "repair_weights",
            },
        )


# === Example Run ===
if __name__ == "__main__":
    np.random.seed(42)
    dummy_input = np.random.rand(8, 64)  # 8 tokens, 64-dimensional embeddings

    attention = MiniMultiHeadAttention(embed_dim=64, num_heads=4, scale=True, seed=42, dropout=0.1, use_bias=True)

    # Example: causal mask (lower triangle: allow attending to current and previous tokens)
    causal_mask = np.tril(np.ones((8, 8))).astype(bool)

    # Always call with return_qkv=True if unpacking 5 values
    result = attention.forward(dummy_input, mask=causal_mask, return_qkv=True)
    if len(result) == 5:
        out, attn_weights, Q, K, V = result
        print(f"Output shape: {out.shape}")
        print(f"Attention shape: {attn_weights.shape}")
        print(f"Q shape: {Q.shape}, K shape: {K.shape}, V shape: {V.shape}")
        # Extract and visualize attention for token 0, head 0
        attn_0_0 = attention.extract_attention(attn_weights, token_idx=0, head_idx=0)
        print(f"Attention for head 0, token 0: {attn_0_0}")
        attention.visualize_attention(attn_weights)
    else:
        out, attn_weights = result
        print(f"Output shape: {out.shape}")
        print(f"Attention shape: {attn_weights.shape}")
        attention.visualize_attention(attn_weights)

    # Test repair_weights
    attention.repair_weights()
    print("Weights repaired and reinitialized.")
