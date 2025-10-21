# LinkedIn Candidate Finder - Exa Websets API

A powerful Python tool for finding and enriching LinkedIn candidate profiles using Exa's Websets API. This tool leverages AI-powered search to find candidates matching specific criteria and automatically enriches their profiles with additional information.

## 🌟 Features

- **Intelligent Candidate Search**: Use natural language queries to find candidates
- **Automatic Verification**: Each candidate is verified against your specific criteria
- **Data Enrichment**: Automatically extract additional information (LinkedIn profiles, emails, skills, experience)
- **Async Processing**: Handles large searches efficiently with async API
- **Progress Tracking**: Monitor search progress in real-time
- **Structured Results**: Get structured data with verification and reasoning
- **Export Capabilities**: Save results in JSON format for further processing

## 📋 Prerequisites

- Python 3.8 or higher
- An Exa API key (get yours at [dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys))

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the repository
git clone <your-repo-url>
cd linkedin-candidate-finder

# Install dependencies
pip install exa_py

# Set your API key
export EXA_API_KEY='your-api-key-here'
```

### 2. Basic Usage

```python
from linkedin_candidate_finder import LinkedInCandidateFinder, SearchCriteria, EnrichmentConfig

# Initialize the finder
finder = LinkedInCandidateFinder()

# Define your search criteria
criteria = SearchCriteria(
    query="Senior Software Engineers at tech startups in San Francisco",
    count=20,
    criteria=[
        "Has 5+ years of software engineering experience",
        "Currently working at a startup",
        "Based in San Francisco Bay Area",
        "Has experience with Python and distributed systems"
    ]
)

# Define what additional information to extract
enrichments = [
    EnrichmentConfig("Find their LinkedIn profile URL"),
    EnrichmentConfig("Extract current company and role"),
    EnrichmentConfig("Find their email if publicly available"),
    EnrichmentConfig("List their top 3 technical skills")
]

# Run the search and get results
candidates = finder.search_and_wait(
    search_criteria=criteria,
    enrichments=enrichments,
    external_id="senior-engineers-sf-2024"
)

# Process results
for candidate in candidates:
    print(f"Found: {candidate['url']}")
    print(f"Status: {candidate['status']}")
    print(f"Properties: {candidate['properties']}")
```

### 3. Run Example Searches

```bash
python linkedin_candidate_finder.py
```

This will present you with several example searches:
1. ML Engineers at AI startups
2. Sales Leaders in SaaS
3. PhD Candidates in NLP
4. Custom search

## 🔍 Understanding Exa Websets

### What is a Webset?

A **Webset** is a container that organizes your collection of web content. Think of it as a smart search project that:
- Searches the web for entities matching your criteria
- Verifies each result against your requirements
- Enriches results with additional data
- Provides structured, validated results

### Key Concepts

#### 1. **Search** (WebsetSearch)
An agent that searches and crawls the web to find entities matching your criteria. For example:
```python
search = {
    "query": "CTOs at B2B SaaS companies in NYC",
    "count": 50,
    "entity": {"type": "person"},
    "criteria": [
        {"description": "Currently holds CTO or VP Engineering title"},
        {"description": "Works at a B2B SaaS company"},
        {"description": "Based in New York City"}
    ]
}
```

#### 2. **Items** (WebsetItem)
Structured results with:
- Source content (webpage text)
- Verification status (pass/fail for each criterion)
- Type-specific fields (for people: name, title, company, etc.)
- Reasoning and references explaining the match

#### 3. **Enrichments**
Agents that enhance existing items with additional data:
```python
enrichment = {
    "description": "Find their LinkedIn profile URL and extract current role",
    "format": "text"
}
```

### How It Works

```
1. CREATE WEBSET
   ↓
2. SEARCH AGENT FINDS CANDIDATES
   ↓
3. VERIFICATION AGAINST CRITERIA
   ↓
4. ENRICHMENT EXTRACTION
   ↓
