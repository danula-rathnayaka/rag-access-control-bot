from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    def __init__(self, model_name="BAAI/bge-base-en-v1.5"):
        """
        Create the Embedding Service object with the required model

        :param model_name: String, Optional, Hugging Face model to use for embedding. Default "BAAI/bge-base-en-v1.5".
        """
        self.model_name = model_name
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs={'normalize_embeddings': True}
        )

    def get_embedding(self, query):
        """
        Generates a normalized embedding vector for a given text query using a specified Hugging Face model.

        :param query: String, the input text to be embedded.

        :return list: A list of float values representing the normalized embedding vector.
        """
        try:
            # Initialize the HuggingFaceEmbeddings model with normalization enabled

            # Generate the embedding for the input query
            embedding = self.embedding_model.embed_query(query)

            print(
                f"Successfully generated embedding for query: '{query[:15]}...' using model: '{self.model_name}'")
            return embedding

        except Exception:
            print(f"Error generating embedding for query: '{query[:15]}' with model: '{self.model_name}'")
            raise
