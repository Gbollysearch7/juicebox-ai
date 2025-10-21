# LinkedIn Candidate Finder - Complete Package

## 📦 Package Contents

This zip file contains a complete, production-ready tool for finding LinkedIn candidates using the Exa Websets API.

**Total Files: 8**
**Total Size: ~94 KB**

### Core Files

1. **linkedin_candidate_finder.py** (20 KB)
   - Main tool implementation
   - LinkedInCandidateFinder class
   - SearchCriteria and EnrichmentConfig classes
   - Built-in examples for ML Engineers, Sales Leaders, PhD Candidates
   - Interactive CLI interface

2. **utilities.py** (17 KB)
   - CandidateExporter (JSON, CSV, Markdown export)
   - BatchSearchManager (run multiple searches)
   - ProgressMonitor (real-time tracking)
   - CandidateFilter (filtering and deduplication)
   - Example utility functions

3. **examples.py** (22 KB)
   - 12 complete, ready-to-run examples:
     * Senior ML Engineers
     * Frontend Engineers (React)
     * DevOps Engineers (Kubernetes)
     * Enterprise Account Executives
     * Growth Marketing Managers
     * VP of Engineering
     * Fintech CTOs
     * NLP PhD Candidates
     * Computer Vision Research Scientists
     * Healthcare Product Managers
     * Blockchain Developers
     * Full Engineering Team (batch search)

### Documentation

4. **README.md** (16 KB)
   - Complete API reference
   - Installation and setup instructions
   - Detailed usage examples
   - Best practices and tips
   - Troubleshooting guide
   - FAQ section

5. **QUICKSTART.md** (6 KB)
   - 2-minute installation
   - 5-minute first search
   - Common use cases
   - Quick troubleshooting

6. **PROJECT_OVERVIEW.md** (12 KB)
   - System architecture
   - Data flow diagrams
   - Component breakdown
   - Understanding Exa Websets
   - Technology stack
   - Future enhancements

### Configuration

7. **requirements.txt**
   - Python dependencies (exa_py, python-dotenv)

8. **.env.example**
   - Environment variable template
   - Configuration options

## 🚀 Quick Start

### Step 1: Extract the Zip
```bash
unzip linkedin_candidate_finder.zip
cd linkedin_candidate_finder
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Your API Key
```bash
# Get your API key from: https://dashboard.exa.ai/api-keys
export EXA_API_KEY='your-api-key-here'

# Or create a .env file
cp .env.example .env
# Edit .env and add your API key
```

### Step 4: Run Your First Search
```bash
# Interactive examples
python linkedin_candidate_finder.py

# Or run specific examples
python examples.py

# Or use utilities
python utilities.py
```

## 📖 What to Read First

**If you want to...**

- **Get started quickly**: Read `QUICKSTART.md`
- **Understand the system**: Read `PROJECT_OVERVIEW.md`
- **See complete documentation**: Read `README.md`
- **Run examples**: Open `examples.py`
- **Learn the API**: Look at `linkedin_candidate_finder.py`

## 💡 Simple Usage Example

```python
from linkedin_candidate_finder import (
    LinkedInCandidateFinder,
    SearchCriteria,
    EnrichmentConfig
)

# Initialize
finder = LinkedInCandidateFinder()

# Define search
criteria = SearchCriteria(
    query="Software Engineers at tech startups",
    count=20,
    criteria=[
        "Has 3+ years of software engineering experience",
        "Currently employed at a startup",
        "Based in United States"
    ]
)

# Define enrichments
enrichments = [
    EnrichmentConfig("Find their LinkedIn profile"),
    EnrichmentConfig("Extract current company and role"),
    EnrichmentConfig("List their top technical skills")
]

# Run search
candidates = finder.search_and_wait(
    search_criteria=criteria,
    enrichments=enrichments
)

# Process results
print(f"Found {len(candidates)} candidates")
for candidate in candidates:
    print(f"- {candidate['url']}")