5. STRUCTURED RESULTS RETURNED
```

## 📚 API Reference

### LinkedInCandidateFinder

Main class for interacting with the Exa Websets API.

#### `__init__(api_key: Optional[str] = None)`
Initialize the finder with your API key.

```python
finder = LinkedInCandidateFinder(api_key="your-key")
# or use environment variable
finder = LinkedInCandidateFinder()  # reads from EXA_API_KEY
```

#### `create_candidate_search(...)`
Create a new search for candidates.

**Parameters:**
- `search_criteria` (SearchCriteria): Defines what candidates you're looking for
- `enrichments` (List[EnrichmentConfig], optional): Additional data to extract
- `external_id` (str, optional): Your own identifier for this search
- `metadata` (Dict, optional): Additional metadata

**Returns:** Dictionary with webset ID and status

#### `wait_for_results(webset_id: str, timeout: int = 3600)`
Wait for a webset to complete processing.

**Parameters:**
- `webset_id`: The ID of the webset
- `timeout`: Maximum wait time in seconds (default: 1 hour)

#### `get_candidates(webset_id: str, limit: Optional[int] = None)`
Retrieve candidate results from a completed webset.

**Returns:** List of candidate dictionaries with all extracted information

#### `search_and_wait(...)`
Convenience method that combines create, wait, and get.

```python
# Simple one-liner to get results
candidates = finder.search_and_wait(criteria, enrichments)
```

### SearchCriteria

Defines what candidates you're looking for.

**Attributes:**
- `query` (str): Natural language description of candidates
- `count` (int): Number of candidates to find (default: 10)
- `entity` (EntityType): Type of entity (PERSON, COMPANY, etc.)
- `criteria` (List[str], optional): Specific requirements to verify
- `exclude_criteria` (List[str], optional): Requirements to exclude

**Example:**
```python
criteria = SearchCriteria(
    query="Product Managers at fintech startups",
    count=30,
    entity=EntityType.PERSON,
    criteria=[
        "Has 3+ years of product management experience",
        "Currently works at a fintech company",
        "Has experience with payments or banking products"
    ]
)
```

### EnrichmentConfig

Defines additional data to extract for each candidate.

**Attributes:**
- `description` (str): What information to find
- `format` (str): "text" or "json" (default: "text")
- `schema` (Dict, optional): For JSON format, defines the structure

**Examples:**
```python
# Simple text enrichment
enrichment = EnrichmentConfig(
    description="Find their LinkedIn profile URL"
)

