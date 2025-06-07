from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from chatbot_manager import ChatbotManager

app = FastAPI()
security = HTTPBasic()

chatbot_manager: ChatbotManager = None


@app.on_event("startup")
async def startup_event():
    global chatbot_manager
    chatbot_manager = ChatbotManager()


# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    user_role = chatbot_manager.authenticate_user(credentials.username, credentials.password)
    if user_role is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": credentials.username, "role": user_role}


# Login endpoint
@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


@app.get("/")
def test():
    return {"message": "Hi there. Please login to chat. Use /login"}


@app.get("/save_folder_data")
def save_data():
    message = chatbot_manager.extract_and_save_data()
    return {"message": message}


# Protected chat endpoint
@app.post("/chat")
def query(message: str, user=Depends(authenticate)):
    username = user["username"]
    response = chatbot_manager.chat(message, username)
    return {"message": response}
