"""
Consultation Recommender for GENOMOS Phase 6

Finds similar consultations based on:
- Shared SMK references
- Query text similarity
- Agent involvement overlap
- Temporal proximity
"""

from typing import List, Dict, Tuple, Set
from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType
from models.knowledge_graph import ConsultationSimilarity


class ConsultationRecommender:
    """
    Recommendation engine for finding related consultations.
    """

    def __init__(self, blockchain: AgentDNAChain = None, db_path: str = "./data/genomos.db"):
        """
        Initialize recommender with blockchain access.

        Args:
            blockchain: Pre-loaded blockchain instance (optional)
            db_path: Path to GENOMOS database if blockchain not provided
        """
        if blockchain is None:
            blockchain = AgentDNAChain(db_path=db_path)
        self.blockchain = blockchain

    def find_similar_consultations(
        self,
        consultation_id: str,
        limit: int = 10,
        min_score: float = 0.1
    ) -> List[ConsultationSimilarity]:
        """
        Find consultations similar to the given one.

        Args:
            consultation_id: ID of the consultation to find similar ones for
            limit: Maximum number of recommendations to return
            min_score: Minimum similarity score threshold (0-1)

        Returns:
            List of ConsultationSimilarity objects, sorted by score (highest first)
        """
        # Find the target consultation
        target_consultation = self._get_consultation(consultation_id)
        if not target_consultation:
            return []

        # Get all other consultations
        all_consultations = self._get_all_consultations()

        # Calculate similarity scores
        similarities = []
        for other_consultation in all_consultations:
            other_id = other_consultation["data"].get("consultation_id")

            # Skip self
            if other_id == consultation_id:
                continue

            # Calculate similarity
            score, shared_smk, shared_agents, reason = self._calculate_similarity(
                target_consultation["data"],
                other_consultation["data"]
            )

            if score >= min_score:
                similarities.append(ConsultationSimilarity(
                    consultation_id=other_id,
                    similarity_score=score,
                    shared_smk=shared_smk,
                    shared_agents=shared_agents,
                    reason=reason,
                    consultation_summary=other_consultation["data"].get("human_query", "")[:100],
                    timestamp=other_consultation["timestamp"]
                ))

        # Sort by score (descending) and apply limit
        similarities.sort(key=lambda x: x.similarity_score, reverse=True)
        return similarities[:limit]

    def _get_consultation(self, consultation_id: str) -> Dict:
        """Get a specific consultation from blockchain."""
        for block in self.blockchain.chain:
            if block.gene_type == GeneType.CONSULTATION:
                if block.data.get("consultation_id") == consultation_id:
                    return {
                        "data": block.data,
                        "timestamp": block.timestamp,
                        "block_index": block.index
                    }
        return None

    def _get_all_consultations(self) -> List[Dict]:
        """Get all consultations from blockchain."""
        consultations = []
        for block in self.blockchain.chain:
            if block.gene_type == GeneType.CONSULTATION:
                consultations.append({
                    "data": block.data,
                    "timestamp": block.timestamp,
                    "block_index": block.index
                })
        return consultations

    def _calculate_similarity(
        self,
        consultation1: Dict,
        consultation2: Dict
    ) -> Tuple[float, List[str], List[str], str]:
        """
        Calculate similarity between two consultations.

        Args:
            consultation1: First consultation data
            consultation2: Second consultation data

        Returns:
            Tuple of (score, shared_smk, shared_agents, reason)
        """
        score = 0.0
        reason_parts = []

        # 1. SMK Reference Overlap (weight: 0.6)
        smk1 = set(self._extract_smk_numbers(consultation1.get("synthesis", {}).get("related_smk", [])))
        smk2 = set(self._extract_smk_numbers(consultation2.get("synthesis", {}).get("related_smk", [])))
        shared_smk = list(smk1 & smk2)

        if shared_smk:
            smk_score = len(shared_smk) / max(len(smk1), len(smk2), 1)
            score += smk_score * 0.6
            reason_parts.append(f"{len(shared_smk)} shared SMK reference(s)")

        # 2. Agent Overlap (weight: 0.2)
        agents1 = set(consultation1.get("agent_responses", {}).keys())
        agents2 = set(consultation2.get("agent_responses", {}).keys())
        shared_agents = list(agents1 & agents2)

        if shared_agents:
            agent_score = len(shared_agents) / max(len(agents1), len(agents2), 1)
            score += agent_score * 0.2
            reason_parts.append(f"{len(shared_agents)} shared agent(s)")

        # 3. Query Text Similarity (weight: 0.2) - Simple word overlap
        query1_words = set(self._tokenize(consultation1.get("human_query", "")))
        query2_words = set(self._tokenize(consultation2.get("human_query", "")))

        if query1_words and query2_words:
            shared_words = query1_words & query2_words
            # Jaccard similarity
            text_score = len(shared_words) / len(query1_words | query2_words)
            if text_score > 0.2:  # Only count if significant overlap
                score += text_score * 0.2
                reason_parts.append(f"similar query topics")

        # Build human-readable reason
        if not reason_parts:
            reason = "Low similarity"
        else:
            reason = ", ".join(reason_parts)

        return (score, shared_smk, shared_agents, reason)

    @staticmethod
    def _extract_smk_numbers(smk_list: List[str]) -> List[str]:
        """
        Extract SMK numbers from references like "SMK#043" -> "043".
        """
        numbers = []
        for smk_ref in smk_list:
            # Extract digits
            import re
            match = re.search(r'(\d+)', smk_ref)
            if match:
                numbers.append(match.group(1).zfill(3))
        return numbers

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        """
        Simple word tokenization for text similarity.

        Lowercases, removes punctuation, and splits on whitespace.
        """
        import re
        # Lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        # Split and filter out short words
        words = [w for w in text.split() if len(w) > 3]
        return set(words)


def find_related_consultations(
    consultation_id: str,
    blockchain: AgentDNAChain = None,
    limit: int = 10,
    min_score: float = 0.1
) -> List[ConsultationSimilarity]:
    """
    Convenience function to find related consultations.

    Args:
        consultation_id: ID of consultation to find relations for
        blockchain: Optional pre-loaded blockchain
        limit: Max number of results
        min_score: Minimum similarity threshold

    Returns:
        List of similar consultations
    """
    recommender = ConsultationRecommender(blockchain=blockchain)
    return recommender.find_similar_consultations(
        consultation_id=consultation_id,
        limit=limit,
        min_score=min_score
    )
