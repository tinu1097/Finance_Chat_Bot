from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import re
import time  # Import time for tracking
from tqdm import tqdm  # Import tqdm for progress visualization

from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify a list of origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define the request model for the API
class QuestionRequest(BaseModel):
    question: str

# Define the response model for the API
class ResponseModel(BaseModel):
    response: str

# Define the endpoint
@app.post("/ask-finance-question", response_model=ResponseModel)
async def ask_finance_question(request: QuestionRequest):
    # Prepare the JSON payload as per your structure
    payload = {
        "model": "llama3_8b_client_finance",
        "messages": [
            {"role": "system", "content": "You are a financial expert bot specializing in answering finance-related queries."},
            {"role": "user", "content": request.question},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "financial_response",
                "strict": "true",
                "schema": {
                    "type": "object",
                    "properties": {
                        "response": {"type": "string"}
                    },
                    "required": ["response"]
                }
            }
        },
        "temperature": 0.6,
        "max_tokens": 150,
        "stream": False
    }

    # Define the external API endpoint
    external_api_url = "http://127.0.0.1:1234/v1/chat/completions"

    try:
        # Start the timer
        start_time = time.time()

        # Simulate processing time with tqdm
        for _ in tqdm(range(1), desc="Processing Request"):
            # Make the request to the external API
            response = requests.post(
                external_api_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

        # Stop the timer
        elapsed_time = time.time() - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")

        # Raise an exception if the response is not successful
        response.raise_for_status()

        # Parse the response
        response_data = response.json()

        # Extract the content from the assistant's message
        assistant_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
        match = re.search(r'"response": "(.*)', assistant_content)
        if match:
            assistant_content = match.group(1).strip()
        return {"response": assistant_content}

    except requests.exceptions.RequestException as e:
        # Handle any errors from the external API
        raise HTTPException(status_code=500, detail=f"Error communicating with the external API: {e}")