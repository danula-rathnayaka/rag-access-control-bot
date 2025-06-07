from datetime import datetime
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


async def generate_response(
        user_query,
        retrieved_contexts,
        memory,
        model="llama-3.1-8b-instant"):
    llm = ChatGroq(
        model=model,
        temperature=0.2,
        max_tokens=1024
    )

    # Create message chain
    messages = [
        ("system",
         """You are a financial assistant for FinSolve Technologies. 
         - Answer strictly based on provided context
         - Cite sources using [1][2] notation
         - If unsure, say "I don't have enough information"
         - Maintain professional tone
         - Current date: {date}""".format(date=datetime.now().strftime("%Y-%m-%d"))),
        *memory.load_memory_variables({})["chat_history"],
        ("human", f"""
        Context:
        {"\n".join(retrieved_contexts)}
        
        Question:
        {user_query}
        """)
    ]

    # Get and store response
    response = await llm.ainvoke(messages)
    memory.save_context(
        {"input": user_query},
        {"output": response.content}
    )

    return response.content
