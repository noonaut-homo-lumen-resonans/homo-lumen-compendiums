"""
Pattern Analyzer for GENOMOS

Detects recurring patterns in blockchain data:
1. SMK Co-occurrence patterns
2. Agent collaboration patterns
3. Temporal patterns (time-based)
4. Topic clustering (consultation similarity)

Philosophy: "The genome learns from its own history"
"""

from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from itertools import combinations
import logging
import re

# NLP libraries for topic clustering
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import KMeans
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. Topic clustering will be limited.")

logger = logging.getLogger(__name__)


class PatternAnalyzer:
    """
    Analyzer for detecting patterns in GENOMOS blockchain.

    Features:
    - SMK co-occurrence detection
    - Agent collaboration analysis
    - Temporal pattern recognition
    - Topic clustering (TF-IDF + K-means)
    """

    def __init__(self, blockchain):
        """
        Initialize Pattern Analyzer.

        Args:
            blockchain: AgentDNAChain instance
        """
        self.blockchain = blockchain
        self.patterns_detected: List[Dict[str, Any]] = []

    def analyze_all(
        self,
        min_confidence: float = 0.5,
        lookback_days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Run all pattern detection algorithms.

        Args:
            min_confidence: Minimum confidence threshold (0.0-1.0)
            lookback_days: Analyze last N days of data

        Returns:
            List of detected patterns
        """
        patterns = []

        logger.info(f"🔍 Starting pattern analysis (lookback: {lookback_days} days)...")

        # Algorithm 1: SMK Co-occurrence
        smk_patterns = self.detect_smk_patterns(min_confidence)
        patterns.extend(smk_patterns)
        logger.info(f"✅ SMK patterns: {len(smk_patterns)} detected")

        # Algorithm 2: Agent Collaboration
        agent_patterns = self.detect_agent_patterns(min_confidence)
        patterns.extend(agent_patterns)
        logger.info(f"✅ Agent patterns: {len(agent_patterns)} detected")

        # Algorithm 3: Temporal Patterns
        temporal_patterns = self.detect_temporal_patterns(lookback_days)
        patterns.extend(temporal_patterns)
        logger.info(f"✅ Temporal patterns: {len(temporal_patterns)} detected")

        # Algorithm 4: Topic Clusters
        if SKLEARN_AVAILABLE:
            topic_patterns = self.detect_topic_clusters(min_confidence)
            patterns.extend(topic_patterns)
            logger.info(f"✅ Topic clusters: {len(topic_patterns)} detected")
        else:
            logger.warning("⚠️ Topic clustering skipped (scikit-learn not available)")

        self.patterns_detected = patterns
        logger.info(f"🎯 Total patterns detected: {len(patterns)}")

        return patterns

    def detect_smk_patterns(self, min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """
        Algorithm 1: Detect SMK co-occurrence patterns.

        Finds SMK pairs/triples that appear together frequently in consultations.

        Args:
            min_confidence: Minimum confidence threshold

        Returns:
            List of SMK patterns
        """
        patterns = []

        try:
            # Get all consultations
            consultations = self.blockchain.get_genes_by_type("consultation")
            if not consultations:
                return patterns

            # Extract SMK references from each consultation
            smk_sets = []
            for consultation in consultations:
                data = consultation.data
                smk_refs = data.get("related_smk", [])
                if len(smk_refs) >= 2:  # Need at least 2 SMKs for pattern
                    smk_sets.append(set(smk_refs))

            if len(smk_sets) < 3:  # Need enough data
                return patterns

            # Count SMK pair co-occurrences
            pair_counts = Counter()
            for smk_set in smk_sets:
                for pair in combinations(sorted(smk_set), 2):
                    pair_counts[pair] += 1

            # Calculate confidence scores
            total_consultations = len(smk_sets)
            for (smk1, smk2), count in pair_counts.items():
                confidence = count / total_consultations

                if confidence >= min_confidence:
                    patterns.append({
                        "pattern_id": f"SMK_PAIR_{smk1}_{smk2}",
                        "pattern_type": "smk_combination",
                        "description": f"{smk1} and {smk2} frequently appear together",
                        "confidence": round(confidence, 3),
                        "data": {
                            "smk1": smk1,
                            "smk2": smk2,
                            "occurrences": count,
                            "total_consultations": total_consultations,
                            "percentage": round(confidence * 100, 1)
                        },
                        "discovered_at": datetime.now().isoformat()
                    })

        except Exception as e:
            logger.error(f"❌ SMK pattern detection failed: {e}")

        return patterns

    def detect_agent_patterns(self, min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """
        Algorithm 2: Detect agent collaboration patterns.

        Finds agent combinations that work together frequently.

        Args:
            min_confidence: Minimum confidence threshold

        Returns:
            List of agent collaboration patterns
        """
        patterns = []

        try:
            # Get all consultations
            consultations = self.blockchain.get_genes_by_type("consultation")
            if not consultations:
                return patterns

            # Extract agent combinations
            agent_sets = []
            for consultation in consultations:
                data = consultation.data
                agents = data.get("agents", [])
                if len(agents) >= 2:
                    agent_sets.append(set(agents))

            if len(agent_sets) < 3:
                return patterns

            # Count agent pair co-occurrences
            pair_counts = Counter()
            for agent_set in agent_sets:
                for pair in combinations(sorted(agent_set), 2):
                    pair_counts[pair] += 1

            # Calculate confidence
            total_consultations = len(agent_sets)
            for (agent1, agent2), count in pair_counts.items():
                confidence = count / total_consultations

                if confidence >= min_confidence:
                    patterns.append({
                        "pattern_id": f"AGENT_COLLAB_{agent1}_{agent2}",
                        "pattern_type": "agent_collaboration",
                        "description": f"{agent1} and {agent2} frequently collaborate",
                        "confidence": round(confidence, 3),
                        "data": {
                            "agent1": agent1,
                            "agent2": agent2,
                            "collaborations": count,
                            "total_consultations": total_consultations,
                            "percentage": round(confidence * 100, 1)
                        },
                        "discovered_at": datetime.now().isoformat()
                    })

        except Exception as e:
            logger.error(f"❌ Agent pattern detection failed: {e}")

        return patterns

    def detect_temporal_patterns(self, lookback_days: int = 30) -> List[Dict[str, Any]]:
        """
        Algorithm 3: Detect temporal patterns.

        Analyzes activity by hour-of-day and day-of-week.

        Args:
            lookback_days: Analyze last N days

        Returns:
            List of temporal patterns
        """
        patterns = []

        try:
            # Get all blocks from last N days
            cutoff_date = datetime.now() - timedelta(days=lookback_days)

            all_blocks = self.blockchain.get_all_blocks()
            recent_blocks = [
                b for b in all_blocks
                if datetime.fromisoformat(b.timestamp) > cutoff_date
            ]

            if len(recent_blocks) < 10:  # Need enough data
                return patterns

            # Analyze by hour of day
            hour_counts = Counter()
            day_counts = Counter()

            for block in recent_blocks:
                dt = datetime.fromisoformat(block.timestamp)
                hour_counts[dt.hour] += 1
                day_counts[dt.strftime("%A")] += 1  # Monday, Tuesday, etc.

            # Find peak hours (top 3)
            total_blocks = len(recent_blocks)
            top_hours = hour_counts.most_common(3)

            for hour, count in top_hours:
                percentage = (count / total_blocks) * 100
                if percentage >= 15:  # At least 15% of activity
                    patterns.append({
                        "pattern_id": f"TEMPORAL_HOUR_{hour}",
                        "pattern_type": "temporal_activity",
                        "description": f"Peak activity at {hour:02d}:00 ({percentage:.1f}%)",
                        "confidence": round(percentage / 100, 3),
                        "data": {
                            "hour": hour,
                            "count": count,
                            "total_blocks": total_blocks,
                            "percentage": round(percentage, 1)
                        },
                        "discovered_at": datetime.now().isoformat()
                    })

            # Find peak days (top 2)
            top_days = day_counts.most_common(2)

            for day, count in top_days:
                percentage = (count / total_blocks) * 100
                if percentage >= 20:  # At least 20% of activity
                    patterns.append({
                        "pattern_id": f"TEMPORAL_DAY_{day}",
                        "pattern_type": "temporal_activity",
                        "description": f"Peak activity on {day} ({percentage:.1f}%)",
                        "confidence": round(percentage / 100, 3),
                        "data": {
                            "day": day,
                            "count": count,
                            "total_blocks": total_blocks,
                            "percentage": round(percentage, 1)
                        },
                        "discovered_at": datetime.now().isoformat()
                    })

        except Exception as e:
            logger.error(f"❌ Temporal pattern detection failed: {e}")

        return patterns

    def detect_topic_clusters(
        self,
        min_confidence: float = 0.5,
        n_clusters: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Algorithm 4: Detect topic clusters using TF-IDF + K-means.

        Groups similar consultations by content.

        Args:
            min_confidence: Minimum similarity threshold
            n_clusters: Number of clusters to create

        Returns:
            List of topic cluster patterns
        """
        patterns = []

        if not SKLEARN_AVAILABLE:
            return patterns

        try:
            # Get all consultations
            consultations = self.blockchain.get_genes_by_type("consultation")
            if len(consultations) < n_clusters * 2:  # Need enough data
                return patterns

            # Extract questions
            questions = []
            consultation_ids = []
            for consultation in consultations:
                data = consultation.data
                question = data.get("human_query", "")
                if question:
                    questions.append(question)
                    consultation_ids.append(data.get("consultation_id", f"CONS_{consultation.index}"))

            if len(questions) < n_clusters * 2:
                return patterns

            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(questions)

            # K-means clustering
            kmeans = KMeans(n_clusters=min(n_clusters, len(questions)), random_state=42)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)

            # Analyze clusters
            clusters = defaultdict(list)
            for idx, label in enumerate(cluster_labels):
                clusters[label].append(idx)

            # Create pattern for each cluster
            for cluster_id, indices in clusters.items():
                if len(indices) >= 2:  # Cluster must have at least 2 consultations
                    # Calculate average similarity within cluster
                    cluster_vectors = tfidf_matrix[indices]
                    similarities = cosine_similarity(cluster_vectors)
                    avg_similarity = np.mean(similarities[np.triu_indices_from(similarities, k=1)])

                    if avg_similarity >= min_confidence:
                        # Get sample consultation IDs
                        sample_ids = [consultation_ids[i] for i in indices[:3]]

                        patterns.append({
                            "pattern_id": f"TOPIC_CLUSTER_{cluster_id}",
                            "pattern_type": "topic_cluster",
                            "description": f"Topic cluster with {len(indices)} similar consultations",
                            "confidence": round(float(avg_similarity), 3),
                            "data": {
                                "cluster_id": int(cluster_id),
                                "consultation_count": len(indices),
                                "avg_similarity": round(float(avg_similarity), 3),
                                "sample_consultations": sample_ids
                            },
                            "discovered_at": datetime.now().isoformat()
                        })

        except Exception as e:
            logger.error(f"❌ Topic clustering failed: {e}")

        return patterns

    def calculate_confidence(self, pattern_data: Dict[str, Any]) -> float:
        """
        Calculate confidence score for a pattern.

        Based on:
        - Sample size (more data = higher confidence)
        - Consistency (regularity of occurrence)
        - Recency (recent patterns weighted higher)

        Args:
            pattern_data: Pattern data dict

        Returns:
            Confidence score (0.0 - 1.0)
        """
        # Base confidence from pattern
        base_confidence = pattern_data.get("confidence", 0.5)

        # Sample size factor
        sample_size = pattern_data.get("data", {}).get("count", 0)
        size_factor = min(sample_size / 10, 1.0)  # Max at 10+ samples

        # Combine factors
        confidence = (base_confidence * 0.7) + (size_factor * 0.3)

        return round(confidence, 3)