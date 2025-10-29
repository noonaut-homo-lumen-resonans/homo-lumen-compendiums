"""
AMA Status Check
Simple check to verify AMA implementation status
"""

import os
import json
from datetime import datetime

def check_ama_status():
    """Check the status of AMA implementation"""
    
    print("🧠 AMA Implementation Status Check")
    print("=" * 60)
    
    # Check core files
    core_files = [
        "src/core/comprehensive_mcp_architecture.py",
        "src/core/agent_coordination_hub.py", 
        "src/core/polycomputational_engine.py",
        "src/core/lira_biofelt_tools.py",
        "src/core/ama_fire_layers.py",
        "src/core/biofelt_responsive.py",
        "src/core/mcp_connector.py"
    ]
    
    print("📁 Core Files:")
    core_status = {}
    for file_path in core_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file_path} ({size:,} bytes)")
            core_status[file_path] = {"exists": True, "size": size}
        else:
            print(f"   ❌ {file_path} - MISSING")
            core_status[file_path] = {"exists": False, "size": 0}
    
    # Check test files
    test_files = [
        "simple_ama_test.py",
        "test_ama_implementation.py"
    ]
    
    print("\n🧪 Test Files:")
    test_status = {}
    for file_path in test_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file_path} ({size:,} bytes)")
            test_status[file_path] = {"exists": True, "size": size}
        else:
            print(f"   ❌ {file_path} - MISSING")
            test_status[file_path] = {"exists": False, "size": 0}
    
    # Check requirements
    print("\n📦 Dependencies:")
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print(f"   ✅ {requirements_file} exists")
        with open(requirements_file, 'r') as f:
            requirements = f.read()
            print(f"   📋 {len(requirements.splitlines())} dependencies listed")
    else:
        print(f"   ❌ {requirements_file} - MISSING")
    
    # Summary
    print("\n📊 Summary:")
    total_files = len(core_files) + len(test_files)
    existing_files = sum(1 for status in core_status.values() if status["exists"]) + \
                    sum(1 for status in test_status.values() if status["exists"])
    
    print(f"   📁 Files: {existing_files}/{total_files} present")
    print(f"   🧠 Core Components: {sum(1 for status in core_status.values() if status['exists'])}/{len(core_files)}")
    print(f"   🧪 Tests: {sum(1 for status in test_status.values() if status['exists'])}/{len(test_files)}")
    
    # Implementation status
    if existing_files >= total_files - 1:  # Allow 1 missing file
        print("\n🎉 AMA Implementation Status: READY")
        print("\n📋 Next Steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run test: python simple_ama_test.py")
        print("   3. Start server: python -m uvicorn src.core.comprehensive_mcp_architecture:app --reload")
        print("   4. Test API: http://localhost:8000/docs")
    else:
        print("\n⚠️  AMA Implementation Status: INCOMPLETE")
        print("   Some core files are missing. Check the list above.")
    
    # Save status report
    status_report = {
        "timestamp": datetime.now().isoformat(),
        "core_files": core_status,
        "test_files": test_status,
        "total_files": total_files,
        "existing_files": existing_files,
        "ready": existing_files >= total_files - 1
    }
    
    with open("ama_status_report.json", "w") as f:
        json.dump(status_report, f, indent=2)
    
    print(f"\n📄 Status report saved to: ama_status_report.json")
    
    return status_report

if __name__ == "__main__":
    check_ama_status() 