"""
LinkedIn Candidate Finder using Exa Websets API

This tool helps you find candidates on LinkedIn using Exa's powerful Websets API.
Websets allows you to search for people matching specific criteria and enriches
the results with additional information.
"""

import os
import time
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

try:
    from exa_py import Exa
    from exa_py.websets.types import CreateWebsetParameters, CreateEnrichmentParameters
except ImportError:
    print("Please install exa_py: pip install exa_py")
    exit(1)


class EntityType(str, Enum):
    """Entity types supported by Websets"""
    PERSON = "person"
    COMPANY = "company"
    RESEARCH_PAPER = "research_paper"
    ARTICLE = "article"


@dataclass
class SearchCriteria:
    """Defines search criteria for finding candidates"""
    query: str
    count: int = 10
    entity: EntityType = EntityType.PERSON
    criteria: Optional[List[str]] = None
    exclude_criteria: Optional[List[str]] = None
    

@dataclass
class EnrichmentConfig:
    """Configuration for enriching candidate data"""
    description: str
    format: str = "text"  # or "json"
    schema: Optional[Dict] = None


class LinkedInCandidateFinder:
    """
    A tool to find and enrich LinkedIn candidate profiles using Exa Websets API.
    
    Key Features:
    - Search for people matching specific criteria
    - Automatically verify candidates against your requirements
    - Enrich profiles with additional information (emails, skills, experience)
    - Monitor for new candidates matching your criteria
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LinkedIn Candidate Finder.
        
        Args:
            api_key: Your Exa API key. If not provided, reads from EXA_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('EXA_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Exa API key is required. Set EXA_API_KEY environment variable "
                "or pass api_key to constructor. Get your key at: https://dashboard.exa.ai/api-keys"
            )
        
        self.exa = Exa(self.api_key)
        
    def create_candidate_search(
        self,
        search_criteria: SearchCriteria,
        enrichments: Optional[List[EnrichmentConfig]] = None,
        external_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a new webset to find candidates matching your criteria.
        
        Args:
            search_criteria: Defines what candidates you're looking for
            enrichments: Additional data to extract for each candidate
            external_id: Your own identifier for this search
            metadata: Additional metadata to attach to the webset
            
        Returns:
            Dictionary containing webset information including ID and status
            
        Example:
            >>> finder = LinkedInCandidateFinder()
            >>> criteria = SearchCriteria(
            ...     query="Senior ML Engineers at AI startups in San Francisco",
            ...     count=20,
            ...     criteria=[
            ...         "Has 5+ years of experience in machine learning",
            ...         "Currently working at a startup",
            ...         "Based in San Francisco Bay Area"
            ...     ]
            ... )
            >>> enrichments = [
            ...     EnrichmentConfig("Find their LinkedIn profile URL"),
            ...     EnrichmentConfig("Extract their current role and company"),
            ...     EnrichmentConfig("Find their email address if publicly available")
            ... ]
            >>> webset = finder.create_candidate_search(criteria, enrichments)
        """
        print(f"🔍 Creating candidate search: '{search_criteria.query}'")
        print(f"   Looking for {search_criteria.count} candidates...")
        
        # Build search parameters
        search_params = {
            "query": search_criteria.query,
            "count": search_criteria.count,
            "entity": {"type": search_criteria.entity.value}
        }
        
        # Add criteria if provided
        if search_criteria.criteria:
            search_params["criteria"] = [
                {"description": criterion} 
                for criterion in search_criteria.criteria
            ]
            
        # Add exclude criteria if provided
        if search_criteria.exclude_criteria:
            # This would be used in the exclude parameter
            pass
        
        # Build enrichment parameters
        enrichment_params = []
        if enrichments:
            for enrich in enrichments:
                params = CreateEnrichmentParameters(
                    description=enrich.description,
                    format=enrich.format
                )
                if enrich.schema:
                    params.schema = enrich.schema
                enrichment_params.append(params)
        
        # Create the webset
        try:
            webset = self.exa.websets.create(
                params=CreateWebsetParameters(
                    search=search_params,
                    enrichments=enrichment_params if enrichment_params else None,
                    externalId=external_id,
                    metadata=metadata or {}
                )
            )
            
            print(f"✅ Webset created successfully!")
            print(f"   Webset ID: {webset.id}")
            print(f"   Status: {webset.status}")
            
            return {
                "id": webset.id,
                "status": webset.status,
                "external_id": external_id,
                "search_query": search_criteria.query
            }
            
        except Exception as e:
            print(f"❌ Error creating webset: {str(e)}")
            raise
    
    def wait_for_results(
        self,
        webset_id: str,
        timeout: int = 3600,
        check_interval: int = 10
    ) -> Dict[str, Any]:
        """
        Wait for a webset to complete processing.
        
        Args:
            webset_id: The ID of the webset to wait for
            timeout: Maximum time to wait in seconds (default: 1 hour)
            check_interval: How often to check status in seconds
            
        Returns:
            The completed webset information
        """
        print(f"⏳ Waiting for webset {webset_id} to complete...")
        print(f"   This may take a while depending on the search complexity.")
        
        try:
            # Exa provides a convenient wait_until_idle method
            webset = self.exa.websets.wait_until_idle(
                webset_id,
                timeout=timeout
            )
            
            print(f"✅ Webset processing complete!")
            print(f"   Status: {webset.status}")
            
            return webset
            
        except Exception as e:
            print(f"❌ Error waiting for webset: {str(e)}")
            raise
    
    def get_candidates(
        self,
        webset_id: str,
        limit: Optional[int] = None,
        include_content: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Retrieve candidate results from a webset.
        
        Args:
            webset_id: The ID of the webset
            limit: Maximum number of candidates to retrieve
            include_content: Whether to include full content
            
        Returns:
            List of candidate items with their information
        """
        print(f"📋 Fetching candidates from webset {webset_id}...")
        
        try:
            items = self.exa.websets.items.list(
                webset_id=webset_id,
                limit=limit
            )
            
            candidates = []
            for item in items.data:
                candidate_data = {
                    "id": item.id,
                    "url": item.url,
                    "title": getattr(item, 'title', None),
                    "status": item.status,
                    "verification": getattr(item, 'verification', None),
                    "properties": getattr(item, 'properties', {}),
                    "enrichments": getattr(item, 'enrichments', [])
                }
                
                if include_content and hasattr(item, 'content'):
                    candidate_data['content'] = item.content
                    
                candidates.append(candidate_data)
            
            print(f"✅ Retrieved {len(candidates)} candidates")
            
            return candidates
            
        except Exception as e:
            print(f"❌ Error fetching candidates: {str(e)}")
            raise
    
    def search_and_wait(
        self,
        search_criteria: SearchCriteria,
        enrichments: Optional[List[EnrichmentConfig]] = None,
        external_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Convenience method to create a search and wait for results.
        
        This combines create_candidate_search, wait_for_results, and get_candidates
        into a single method for simpler usage.
        
        Args:
            search_criteria: What candidates you're looking for
            enrichments: Additional data to extract
            external_id: Your own identifier
            
        Returns:
            List of candidate results
        """
        # Create the webset
        webset_info = self.create_candidate_search(
            search_criteria=search_criteria,
            enrichments=enrichments,
            external_id=external_id
        )
        
        # Wait for completion
        self.wait_for_results(webset_info['id'])
        
        # Get and return results
        return self.get_candidates(webset_info['id'])
    
    def get_webset_status(self, webset_id: str) -> Dict[str, Any]:
        """
        Check the status of a webset.
        
        Args:
            webset_id: The ID of the webset
            
        Returns:
            Status information including progress
        """
        try:
            webset = self.exa.websets.get(webset_id)
            
            status_info = {
                "id": webset.id,
                "status": webset.status,
                "searches": []
            }
            
            # Get search progress if available
            if hasattr(webset, 'searches') and webset.searches:
                for search in webset.searches:
                    search_info = {
                        "id": search.id,
                        "status": search.status,
                        "query": search.query
                    }
                    
                    if hasattr(search, 'progress'):
                        search_info["progress"] = {
                            "found": search.progress.found,
                            "analyzed": search.progress.analyzed,
                            "completion": search.progress.completion,
                            "time_left": search.progress.timeLeft
                        }
                    
                    status_info["searches"].append(search_info)
            
            return status_info
            
        except Exception as e:
            print(f"❌ Error getting webset status: {str(e)}")
            raise
    
    def list_websets(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        List your recent websets.
        
        Args:
            limit: Maximum number of websets to return
            
        Returns:
            List of webset information
        """
        try:
            websets = self.exa.websets.list(limit=limit)
            
            result = []
            for webset in websets.data:
                result.append({
                    "id": webset.id,
                    "status": webset.status,
                    "external_id": getattr(webset, 'externalId', None),
                    "title": getattr(webset, 'title', None),
                    "created_at": getattr(webset, 'createdAt', None)
                })
            
            return result
            
        except Exception as e:
            print(f"❌ Error listing websets: {str(e)}")
            raise


# Example usage and templates
def example_ml_engineer_search():
    """Example: Finding ML Engineers at AI startups"""
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="Senior Machine Learning Engineers at AI startups",
        count=15,
        entity=EntityType.PERSON,
        criteria=[
            "Has 5+ years of experience in machine learning or AI",
            "Currently working at an AI-focused startup",
            "Has experience with deep learning frameworks like PyTorch or TensorFlow",
            "Located in United States"
        ]
    )
    
    enrichments = [
        EnrichmentConfig(
            description="Find their LinkedIn profile URL",
            format="text"
        ),
        EnrichmentConfig(
            description="Extract current company, role, and years of experience",
            format="text"
        ),
        EnrichmentConfig(
            description="Find their GitHub profile if available",
            format="text"
        ),
        EnrichmentConfig(
            description="List their technical skills and expertise areas",
            format="text"
        )
    ]
    
    results = finder.search_and_wait(
        search_criteria=criteria,
        enrichments=enrichments,
        external_id="ml-engineers-2024"
    )
    
    return results


def example_sales_leader_search():
    """Example: Finding Sales Leaders in SaaS"""
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="VP of Sales or Sales Directors at B2B SaaS companies",
        count=20,
        entity=EntityType.PERSON,
        criteria=[
            "Currently holds VP of Sales, Director of Sales, or Head of Sales title",
            "Works at a B2B SaaS company",
            "Has experience with enterprise sales",
            "Based in United States"
        ]
    )
    
    enrichments = [
        EnrichmentConfig(
            description="Find LinkedIn profile and contact information",
            format="text"
        ),
        EnrichmentConfig(
            description="Extract current company details and their product",
            format="text"
        ),
        EnrichmentConfig(
            description="Identify years in current role and total years in sales",
            format="text"
        )
    ]
    
    results = finder.search_and_wait(
        search_criteria=criteria,
        enrichments=enrichments,
        external_id="saas-sales-leaders"
    )
    
    return results


def example_phd_candidate_search():
    """Example: Finding PhD candidates for research positions"""
    finder = LinkedInCandidateFinder()
    
    criteria = SearchCriteria(
        query="PhD students or recent graduates in Computer Science focusing on NLP",
        count=10,
        entity=EntityType.PERSON,
        criteria=[
            "Currently pursuing or recently completed PhD in Computer Science or related field",
            "Research focus on Natural Language Processing, Computational Linguistics, or related areas",
            "Has publications in top-tier conferences (ACL, EMNLP, NeurIPS, etc.)",
            "Available or graduating within 6 months"
        ]
    )
    
    enrichments = [
        EnrichmentConfig(
            description="Find their academic homepage and LinkedIn profile",
            format="text"
        ),
        EnrichmentConfig(
            description="List their research topics and key publications",
            format="text"
        ),
        EnrichmentConfig(
            description="Extract their university and advisor information",
            format="text"
        ),
        EnrichmentConfig(
            description="Find their Google Scholar profile or publication count",
            format="text"
        )
    ]
    
    results = finder.search_and_wait(
        search_criteria=criteria,
        enrichments=enrichments,
        external_id="nlp-phd-candidates"
    )
    
    return results


if __name__ == "__main__":
    import sys
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║  LinkedIn Candidate Finder - Powered by Exa Websets API  ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check for API key
    if not os.getenv('EXA_API_KEY'):
        print("❌ Error: EXA_API_KEY environment variable not set")
        print("   Get your API key at: https://dashboard.exa.ai/api-keys")
        print("   Then set it: export EXA_API_KEY='your-key-here'")
        sys.exit(1)
    
    print("\n📚 Available Examples:")
    print("1. Find ML Engineers at AI startups")
    print("2. Find Sales Leaders in SaaS")
    print("3. Find PhD Candidates in NLP")
    print("4. Custom search")
    
    choice = input("\nSelect an example (1-4): ").strip()
    
    try:
        if choice == "1":
            print("\n" + "="*60)
            print("Example: Finding ML Engineers")
            print("="*60)
            results = example_ml_engineer_search()
            
        elif choice == "2":
            print("\n" + "="*60)
            print("Example: Finding Sales Leaders")
            print("="*60)
            results = example_sales_leader_search()
            
        elif choice == "3":
            print("\n" + "="*60)
            print("Example: Finding PhD Candidates")
            print("="*60)
            results = example_phd_candidate_search()
            
        elif choice == "4":
            print("\n" + "="*60)
            print("Custom Search")
            print("="*60)
            
            query = input("Enter your search query: ")
            count = int(input("How many candidates to find? (default 10): ") or "10")
            
            finder = LinkedInCandidateFinder()
            criteria = SearchCriteria(query=query, count=count)
            
            results = finder.search_and_wait(
                search_criteria=criteria,
                enrichments=[
                    EnrichmentConfig("Find their LinkedIn profile"),
                    EnrichmentConfig("Extract current role and company")
                ]
            )
        else:
            print("Invalid choice")
            sys.exit(1)
        
        # Display results
        print("\n" + "="*60)
        print(f"📊 Results Summary: Found {len(results)} candidates")
        print("="*60)
        
        for i, candidate in enumerate(results, 1):
            print(f"\n{i}. Candidate:")
            print(f"   URL: {candidate.get('url')}")
            print(f"   Status: {candidate.get('status')}")
            
            if candidate.get('properties'):
                print(f"   Properties: {json.dumps(candidate['properties'], indent=6)}")
            
            if candidate.get('enrichments'):
                print(f"   Enrichments: {len(candidate['enrichments'])} available")
        
        # Option to save results
        save = input("\n💾 Save results to file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"candidates_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Results saved to {filename}")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Search interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
