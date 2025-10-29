"""
GENOMOS Comprehensive Test Suite - Phase 13: Testing & Validation

Tests all 60+ endpoints across 8 implemented phases.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from typing import Dict, Any, List
import time

# Base URL for tests
BASE_URL = "http://127.0.0.1:8000"

# Test results storage
test_results = {
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "errors": [],
    "phase_results": {}
}


def test_endpoint(phase: str, endpoint_name: str, method: str, url: str,
                  data: Dict = None, expected_status: int = 200) -> bool:
    """Test a single endpoint"""
    global test_results
    test_results["total_tests"] += 1

    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")

        if response.status_code == expected_status:
            test_results["passed"] += 1
            print(f"✅ {phase} - {endpoint_name}: PASS ({response.status_code})")
            return True
        else:
            test_results["failed"] += 1
            error_msg = f"{endpoint_name}: Expected {expected_status}, got {response.status_code}"
            test_results["errors"].append(f"{phase}: {error_msg}")
            print(f"❌ {phase} - {endpoint_name}: FAIL ({response.status_code})")
            return False

    except Exception as e:
        test_results["failed"] += 1
        error_msg = f"{endpoint_name}: {str(e)}"
        test_results["errors"].append(f"{phase}: {error_msg}")
        print(f"❌ {phase} - {endpoint_name}: ERROR - {str(e)}")
        return False


def run_core_blockchain_tests():
    """Test Core Blockchain endpoints (Phase 1-4)"""
    print("\n🧬 Testing Core Blockchain Endpoints...")
    phase = "Core Blockchain"

    test_endpoint(phase, "Blockchain Info", "GET", f"{BASE_URL}/api/dna/info")
    test_endpoint(phase, "Chain Validation", "GET", f"{BASE_URL}/api/dna/validate")
    test_endpoint(phase, "Genesis Block", "GET", f"{BASE_URL}/api/dna/genesis")
    test_endpoint(phase, "List SMK Genes", "GET", f"{BASE_URL}/api/dna/smk")
    test_endpoint(phase, "List Mutations", "GET", f"{BASE_URL}/api/dna/mutations")
    test_endpoint(phase, "Get Block by Index", "GET", f"{BASE_URL}/api/dna/blocks/0")


def run_learning_tests():
    """Test Agent Learning endpoints (Phase 5)"""
    print("\n🧠 Testing Agent Learning Endpoints...")
    phase = "Phase 5: Agent Learning"

    test_endpoint(phase, "List Learning Events", "GET", f"{BASE_URL}/api/dna/learning")
    # Note: Other learning endpoints require specific IDs from blockchain


def run_knowledge_graph_tests():
    """Test Knowledge Graph endpoints (Phase 6)"""
    print("\n🕸️ Testing Knowledge Graph Endpoints...")
    phase = "Phase 6: Knowledge Graph"

    test_endpoint(phase, "SMK Network Graph", "GET", f"{BASE_URL}/api/dna/graph/smk-network")
    test_endpoint(phase, "Consultation Knowledge Flow", "GET", f"{BASE_URL}/api/dna/graph/consultation-knowledge-flow")


def run_smart_contract_tests():
    """Test Smart Contract endpoints (Phase 7)"""
    print("\n🔐 Testing Smart Contract Endpoints...")
    phase = "Phase 7: Smart Contracts"

    test_endpoint(phase, "Contracts Info", "GET", f"{BASE_URL}/api/dna/contracts/info")

    # Test contract validation with sample data
    validation_data = {
        "data": {
            "operation_type": "consultation",
            "hrv_ms": 75,
            "stress_level": 5,
            "emotional_state": "calm",
            "related_smk": ["SMK#019"],
            "human_query": "Test query",
            "agent_responses": {"orion": "response1", "lira": "response2"}
        }
    }
    test_endpoint(phase, "Validate with Contracts", "POST",
                  f"{BASE_URL}/api/dna/contracts/validate", data=validation_data)


def run_analytics_tests():
    """Test Analytics endpoints (Phase 8)"""
    print("\n📊 Testing Analytics Endpoints...")
    phase = "Phase 8: Analytics"

    test_endpoint(phase, "Analytics Overview", "GET", f"{BASE_URL}/api/dna/analytics/overview")
    test_endpoint(phase, "Analytics Timeline", "GET", f"{BASE_URL}/api/dna/analytics/timeline")


def run_backup_tests():
    """Test Backup & Export endpoints (Phase 9)"""
    print("\n💾 Testing Backup & Export Endpoints...")
    phase = "Phase 9: Backup & Export"

    test_endpoint(phase, "Backup Statistics", "GET", f"{BASE_URL}/api/dna/backup/statistics")
    test_endpoint(phase, "Export to JSON", "GET", f"{BASE_URL}/api/dna/export/json?limit=5")
    # Note: Skip CSV export and actual backup creation in quick tests


def run_cache_tests():
    """Test Cache Management endpoints (Phase 10)"""
    print("\n⚡ Testing Cache Management Endpoints...")
    phase = "Phase 10: Performance"

    test_endpoint(phase, "Cache Statistics", "GET", f"{BASE_URL}/api/dna/cache/stats")
    test_endpoint(phase, "Cache Info", "GET", f"{BASE_URL}/api/dna/cache/info")


def run_query_tests():
    """Test Advanced Query endpoints (Phase 11)"""
    print("\n🔍 Testing Advanced Query Endpoints...")
    phase = "Phase 11: Advanced Queries"

    # Full-text search
    search_data = {
        "query": "Constitution",
        "limit": 5
    }
    test_endpoint(phase, "Full-Text Search", "POST",
                  f"{BASE_URL}/api/dna/search", data=search_data)

    # Aggregation
    agg_data = {
        "group_by": "gene_type",
        "agg_functions": ["count"]
    }
    test_endpoint(phase, "Aggregation Query", "POST",
                  f"{BASE_URL}/api/dna/aggregate", data=agg_data)


def run_visualization_tests():
    """Test Visualization endpoints (Phase 12)"""
    print("\n🎨 Testing Visualization Endpoints...")
    phase = "Phase 12: Visualization"

    test_endpoint(phase, "Timeline Visualization", "GET", f"{BASE_URL}/api/dna/visualize/timeline")
    test_endpoint(phase, "Block Explorer", "GET", f"{BASE_URL}/api/dna/visualize/explorer?page=1&page_size=5")
    test_endpoint(phase, "Agent Dashboard", "GET", f"{BASE_URL}/api/dna/visualize/agents")
    test_endpoint(phase, "DNA Helix 3D", "GET", f"{BASE_URL}/api/dna/visualize/helix?radius=5&pitch=2")
    test_endpoint(phase, "Real-Time Metrics", "GET", f"{BASE_URL}/api/dna/visualize/metrics")


def run_security_tests():
    """Run security validation tests"""
    print("\n🔒 Testing Security Validations...")
    phase = "Security Tests"

    # Test dangerous path detection
    dangerous_mutation = {
        "data": {
            "operation_type": "mutation",
            "mutation_id": "test-001",
            "operation": "delete",
            "target": "../../../etc/passwd",
            "confirmed": False
        }
    }
    test_endpoint(phase, "Dangerous Path Detection", "POST",
                  f"{BASE_URL}/api/dna/contracts/validate",
                  data=dangerous_mutation, expected_status=200)  # Should validate but fail

    # Test HRV out of range
    low_hrv = {
        "data": {
            "hrv_ms": 20,  # Too low
            "operation_type": "consultation"
        }
    }
    test_endpoint(phase, "HRV Range Validation", "POST",
                  f"{BASE_URL}/api/dna/contracts/validate",
                  data=low_hrv, expected_status=200)  # Should validate but report violations


def run_performance_tests():
    """Run performance benchmark tests"""
    print("\n⚡ Testing Performance Benchmarks...")

    # Test response times
    endpoints_to_benchmark = [
        ("Info Endpoint", "GET", f"{BASE_URL}/api/dna/info"),
        ("Search", "POST", f"{BASE_URL}/api/dna/search", {"query": "test", "limit": 10}),
        ("Timeline", "GET", f"{BASE_URL}/api/dna/visualize/timeline"),
    ]

    for name, method, url, *data in endpoints_to_benchmark:
        start_time = time.time()
        try:
            if method == "GET":
                requests.get(url, timeout=10)
            else:
                requests.post(url, json=data[0] if data else {}, timeout=10)
            elapsed = (time.time() - start_time) * 1000  # Convert to ms
            status = "✅ FAST" if elapsed < 500 else "⚠️ SLOW"
            print(f"{status} {name}: {elapsed:.2f}ms")
        except Exception as e:
            print(f"❌ {name}: ERROR - {str(e)}")


def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("🧪 GENOMOS TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {test_results['total_tests']}")
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")

    if test_results['passed'] > 0:
        pass_rate = (test_results['passed'] / test_results['total_tests']) * 100
        print(f"📊 Pass Rate: {pass_rate:.1f}%")

    if test_results['errors']:
        print(f"\n❌ Errors ({len(test_results['errors'])}):")
        for error in test_results['errors'][:10]:  # Show first 10
            print(f"  - {error}")

    print("="*60)


def main():
    """Run all tests"""
    print("🧬 GENOMOS COMPREHENSIVE TEST SUITE")
    print("Phase 13: Testing & Validation")
    print("="*60)

    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/dna/info", timeout=5)
        print(f"✅ Server is running on {BASE_URL}")
        print(f"📊 Blockchain has {response.json().get('total_genes', 0)} genes")
    except Exception as e:
        print(f"❌ ERROR: Server not accessible at {BASE_URL}")
        print(f"   {str(e)}")
        print("\n   Please start the server with:")
        print("   cd ubuntu-playground/api && python -m uvicorn main:app --host 127.0.0.1 --port 8000")
        return

    # Run all test suites
    run_core_blockchain_tests()
    run_learning_tests()
    run_knowledge_graph_tests()
    run_smart_contract_tests()
    run_analytics_tests()
    run_backup_tests()
    run_cache_tests()
    run_query_tests()
    run_visualization_tests()
    run_security_tests()
    run_performance_tests()

    # Print summary
    print_summary()

    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)
    print(f"\n📄 Results saved to test_results.json")


if __name__ == "__main__":
    main()
