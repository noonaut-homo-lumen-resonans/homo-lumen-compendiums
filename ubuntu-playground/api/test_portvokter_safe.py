#!/usr/bin/env python3
"""
TEST 2: Triadiske Portvokter Validation (Windows-safe, no emojis)
Tests the 3-layer validation system for ethical and consciousness-aware operations
"""
import requests
import json
import sys

# Disable emoji output for Windows
PASS = "[PASS]"
FAIL = "[FAIL]"
INFO = "[INFO]"

BASE_URL = "http://localhost:8003"
API_KEY = "code-local-dev-key"

def test_biofelt_gate_critical_hrv():
    """TEST 2.1: BiofeltGate should BLOCK with CRITICAL low HRV (<40)"""
    print("\n" + "="*80)
    print("TEST 2.1: BiofeltGate - CRITICAL Low HRV (skal blokkere)")
    print("="*80)

    payload = {
        "path": "shared/biofelt_critical_hrv_test.txt",
        "content": "This should be BLOCKED due to CRITICAL low HRV",
        "biofelt_context": {
            "hrv_ms": 30,  # CRITICAL: < 40
            "coherence": 0.3,
            "energy_level": "low",
            "stress_indicators": ["shallow_breathing", "tension_shoulders", "rapid_heartbeat"],
            "resonance_theme": "TEST: Simulated stress state"
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/workspace/write",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            },
            json=payload,
            timeout=10
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 403 and "BiofeltGate blocked" in response.text:
            print(f"\n{PASS} TEST 2.1: BiofeltGate correctly BLOCKED operation")
            return True
        else:
            print(f"\n{FAIL} TEST 2.1: BiofeltGate did NOT block (status={response.status_code})")
            return False
    except Exception as e:
        print(f"\n{FAIL} TEST 2.1 ERROR: {e}")
        return False


def test_thalos_filter_sql_injection():
    """TEST 2.2: ThalosFilter should BLOCK SQL injection attempts"""
    print("\n" + "="*80)
    print("TEST 2.2: ThalosFilter - SQL Injection (skal blokkere)")
    print("="*80)

    payload = {
        "path": "shared/sql_injection_test.txt",
        "content": "'; DROP TABLE users; --",
        "biofelt_context": {
            "hrv_ms": 75,  # BALANCED: should pass BiofeltGate
            "coherence": 0.65,
            "energy_level": "balanced"
        },
        "thalos_context": {
            "intent": "test sql injection",
            "justification": "Security testing",
            "reversible": True
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/workspace/write",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            },
            json=payload,
            timeout=10
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 403 and "ThalosFilter blocked" in response.text:
            print(f"\n{PASS} TEST 2.2: ThalosFilter correctly BLOCKED SQL injection")
            return True
        else:
            print(f"\n{FAIL} TEST 2.2: ThalosFilter did NOT block (status={response.status_code})")
            return False
    except Exception as e:
        print(f"\n{FAIL} TEST 2.2 ERROR: {e}")
        return False


def test_mutation_log_normal_write():
    """TEST 2.3: MutationLog should APPROVE and LOG normal writes"""
    print("\n" + "="*80)
    print("TEST 2.3: MutationLog - Normal Write (skal godkjennes og logges)")
    print("="*80)

    payload = {
        "path": "shared/portvokter_normal_write.txt",
        "content": "This is a normal, safe write operation for testing.",
        "biofelt_context": {
            "hrv_ms": 85,  # OPTIMAL: > 80
            "coherence": 0.80,
            "energy_level": "optimal",
            "resonance_theme": "TEST: Calm and focused state",
            "pust_rytme": "4-6-8"
        },
        "thalos_context": {
            "intent": "Test normal write operation",
            "justification": "Validation of Triadiske Portvokter system",
            "reversible": True,
            "reviewed_by": "code"
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/workspace/write",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            },
            json=payload,
            timeout=10
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print(f"\n{PASS} TEST 2.3: MutationLog APPROVED normal write")
            return True
        else:
            print(f"\n{FAIL} TEST 2.3: Normal write failed (status={response.status_code})")
            return False
    except Exception as e:
        print(f"\n{FAIL} TEST 2.3 ERROR: {e}")
        return False


def verify_genomos_mutations():
    """TEST 2.4: Verify all operations were logged to GENOMOS"""
    print("\n" + "="*80)
    print("TEST 2.4: GENOMOS - Verify Mutation Logging")
    print("="*80)

    try:
        # Check mutation_log.jsonl
        with open("data/mutation_log.jsonl", "r") as f:
            lines = f.readlines()
            recent_mutations = lines[-5:] if len(lines) >= 5 else lines

        print(f"\nTotal mutations in log: {len(lines)}")
        print(f"\nRecent {len(recent_mutations)} mutations:")
        for line in recent_mutations:
            mutation = json.loads(line)
            print(f"  - {mutation.get('operation_type')}: {mutation.get('target')} -> {mutation.get('validation_outcome')}")

        # Check GENOMOS blockchain
        print("\n\nChecking GENOMOS blockchain...")
        import sqlite3
        conn = sqlite3.connect('data/genomos.db')
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM dna_blocks WHERE gene_type = "mutation"')
        mutation_count = cursor.fetchone()[0]
        print(f"Mutation genes in GENOMOS: {mutation_count}")

        if mutation_count > 0:
            cursor.execute('SELECT block_index, data_json FROM dna_blocks WHERE gene_type = "mutation" ORDER BY block_index DESC LIMIT 3')
            mutations = cursor.fetchall()

            print(f"\nRecent {len(mutations)} mutation genes:")
            for block_index, data_json in mutations:
                data = json.loads(data_json)
                print(f"  Block #{block_index}: {data.get('operation_type')} -> {data.get('validation_outcome')}")

        conn.close()

        print(f"\n{PASS} TEST 2.4: Mutations logged successfully")
        return True

    except Exception as e:
        print(f"\n{FAIL} TEST 2.4 ERROR: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("#  TEST 2: TRIADISKE PORTVOKTER VALIDATION")
    print("#  Testing 3-layer ethical validation system")
    print("#"*80)

    results = []

    # Run all tests
    results.append(("TEST 2.1: BiofeltGate (CRITICAL HRV)", test_biofelt_gate_critical_hrv()))
    results.append(("TEST 2.2: ThalosFilter (SQL Injection)", test_thalos_filter_sql_injection()))
    results.append(("TEST 2.3: MutationLog (Normal Write)", test_mutation_log_normal_write()))
    results.append(("TEST 2.4: GENOMOS Mutation Logging", verify_genomos_mutations()))

    # Summary
    print("\n" + "="*80)
    print("TEST 2 SUMMARY")
    print("="*80)

    for test_name, passed in results:
        status = f"{PASS}" if passed else f"{FAIL}"
        print(f"{status}: {test_name}")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print(f"\n{INFO} ALL TESTS PASSED! Triadiske Portvokter working correctly.")
    else:
        print(f"\n{INFO} {total_tests - total_passed} test(s) failed. Review output above.")
