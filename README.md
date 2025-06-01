# Python FastAPI Survey Analysis API

## Story
Our school requested the development of a survey program: "We want you to develop a survey program for our school so that teachers and administrators can create surveys whenever they want. Only people in the specified category can participate in these surveys. Additionally, we want to view the survey results and download a survey as a PDF whenever we want." To fulfill this request, I developed an API using Python FastAPI that visualizes the survey data.

## Purpose
The primary purpose of this project is to count and visualize the answers to survey questions. The API processes survey data, creates visualizations, converts them to base64 format, and sends them back to the website for display.

## Features
- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **Data Validation**: Pydantic models for robust data validation
- **Interactive Documentation**: Automatic Swagger UI at `/docs`
- **Visualization**: Beautiful charts using matplotlib and seaborn
- **Base64 Encoding**: Charts converted to base64 for easy web integration
- **CORS Support**: Cross-origin requests enabled
- **Error Handling**: Comprehensive error handling and logging

## Installation

```bash
pip install -r requirements.txt
```

**If uvicorn doesn't work on linux try this:**
```bash
sudo apt install uvicorn
```

## Run Server

```bash
# Method 1: Direct run
python survey-counter.py

# Method 2: Using uvicorn
uvicorn survey-counter:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation
Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## CURL Request Example

```curl
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "questions": [
      {
        "question": "What is your favorite programming language?",
        "answers": ["Python", "JavaScript", "Java", "C++", "Go"],
        "response": ["Python", "Python", "JavaScript", "Python", "Java", "JavaScript", "Python", "Go", "Python"]
      },
      {
        "question": "How many years of experience do you have?",
        "answers": ["0-1 years", "2-5 years", "6-10 years", "10+ years"],
        "response": ["2-5 years", "6-10 years", "2-5 years", "10+ years", "2-5 years", "0-1 years", "6-10 years", "2-5 years"]
      }
    ]
  }'
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/`      | API information and available endpoints |
| GET    | `/health` | Health check endpoint |
| POST   | `/analyze` | Analyze survey data and generate visualizations |

## JSON Structure

### Request Sample
```json
{
  "questions": [
    {
      "question": "How do you rate our school?",
      "answers": ["Excellent", "Good", "Average", "Poor"],
      "response": ["Good", "Excellent", "Good", "Average", "Poor", "Good"]
    },
    {
      "question": "Would you recommend our school to others?",
      "answers": ["Yes", "No"],
      "response": ["Yes", "Yes", "No", "Yes"]
    }
  ]
}
```

### Response Sample
```json
{
  "plots": [
    "iVBORw0KGgoAAAANSUhEUgAA...",
    "iVBORw0KGgoAAAANSUhEUgBB..."
  ],
  "success": true,
  "message": "2 plots created successfully"
}
```

## Technologies Used
- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Matplotlib**: Plotting library for creating static visualizations
- **Seaborn**: Statistical data visualization based on matplotlib
- **Uvicorn**: ASGI server implementation for running the application

## Error Handling
The API includes comprehensive error handling:
- Invalid JSON structure
- Missing required fields
- Empty response data
- Plotting errors
- Server errors

All errors return appropriate HTTP status codes and descriptive error messages.