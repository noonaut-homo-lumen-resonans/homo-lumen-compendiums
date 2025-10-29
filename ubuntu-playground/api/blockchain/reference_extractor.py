"""
Reference Extractor for GENOMOS Phase 6

Shared utility for extracting SMK references from any text content.
Used by SMK ingestion, consultations, and agent learning.
"""

import re
from typing import List, Dict, Set, Optional
from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType


def extract_smk_references(text: str) -> List[str]:
    """
    Extract SMK references from any text content.

    Matches patterns like:
    - SMK#032, SMK#32, SMK#003
    - SMK_032, SMK_32
    - SMK 032, SMK 32
    - [SMK#032]

    Args:
        text: Any string content to scan

    Returns:
        Sorted list of unique SMK numbers (zero-padded to 3 digits)
    """
    if not text:
        return []

    references = set()

    # Find patterns like SMK#032, SMK_032, SMK 032, etc.
    patterns = [
        r'SMK[#_\s]?(\d+)',
        r'\[SMK[#_\s]?(\d+)\]',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            smk_num = match.group(1)
            # Zero-pad to 3 digits for consistency
            smk_num_padded = smk_num.zfill(3)
            references.add(smk_num_padded)

    return sorted(list(references))


def extract_smk_references_from_consultation(consultation_data: Dict) -> List[str]:
    """
    Extract all SMK references from a consultation.

    Scans:
    - human_query
    - All agent_responses text
    - synthesis.summary
    - synthesis.key_insights

    Args:
        consultation_data: Dict with consultation fields

    Returns:
        Sorted list of unique SMK numbers found
    """
    all_text_parts = []

    # Human query
    if "human_query" in consultation_data:
        all_text_parts.append(consultation_data["human_query"])

    # Agent responses
    if "agent_responses" in consultation_data:
        for agent_name, response_data in consultation_data["agent_responses"].items():
            if isinstance(response_data, dict) and "response" in response_data:
                all_text_parts.append(response_data["response"])
            elif isinstance(response_data, str):
                all_text_parts.append(response_data)

    # Synthesis
    if "synthesis" in consultation_data:
        synthesis = consultation_data["synthesis"]
        if isinstance(synthesis, dict):
            if "summary" in synthesis:
                all_text_parts.append(synthesis["summary"])
            if "key_insights" in synthesis and isinstance(synthesis["key_insights"], list):
                all_text_parts.extend(synthesis["key_insights"])

    # Combine all text and extract references
    combined_text = " ".join(all_text_parts)
    return extract_smk_references(combined_text)


def validate_smk_references(
    smk_numbers: List[str],
    blockchain: Optional[AgentDNAChain] = None,
    db_path: str = "./data/genomos.db"
) -> Dict[str, any]:
    """
    Validate that SMK references exist in the blockchain.

    Args:
        smk_numbers: List of SMK numbers to validate
        blockchain: Optional pre-loaded blockchain instance
        db_path: Path to GENOMOS database if blockchain not provided

    Returns:
        Dict with:
        - valid: List of SMK numbers that exist
        - invalid: List of SMK numbers that don't exist
        - warnings: List of warning messages
    """
    if blockchain is None:
        blockchain = AgentDNAChain(db_path=db_path)

    # Get all SMK numbers in blockchain
    existing_smks = set()
    for block in blockchain.chain:
        if block.gene_type == GeneType.SMK:
            smk_num = block.data.get("smk_number")
            if smk_num:
                existing_smks.add(smk_num.zfill(3))

    valid = []
    invalid = []
    warnings = []

    for smk_num in smk_numbers:
        smk_padded = smk_num.zfill(3)
        if smk_padded in existing_smks:
            valid.append(smk_padded)
        else:
            invalid.append(smk_padded)
            # Try to suggest close matches
            close_matches = [
                s for s in existing_smks
                if abs(int(s) - int(smk_padded)) <= 5
            ]
            if close_matches:
                warnings.append(
                    f"SMK#{smk_padded} not found. Did you mean: {', '.join([f'SMK#{s}' for s in close_matches[:3]])}?"
                )
            else:
                warnings.append(f"SMK#{smk_padded} not found in blockchain")

    return {
        "valid": valid,
        "invalid": invalid,
        "warnings": warnings
    }


def merge_smk_references(*ref_lists: List[str]) -> List[str]:
    """
    Merge multiple SMK reference lists into one sorted unique list.

    Args:
        *ref_lists: Variable number of reference lists

    Returns:
        Sorted unique list of all SMK numbers
    """
    all_refs = set()
    for ref_list in ref_lists:
        if ref_list:
            all_refs.update(ref_list)
    return sorted(list(all_refs))
