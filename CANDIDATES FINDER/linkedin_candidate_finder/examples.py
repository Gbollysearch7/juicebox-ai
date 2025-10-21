"""
Real-World Examples for LinkedIn Candidate Finder

This file contains complete, ready-to-run examples for various
recruiting and sourcing scenarios using the Exa Websets API.
"""

from linkedin_candidate_finder import (
    LinkedInCandidateFinder,
    SearchCriteria,
    EnrichmentConfig,
    EntityType
)
from utilities import CandidateExporter, BatchSearchManager, CandidateFilter


# ============================================================================
# TECH RECRUITING EXAMPLES
# ============================================================================

def find_senior_ml_engineers():
    """
    Scenario: You're hiring senior ML engineers for an AI startup.
    
    Requirements:
    - 5+ years of ML/AI experience
    - Experience with production ML systems
    - Strong Python skills
    - Currently employed (to gauge market rate)
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Senior Machine Learning Engineers with production ML experience",
        count=40,
        entity=EntityType.PERSON,
        criteria=[
            "Has 5+ years of machine learning or AI engineering experience",
            "Has deployed ML models to production environments",
            "Strong proficiency in Python and ML frameworks (TensorFlow, PyTorch, or similar)",
            "Currently employed at a tech company",
            "Located in United States or open to remote work"
        ]
    )
    
    enrichments = [
        EnrichmentConfig(
            description="Find their LinkedIn profile URL and current employment status"
        ),
        EnrichmentConfig(
            description="Extract: current company, current role, years in current role"
        ),
        EnrichmentConfig(
            description="List their top ML/AI skills and frameworks they've used"
        ),
        EnrichmentConfig(
            description="Find their GitHub profile if publicly available"
        ),
        EnrichmentConfig(
            description="Identify if they have published papers or patents in ML/AI"
        )
    ]
    
    print("🔍 Searching for Senior ML Engineers...")
    candidates = finder.search_and_wait(
        search_criteria=criteria,
        enrichments=enrichments,
        external_id="senior-ml-engineers-q1-2025"
    )
    
    # Filter and export
    candidates = CandidateFilter.filter_by_verification(candidates, passed=True)
    
    exporter = CandidateExporter()
    exporter.to_json(candidates, 'ml_engineers.json')
    exporter.to_csv(candidates, 'ml_engineers.csv')
    
    print(f"✅ Found {len(candidates)} qualified ML engineers")
    return candidates


def find_frontend_engineers_react():
    """
    Scenario: You need frontend engineers with React expertise.
    
    Requirements:
    - 3-5 years frontend experience
    - Expert in React
    - Experience with modern tools (TypeScript, Next.js, etc.)
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Frontend Engineers specializing in React and modern JavaScript",
        count=50,
        entity=EntityType.PERSON,
        criteria=[
            "Has 3-5 years of frontend web development experience",
            "Expert-level proficiency in React and JavaScript",
            "Experience with TypeScript and modern frontend tooling",
            "Has worked on consumer-facing web applications",
            "Currently employed or recently left a position"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn and GitHub profiles"),
        EnrichmentConfig("Extract current/most recent company and role"),
        EnrichmentConfig("List specific technologies and frameworks they've used"),
        EnrichmentConfig("Identify any notable projects or open source contributions")
    ]
    
    print("🔍 Searching for Frontend Engineers...")
    return finder.search_and_wait(criteria, enrichments, "frontend-react-engineers")


