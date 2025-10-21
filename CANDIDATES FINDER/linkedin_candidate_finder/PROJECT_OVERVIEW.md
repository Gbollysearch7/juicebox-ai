# LinkedIn Candidate Finder - Project Overview

## What This Tool Does

This is a comprehensive Python tool for finding and enriching LinkedIn candidate profiles using **Exa's Websets API**. It automates the entire candidate sourcing process, from search to data enrichment, using AI-powered search technology.

## Key Capabilities

### 1. **Intelligent Candidate Search**
- Use natural language to describe who you're looking for
- Automatically searches and crawls the web to find matching candidates
- Verifies each candidate against your specific criteria

### 2. **Automatic Data Enrichment**
- Extracts LinkedIn profiles, emails, and contact information
- Gathers professional details (current role, company, experience)
- Identifies skills, certifications, and achievements

### 3. **Structured, Validated Results**
- Each candidate includes verification status with reasoning
- Structured data fields for easy processing
- References to source materials for transparency

### 4. **Batch Processing & Monitoring**
- Run multiple searches simultaneously
- Monitor progress in real-time
- Export results in multiple formats (JSON, CSV, Markdown)

## Project Structure

```
linkedin-candidate-finder/
│
├── linkedin_candidate_finder.py    # Main tool implementation
├── utilities.py                     # Advanced utilities (batch, export, filtering)
├── examples.py                      # Real-world recruiting examples
├── requirements.txt                 # Python dependencies
│
├── README.md                        # Complete documentation
├── QUICKSTART.md                   # Quick start guide
└── PROJECT_OVERVIEW.md             # This file
```

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────┐
│         LinkedInCandidateFinder                 │
│  (Main interface to Exa Websets API)            │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Search  │ │  Enrich  │ │  Export  │
│  Module  │ │  Module  │ │  Module  │
└──────────┘ └──────────┘ └──────────┘
        │           │           │
        └───────────┼───────────┘
                    ▼
          ┌─────────────────┐
          │  Exa Websets    │
          │      API        │
          └─────────────────┘
```

### Data Flow

```
1. USER INPUT
   ↓
   Define search criteria & enrichments
   ↓
2. CREATE WEBSET
   ↓
   POST /websets/v0/websets
   ↓
3. ASYNC SEARCH
   ↓
   Exa searches and crawls the web
   ↓
4. VERIFICATION
   ↓
   Each candidate verified against criteria
   ↓
5. ENRICHMENT
   ↓
   Additional data extracted for each candidate
   ↓
6. RESULTS
   ↓
   GET /websets/v0/websets/{id}/items
   ↓
7. PROCESS & EXPORT
   ↓
   Filter, deduplicate, export to JSON/CSV/MD
```

## Key Classes

### LinkedInCandidateFinder
Main interface for interacting with the API.

**Methods:**
- `create_candidate_search()` - Create a new search
- `wait_for_results()` - Wait for search completion
- `get_candidates()` - Retrieve results
- `search_and_wait()` - Convenience method (all-in-one)
- `get_webset_status()` - Check progress
- `list_websets()` - List your searches

### SearchCriteria
Defines what candidates you're looking for.

**Attributes:**
- `query` - Natural language description
- `count` - Number of candidates to find
- `entity` - Type (person, company, etc.)
- `criteria` - Specific requirements to verify

### EnrichmentConfig
Defines additional data to extract.

**Attributes:**
- `description` - What to extract
- `format` - "text" or "json"
- `schema` - Structure for JSON format

### Utility Classes
- `CandidateExporter` - Export to JSON/CSV/Markdown
- `BatchSearchManager` - Run multiple searches
- `ProgressMonitor` - Real-time progress tracking
- `CandidateFilter` - Filter and deduplicate results

## Understanding Exa Websets

### What is a Webset?

A **Webset** is an AI-powered container that:
1. Searches the web for entities matching your criteria
2. Verifies each result against your requirements
3. Enriches results with additional data
4. Returns structured, validated information

### Key Concepts

#### Webset (Container)
- Organizes your collection of web content
- Can contain multiple searches and enrichments
- Tracks overall status and progress

#### Search (Agent)
- Searches and crawls the web
- Finds entities matching your query and criteria
- Can take seconds to minutes depending on complexity

#### Item (Result)
- Structured result for each candidate found
- Includes source content, verification, and properties
- Contains type-specific fields (for people: name, title, company, etc.)

#### Enrichment (Agent)
- Enhances existing items with additional data
- Searches web to extract specific information
- Returns structured data based on your description

### API Workflow

```python
# 1. Create a Webset with search
webset = exa.websets.create(
    params=CreateWebsetParameters(
        search={
            "query": "ML Engineers at AI startups",
            "count": 20,
            "criteria": [...]
        },
        enrichments=[...]
    )
)

# 2. Wait for completion (async)
webset = exa.websets.wait_until_idle(webset.id)

