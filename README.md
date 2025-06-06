# Curriculum Generator Web Service

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
3. Run the Flask development server:
   ```bash
   python app.py
   ```
4. Test the `/generate` endpoint with `curl`:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"topic": "Python programming"}' http://localhost:5000/generate
   ```
