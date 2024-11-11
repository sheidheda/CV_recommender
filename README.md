# Resume assistant API

This project is a FastAPI-based web application that processes a resume (PDF format) and a job description, then generates a tailored executive summary, relevant experience, and skill list using the LLaMA language model through the Groq API.

## Features

- **Upload Resume**: Accepts a PDF file as input.
- **Job Description Input**: Takes a job description as text input.
- **AI-Powered Summarization**: Uses LLaMA model to extract and summarize relevant information from the resume.
- **JSON Response**: Returns a structured JSON response with sections for summary, experience, and skills.

## Project Structure

- **main.py**: The primary FastAPI application file containing all API endpoint definitions.
- **requirements.txt**: Lists all necessary Python packages required to run the application.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the project root with the following keys:
   ```plaintext
   GROQ_API_KEY=your_groq_api_key
   LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key
   ```

## Usage

1. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **API Endpoint**:
   - **POST** `/generate_summary`: Takes a resume file and job description, then returns a JSON response with tailored summaries, relevant experiences, and skills.

3. **Example API Request**:
   Use a tool like [curl](https://curl.se/) or [Postman](https://www.postman.com/) to send a request:

   ```bash
   curl -X 'POST' \
     'http://127.0.0.1:8000/generate_summary' \
     -F 'resume=@path_to_resume.pdf' \
     -F 'job_description="Enter the job description here"'
   ```

   The API will respond with a JSON object containing a summary, relevant experience, and skills for the provided job description.

## Example Response

```json
{
  "summary": [
    "Executive summary tailored to job description 1",
    "Executive summary tailored to job description 2",
    "Executive summary tailored to job description 3"
  ],
  "experience": [
    "List of relevant experiences with key performance indicators and good structure"
  ],
  "skills": [
    "Top 10 relevant skills for the job"
  ]
}
```

## Dependencies

The main dependencies are listed below. For the full list, see `requirements.txt`:

- **FastAPI**: Web framework for building APIs with Python.
- **Groq API**: Connects to the Groq service for AI model responses.
- **LLaMA Parse**: Parses PDF content using LLaMA.
- **Nest Asyncio**: Allows the FastAPI application to handle nested async calls.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you’d like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Contact

For questions or collaboration, please reach out via:

- **Email**: faithfulmiracleajah@gmail.com
- **LinkedIn**: [LinkedIn Profile](https://www.linkedin.com)
- **GitHub**: [GitHub Profile](https://github.com)