# 3. Get results
items = exa.websets.items.list(webset_id=webset.id)
```

## Use Cases

### 1. Technical Recruiting
- Software Engineers (frontend, backend, full-stack)
- Data Scientists & ML Engineers
- DevOps & Infrastructure Engineers
- Engineering Leadership (VPs, Directors, Managers)

### 2. Sales & Marketing Hiring
- Account Executives
- Sales Development Representatives
- Marketing Managers
- Customer Success Managers

### 3. Academic Recruiting
- PhD Candidates
- Research Scientists
- Postdoctoral Researchers
- University Faculty

### 4. Executive Search
- C-level Executives (CTO, VP Engineering, etc.)
- Directors and VPs
- Industry-specific leadership

### 5. Specialized Industries
- Healthcare/HealthTech
- Fintech/Blockchain
- Climate Tech
- AI/ML Research

## API Features

### Async-First Design
- Searches run asynchronously in the background
- Can take seconds to minutes depending on complexity
- Use webhooks or polling to check status

### Structured Results
- Every result includes structured properties
- Verification status with reasoning and references
- Type-specific fields (person, company, etc.)

### Event-Driven
- Events published when items are found
- Webhooks notify when enrichments complete
- Process data as it arrives

### Scalable
- Find 1-1000+ candidates per search
- Large searches (1000+) can take ~1 hour
- Auto-stops if requested count not found

## Performance Characteristics

### Search Times
- Small searches (10-50): 1-5 minutes
- Medium searches (50-200): 5-20 minutes
- Large searches (200-1000): 20-60 minutes
- Very large searches (1000+): 60+ minutes

### Rate Limits
- Depends on your Exa plan
- Check dashboard for current limits
- Plan provides quota for searches and enrichments

### Best Practices
- Start with small counts (10-20) for testing
- Use specific criteria to improve quality
- Enable enrichments only for needed data
- Monitor progress for long-running searches

## Technology Stack

### Dependencies
- **exa_py** - Official Exa Python SDK
- **python-dotenv** - Environment variable management

### Requirements
- Python 3.8+
- Exa API key (free tier available)

### Compatible With
- Linux, macOS, Windows
- Command line or Python scripts
- Jupyter notebooks
- Web applications (via API integration)

## Getting Started

### Quick Start (3 steps)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
export EXA_API_KEY='your-key-here'

# 3. Run
python linkedin_candidate_finder.py
```

### Your First Search

```python
from linkedin_candidate_finder import *

finder = LinkedInCandidateFinder()

criteria = SearchCriteria(
    query="Software Engineers at tech companies",
    count=10
)

candidates = finder.search_and_wait(criteria)
```

## Example Outputs

### JSON Output
```json
{
  "id": "item_123",
  "url": "https://linkedin.com/in/johndoe",
  "title": "John Doe - Senior Engineer at TechCo",
  "status": "completed",
  "verification": {
    "passed": true,
    "criteria_results": [...]
  },
  "properties": {
    "name": "John Doe",
    "current_role": "Senior Engineer",
    "current_company": "TechCo"
  },
  "enrichments": [...]
}
```

### CSV Output
```csv
id,url,title,status,property_name,property_current_role
item_123,https://linkedin.com/in/johndoe,"John Doe - Senior Engineer",completed,John Doe,Senior Engineer
```

## Extending the Tool

### Custom Enrichments

```python
# Extract specific structured data
enrichment = EnrichmentConfig(
    description="Extract work history",
    format="json",
    schema={
        "type": "object",
        "properties": {
            "companies": {"type": "array"},
            "years_experience": {"type": "number"}
        }
    }
)
```

### Custom Filters

```python
from utilities import CandidateFilter

# Filter by any criteria
def filter_by_location(candidates, location):
    return [
        c for c in candidates
        if location.lower() in c.get('properties', {}).get('location', '').lower()
    ]
```

### Integration with Other Tools

```python
# Export to ATS
def export_to_ats(candidates):
    for candidate in candidates:
        ats_api.create_candidate({
            'name': candidate['properties']['name'],
            'linkedin': candidate['url'],
            'source': 'Exa Websets'
        })
```

## Best Practices

### Writing Queries
✅ Clear and specific
✅ Focus on current role/status
✅ Include location if relevant
✅ Mention key technologies/skills

### Defining Criteria
✅ 3-5 criteria for best results
✅ Mix of required and nice-to-have
✅ Specific and measurable
✅ Avoid redundancy with query

### Enrichments
✅ Request only needed data
✅ Use text format for flexibility
✅ Use JSON for structured data
✅ Be specific in descriptions

## Troubleshooting

### Common Issues

**No results found:**
- Query too narrow → broaden criteria
- Too many restrictions → remove some criteria
- Niche role → increase count

**Taking too long:**
- Large count → reduce for testing
- Complex criteria → simplify
- Monitor with `get_webset_status()`

**Low quality results:**
- Vague query → add more specifics
- Missing criteria → add requirements
- Use enrichments to filter post-search

## Resources

- **Exa Docs**: https://docs.exa.ai/websets
- **API Reference**: https://docs.exa.ai/websets/api
- **Get API Key**: https://dashboard.exa.ai/api-keys
- **Example Queries**: https://docs.exa.ai/websets/websets-example-queries
- **Support**: [email protected]

## Future Enhancements

Potential additions:
- [ ] Web UI dashboard
- [ ] Integration with ATS platforms
- [ ] Email automation for outreach
- [ ] Advanced filtering and scoring
- [ ] Candidate matching algorithms
- [ ] Scheduled/recurring searches
- [ ] Team collaboration features

## Contributing

Contributions welcome! Areas of interest:
- Additional example use cases
- Integration with recruiting tools
- Performance optimizations
- Documentation improvements

## License

MIT License - free to use and modify for your needs.

---

Built with [Exa AI](https://exa.ai) - The search engine for AI applications.
