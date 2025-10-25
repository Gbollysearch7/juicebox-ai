# 🧃 Juicebox AI

An AI-powered recruiting platform inspired by Juicebox/PeopleGPT. Find, verify, and rank top talent using natural language search across 800M+ profiles.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18+-61dafb.svg)

## ✨ Features

- 🤖 **AI-Powered Search**: Natural language candidate search using Exa API
- ✅ **Smart Verification**: Automatic verification against custom criteria
- 📊 **AI Ranking**: Candidates scored and ranked by relevance (0-100)
- 🎯 **Multi-Source Enrichment**: LinkedIn, GitHub, skills extraction
- 💬 **Chat Interface**: PeopleGPT-style conversational search (coming soon)
- 📈 **Real-time Updates**: Live search progress and results
- 📤 **Export**: JSON, CSV, Markdown formats
- 🔒 **Type Safe**: Full TypeScript/Pydantic validation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Juicebox AI Platform                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │   Frontend   │ ◄─────► │   Backend    │                  │
│  │              │  HTTP   │              │                  │
│  │ React + Vite │  REST   │   FastAPI    │ ◄────┐          │
│  │  (Port 3000) │  WebSocket (Port 8000) │      │          │
│  └──────────────┘         └──────────────┘      │          │
│                                   │              │          │
│                                   ▼              ▼          │
│                          ┌─────────────────────────┐        │
│                          │   Core Search Engine    │        │
│                          │   (Exa API Wrapper)     │        │
│                          └─────────────────────────┘        │
│                                   │                          │
│                                   ▼                          │
│                          ┌─────────────────────┐            │
│                          │      Exa API        │            │
│                          │   (External AI)     │            │
│                          └─────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
juicebox-ai/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── routes/
│   │   │       ├── search.py          # Search endpoints
│   │   │       └── candidates.py      # Candidate endpoints
│   │   ├── core/              # Core functionality
│   │   │   ├── config.py              # Configuration
│   │   │   ├── finder.py              # Candidate search engine
│   │   │   └── utilities.py           # Helpers
│   │   ├── models/            # Data models
│   │   │   └── schemas.py             # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   └── search_service.py      # Search orchestration
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
│
├── frontend/                   # React Frontend (coming soon)
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   └── services/         # API client
│   └── package.json
│
├── CANDIDATES FINDER/          # Original CLI tool
│   └── linkedin_candidate_finder/
│       ├── linkedin_candidate_finder.py
│       ├── utilities.py
│       ├── examples.py
│       └── README.md
│
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+ (for frontend)
- Exa API key ([Get one here](https://dashboard.exa.ai/api-keys))

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your EXA_API_KEY

# 4. Run the server
python run.py
```

The API will start at **http://localhost:8000**

- 📚 API Docs: http://localhost:8000/docs
- 🔄 Alternative Docs: http://localhost:8000/redoc

### Frontend Setup (Coming Soon)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📖 Usage Examples

### Using the API

#### 1. Create a Search

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Senior ML Engineers at AI startups in San Francisco",
    "count": 10,
    "criteria": [
      "Has 5+ years of machine learning experience",
      "Currently employed at a tech startup",
      "Based in San Francisco Bay Area"
    ],
    "enrichments": [
      "Find their LinkedIn profile",
      "Extract current role and company"
    ]
  }'
```

#### 2. Check Search Status

```bash
curl "http://localhost:8000/api/v1/search/{search_id}"
```

#### 3. Get Candidates

```bash
curl "http://localhost:8000/api/v1/candidates?min_score=70&verified_only=true"
```

### Using the Python Client

```python
from app.core.finder import LinkedInCandidateFinder, SearchCriteria, EnrichmentConfig

# Initialize
finder = LinkedInCandidateFinder(api_key="your_exa_api_key")

# Define search
criteria = SearchCriteria(
    query="Senior Software Engineers with React experience",
    count=10,
    criteria=["Has 3+ years React development experience"]
)

enrichments = [
    EnrichmentConfig("Find their LinkedIn profile"),
    EnrichmentConfig("Extract skills and experience")
]

# Run search
candidates = finder.search_and_wait(criteria, enrichments)

# Process results
for candidate in candidates:
    print(f"{candidate['properties']['name']} - Score: {candidate.get('score')}")
```

## 🎯 Use Cases

### Tech Recruiting
- Software Engineers (Frontend, Backend, Full-Stack)
- ML/AI Engineers and Data Scientists
- DevOps and Platform Engineers
- Engineering Leaders (VP, Director, CTO)

### Sales & Marketing
- Account Executives
- Sales Development Representatives
- Growth Marketing Managers
- Marketing Leaders

### Academic & Research
- PhD Candidates
- Research Scientists
- Postdoctoral Researchers
- Faculty Hiring

### Executive Search
- C-Level Executives
- VP and Director Roles
- Industry-Specific Leadership

## 🔧 API Reference

### Search Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/search` | Create a new candidate search |
| `GET` | `/api/v1/search/{id}` | Get search status and results |
| `GET` | `/api/v1/search` | List all searches |

### Candidate Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/candidates` | Get all candidates with filters |
| `GET` | `/api/v1/candidates/{id}` | Get specific candidate details |

See full API documentation at: **http://localhost:8000/docs**

## 🧪 Testing

### Test the Backend API

```bash
cd backend
python test_api.py
```

This will:
- Check health endpoint
- List existing searches
- Optionally create a test search
- Retrieve and display results

### Manual Testing

Visit the interactive API docs:
- http://localhost:8000/docs

You can test all endpoints directly from the browser.

## 📊 Features Comparison

| Feature | Juicebox AI | Juicebox/PeopleGPT |
|---------|-------------|---------------------|
| AI-Powered Search | ✅ | ✅ |
| Natural Language Queries | ✅ | ✅ |
| Candidate Verification | ✅ | ✅ |
| AI Ranking/Scoring | ✅ | ✅ |
| Multi-Source Data | 🚧 In Progress | ✅ |
| Chat Interface | 🚧 Coming Soon | ✅ |
| Team Collaboration | 📅 Planned | ✅ |
| Email Automation | 📅 Planned | ✅ |
| 800M+ Profile Access | ✅ (via Exa) | ✅ |

## 🛣️ Roadmap

### Phase 1: Core Platform (Current)
- [x] Backend API with FastAPI
- [x] AI-powered candidate search
- [x] Verification and ranking
- [x] RESTful API endpoints
- [ ] WebSocket for real-time updates

### Phase 2: Frontend (Next)
- [ ] React frontend with Vite
- [ ] Chat-style interface (PeopleGPT-like)
- [ ] Beautiful candidate cards
- [ ] Real-time search results
- [ ] Filters and saved searches

### Phase 3: Enhanced Features
- [ ] Multi-source data aggregation (LinkedIn, GitHub, Twitter)
- [ ] Advanced AI ranking algorithms
- [ ] Candidate similarity matching
- [ ] Export to ATS platforms

### Phase 4: Automation
- [ ] Email templates and sequences
- [ ] LinkedIn automation
- [ ] Scheduling and follow-ups
- [ ] Analytics dashboard

### Phase 5: Collaboration
- [ ] User authentication
- [ ] Team workspaces
- [ ] Shared candidate pools
- [ ] Comments and notes

## 🔐 Environment Variables

Create a `.env` file in the backend directory:

```bash
# Required
EXA_API_KEY=your_exa_api_key_here

# Optional - Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Optional - Search
DEFAULT_CANDIDATE_COUNT=10
MAX_CANDIDATE_COUNT=100
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Inspired by [Juicebox/PeopleGPT](https://juicebox.ai)
- Powered by [Exa AI](https://exa.ai)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend with [React](https://react.dev)

## 📧 Support

For questions or issues, please open an issue on GitHub.

---

**Made with ❤️ by the Juicebox AI Team**
