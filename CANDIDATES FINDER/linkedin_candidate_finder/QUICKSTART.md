# Quick Start Guide

## Installation (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export EXA_API_KEY='your-api-key-here'

# 3. Test it works
python -c "from linkedin_candidate_finder import LinkedInCandidateFinder; print('✅ Ready to go!')"
```

## Your First Search (5 minutes)

Create a file called `my_first_search.py`:

```python
from linkedin_candidate_finder import (
    LinkedInCandidateFinder,
    SearchCriteria,
    EnrichmentConfig
)

# Initialize
finder = LinkedInCandidateFinder()

# Define what you're looking for
criteria = SearchCriteria(
    query="Product Managers at tech companies",
    count=10,
    criteria=[
        "Has 3+ years of product management experience",
        "Currently employed at a tech company"
    ]
)

# Define what extra info you want
enrichments = [
    EnrichmentConfig("Find their LinkedIn profile"),
    EnrichmentConfig("Extract current company and role")
]

# Run the search (this will take a few minutes)
candidates = finder.search_and_wait(
    search_criteria=criteria,
    enrichments=enrichments
)

# Show results
print(f"Found {len(candidates)} candidates:")
for i, candidate in enumerate(candidates, 1):
    print(f"{i}. {candidate['url']}")
```

Run it:
```bash
python my_first_search.py
```

## Common Use Cases

### 1. Finding Engineers

```python
criteria = SearchCriteria(
    query="Backend Engineers with Python experience",
    count=30,
    criteria=[
        "Has 3-7 years of backend engineering experience",
        "Proficient in Python",
        "Currently employed"
    ]
)

enrichments = [
    EnrichmentConfig("Find LinkedIn and GitHub profiles"),
    EnrichmentConfig("List their tech stack and frameworks"),
    EnrichmentConfig("Extract years of experience")
]
```

### 2. Finding Sales Professionals

```python
criteria = SearchCriteria(
    query="Sales Directors at B2B SaaS companies",
    count=25,
    criteria=[
        "Currently holds Director or VP of Sales title",
        "Works at a B2B SaaS company",
        "Based in United States"
    ]
)

enrichments = [
    EnrichmentConfig("Find LinkedIn profile"),
    EnrichmentConfig("Extract company details"),
    EnrichmentConfig("Find professional email if available")
]
```

### 3. Finding Investors

```python
criteria = SearchCriteria(
    query="Venture Capital investors focused on AI",
    count=20,
    criteria=[
        "Works at a VC firm",
        "Invests in AI/ML companies",
        "Active on LinkedIn"
    ]
)

enrichments = [
    EnrichmentConfig("Find LinkedIn and Twitter profiles"),
    EnrichmentConfig("List portfolio companies"),
    EnrichmentConfig("Identify investment thesis")
]
```

### 4. Academic Recruiting

```python
criteria = SearchCriteria(
    query="PhD students in Computer Science",
    count=15,
    criteria=[
        "Currently pursuing PhD in CS or related field",
        "Research focus on machine learning",
        "Expected graduation within 12 months"
    ]
)

enrichments = [
    EnrichmentConfig("Find academic homepage and LinkedIn"),
    EnrichmentConfig("List publications and research areas"),
    EnrichmentConfig("Extract university and advisor")
]
```

## Exporting Results

### To JSON
```python
from utilities import CandidateExporter

exporter = CandidateExporter()
exporter.to_json(candidates, 'candidates.json')
```

### To CSV
```python
exporter.to_csv(candidates, 'candidates.csv')
```

### To Markdown
```python
exporter.to_markdown(candidates, 'candidates.md')
```

## Running Multiple Searches

```python
from utilities import BatchSearchManager

batch = BatchSearchManager(finder)

# Add searches
batch.add_search("engineers", engineer_criteria, engineer_enrichments)
batch.add_search("managers", manager_criteria, manager_enrichments)
batch.add_search("designers", designer_criteria, designer_enrichments)

# Run all at once
batch.run_all(parallel=True)

# Export everything
batch.export_all(format='json')
```

## Monitoring Progress

```python
from utilities import ProgressMonitor

# Create search
webset_info = finder.create_candidate_search(criteria, enrichments)

# Set up monitoring
monitor = ProgressMonitor(finder, webset_info['id'])

def print_progress(status):
    for search in status.get('searches', []):
        if 'progress' in search:
            print(f"Progress: {search['progress']['completion']}%")

monitor.add_callback(print_progress)
monitor.monitor(interval=15)
```

## Tips for Better Results

### ✅ DO:
- Use clear, specific queries
- Add 3-5 criteria to filter results
- Request reasonable counts (10-50 for testing, up to 1000 for production)
- Use enrichments to get the data you need
- Test with small counts first

### ❌ DON'T:
- Make queries too broad ("software engineers")
- Make queries too narrow (too many restrictive criteria)
- Request massive counts (1000+) without testing first
- Forget to wait for results before accessing them

## Troubleshooting

**"No results found"**
- Try broadening your criteria
- Reduce the number of restrictions
- Check if your query is too specific

**"Taking too long"**
- Large searches (500+) can take 30-60 minutes
- Use `get_webset_status()` to check progress
- Consider running smaller searches

**"API key error"**
```bash
# Make sure it's set correctly
echo $EXA_API_KEY

# Set it again if needed
export EXA_API_KEY='your-key'
```

## Next Steps

1. **Read the full README.md** for detailed documentation
2. **Check out utilities.py** for advanced features
3. **Experiment with different queries** to find what works
4. **Join the Exa Discord** for community support

## Getting Help

- **Documentation**: See README.md
- **Examples**: Run `python linkedin_candidate_finder.py`
- **Exa Support**: [email protected]
- **API Docs**: https://docs.exa.ai/websets

Happy searching! 🚀