```

## 🎯 Key Features

### Core Capabilities
✅ Natural language candidate search
✅ AI-powered verification with reasoning
✅ Automatic data enrichment
✅ Structured, validated results
✅ Async processing with progress tracking

### Advanced Features
✅ Batch processing (multiple searches at once)
✅ Real-time progress monitoring
✅ Export to JSON, CSV, Markdown
✅ Filtering and deduplication
✅ Custom enrichment schemas
✅ External ID tracking

### Included Examples
✅ 12 real-world recruiting scenarios
✅ Tech, Sales, Leadership, Academic roles
✅ Industry-specific examples
✅ Batch search examples

## 🔧 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Dependencies**: exa_py, python-dotenv (auto-installed)
- **API Key**: Free tier available at https://exa.ai

## 📊 What's Exa Websets?

Exa Websets is an AI-powered API that:
1. **Searches** the web for people/companies matching your criteria
2. **Verifies** each result against your requirements with reasoning
3. **Enriches** results with additional structured data
4. **Returns** validated, structured information

**Perfect for:**
- Recruiting and talent sourcing
- Lead generation
- Market research
- Academic recruiting
- Executive search

## 🎓 Learning Path

**Beginner (30 minutes)**
1. Read QUICKSTART.md
2. Run `python linkedin_candidate_finder.py`
3. Try one of the built-in examples
4. Modify the search criteria

**Intermediate (2 hours)**
1. Read README.md thoroughly
2. Run examples from `examples.py`
3. Try batch searches with utilities
4. Export results to different formats

**Advanced (1 day)**
1. Read PROJECT_OVERVIEW.md
2. Understand the architecture
3. Create custom enrichments
4. Build your own recruiting workflows
5. Integrate with your ATS/CRM

## 💼 Use Cases

This tool is perfect for:

### Tech Recruiting
- Software Engineers (all levels, all stacks)
- ML Engineers & Data Scientists
- DevOps & Infrastructure Engineers
- Engineering Managers & Leaders

### Sales & Marketing
- Account Executives
- SDRs and BDRs
- Marketing Managers
- Customer Success Managers

### Executive Search
- C-level Executives (CTO, VP Eng, etc.)
- Directors and VPs
- Industry-specific leadership

### Academic Recruiting
- PhD Candidates
- Research Scientists
- Postdocs
- Faculty

### Specialized Industries
- Healthcare/HealthTech
- Fintech/Blockchain
- Climate Tech
- AI/ML Research

## 📈 Typical Workflow

```
1. Define who you're looking for
   ↓
2. Run search (takes 1-60 minutes depending on size)
   ↓
3. Review and filter results
   ↓
4. Export to your ATS/spreadsheet
   ↓
5. Begin outreach
```

## 🛠️ Customization

The tool is highly customizable:

**Custom Searches**
- Modify search criteria
- Add/remove requirements
- Change entity types

**Custom Enrichments**
- Extract any data from profiles
- Use structured JSON schemas
- Combine multiple enrichments

**Custom Workflows**
- Batch multiple role searches
- Set up monitoring and alerts
- Integrate with your systems

## 🐛 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key is required"
```bash
export EXA_API_KEY='your-key-here'
```

### "Search takes too long"
- Large searches can take 30-60 minutes
- Start with count=10 for testing
- Monitor progress with `get_webset_status()`

### "No results found"
- Query might be too narrow
- Try removing some criteria
- Broaden your search terms

## 📚 Additional Resources

- **Exa Documentation**: https://docs.exa.ai/websets
- **API Reference**: https://docs.exa.ai/websets/api
- **Get API Key**: https://dashboard.exa.ai/api-keys
- **Example Queries**: https://docs.exa.ai/websets/websets-example-queries
- **Support Email**: [email protected]

## 🤝 Support

### Need Help?

1. **Check the docs**: All 3 documentation files cover common issues
2. **Run examples**: See working code in `examples.py`
3. **Read the code**: Well-commented source code
4. **Contact Exa**: [email protected] for API issues

### Want to Contribute?

This is open-source code! Feel free to:
- Add new examples
- Improve documentation
- Fix bugs
- Add features

## 📄 License

MIT License - Free to use and modify for your needs.

## 🙏 Credits

Built with:
- **Exa AI** - The search engine for AI applications
- **Python** - Programming language
- **exa_py** - Official Exa Python SDK

---

## 🎉 You're Ready!

Everything you need is in this package:
- ✅ Complete, working code
- ✅ Comprehensive documentation
- ✅ 12 real-world examples
- ✅ Utilities for advanced workflows
- ✅ Quick start guides

**Next Step**: Read `QUICKSTART.md` and start finding candidates!

Happy recruiting! 🚀
