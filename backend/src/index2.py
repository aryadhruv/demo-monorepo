#Example 2 : 
import asyncio
import json
import os
from typing import AsyncGenerator, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain.schema import BaseMemory
from langchain.schema.runnable import RunnableConfig
from pydantic import BaseModel
from langchain.tools import BaseTool
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI, OpenAI
from langchain.memory import ConversationSummaryBufferMemory

from .utils.prompt import ClientMessage

# -----------------------------------------------------------------------------
# FastAPI Application Initialization
# -----------------------------------------------------------------------------
app = FastAPI(debug=True)

@app.get("/hi")
async def read_root():
    return {"message": "Hello from FastAPI root!"}


# -----------------------------------------------------------------------------
# Request Model
# -----------------------------------------------------------------------------
class Request(BaseModel):
    messages: List[ClientMessage]


# -----------------------------------------------------------------------------
# Utility Functions and Models
# -----------------------------------------------------------------------------
async def get_prompt() -> ChatPromptTemplate:
    """
    Create and return a chat prompt template.
    This prompt includes a system message and placeholders for history and scratchpad.
    """
    messages = [
        SystemMessagePromptTemplate.from_template("You're an helpful agent"),
        MessagesPlaceholder("history"),
        ("user", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
    return ChatPromptTemplate.from_messages(messages)


def add_numbers(i: int, j: int) -> int:
    """
    A simple function that adds two numbers.
    """
    return i + j


async def get_tools() -> List[BaseTool]:
    """
    Return a list of tools available to the agent.
    Here we wrap the add_numbers function as a structured tool.
    """
    return [
        StructuredTool.from_function(
            function=add_numbers,
            name="add_numbers",
            description="Add two numbers",
        ),
    ]


def get_chat_model() -> ChatOpenAI:
    """
    Initialize and return the chat model configured for streaming responses.
    """
    return ChatOpenAI(
        streaming=True,
        temperature=0,
        model="gpt-4o-2024-05-13",
        verbose=True,
    )


async def get_chain(memory: BaseMemory) -> AgentExecutor:
    """
    Create an agent executor using a LangChain agent.
    It composes the prompt, tools, and memory to process user input.
    """
    prompt = await get_prompt()
    tools = await get_tools()
    agent = create_openai_tools_agent(get_chat_model(), tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )


def get_summarize_model() -> OpenAI:
    """
    Initialize and return the summarization model.
    """
    return OpenAI(
        temperature=0,
        model="gpt-3.5-turbo-instruct",
    )


def get_memory() -> ConversationSummaryBufferMemory:
    """
    Initialize conversation memory which summarizes the conversation once a token limit is reached.
    """
    return ConversationSummaryBufferMemory(
        llm=get_summarize_model(),
        output_key="output",
        return_messages=True,
        max_token_limit=2000,
        input_key="input",
    )


# -----------------------------------------------------------------------------
# Global Memory Initialization
# -----------------------------------------------------------------------------
memory = get_memory()


# -----------------------------------------------------------------------------
# FastAPI Endpoint for Chat Streaming
# -----------------------------------------------------------------------------
@app.post("/api/chat")
async def handle_chat_data(request: Request, protocol: str = Query("data")):
    """
    Endpoint to handle chat requests.
    It processes the last user message, runs the agent executor,
    and streams the response tokens back to the client.
    """
    messages = request.messages
    if not messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    input_text = messages[-1].content
    stream_input = {"input": input_text}

    runnable = await get_chain(memory)
    token_callback = AsyncIteratorCallbackHandler()

    stream_task = asyncio.create_task(
        runnable.ainvoke(
            input=stream_input,
            config=RunnableConfig(callbacks=[token_callback]),
        )
    )

    async def token_stream_generator() -> AsyncGenerator[str, None]:
        # Stream each token received from the callback handler.
        async for token in token_callback.aiter():
            yield f"0:{json.dumps(token)}\n"
        await stream_task
        # Yield a final message indicating the end of the stream.
        finish_payload = {
            "finishReason": "stop",
            "usage": {"promptTokens": 0, "completionTokens": 0},
            "isContinued": False,
        }
        yield f"e:{json.dumps(finish_payload)}\n"

    response = StreamingResponse(token_stream_generator(), media_type="text/event-stream")
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


# -----------------------------------------------------------------------------
# Main: Run the Application with Uvicorn
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
