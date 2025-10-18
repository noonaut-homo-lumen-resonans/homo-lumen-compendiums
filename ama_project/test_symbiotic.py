"""
Simple test for SymbioticMCPArchitecture
"""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.symbiotic_mcp_architecture import SymbioticMCPArchitecture

async def test_symbiotic():
    """Test SymbioticMCPArchitecture"""
    
    print("🧠 Testing SymbioticMCPArchitecture...")
    
    # Initialize architecture
    arch = SymbioticMCPArchitecture()
    
    # Test biofelt validation
    biofelt = {"hrv_score": 75, "coherence": 0.7}
    result = await arch.process_with_biofelt_validation({"test": "data"}, biofelt)
    
    print(f"✅ Mode: {result['mode']}")
    print(f"✅ Active agents: {result['active_agents']}")
    print("🎉 SymbioticMCPArchitecture works!")

if __name__ == "__main__":
    asyncio.run(test_symbiotic()) 