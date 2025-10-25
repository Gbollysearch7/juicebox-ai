# Juicebox AI - Backend API

FastAPI backend for the Juicebox AI recruiting platform. Provides RESTful API endpoints for AI-powered candidate search and ranking.

## Features

- 🚀 **Fast & Async**: Built with FastAPI for high performance
- 🔍 **AI-Powered Search**: Natural language candidate search using Exa API
- ✅ **Smart Verification**: Automatic candidate verification against criteria
- 📊 **AI Ranking**: Candidates scored and ranked by relevance
- 🔄 **Real-time Updates**: WebSocket support for live search progress
- 📝 **Auto Documentation**: Interactive API docs at `/docs`
- 🔒 **Type Safe**: Full Pydantic validation

## Quick Start

### 1. Installation

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Exa API key
# EXA_API_KEY=your_key_here
```

### 3. Run the Server

```bash
python run.py
```

The API will start at `http://localhost:8000`

- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## API Endpoints

### Search Endpoints

#### Create Search
```http
POST /api/v1/search
```

**Request Body:**
```json
{
  "query": "Senior ML Engineers at AI startups in San Francisco",
  "count": 10,
  "entity": "person",
  "criteria": [
    "Has 5+ years of machine learning experience",
    "Currently employed at a tech startup",
    "Based in San Francisco Bay Area"
  ],
  "enrichments": [
    "Find their LinkedIn profile",
    "Extract current role and company"
  ]
}
```

**Response:**
```json
{
  "search_id": "abc-123-def",
  "status": "pending",
  "query": "Senior ML Engineers...",
  "count": 10,
  "created_at": "2024-10-22T12:00:00",
  "message": "Search created successfully"
}
```

#### Get Search Status
```http
GET /api/v1/search/{search_id}
```

**Response:**
```json
{
  "search_id": "abc-123-def",
  "status": "completed",
  "query": "Senior ML Engineers...",
  "total_requested": 10,
  "total_found": 8,
  "progress_percent": 80.0,
  "candidates": [...]
}
```

#### List All Searches
```http
GET /api/v1/search
```

### Candidate Endpoints

#### Get All Candidates
```http
GET /api/v1/candidates?min_score=70&verified_only=true
```

**Query Parameters:**
- `search_id` (optional): Filter by search
- `min_score` (optional): Minimum score (0-100)
- `verified_only` (optional): Only verified candidates

**Response:**
```json
{
  "total": 5,
  "candidates": [
    {
      "id": "cand-123",
      "url": "https://linkedin.com/in/johndoe",
      "title": "John Doe - Senior ML Engineer",
      "status": "completed",
      "score": 95.5,
      "verification": {
        "passed": true,
        "criteria_results": [...]
      },
      "properties": {
        "name": "John Doe",
        "current_role": "Senior ML Engineer",
        "current_company": "AI Startup Inc",
        "location": "San Francisco, CA"
      },
      "enrichments": [...]
    }
  ]
}
```

#### Get Candidate by ID
```http
GET /api/v1/candidates/{candidate_id}
```

## Example Usage

### Python (requests)

```python
import requests

# Create search
response = requests.post("http://localhost:8000/api/v1/search", json={
    "query": "Senior Software Engineers with React experience",
    "count": 10,
    "criteria": ["Has 3+ years React experience"],
    "enrichments": ["Find LinkedIn profile"]
})

search_id = response.json()["search_id"]

# Check status
status = requests.get(f"http://localhost:8000/api/v1/search/{search_id}")
print(status.json())

# Get candidates
candidates = requests.get("http://localhost:8000/api/v1/candidates", params={
    "search_id": search_id,
    "min_score": 70
})
print(candidates.json())
```

### JavaScript (fetch)

```javascript
// Create search
const response = await fetch('http://localhost:8000/api/v1/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "Senior Software Engineers with React experience",
    count: 10,
    criteria: ["Has 3+ years React experience"],
    enrichments: ["Find LinkedIn profile"]
  })
});

const { search_id } = await response.json();

// Check status
const status = await fetch(`http://localhost:8000/api/v1/search/${search_id}`);
const searchData = await status.json();

// Get candidates
const candidates = await fetch(
  `http://localhost:8000/api/v1/candidates?search_id=${search_id}&min_score=70`
);
const candidatesData = await candidates.json();
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── search.py          # Search endpoints
│   │       └── candidates.py      # Candidate endpoints
│   ├── core/
│   │   ├── config.py              # Configuration
│   │   ├── finder.py              # LinkedIn candidate finder
│   │   └── utilities.py           # Helper utilities
│   ├── models/
│   │   └── schemas.py             # Pydantic models
│   ├── services/
│   │   └── search_service.py      # Search business logic
│   └── main.py                    # FastAPI app
├── requirements.txt
├── run.py                         # Run script
└── .env.example                   # Environment variables example
```

## Configuration

Environment variables (`.env` file):

```bash
# Required
EXA_API_KEY=your_api_key_here

# Optional - Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Optional - Search Settings
DEFAULT_CANDIDATE_COUNT=10
MAX_CANDIDATE_COUNT=100

# Optional - Cache
REDIS_URL=redis://localhost:6379
```

## Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run with Auto-Reload

```bash
python run.py
```

The server will auto-reload on code changes when `DEBUG=True`.

### Run Tests

```bash
pytest
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Interactive documentation allows you to:
- View all endpoints
- Test API calls directly
- See request/response schemas
- Download OpenAPI spec

## Troubleshooting

### Port Already in Use

```bash
# Change port in .env
PORT=8001
```

### Exa API Key Issues

Make sure your `.env` file contains:
```bash
EXA_API_KEY=your_actual_key_here
```

Get your key at: https://dashboard.exa.ai/api-keys

### CORS Issues

Add your frontend URL to `BACKEND_CORS_ORIGINS` in [config.py](app/core/config.py:24)

## Next Steps

- [ ] Add WebSocket endpoint for real-time search updates
- [ ] Implement caching with Redis
- [ ] Add user authentication
- [ ] Add rate limiting
- [ ] Deploy to production

## Support

For issues or questions, please open an issue on GitHub.
