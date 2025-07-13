from memory.vector_store.embedder import embed_text, package_embedding


def inject_fake_vector():
    vector = [0.1] * 768
    package_embedding(
        text="Injected vector from dev-experiment.",
        vector=vector,
        meta={"agent": "dev-injector", "watermark": "mutation-test"},
    )
