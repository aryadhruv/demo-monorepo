#Dhruv's old script
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI, api_key
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

app = FastAPI()

# Configure CORS: adjust allowed origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your actual frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("OPENAI_API_KEY not set in environment variables.")

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    messages = data.get("messages")
    if not messages:
        raise HTTPException(status_code=400, detail="Missing 'messages' in payload.")

    try:
        # Call OpenAI's ChatCompletion API
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=False  # For a basic implementation; can be changed to stream responses
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    # Extract the reply from the API response
    reply = completion.choices[0].message.content
    return reply

if __name__ == "__main__":
    # Run the app with uvicorn for development; for production, use a production ASGI server
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
