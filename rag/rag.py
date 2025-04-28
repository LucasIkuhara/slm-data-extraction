from typing import List
from embedding_store import EmbeddingStore
from embed_fn import embed_str
from page_reader import DocumentPage, PageReader
from embed_fn import embed_str


class Rag:

    def __init__(self, store: EmbeddingStore, page_reader: PageReader, model_name: str):
        self.store = store
        self.page_reader = page_reader
        self.model = model_name

    def get_context_by_prompt(
        self, prompt: str, allowed_sources: List[str], n: int = 10
    ) -> List[DocumentPage]:
        """
        Fetches the N most relevant pages based on
        cosine similarity from the entered prompt.

        Args:
            prompt: The prompt used to base the search.
            allowed_sources: What documents to include in the search.
            n: The maximum number of returned files.

        Returns:
            The N most relevant pages, in descending order of relevance.
        """

        # Embed input prompt and query vector Db
        x = embed_str(prompt, self.model)
        query_result = self.store.fetch_closest_embeddings(
            x, self.model, n, allowed_sources
        )

        files = []
        for document, page, _, _ in query_result:
            page_txt = self.page_reader.get_file(document, page)
            v = DocumentPage(document, page, page_txt)
            files.append(v)

        return files
