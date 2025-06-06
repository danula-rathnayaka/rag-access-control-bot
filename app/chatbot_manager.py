from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.embedding_service import EmbeddingService
from services.user_database_service import UserDatabaseService
from services.vector_db_service import VectorStore
from utils.file_reader import read_files_in_folder


class ChatbotManager:
    def __init__(self):
        self.user_db = UserDatabaseService()
        self.vector_store = VectorStore()
        self.embedding_service = EmbeddingService()

    def authenticate_user(self, username, password):
        user = self.user_db.get_user(username)
        if not user or user["password"] != password:
            return None
        return user["role"]

    def extract_and_save_data(self):
        folder_file_data = read_files_in_folder()

        extracted_data = {
            "docs": [],
            "embeddings": [],
            "access_role": [],
            "ids": []
        }

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1024,
            chunk_overlap=256,
        )

        for file_data in folder_file_data:
            file_content = file_data["content"]

            text_chunks = text_splitter.split_text(file_content)

            for i in range(len(text_chunks)):
                embedding = self.embedding_service.get_embedding(text_chunks[i])

                extracted_data["embeddings"].append(embedding)
                extracted_data["docs"].append(text_chunks[i])
                extracted_data["access_role"].append({"role_access": file_data["subfolder"]})
                extracted_data["ids"].append(file_data["file_name"] + "part - " + str(i + 1))

        self.vector_store.save_documents(
            documents=extracted_data["docs"],
            metadatas=extracted_data["access_role"],
            ids=extracted_data["ids"],
            embeddings=extracted_data["embeddings"]
        )

        return "Saved Successfully"

    def chat(self, message, username):
        # TODO
        pass
