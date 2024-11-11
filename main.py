import nest_asyncio
import asyncio
import logging
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel
from llama_parse import LlamaParse
import os
from dotenv import load_dotenv
from groq import Groq
import json

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Set up Groq client and LLaMA model
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = "llama-3.2-3b-preview"  # Specify the LLaMA model you are using

# Model input class for JSON response
class JobDescription(BaseModel):
    description: str

# Endpoint to handle the resume PDF and job description
@app.post("/generate_summary")
async def generate_summary(resume: UploadFile = File(...), job_description: str = Form(...)):

    # Step 1: Extract the resume file bytes
    try:
        resume_bytes = await resume.read()  # Get the bytes of the uploaded file
        logging.info("Resume file received, starting PDF parsing.")
        
        # Initialize the LlamaParse parser
        parser = LlamaParse(
            api_key=os.getenv("LLAMA_CLOUD_API_KEY"),  # Fetch API key from environment variables
            result_type="markdown",  # Use markdown format for the extracted content
            num_workers=4,  # Number of workers for API calls
            verbose=True,
            language="en",  # Language for the resume
        )
        
        # Use LlamaParse to process the uploaded PDF file
        extra_info = {"file_name": resume.filename}
        documents = parser.load_data(resume_bytes, extra_info=extra_info)

        # If no documents were extracted, raise an error
        if not documents:
            logging.error("Failed to extract text from the PDF.")
            raise HTTPException(status_code=400, detail="No text found in the PDF")
        
        logging.info(f"Text successfully extracted from the resume. Parsing {len(documents)} document(s).")

        # Step 2: Extract the markdown content from the documents
        resume_markdown = "\n".join([doc.text for doc in documents])

    except Exception as e:
        logging.error(f"Error during PDF extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

    # Step 3: Prepare the prompt for the LLaMA model to generate a summary
    prompt = f"""
    Given the resume content in markdown format: 
    ```{resume_markdown}``` 
    and the job description: "{job_description}", 
    provide the following in a JSON format:
    
    {{
        "summary": ["3 different executive summaries tailored to fit the job description"],
        "experience": ["outline relevant experiences tailored to the job description with kpis and good structure"],
        "skills": ["List the 10 most relevant skills for the job"]
    }}
    Make sure the summaries are concise and relevant to the job description.
    """
    
    # Log the prompt being sent to the model
    logging.info(f"Sending prompt to Groq API: {prompt[:100]}...")  # Logging the first 100 characters of the prompt

    # Step 4: Generate response using the LLaMA model via Groq client
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.5,
            max_tokens=3024,
            stop=None
        )
        
        logging.info("Response received from Groq API.")


        # Extract the content from the response
        message_content = response.choices[0].message.content.strip()

        # Extract the JSON part wrapped inside the markdown code block
        json_str = message_content.split('```json')[1].split('```')[0].strip()

        # Convert the JSON string to a Python dictionary
        parsed_json = json.loads(json_str)
        
        # Directly return Groq's raw response structure
        return json.dumps(parsed_json, indent=4) # This will include the full response from the Groq API

    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
