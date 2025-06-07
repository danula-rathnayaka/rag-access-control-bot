# DS RPC 01: RAG Chatbot with Role Based Access Control

## Overview

A secure internal chatbot solution that enables role-based access to company data using
Retrieval-Augmented Generation (RAG) architecture. The system provides department-specific information access while
maintaining strict security protocols.

## Key Features

- **Role-Based Access Control**: Five distinct roles with granular permissions
- **Document Intelligence**: Automatic ingestion and processing of departmental documents
- **Conversational Memory**: Session-based chat history preservation
- **Admin Controls**: HR-managed user lifecycle management
- **Semantic Search**: Context-aware document retrieval using ChromaDB

## Supported Roles

| Role        | Access Scope                     |
|-------------|----------------------------------|
| Engineering | Technical docs, architecture     |
| Finance     | Financial reports, expenses      |
| Marketing   | Campaign data, customer insights |
| HR          | Employee records, policies       |
| General     | Company handbook, FAQs           |

## Tech Stack

**Core Components**

- Python 3.10+
- FastAPI (REST API framework)
- ChromaDB (Vector Database)
- Hugging Face (Embedding Models)
- Groq Cloud (LLM Inference)
- SQLite (User Database)

**Supporting Libraries**

- LangChain (Memory Management)
- SQLAlchemy (ORM)

## API Endpoints

| Endpoint            | Method  | Description                                      | Access                |
|---------------------|---------|--------------------------------------------------|-----------------------|
| `/`                 | GET     | Public test endpoint                             | Public                |
| `/login`            | GET     | User authentication                              | Public                |
| `/logout`           | GET     | Logout endpoint                                  | Authenticated         |
| `/test`             | GET     | Authenticated test endpoint                      | Authenticated         |
| `/save_folder_data` | GET     | Trigger data extraction and saving               | HR Admin              |
| `/chat`             | POST    | Main chat interface                              | Authenticated         |
| `/users/add`        | POST    | Add new user (admin only)                        | HR Admin              |
| `/users/update`     | PUT     | Update existing user details (admin only)        | HR Admin              |
| `/users/delete`     | DELETE  | Delete user by username (admin only)             | HR Admin              |

## Getting Started

### Prerequisites

- Python 3.10+
- Groq API key
- Git

### Installation

```
# Clone repository
git clone https://github.com/danula-rathnayaka/rag-access-control-bot.git
cd rag-access-control-bot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### Running the Service

```
uvicorn app.main:app --reload
```

## Document Processing Pipeline

1. **Ingestion**: Automatic detection of new documents in `/data` folder
2. **Chunking**:
    - Token size: 1024
    - Overlap: 256
3. **Embedding**:
    - Model: `BAAI/bge-base-en-v1.5`
4. **LLM**:
    - Model: `llama-3.1-8b-instant`
5. **Storage**: ChromaDB with role-based metadata indexing

![alt text](resources/RPC_01_Thumbnail.jpg)