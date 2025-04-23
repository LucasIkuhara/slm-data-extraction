from typing import List, Optional, Tuple
from sqlalchemy import Connection
import numpy as np
from sqlalchemy import text


class EmbeddingStore:
    """
    Handles the searching and saving of embeddings to a database.
    """

    def __init__(self, db_conn: Connection):
        self.conn = db_conn

    def save_embedding(
        self, file_name: str, page_number: int, embedding: np.array, model_name: str
    ):
        """
        Saves the embeddings and its related metadata at a database.

        Parameters:
         - file_name: The original file from which the text was extracted.
         - page_num: The page from which the text was extracted.
         - embedding: The embedding array.
         - model_name: The embedding model used.

         Raises:
          - sqlalchemy.exc.IntegrityError: In case the embedding already exists.
        """
        statement = text(
            "INSERT INTO EMBEDDING (source_file, page_num, embedding, model) VALUES (:some_file, :page_num, :emb, :model)"
        )
        self.conn.execute(
            statement,
            [
                {
                    "some_file": file_name,
                    "page_num": page_number,
                    "emb": embedding,
                    "model": model_name,
                }
            ],
        )
        self.conn.commit()

    def fetch_closest_embeddings(
        self,
        query_embedding: np.array,
        model_name: str,
        n: int = 10,
        source_files: Optional[List[str]] = None,
    ) -> Tuple[str, int, np.array, str]:
        """
        Parameters:
         - query_embedding: The embedding of the RAG query.
         - model_name: The embedding model used.
         - n: The max number of results to return.
         - source_files: An array of base files to look through.

        Returns:
          A list of tuples containing the source file, page number, embedding and model used.
        """

        query_args = {
            "query": query_embedding,
            "model": model_name,
            "n": n,
        }

        where_clause = "WHERE model = :model"
        if source_files:
            where_clause += " AND source_file IN (:files) "

        statement = text(
            f"""SELECT source_file, page_num, embedding, model FROM EMBEDDING 
            {where_clause}
            ORDER BY embedding <-> :query LIMIT :n; """
        )
        values = self.conn.execute(
            statement,
            [query_args],
        )

        self.conn.commit()
        return [x for x in values]
