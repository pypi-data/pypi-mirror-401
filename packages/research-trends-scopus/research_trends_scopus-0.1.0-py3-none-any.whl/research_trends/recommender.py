"""
Recommendation engine for Research Trends.

Analyzes publication data to recommend:
- Underexplored research areas
- Emerging topics
- Potential collaborations
- High-impact venues
"""

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from research_trends.models import Publication, Recommendation, TrendData
from research_trends.analyzer import TrendAnalyzer


class Recommender:
    """Generates research recommendations based on publication analysis.
    
    Analyzes trends and patterns in publication data to identify:
    - Research gaps and underexplored areas
    - Emerging topics with growth potential
    - Collaboration opportunities
    - Optimal publication venues
    
    Example:
        >>> recommender = Recommender(analyzer)
        >>> recommendations = recommender.get_recommendations(top_n=10)
    """
    
    def __init__(self, analyzer: TrendAnalyzer) -> None:
        """Initialize the recommender.
        
        Args:
            analyzer: TrendAnalyzer instance with analyzed data.
        """
        self.analyzer = analyzer
        self.trends = analyzer.analyze()
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._tfidf_matrix: Optional[np.ndarray] = None
    
    def get_recommendations(
        self,
        top_n: int = 10,
        include_categories: Optional[List[str]] = None,
    ) -> List[Recommendation]:
        """Get comprehensive research recommendations.
        
        Args:
            top_n: Maximum number of recommendations per category.
            include_categories: Categories to include. Options:
                - 'emerging_topics'
                - 'research_gaps'
                - 'collaborations'
                - 'venues'
                If None, includes all categories.
                
        Returns:
            List of Recommendation objects sorted by score.
        """
        categories = include_categories or [
            'emerging_topics',
            'research_gaps',
            'collaborations',
            'venues',
        ]
        
        recommendations: List[Recommendation] = []
        
        if 'emerging_topics' in categories:
            recommendations.extend(self._recommend_emerging_topics(top_n))
        
        if 'research_gaps' in categories:
            recommendations.extend(self._recommend_research_gaps(top_n))
        
        if 'collaborations' in categories:
            recommendations.extend(self._recommend_collaborations(top_n))
        
        if 'venues' in categories:
            recommendations.extend(self._recommend_venues(top_n))
        
        # Sort by score
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        return recommendations
    
    def _recommend_emerging_topics(self, top_n: int) -> List[Recommendation]:
        """Recommend emerging research topics.
        
        Identifies topics showing rapid growth in recent years.
        """
        recommendations = []
        emerging = self.analyzer.get_emerging_keywords(recent_years=2, min_count=3)
        
        for keyword, growth_score in emerging[:top_n]:
            # Normalize growth score to 0-1 range
            normalized_score = min(1.0, growth_score / 10)
            
            rec = Recommendation(
                title=f"Emerging: {keyword.title()}",
                description=(
                    f"'{keyword}' is an emerging topic with significant recent growth. "
                    f"Publications mentioning this keyword have increased substantially."
                ),
                category="emerging_topics",
                score=normalized_score,
                keywords=[keyword],
                rationale=(
                    f"Growth score: {growth_score:.1f}x increase in recent years. "
                    "Early research in emerging areas often receives higher visibility."
                ),
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _recommend_research_gaps(self, top_n: int) -> List[Recommendation]:
        """Recommend underexplored research areas.
        
        Identifies keyword combinations that are underrepresented
        despite being related to popular topics.
        """
        recommendations = []
        
        # Get keyword co-occurrence
        keyword_pairs = self._get_keyword_cooccurrence()
        top_keywords = dict(self.analyzer.get_top_keywords(50))
        
        # Find pairs of popular keywords that rarely appear together
        gaps = []
        
        keywords_list = list(top_keywords.keys())
        for i, kw1 in enumerate(keywords_list):
            for kw2 in keywords_list[i + 1:]:
                pair = tuple(sorted([kw1, kw2]))
                cooccurrence = keyword_pairs.get(pair, 0)
                
                # Both keywords are popular but rarely co-occur
                expected = min(top_keywords[kw1], top_keywords[kw2]) * 0.1
                if cooccurrence < expected and cooccurrence < 3:
                    gap_score = (top_keywords[kw1] + top_keywords[kw2]) / 2
                    gaps.append((pair, gap_score))
        
        # Sort by gap potential
        gaps.sort(key=lambda x: x[1], reverse=True)
        
        for (kw1, kw2), score in gaps[:top_n]:
            normalized_score = min(1.0, score / 50)
            
            rec = Recommendation(
                title=f"Gap: {kw1.title()} + {kw2.title()}",
                description=(
                    f"The intersection of '{kw1}' and '{kw2}' appears underexplored. "
                    f"Both topics are well-studied individually but rarely combined."
                ),
                category="research_gaps",
                score=normalized_score,
                keywords=[kw1, kw2],
                rationale=(
                    "Combining established research areas often leads to novel insights. "
                    "This gap represents an opportunity for interdisciplinary research."
                ),
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _recommend_collaborations(self, top_n: int) -> List[Recommendation]:
        """Recommend potential collaboration opportunities.
        
        Identifies authors and institutions working on similar topics
        but not yet collaborating.
        """
        recommendations = []
        
        # Get author topic profiles
        author_keywords = self._get_author_keywords()
        
        # Find authors with similar interests who haven't collaborated
        network = self.analyzer.get_coauthorship_network()
        existing_collaborations = {
            tuple(sorted([e.source, e.target]))
            for e in network.edges
        }
        
        # Calculate author similarity
        authors = list(author_keywords.keys())
        
        if len(authors) < 2:
            return recommendations
        
        potential_collabs = []
        
        for i, author1 in enumerate(authors[:100]):  # Limit for performance
            for author2 in authors[i + 1:100]:
                pair = tuple(sorted([author1, author2]))
                
                if pair not in existing_collaborations:
                    # Calculate keyword overlap
                    kw1 = set(author_keywords[author1])
                    kw2 = set(author_keywords[author2])
                    
                    if kw1 and kw2:
                        overlap = len(kw1 & kw2)
                        union = len(kw1 | kw2)
                        similarity = overlap / union if union > 0 else 0
                        
                        if similarity > 0.2:  # Threshold
                            common = list(kw1 & kw2)[:5]
                            potential_collabs.append((author1, author2, similarity, common))
        
        # Sort by similarity
        potential_collabs.sort(key=lambda x: x[2], reverse=True)
        
        for author1, author2, sim, common_kw in potential_collabs[:top_n]:
            rec = Recommendation(
                title=f"Collaborate: {author1.split()[-1]} & {author2.split()[-1]}",
                description=(
                    f"{author1} and {author2} work on similar topics but haven't "
                    f"collaborated. Common interests: {', '.join(common_kw[:3])}."
                ),
                category="collaborations",
                score=sim,
                keywords=common_kw,
                rationale=(
                    f"Keyword similarity: {sim:.0%}. "
                    "Collaboration between researchers with complementary expertise "
                    "often leads to high-impact publications."
                ),
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _recommend_venues(self, top_n: int) -> List[Recommendation]:
        """Recommend publication venues.
        
        Identifies high-impact journals/conferences relevant to the research area.
        """
        recommendations = []
        
        # Get journal statistics
        journal_stats = self._get_journal_statistics()
        
        # Sort by impact (avg citations)
        sorted_journals = sorted(
            journal_stats.items(),
            key=lambda x: x[1]['avg_citations'],
            reverse=True
        )
        
        for journal, stats in sorted_journals[:top_n]:
            if stats['count'] < 2:  # Need at least 2 publications
                continue
            
            # Normalize score based on citations and count
            impact_score = min(1.0, stats['avg_citations'] / 100)
            volume_score = min(1.0, stats['count'] / 20)
            combined_score = (impact_score * 0.7) + (volume_score * 0.3)
            
            rec = Recommendation(
                title=f"Venue: {journal[:50]}",
                description=(
                    f"{journal} publishes relevant research with high impact. "
                    f"Average citations: {stats['avg_citations']:.1f}, "
                    f"Publications in dataset: {stats['count']}."
                ),
                category="venues",
                score=combined_score,
                keywords=stats.get('top_keywords', []),
                rationale=(
                    f"Open access rate: {stats['oa_rate']:.0%}. "
                    "This venue has demonstrated interest in your research area."
                ),
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _get_keyword_cooccurrence(self) -> Dict[Tuple[str, str], int]:
        """Calculate keyword co-occurrence frequencies."""
        cooccurrence: Dict[Tuple[str, str], int] = defaultdict(int)
        
        for pub in self.analyzer.publications:
            keywords = [kw.lower().strip() for kw in pub.keywords]
            
            for i, kw1 in enumerate(keywords):
                for kw2 in keywords[i + 1:]:
                    pair = tuple(sorted([kw1, kw2]))
                    cooccurrence[pair] += 1
        
        return dict(cooccurrence)
    
    def _get_author_keywords(self) -> Dict[str, List[str]]:
        """Get keywords associated with each author."""
        author_keywords: Dict[str, List[str]] = defaultdict(list)
        
        for pub in self.analyzer.publications:
            keywords = [kw.lower().strip() for kw in pub.keywords]
            for author in pub.authors:
                author_keywords[author].extend(keywords)
        
        # Get most common keywords per author
        result = {}
        for author, kws in author_keywords.items():
            counter = Counter(kws)
            result[author] = [kw for kw, _ in counter.most_common(10)]
        
        return result
    
    def _get_journal_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Calculate statistics for each journal."""
        journal_data: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                'count': 0,
                'citations': [],
                'open_access': 0,
                'keywords': [],
            }
        )
        
        for pub in self.analyzer.publications:
            if not pub.publication_name:
                continue
            
            journal = pub.publication_name
            journal_data[journal]['count'] += 1
            journal_data[journal]['citations'].append(pub.citation_count)
            journal_data[journal]['keywords'].extend(pub.keywords)
            
            if pub.open_access:
                journal_data[journal]['open_access'] += 1
        
        # Calculate aggregates
        result = {}
        for journal, data in journal_data.items():
            citations = data['citations']
            keyword_counts = Counter([kw.lower() for kw in data['keywords']])
            
            result[journal] = {
                'count': data['count'],
                'avg_citations': np.mean(citations) if citations else 0,
                'total_citations': sum(citations),
                'oa_rate': data['open_access'] / data['count'] if data['count'] > 0 else 0,
                'top_keywords': [kw for kw, _ in keyword_counts.most_common(5)],
            }
        
        return result
    
    def get_topic_suggestions(self, current_keywords: List[str], top_n: int = 10) -> List[str]:
        """Suggest related topics based on current research interests.
        
        Args:
            current_keywords: Keywords representing current interests.
            top_n: Number of suggestions to return.
            
        Returns:
            List of suggested keywords/topics.
        """
        # Build keyword co-occurrence graph
        cooccurrence = self._get_keyword_cooccurrence()
        
        # Find keywords that frequently co-occur with current interests
        related_scores: Dict[str, float] = defaultdict(float)
        
        for kw in current_keywords:
            kw_lower = kw.lower().strip()
            
            for pair, count in cooccurrence.items():
                if kw_lower in pair:
                    other = pair[0] if pair[1] == kw_lower else pair[1]
                    if other not in [k.lower() for k in current_keywords]:
                        related_scores[other] += count
        
        # Sort by score
        sorted_related = sorted(
            related_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [kw for kw, _ in sorted_related[:top_n]]
    
    def explain_recommendation(self, recommendation: Recommendation) -> str:
        """Generate a detailed explanation for a recommendation.
        
        Args:
            recommendation: The recommendation to explain.
            
        Returns:
            Detailed explanation string.
        """
        explanations = {
            'emerging_topics': (
                "This recommendation is based on analyzing publication growth rates. "
                "Topics showing rapid increase in recent publications often indicate "
                "emerging research areas with high potential for impact. Early "
                "contributions to such areas tend to be highly cited."
            ),
            'research_gaps': (
                "This recommendation identifies an underexplored intersection of "
                "established research areas. The analysis found that while both "
                "topics have substantial individual coverage, their combination "
                "is rarely addressed. Interdisciplinary research often leads to "
                "novel discoveries and methodological innovations."
            ),
            'collaborations': (
                "This recommendation is based on analyzing research interests and "
                "existing collaboration networks. The suggested collaborators work "
                "on similar topics but haven't yet published together. "
                "Collaborations between researchers with aligned interests often "
                "produce higher-quality publications."
            ),
            'venues': (
                "This recommendation is based on analyzing publication patterns, "
                "citation impact, and topical alignment. The suggested venue "
                "regularly publishes work in your research area and has "
                "demonstrated good citation metrics."
            ),
        }
        
        base = explanations.get(
            recommendation.category,
            "This recommendation is based on analysis of publication patterns."
        )
        
        return f"{base}\n\nSpecific rationale: {recommendation.rationale}"
    
    def to_report(self) -> str:
        """Generate a text report of all recommendations.
        
        Returns:
            Formatted report string.
        """
        recommendations = self.get_recommendations(top_n=5)
        
        lines = [
            "=" * 60,
            "RESEARCH RECOMMENDATIONS REPORT",
            "=" * 60,
            "",
        ]
        
        # Group by category
        by_category: Dict[str, List[Recommendation]] = defaultdict(list)
        for rec in recommendations:
            by_category[rec.category].append(rec)
        
        category_titles = {
            'emerging_topics': 'Emerging Research Topics',
            'research_gaps': 'Underexplored Research Areas',
            'collaborations': 'Potential Collaborations',
            'venues': 'Recommended Publication Venues',
        }
        
        for category, title in category_titles.items():
            if category in by_category:
                lines.append(f"\n{title}")
                lines.append("-" * len(title))
                
                for i, rec in enumerate(by_category[category], 1):
                    lines.append(f"\n{i}. {rec.title}")
                    lines.append(f"   Score: {rec.score:.2f}")
                    lines.append(f"   {rec.description}")
                    if rec.keywords:
                        lines.append(f"   Keywords: {', '.join(rec.keywords[:5])}")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