def find_devops_kubernetes_experts():
    """
    Scenario: You need DevOps engineers with Kubernetes expertise.
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="DevOps Engineers with Kubernetes and cloud infrastructure experience",
        count=30,
        entity=EntityType.PERSON,
        criteria=[
            "Has 4+ years of DevOps or infrastructure engineering experience",
            "Expert in Kubernetes and container orchestration",
            "Experience with AWS, GCP, or Azure cloud platforms",
            "Proficient in Infrastructure as Code (Terraform, Ansible, etc.)",
            "Currently employed"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn profile"),
        EnrichmentConfig("Extract current role, company, and years of experience"),
        EnrichmentConfig("List their cloud platforms and DevOps tools expertise"),
        EnrichmentConfig("Identify certifications (CKA, AWS, etc.) if mentioned")
    ]
    
    print("🔍 Searching for DevOps Engineers...")
    return finder.search_and_wait(criteria, enrichments, "devops-k8s-experts")


# ============================================================================
# SALES & MARKETING RECRUITING EXAMPLES
# ============================================================================

def find_enterprise_account_executives():
    """
    Scenario: You're building an enterprise sales team.
    
    Requirements:
    - 5+ years enterprise sales experience
    - Proven track record at B2B SaaS companies
    - Experience with $100K+ deal sizes
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Enterprise Account Executives at B2B SaaS companies",
        count=35,
        entity=EntityType.PERSON,
        criteria=[
            "Has 5+ years of enterprise sales experience",
            "Currently or recently worked at a B2B SaaS company",
            "Proven experience closing deals over $100K annually",
            "Carries or has carried a quota",
            "Based in United States"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn profile and professional email if available"),
        EnrichmentConfig("Extract current company, role, and years in sales"),
        EnrichmentConfig("Identify industries they've sold into"),
        EnrichmentConfig("Extract quota achievement or sales metrics if mentioned")
    ]
    
    print("🔍 Searching for Enterprise AEs...")
    return finder.search_and_wait(criteria, enrichments, "enterprise-ae-2025")


def find_growth_marketing_managers():
    """
    Scenario: You need growth marketing specialists for a startup.
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Growth Marketing Managers with B2C or B2B SaaS experience",
        count=25,
        entity=EntityType.PERSON,
        criteria=[
            "Has 3-6 years of growth marketing or performance marketing experience",
            "Experience at a startup or high-growth company",
            "Skilled in digital marketing channels (paid, SEO, content, etc.)",
            "Data-driven approach with analytics experience",
            "Currently employed or recently available"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn profile"),
        EnrichmentConfig("Extract current company, role, and marketing channels expertise"),
        EnrichmentConfig("Identify key metrics or growth achievements mentioned"),
        EnrichmentConfig("List marketing tools and platforms they've used")
    ]
    
    print("🔍 Searching for Growth Marketing Managers...")
    return finder.search_and_wait(criteria, enrichments, "growth-marketing-mgrs")


# ============================================================================
# LEADERSHIP & EXECUTIVE RECRUITING EXAMPLES
# ============================================================================

def find_vp_engineering_candidates():
    """
    Scenario: You're looking for VP of Engineering candidates.
    
    Requirements:
    - 10+ years engineering experience with 3+ in leadership
    - Experience managing engineering teams of 20+
    - Track record of scaling engineering orgs
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="VP of Engineering or Director of Engineering at tech companies",
        count=20,
        entity=EntityType.PERSON,
        criteria=[
            "Has 10+ years of software engineering experience",
            "Has 3+ years in engineering leadership roles",
            "Currently or recently managed engineering teams of 20+ people",
            "Experience scaling engineering organizations",
            "Currently holds VP or Director level position"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn profile and contact information"),
        EnrichmentConfig("Extract current company, role, and team size"),
        EnrichmentConfig("Identify their technical background and expertise areas"),
        EnrichmentConfig("Extract information about companies they've worked at and their growth")
    ]
    
    print("🔍 Searching for VP Engineering candidates...")
    return finder.search_and_wait(criteria, enrichments, "vp-engineering-search")


def find_ctos_fintech():
    """
    Scenario: You're recruiting a CTO with fintech experience.
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="CTOs or VP Engineering with fintech or financial services experience",
        count=15,
        entity=EntityType.PERSON,
        criteria=[
            "Currently or recently held CTO, VP Engineering, or Head of Engineering title",
            "Has worked in fintech, payments, or financial services",
            "Experience with regulatory compliance and security",
            "Led technical teams through scaling challenges",
            "Currently employed or recently available"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn profile and professional network"),
        EnrichmentConfig("Extract career history focusing on fintech companies"),
        EnrichmentConfig("Identify technical expertise and architecture experience"),
        EnrichmentConfig("List any notable achievements or exits")
    ]
    
    print("🔍 Searching for Fintech CTOs...")
    return finder.search_and_wait(criteria, enrichments, "fintech-cto-search")


# ============================================================================
# ACADEMIC & RESEARCH RECRUITING EXAMPLES
# ============================================================================

def find_phd_candidates_nlp():
    """
    Scenario: You're recruiting PhD candidates/graduates for NLP research roles.
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="PhD students or recent graduates in NLP and Computational Linguistics",
        count=20,
        entity=EntityType.PERSON,
        criteria=[
            "Currently pursuing or recently completed PhD in Computer Science, Linguistics, or related field",
            "Research focus on Natural Language Processing or Computational Linguistics",
            "Has publications in top-tier NLP conferences (ACL, EMNLP, NAACL, etc.)",
            "Expected graduation within 12 months or graduated within last 2 years",
            "Located in United States or willing to relocate"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find academic homepage, LinkedIn, and Google Scholar profile"),
        EnrichmentConfig("List their research topics and key publications"),
        EnrichmentConfig("Extract university, advisor, and expected graduation date"),
        EnrichmentConfig("Identify any industry experience or internships")
    ]
    
    print("🔍 Searching for NLP PhD candidates...")
    return finder.search_and_wait(criteria, enrichments, "nlp-phd-candidates")


