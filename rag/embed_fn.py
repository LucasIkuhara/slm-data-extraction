from ollama import Client
from numpy import array


def embed_str(text: str, model: str, client=Client("127.0.0.1")) -> array:
    """
    Embeds the input using an LLM of choice.

    Params:
      - text: The input text.
      - model: A valid ollama model tag.

    Returns:
        An array containing the embedding.
    """
    emb = client.embed(
        model=model,
        input=[text],
    )
    embedding_vec = array(emb.embeddings[0])

    return embedding_vec
