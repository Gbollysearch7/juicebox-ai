"""
Quick test script for the Juicebox AI Backend API
"""
import requests
import time
import json


def test_health_check():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("   Is the server running? Start it with: python run.py")
        return False


def test_create_search():
    """Test creating a search"""
    print("\n🔍 Testing Create Search...")

    search_request = {
        "query": "Senior Software Engineers with Python experience at tech companies",
        "count": 5,
        "entity": "person",
        "criteria": [
            "Has 3+ years of Python development experience",
            "Currently employed at a tech company"
        ],
        "enrichments": [
            "Find their LinkedIn profile",
            "Extract current company and role"
        ]
    }

    try:
        response = requests.post(
            "http://localhost:8000/api/v1/search",
            json=search_request
        )

        if response.status_code == 201:
            data = response.json()
            print("✅ Search created successfully!")
            print(f"   Search ID: {data['search_id']}")
            print(f"   Status: {data['status']}")
            return data['search_id']
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def test_get_search_status(search_id):
    """Test getting search status"""
    print(f"\n🔍 Testing Get Search Status (ID: {search_id})...")

    try:
        response = requests.get(f"http://localhost:8000/api/v1/search/{search_id}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Got search status!")
            print(f"   Status: {data['status']}")
            print(f"   Progress: {data['progress_percent']}%")
            print(f"   Found: {data['total_found']}/{data['total_requested']} candidates")
            return data
        else:
            print(f"❌ Failed with status {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def test_list_searches():
    """Test listing all searches"""
    print("\n🔍 Testing List All Searches...")

    try:
        response = requests.get("http://localhost:8000/api/v1/search")

        if response.status_code == 200:
            searches = response.json()
            print(f"✅ Found {len(searches)} search(es)")
            for search in searches:
                print(f"   - {search['search_id']}: {search['status']} ({search['total_found']} found)")
            return searches
        else:
            print(f"❌ Failed with status {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def test_get_candidates():
    """Test getting candidates"""
    print("\n🔍 Testing Get All Candidates...")

    try:
        response = requests.get("http://localhost:8000/api/v1/candidates")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total']} candidate(s)")
            for candidate in data['candidates'][:3]:  # Show first 3
                print(f"   - {candidate['properties'].get('name', 'Unknown')}")
                print(f"     Role: {candidate['properties'].get('current_role', 'N/A')}")
                print(f"     Score: {candidate.get('score', 'N/A')}")
            return data
        else:
            print(f"❌ Failed with status {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Juicebox AI Backend API Tests")
    print("=" * 60)

    # Test 1: Health check
    if not test_health_check():
        print("\n⚠️  Server is not running. Please start it first:")
        print("   cd backend && python run.py")
        return

    # Test 2: List existing searches
    test_list_searches()

    # Test 3: Create a new search (optional - requires Exa API key)
    print("\n" + "=" * 60)
    print("📝 Note: Creating a search requires a valid EXA_API_KEY in .env")
    print("=" * 60)

    create_search = input("\nDo you want to create a test search? (y/n): ").lower()

    if create_search == 'y':
        search_id = test_create_search()

        if search_id:
            # Test 4: Get search status
            time.sleep(2)  # Wait a bit
            test_get_search_status(search_id)

            # Test 5: Get candidates
            test_get_candidates()

    print("\n" + "=" * 60)
    print("✅ Tests complete!")
    print("=" * 60)
    print("\n📚 Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    main()