def find_research_scientists_computer_vision():
    """
    Scenario: You need research scientists with computer vision expertise.
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Research Scientists specializing in Computer Vision and Deep Learning",
        count=25,
        entity=EntityType.PERSON,
        criteria=[
            "Has PhD or equivalent research experience in Computer Vision or related field",
            "Strong publication record in computer vision conferences (CVPR, ICCV, ECCV, etc.)",
            "Experience with deep learning and neural networks for vision tasks",
            "Currently employed in research role or recently available",
            "Has at least 2 years of post-PhD experience"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn, Google Scholar, and personal webpage"),
        EnrichmentConfig("List research areas, key publications, and citation count"),
        EnrichmentConfig("Extract current affiliation and research group"),
        EnrichmentConfig("Identify any patents or notable projects")
    ]
    
    print("🔍 Searching for Computer Vision Research Scientists...")
    return finder.search_and_wait(criteria, enrichments, "cv-research-scientists")


# ============================================================================
# INDUSTRY-SPECIFIC EXAMPLES
# ============================================================================

def find_healthcare_product_managers():
    """
    Scenario: You need PMs with healthcare/digital health experience.
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Product Managers with healthcare or digital health experience",
        count=30,
        entity=EntityType.PERSON,
        criteria=[
            "Has 4+ years of product management experience",
            "Experience in healthcare, digital health, or health tech",
            "Understanding of healthcare regulations (HIPAA, etc.)",
            "Experience with B2B healthcare products or clinical workflows",
            "Currently employed in healthcare tech"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn profile"),
        EnrichmentConfig("Extract current company, role, and healthcare focus area"),
        EnrichmentConfig("Identify specific healthcare products they've worked on"),
        EnrichmentConfig("List relevant healthcare domain expertise")
    ]
    
    print("🔍 Searching for Healthcare Product Managers...")
    return finder.search_and_wait(criteria, enrichments, "healthcare-pms")


def find_blockchain_developers():
    """
    Scenario: You're building a Web3/blockchain team.
    """
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Blockchain Developers with smart contract and DeFi experience",
        count=25,
        entity=EntityType.PERSON,
        criteria=[
            "Has 2+ years of blockchain development experience",
            "Experience with Solidity and smart contract development",
            "Familiar with Ethereum, Layer 2s, or other blockchain platforms",
            "Understanding of DeFi protocols or NFTs",
            "Currently employed in Web3/crypto space"
        ]
    )
    
    enrichments = [
        EnrichmentConfig("Find LinkedIn and GitHub profiles"),
        EnrichmentConfig("Extract blockchain platforms and protocols they've worked with"),
        EnrichmentConfig("Identify any notable DeFi projects or smart contracts"),
        EnrichmentConfig("List programming languages and blockchain tools expertise")
    ]
    
    print("🔍 Searching for Blockchain Developers...")
    return finder.search_and_wait(criteria, enrichments, "blockchain-developers")


# ============================================================================
# BATCH SEARCH EXAMPLES
# ============================================================================

