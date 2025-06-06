from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from services.embedding_service import EmbeddingService
from app.utils.file_reader import read_files_in_folder
from services.user_database_service import UserDatabaseService
from services.vector_db_service import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

app = FastAPI()
security = HTTPBasic()

user_db = None
vector_store = None
embedding_service = None


@app.on_event("startup")
async def startup_event():
    global user_db, vector_store, embedding_service
    user_db = UserDatabaseService()
    vector_store = VectorStore()
    embedding_service = EmbeddingService()


# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = user_db.get_user(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}


# Login endpoint
@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


@app.get("/save_folder_data")
def save_data():
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
            embedding = embedding_service.get_embedding(text_chunks[i])

            extracted_data["embeddings"].append(embedding)
            extracted_data["docs"].append(text_chunks[i])
            extracted_data["access_role"].append({"role_access": file_data["subfolder"]})
            extracted_data["ids"].append(file_data["file_name"] + "part - " + str(i + 1))

    vector_store.save_documents(
        documents=extracted_data["docs"],
        metadatas=extracted_data["access_role"],
        ids=extracted_data["ids"],
        embeddings=extracted_data["embeddings"]
    )

    query_result = vector_store.query(
        query_embeddings=embedding_service.get_embedding("Onboarding Process"),
        where={'role_access': {'$in': ['management', 'general']}}
    )

    return query_result


# Protected chat endpoint
@app.post("/chat")
def query(user=Depends(authenticate), message: str = "Hello"):
    return "Implement this endpoint."
