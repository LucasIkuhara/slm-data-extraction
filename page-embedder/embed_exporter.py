from sqlalchemy import Connection
import numpy as np
from sqlalchemy import text


class EmbedExporter:
    """
    Handles the exporting of embeddings to a database.
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
