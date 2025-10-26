# 🚀 Juicebox AI - Quick Start Guide

Get your AI-powered recruiting platform running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 18+
- Exa API Key ([Get one here](https://dashboard.exa.ai/api-keys))

## Step 1: Clone the Repository

```bash
git clone https://github.com/Gbollysearch7/juicebox-ai.git
cd juicebox-ai
```

## Step 2: Start the Backend

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add: EXA_API_KEY=your_key_here

# Start the server
python run.py
```

The backend will start at **http://localhost:8000**

✅ Check it's running: http://localhost:8000/docs

## Step 3: Start the Frontend

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start at **http://localhost:5173**

## Step 4: Start Searching! 🎯

1. Open http://localhost:5173 in your browser
2. Enter a search query like:
   - "Senior ML Engineers at AI startups in San Francisco"
   - "VP of Engineering at Series B companies"
   - "Product Managers with fintech experience"

3. Watch as the AI:
   - Searches across the web
   - Verifies candidates against your criteria
   - Ranks them by relevance (0-100 score)
   - Enriches with LinkedIn profiles and details

4. Filter results by:
   - Minimum score
   - Verification status

## Example Search

Try this query:
```
Senior Software Engineers with React and Node.js experience at tech startups
```

The AI will:
1. Find 10 matching candidates
2. Verify they meet your criteria
3. Score each candidate (0-100)
4. Extract LinkedIn profiles and contact info
5. Display beautiful cards with all details

## What You'll See

### Search Interface
- Clean, chat-style search box
- Example queries to get started
- Real-time progress updates

### Candidate Cards
- Name and current role
- Company and location
- AI match score with color coding
- Verification status
- Skills and experience
- LinkedIn and email links

### Filters
- Minimum score slider
- Verified candidates only toggle

## Architecture

```
Frontend (React)  →  Backend (FastAPI)  →  Exa AI API
  localhost:5173       localhost:8000        External
```

## API Endpoints

Once running, explore the interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Key endpoints:
- `POST /api/v1/search` - Create search
- `GET /api/v1/search/{id}` - Get results
- `GET /api/v1/candidates` - List candidates

## Troubleshooting

### Backend won't start
- Make sure you added your Exa API key to `.env`
- Check Python version: `python --version` (need 3.8+)
- Try: `pip install --upgrade pip`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Try: `rm -rf node_modules && npm install`
- Check if port 5173 is already in use

### Can't connect to backend
- Make sure backend is running on port 8000
- Check backend logs for errors
- Visit http://localhost:8000/health

### No search results
- Verify your Exa API key is valid
- Check backend logs for API errors
- Try a broader search query

## Next Steps

### Customize Your Search
Edit the search criteria in [frontend/src/pages/SearchPage.tsx](frontend/src/pages/SearchPage.tsx:28):

```typescript
criteria: [
  'Your custom criteria here',
  'Another requirement',
],
enrichments: [
  'What data to extract',
  'Additional information',
],
```

### Add More Features
- Saved searches
- Export to CSV/PDF
- Email templates
- Team collaboration
- Advanced filters

### Deploy to Production
- Backend: Deploy to Heroku, AWS, or Render
- Frontend: Deploy to Vercel, Netlify, or Cloudflare Pages
- See deployment guides in docs/

## Support

- 📖 Full docs: [README.md](README.md)
- 🐛 Issues: https://github.com/Gbollysearch7/juicebox-ai/issues
- 💬 Questions: Open a GitHub discussion

## Success! 🎉

You now have a fully functional AI recruiting platform similar to Juicebox/PeopleGPT!

Happy recruiting! 🚀