# Structured JSON enrichment
enrichment = EnrichmentConfig(
    description="Extract work history",
    format="json",
    schema={
        "type": "object",
        "properties": {
            "current_company": {"type": "string"},
            "current_role": {"type": "string"},
            "years_experience": {"type": "number"},
            "previous_companies": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
)
```

## 💡 Example Use Cases

### 1. Recruiting for Tech Roles

```python
criteria = SearchCriteria(
    query="Full-stack engineers with React and Node.js experience",
    count=50,
    criteria=[
        "Has 3-7 years of full-stack development experience",
        "Proficient in React and Node.js",
        "Currently employed but open to opportunities",
        "Located in US or remote-friendly"
    ]
)

enrichments = [
    EnrichmentConfig("Find LinkedIn profile and GitHub account"),
    EnrichmentConfig("Extract their tech stack and frameworks"),
    EnrichmentConfig("Identify their most recent projects"),
    EnrichmentConfig("Find their contact email if available")
]
```

### 2. Finding Sales Prospects

```python
criteria = SearchCriteria(
    query="Decision makers at mid-size SaaS companies",
    count=100,
    criteria=[
        "Holds title of VP, Director, or C-level in Sales or Revenue",
        "Company has 50-500 employees",
        "Company sells B2B SaaS products",
        "Based in North America"
    ]
)

enrichments = [
    EnrichmentConfig("Find their LinkedIn profile"),
    EnrichmentConfig("Extract company details and product"),
    EnrichmentConfig("Identify recent company news or funding"),
    EnrichmentConfig("Find their professional email")
]
```

### 3. Academic Recruiting

```python
criteria = SearchCriteria(
    query="PhD candidates in Machine Learning graduating in 2024-2025",
    count=25,
    criteria=[
        "Currently pursuing or recently completed PhD in CS/ML",
        "Research focus on deep learning or computer vision",
        "Has publications in top-tier venues",
        "Expected graduation date within next 12 months"
    ]
)

enrichments = [
    EnrichmentConfig("Find their academic homepage and LinkedIn"),
    EnrichmentConfig("List their key publications and research areas"),
    EnrichmentConfig("Extract university and advisor information"),
    EnrichmentConfig("Find their Google Scholar profile")
]
```

### 4. Investor/Partnership Outreach

```python
criteria = SearchCriteria(
    query="VCs focused on early-stage AI startups",
    count=40,
    criteria=[
        "Works at a venture capital firm",
        "Focuses on seed to Series A investments",
        "Has invested in AI/ML companies",
        "Active on LinkedIn or Twitter"
    ]
)

enrichments = [
    EnrichmentConfig("Find their LinkedIn and Twitter profiles"),
    EnrichmentConfig("List their portfolio companies"),
    EnrichmentConfig("Identify their investment thesis"),
    EnrichmentConfig("Find their preferred contact method")
]
```

## 🎯 Best Practices

### Writing Effective Queries

**✅ Good Queries:**
- "Senior DevOps Engineers at cloud-native startups"
- "Marketing Directors at D2C e-commerce brands"
- "Research Scientists focusing on NLP at tech companies"

**❌ Avoid:**
- Too vague: "software engineers" (too broad)
- Too narrow: "Senior Staff Principal Architect L7 at Google in Mountain View office" (too specific)
- Questions: "Who are the best engineers?" (use declarative statements)

### Defining Criteria

**✅ Good Criteria:**
- "Has 5+ years of experience"
- "Currently employed at a Series B+ startup"
- "Based in United States or Canada"
- "Experience with AWS, Kubernetes, or similar cloud platforms"

**❌ Avoid:**
- Subjective: "Is a great culture fit"
- Redundant: Repeating information from query
- Too restrictive: Combining too many AND conditions

### Choosing Enrichments

**Essential Enrichments:**
1. Contact information (LinkedIn, email)
2. Current role and company
3. Years of experience
4. Key skills or expertise

**Nice-to-Have Enrichments:**
- Social media profiles
- Recent activities or posts
- Education background
- Certifications or awards

## ⚙️ Configuration

### Environment Variables

```bash
# Required
export EXA_API_KEY='your-api-key-here'

# Optional - for advanced usage
export EXA_TIMEOUT=3600  # Search timeout in seconds
export EXA_MAX_RETRIES=3  # Number of retries on failure
```

### Rate Limits and Quotas

Exa Websets API has the following characteristics:
- **Async-first**: Searches run asynchronously, can take seconds to minutes
- **Large searches**: 1000+ results can take ~1 hour
- **Auto-stop**: Searches stop if requested count isn't found before limit (50x requested or 50,000 max)

Check your plan limits at [dashboard.exa.ai](https://dashboard.exa.ai)

## 🔧 Advanced Usage

### Monitoring Search Progress

```python
# Create search
webset_info = finder.create_candidate_search(criteria, enrichments)

# Check progress periodically
while True:
    status = finder.get_webset_status(webset_info['id'])
    
    for search in status['searches']:
        if 'progress' in search:
            progress = search['progress']
            print(f"Found: {progress['found']}")
            print(f"Analyzed: {progress['analyzed']}")
            print(f"Completion: {progress['completion']}%")
            print(f"Time left: {progress['time_left']}s")
    
    if status['status'] == 'idle':
        break
    
    time.sleep(10)
```

### Using External IDs for Tracking

```python
# Use your own identifiers to track searches
finder.create_candidate_search(
    criteria=criteria,
    enrichments=enrichments,
    external_id="q4-2024-ml-hiring",  # Your tracking ID
    metadata={
        "campaign": "Q4 Hiring",
        "department": "Engineering",
        "requisition_id": "ENG-2024-089"
    }
)

# Later, list your searches
websets = finder.list_websets(limit=20)
for ws in websets:
    print(f"ID: {ws['external_id']}, Status: {ws['status']}")
```

### Batch Processing Multiple Searches

```python
searches = [
    ("Senior Engineers", "Senior SWE at FAANG", 50),
    ("Mid-level Engineers", "Mid-level SWE with 3-5 years", 100),
    ("Junior Engineers", "Junior SWE, recent grads", 150)
]

webset_ids = []
for name, query, count in searches:
    criteria = SearchCriteria(query=query, count=count)
    webset = finder.create_candidate_search(
        criteria,
        enrichments=[EnrichmentConfig("Find LinkedIn profile")],
        external_id=name
    )
    webset_ids.append(webset['id'])

# Wait for all to complete
for webset_id in webset_ids:
    finder.wait_for_results(webset_id)
    candidates = finder.get_candidates(webset_id)
    print(f"Webset {webset_id}: {len(candidates)} candidates found")
```

## 📊 Output Format

Results are returned as a list of dictionaries with the following structure:

```json
{
  "id": "item_abc123",
  "url": "https://linkedin.com/in/johndoe",
  "title": "John Doe - Senior ML Engineer at StartupAI",
  "status": "completed",
  "verification": {
    "passed": true,
    "criteria_results": [
      {
        "description": "Has 5+ years of ML experience",
        "passed": true,
        "reasoning": "Profile shows 7 years of ML experience...",
        "references": ["https://..."]
      }
    ]
  },
  "properties": {
    "name": "John Doe",
    "current_role": "Senior ML Engineer",
    "current_company": "StartupAI",
    "location": "San Francisco, CA"
  },
  "enrichments": [
    {
      "description": "Find LinkedIn profile",
      "status": "completed",
      "result": "https://linkedin.com/in/johndoe"
    }
  ]
}
```

## 🐛 Troubleshooting

### Common Issues

**Issue: "API key is required"**
```bash
# Make sure your API key is set
echo $EXA_API_KEY
export EXA_API_KEY='your-key-here'
```

**Issue: Search takes too long**
- Large searches (1000+ results) can take up to an hour
- Reduce `count` to get faster results
- Use `get_webset_status()` to monitor progress

**Issue: Few or no results**
- Query might be too narrow - try broadening criteria
- Remove some restrictive criteria
- Increase `count` parameter

**Issue: Low-quality results**
- Add more specific criteria to filter results
- Use exclude_criteria to remove unwanted matches
- Refine your query language

## 📖 Additional Resources

- [Exa API Documentation](https://docs.exa.ai)
- [Exa Websets Guide](https://docs.exa.ai/websets/api/overview)
- [Example Queries](https://docs.exa.ai/websets/websets-example-queries)
- [Get API Key](https://dashboard.exa.ai/api-keys)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this code in your projects!

## 💬 Support

- For Exa API issues: [email protected]
- For this tool: Open an issue on GitHub

## 🙏 Acknowledgments

Built with [Exa AI](https://exa.ai) - The search engine for AI applications.
