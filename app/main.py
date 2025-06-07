from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from chatbot_manager import ChatbotManager

app = FastAPI()
security = HTTPBasic()

chatbot_manager: ChatbotManager = None


@app.on_event("startup")
async def startup_event():
    global chatbot_manager
    chatbot_manager = ChatbotManager()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    user_role = chatbot_manager.authenticate_user(credentials.username, credentials.password)
    if user_role is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": credentials.username, "role": user_role}


@app.get("/")
def test():
    # Public test endpoint, no auth needed
    return {"message": "Hi there. Please login to chat. Use /login"}


@app.get("/login")
def login(user=Depends(authenticate)):
    # Login endpoint, returns welcome message and role
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


@app.get("/logout")
def logout(user=Depends(authenticate)):
    # Logout endpoint, returns goodbye message
    return {"message": f"Goodbye {user['username']}! You've been logged out."}


@app.get("/test")
def test(user=Depends(authenticate)):
    # Authenticated test endpoint to verify login and chat access
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


@app.get("/save_folder_data")
def save_data():
    # Trigger data extraction and saving
    message = chatbot_manager.extract_and_save_data()
    return {"message": message}


@app.post("/chat")
async def query(message: str, user=Depends(authenticate)):
    # Chat endpoint to send message and receive response
    username = user["username"]
    role = user["role"]
    response = await chatbot_manager.chat(message, str(username), str(role))
    return {"message": response}


@app.post("/users/add")
def add_user(username: str = Body(...), password: str = Body(...), role: str = Body(...), user=Depends(authenticate)):
    # Add a new user (admin only)
    if user["role"] != "hr":
        raise HTTPException(status_code=403, detail="Only admin can add users.")
    message = chatbot_manager.add_user(username, password, role)
    return {"message": message}


@app.put("/users/update")
def update_user(username: str = Body(...), password: str = Body(None), role: str = Body(None),
                user=Depends(authenticate)):
    # Update existing user details (admin only)
    if user["role"] != "hr":
        raise HTTPException(status_code=403, detail="Only admin can update users.")
    message = chatbot_manager.update_user(username, password, role)
    return {"message": message}


@app.delete("/users/delete")
def delete_user(username: str = Body(...), user=Depends(authenticate)):
    # Delete user by username (admin only)
    if user["role"] != "hr":
        raise HTTPException(status_code=403, detail="Only admin can delete users.")
    message = chatbot_manager.delete_user(username)
    return {"message": message}