def run_full_engineering_team_search():
    """
    Scenario: You're building an entire engineering team and need multiple roles.
    
    This example shows how to search for multiple roles simultaneously.
    """
    finder = LinkedInCandidateFinder()
    batch = BatchSearchManager(finder)
    
    # Define common enrichments
    standard_enrichments = [
        EnrichmentConfig("Find LinkedIn and GitHub profiles"),
        EnrichmentConfig("Extract current company and role"),
        EnrichmentConfig("List technical skills and expertise")
    ]
    
    # Backend Engineers
    batch.add_search(
        name="backend-engineers",
        criteria=SearchCriteria(
            query="Backend Engineers with Python and distributed systems",
            count=30,
            criteria=[
                "Has 3-7 years backend engineering experience",
                "Proficient in Python and distributed systems",
                "Currently employed"
            ]
        ),
        enrichments=standard_enrichments
    )
    
    # Frontend Engineers
    batch.add_search(
        name="frontend-engineers",
        criteria=SearchCriteria(
            query="Frontend Engineers with React and TypeScript",
            count=25,
            criteria=[
                "Has 3-6 years frontend engineering experience",
                "Expert in React and TypeScript",
                "Currently employed"
            ]
        ),
        enrichments=standard_enrichments
    )
    
    # DevOps Engineers
    batch.add_search(
        name="devops-engineers",
        criteria=SearchCriteria(
            query="DevOps Engineers with Kubernetes and AWS",
            count=20,
            criteria=[
                "Has 4+ years DevOps experience",
                "Expert in Kubernetes and AWS",
                "Currently employed"
            ]
        ),
        enrichments=standard_enrichments
    )
    
    # Engineering Managers
    batch.add_search(
        name="engineering-managers",
        criteria=SearchCriteria(
            query="Engineering Managers with 5+ years experience",
            count=15,
            criteria=[
                "Has 2+ years in engineering leadership",
                "Managed teams of 5-15 engineers",
                "Currently employed"
            ]
        ),
        enrichments=[
            EnrichmentConfig("Find LinkedIn profile"),
            EnrichmentConfig("Extract team size and management experience"),
            EnrichmentConfig("Identify technical background")
        ]
    )
    
    print("🚀 Running batch search for entire engineering team...")
    batch.run_all(parallel=True)
    
    # Export all results
    batch.export_all(format='json', output_dir='./team_search_results')
    batch.export_all(format='csv', output_dir='./team_search_results')
    
    return batch.get_all_results()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    import os
    
    if not os.getenv('EXA_API_KEY'):
        print("❌ Error: EXA_API_KEY not set")
        print("   Get your key at: https://dashboard.exa.ai/api-keys")
        sys.exit(1)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         Real-World Recruiting Examples                       ║
║         Powered by Exa Websets API                           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📂 TECH RECRUITING:")
    print("1.  Senior ML Engineers")
    print("2.  Frontend Engineers (React)")
    print("3.  DevOps Engineers (Kubernetes)")
    
    print("\n💼 SALES & MARKETING:")
    print("4.  Enterprise Account Executives")
    print("5.  Growth Marketing Managers")
    
    print("\n👔 LEADERSHIP:")
    print("6.  VP of Engineering")
    print("7.  CTOs with Fintech Experience")
    
    print("\n🎓 ACADEMIC:")
    print("8.  PhD Candidates in NLP")
    print("9.  Computer Vision Research Scientists")
    
    print("\n🏥 INDUSTRY-SPECIFIC:")
    print("10. Healthcare Product Managers")
    print("11. Blockchain Developers")
    
    print("\n🔄 BATCH SEARCHES:")
    print("12. Full Engineering Team (multiple roles)")
    
    choice = input("\nSelect an example (1-12): ").strip()
    
    examples = {
        "1": ("Senior ML Engineers", find_senior_ml_engineers),
        "2": ("Frontend Engineers", find_frontend_engineers_react),
        "3": ("DevOps Engineers", find_devops_kubernetes_experts),
        "4": ("Enterprise AEs", find_enterprise_account_executives),
        "5": ("Growth Marketing", find_growth_marketing_managers),
        "6": ("VP Engineering", find_vp_engineering_candidates),
        "7": ("Fintech CTOs", find_ctos_fintech),
        "8": ("NLP PhDs", find_phd_candidates_nlp),
        "9": ("CV Research Scientists", find_research_scientists_computer_vision),
        "10": ("Healthcare PMs", find_healthcare_product_managers),
        "11": ("Blockchain Devs", find_blockchain_developers),
        "12": ("Full Team", run_full_engineering_team_search),
    }
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\n{'='*60}")
        print(f"Running: {name}")
        print(f"{'='*60}\n")
        
        try:
            results = func()
            
            if isinstance(results, list):
                print(f"\n✅ Complete! Found {len(results)} candidates")
            elif isinstance(results, dict):
                print(f"\n✅ Complete! Found candidates across {len(results)} searches")
                for search_name, candidates in results.items():
                    print(f"   - {search_name}: {len(candidates)} candidates")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Search interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Invalid choice")
