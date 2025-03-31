# CV Parser

A FastAPI service that parses resumes and CVs from various document formats.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up the Gemini API key:
```bash
export GEMINI_API_KEY=your_api_key_here
```

3. Run the API server:
```bash
python api.py
```

The server will start on http://localhost:8000

## API Usage

### Upload a Document

**Endpoint:** `POST /upload/`

**Supported formats:** PDF, DOCX, JPG, JPEG, PNG

**Example using curl:**
```bash
curl -X 'POST' \
  'http://localhost:8000/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/resume.pdf'
```

## Command Line Usage

You can also use the parser directly from the command line:

```bash
python main.py /path/to/your/resume.pdf
```
