"""
Advanced utilities for LinkedIn Candidate Finder

This module provides additional functionality for:
- CSV import/export
- Batch processing
- Real-time monitoring
- Result filtering and deduplication
"""

import csv
import json
import time
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from linkedin_candidate_finder import LinkedInCandidateFinder, SearchCriteria, EnrichmentConfig


class CandidateExporter:
    """Export candidate results to various formats"""
    
    @staticmethod
    def to_csv(candidates: List[Dict[str, Any]], filename: str, fields: Optional[List[str]] = None):
        """
        Export candidates to CSV file.
        
        Args:
            candidates: List of candidate dictionaries
            filename: Output CSV filename
            fields: List of fields to include (default: all)
        """
        if not candidates:
            print("No candidates to export")
            return
        
        # Default fields if not specified
        if fields is None:
            fields = ['id', 'url', 'title', 'status']
            # Add property fields
            if candidates[0].get('properties'):
                for key in candidates[0]['properties'].keys():
                    fields.append(f'property_{key}')
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            
            for candidate in candidates:
                row = {}
                for field in fields:
                    if field.startswith('property_'):
                        prop_name = field.replace('property_', '')
                        row[field] = candidate.get('properties', {}).get(prop_name, '')
                    else:
                        row[field] = candidate.get(field, '')
                writer.writerow(row)
        
        print(f"✅ Exported {len(candidates)} candidates to {filename}")
    
    @staticmethod
    def to_json(candidates: List[Dict[str, Any]], filename: str, pretty: bool = True):
        """
        Export candidates to JSON file.
        
        Args:
            candidates: List of candidate dictionaries
            filename: Output JSON filename
            pretty: Whether to format JSON with indentation
        """
        with open(filename, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(candidates, f, indent=2, ensure_ascii=False)
            else:
                json.dump(candidates, f, ensure_ascii=False)
        
        print(f"✅ Exported {len(candidates)} candidates to {filename}")
    
    @staticmethod
    def to_markdown(candidates: List[Dict[str, Any]], filename: str):
        """
        Export candidates to Markdown file.
        
        Args:
            candidates: List of candidate dictionaries
            filename: Output Markdown filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Candidate Search Results\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"**Total Candidates:** {len(candidates)}\n\n")
            f.write("---\n\n")
            
            for i, candidate in enumerate(candidates, 1):
                f.write(f"## {i}. {candidate.get('title', 'Candidate')}\n\n")
                f.write(f"- **URL:** {candidate.get('url')}\n")
                f.write(f"- **Status:** {candidate.get('status')}\n")
                
                if candidate.get('properties'):
                    f.write(f"\n**Properties:**\n")
                    for key, value in candidate['properties'].items():
                        f.write(f"- {key}: {value}\n")
                
                if candidate.get('enrichments'):
                    f.write(f"\n**Enrichments:** {len(candidate['enrichments'])} available\n")
                
                f.write("\n---\n\n")
        
        print(f"✅ Exported {len(candidates)} candidates to {filename}")


class BatchSearchManager:
    """Manage multiple searches in batch"""
    
    def __init__(self, finder: LinkedInCandidateFinder):
        self.finder = finder
        self.searches = []
    
    def add_search(
        self,
        name: str,
        criteria: SearchCriteria,
        enrichments: Optional[List[EnrichmentConfig]] = None
    ):
        """
        Add a search to the batch.
        
        Args:
            name: Identifier for this search
            criteria: Search criteria
            enrichments: Enrichment configurations
        """
        self.searches.append({
            'name': name,
            'criteria': criteria,
            'enrichments': enrichments or [],
            'webset_id': None,
            'status': 'pending',
            'results': None
        })
        print(f"➕ Added search: {name}")
    
    def run_all(self, parallel: bool = False):
        """
        Execute all searches in the batch.
        
        Args:
            parallel: If True, start all searches at once. If False, run sequentially.
        """
        print(f"\n🚀 Starting {len(self.searches)} searches...")
        
        if parallel:
            # Start all searches
            for search in self.searches:
                print(f"\n📋 Starting: {search['name']}")
                webset_info = self.finder.create_candidate_search(
                    search_criteria=search['criteria'],
                    enrichments=search['enrichments'],
                    external_id=search['name']
                )
                search['webset_id'] = webset_info['id']
                search['status'] = 'running'
            
            # Wait for all to complete
            for search in self.searches:
                print(f"\n⏳ Waiting for: {search['name']}")
                self.finder.wait_for_results(search['webset_id'])
                search['results'] = self.finder.get_candidates(search['webset_id'])
                search['status'] = 'completed'
                print(f"✅ {search['name']}: Found {len(search['results'])} candidates")
        else:
            # Run sequentially
            for search in self.searches:
                print(f"\n📋 Processing: {search['name']}")
                search['results'] = self.finder.search_and_wait(
                    search_criteria=search['criteria'],
                    enrichments=search['enrichments'],
                    external_id=search['name']
                )
                search['status'] = 'completed'
                print(f"✅ {search['name']}: Found {len(search['results'])} candidates")
    
    def get_all_results(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get results from all searches as a dictionary"""
        return {
            search['name']: search['results']
            for search in self.searches
            if search['results'] is not None
        }
    
    def export_all(self, format: str = 'json', output_dir: str = '.'):
        """
        Export all search results.
        
        Args:
            format: 'json', 'csv', or 'markdown'
            output_dir: Directory to save files
        """
        exporter = CandidateExporter()
        
        for search in self.searches:
            if search['results']:
                filename = f"{output_dir}/{search['name']}.{format}"
                
                if format == 'json':
                    exporter.to_json(search['results'], filename)
                elif format == 'csv':
                    exporter.to_csv(search['results'], filename)
                elif format == 'markdown':
                    exporter.to_markdown(search['results'], filename)


class ProgressMonitor:
    """Monitor search progress with callbacks"""
    
    def __init__(self, finder: LinkedInCandidateFinder, webset_id: str):
        self.finder = finder
        self.webset_id = webset_id
        self.callbacks = []
    
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """
        Add a callback function to be called on progress updates.
        
        Args:
            callback: Function that accepts progress dict
        """
        self.callbacks.append(callback)
    
    def monitor(self, interval: int = 10, timeout: int = 3600):
        """
        Monitor search progress and call callbacks.
        
        Args:
            interval: Seconds between checks
            timeout: Maximum time to monitor
        """
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print("⚠️  Timeout reached")
                break
            
            status = self.finder.get_webset_status(self.webset_id)
            
            # Call all callbacks with status
            for callback in self.callbacks:
                try:
                    callback(status)
                except Exception as e:
                    print(f"Callback error: {e}")
            
            # Check if completed
            if status['status'] == 'idle':
                print("✅ Search completed!")
                break
            
            time.sleep(interval)


class CandidateFilter:
    """Filter and deduplicate candidate results"""
    
    @staticmethod
    def deduplicate(candidates: List[Dict[str, Any]], key: str = 'url') -> List[Dict[str, Any]]:
        """
        Remove duplicate candidates based on a key.
        
        Args:
            candidates: List of candidates
            key: Field to use for deduplication
        
        Returns:
            List of unique candidates
        """
        seen = set()
        unique = []
        
        for candidate in candidates:
            value = candidate.get(key)
            if value and value not in seen:
                seen.add(value)
                unique.append(candidate)
        
        print(f"🔍 Deduplicated: {len(candidates)} → {len(unique)} candidates")
        return unique
    
    @staticmethod
    def filter_by_status(
        candidates: List[Dict[str, Any]],
        status: str = 'completed'
    ) -> List[Dict[str, Any]]:
        """
        Filter candidates by status.
        
        Args:
            candidates: List of candidates
            status: Status to filter by
        
        Returns:
            Filtered list
        """
        filtered = [c for c in candidates if c.get('status') == status]
        print(f"🔍 Filtered by status '{status}': {len(filtered)} candidates")
        return filtered
    
    @staticmethod
    def filter_by_verification(
        candidates: List[Dict[str, Any]],
        passed: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Filter candidates by verification status.
        
        Args:
            candidates: List of candidates
            passed: If True, only return verified candidates
        
        Returns:
            Filtered list
        """
        filtered = [
            c for c in candidates
            if c.get('verification', {}).get('passed') == passed
        ]
        print(f"🔍 Filtered by verification: {len(filtered)} candidates")
        return filtered
    
    @staticmethod
    def filter_by_property(
        candidates: List[Dict[str, Any]],
        property_name: str,
        property_value: Any
    ) -> List[Dict[str, Any]]:
        """
        Filter candidates by a specific property value.
        
        Args:
            candidates: List of candidates
            property_name: Name of the property
            property_value: Value to match
        
        Returns:
            Filtered list
        """
        filtered = [
            c for c in candidates
            if c.get('properties', {}).get(property_name) == property_value
        ]
        print(f"🔍 Filtered by {property_name}={property_value}: {len(filtered)} candidates")
        return filtered


# Example usage functions

def example_batch_search():
    """Example of running multiple searches in batch"""
    finder = LinkedInCandidateFinder()
    batch = BatchSearchManager(finder)
    
    # Add multiple searches
    batch.add_search(
        name="senior-engineers",
        criteria=SearchCriteria(
            query="Senior Software Engineers in San Francisco",
            count=20
        ),
        enrichments=[
            EnrichmentConfig("Find LinkedIn profile"),
            EnrichmentConfig("Extract current company and role")
        ]
    )
    
    batch.add_search(
        name="product-managers",
        criteria=SearchCriteria(
            query="Product Managers at SaaS companies",
            count=15
        ),
        enrichments=[
            EnrichmentConfig("Find LinkedIn profile"),
            EnrichmentConfig("Extract years of experience")
        ]
    )
    
    batch.add_search(
        name="data-scientists",
        criteria=SearchCriteria(
            query="Data Scientists with ML experience",
            count=25
        ),
        enrichments=[
            EnrichmentConfig("Find LinkedIn and GitHub profiles"),
            EnrichmentConfig("List technical skills")
        ]
    )
    
    # Run all searches in parallel
    batch.run_all(parallel=True)
    
    # Export all results
    batch.export_all(format='json', output_dir='./results')
    batch.export_all(format='csv', output_dir='./results')
    
    return batch.get_all_results()


def example_progress_monitoring():
    """Example of monitoring search progress with callbacks"""
    finder = LinkedInCandidateFinder()
    
    # Create a search
    criteria = SearchCriteria(
        query="ML Engineers at AI startups",
        count=50
    )
    
    webset_info = finder.create_candidate_search(
        search_criteria=criteria,
        enrichments=[EnrichmentConfig("Find LinkedIn profile")]
    )
    
    # Set up progress monitoring
    monitor = ProgressMonitor(finder, webset_info['id'])
    
    # Add callback to print progress
    def print_progress(status):
        for search in status.get('searches', []):
            if 'progress' in search:
                p = search['progress']
                print(f"Progress: {p['completion']}% | "
                      f"Found: {p['found']} | "
                      f"Analyzed: {p['analyzed']} | "
                      f"Time left: {p['time_left']}s")
    
    monitor.add_callback(print_progress)
    
    # Monitor with 15-second intervals
    monitor.monitor(interval=15, timeout=3600)
    
    # Get final results
    return finder.get_candidates(webset_info['id'])


def example_filtering_and_export():
    """Example of filtering results and exporting to different formats"""
    finder = LinkedInCandidateFinder()
    
    # Run search
    criteria = SearchCriteria(
        query="Software Engineers in NYC",
        count=100
    )
    
    candidates = finder.search_and_wait(
        search_criteria=criteria,
        enrichments=[
            EnrichmentConfig("Find LinkedIn profile"),
            EnrichmentConfig("Extract current role")
        ]
    )
    
    # Apply filters
    candidates = CandidateFilter.deduplicate(candidates)
    candidates = CandidateFilter.filter_by_status(candidates, 'completed')
    candidates = CandidateFilter.filter_by_verification(candidates, passed=True)
    
    # Export to multiple formats
    exporter = CandidateExporter()
    exporter.to_json(candidates, 'candidates.json')
    exporter.to_csv(candidates, 'candidates.csv')
    exporter.to_markdown(candidates, 'candidates.md')
    
    return candidates


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║         LinkedIn Candidate Finder - Utilities            ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("\n📚 Available Examples:")
    print("1. Batch search - Run multiple searches")
    print("2. Progress monitoring - Real-time search tracking")
    print("3. Filtering and export - Process and export results")
    
    choice = input("\nSelect an example (1-3): ").strip()
    
    try:
        if choice == "1":
            print("\n" + "="*60)
            print("Batch Search Example")
            print("="*60)
            results = example_batch_search()
            print(f"\nCompleted {len(results)} searches!")
            
        elif choice == "2":
            print("\n" + "="*60)
            print("Progress Monitoring Example")
            print("="*60)
            results = example_progress_monitoring()
            print(f"\nFound {len(results)} candidates!")
            
        elif choice == "3":
            print("\n" + "="*60)
            print("Filtering and Export Example")
            print("="*60)
            results = example_filtering_and_export()
            print(f"\nProcessed {len(results)} candidates!")
            
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
