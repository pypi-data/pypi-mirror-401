"""Tests for the LLM review module."""
import json
import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from scholar.llm_review import *
from scholar.llm_review import _format_paper_for_prompt, _collect_available_tags
from scholar.review import (
    ReviewSession, ReviewDecision, DecisionStatus, ReviewSource
)
from scholar.scholar import Paper


class TestDataStructures:
    """Tests for LLM review data structures."""

    def test_llm_decision_creation(self):
        """Can create an LLM decision."""
        decision = LLMDecision(
            paper_id="doi:10.1234/test",
            status="kept",
            tags=["relevant", "ml-focused"],
            confidence=0.85,
            reasoning="Paper discusses machine learning methods.",
        )
        assert decision.paper_id == "doi:10.1234/test"
        assert decision.status == "kept"
        assert decision.confidence == 0.85

    def test_llm_batch_result_creation(self):
        """Can create a batch result."""
        decisions = [
            LLMDecision(
                paper_id="doi:1",
                status="kept",
                tags=["good"],
                confidence=0.9,
                reasoning="Relevant.",
            ),
        ]
        result = LLMBatchResult(
            decisions=decisions,
            model_id="gpt-4",
            timestamp="2024-01-01T00:00:00",
        )
        assert len(result.decisions) == 1
        assert result.model_id == "gpt-4"
class TestExampleGathering:
    """Tests for example gathering functions."""

    def _create_session_with_examples(self):
        """Helper to create a session with various examples."""
        session = ReviewSession(
            query="test query",
            providers=["test"],
            timestamp=datetime.now(),
        )

        # Add some kept papers with tags
        for i in range(3):
            paper = Paper(
                title=f"Kept Paper {i}",
                authors=["Author"],
                year=2024,
                doi=f"10.1234/kept{i}",
            )
            decision = ReviewDecision(
                paper=paper,
                provider="test",
                status=DecisionStatus.KEPT,
                tags=["relevant", "ml"],
            )
            session.decisions.append(decision)

        # Add some discarded papers with tags
        for i in range(3):
            paper = Paper(
                title=f"Discarded Paper {i}",
                authors=["Author"],
                year=2024,
                doi=f"10.1234/discarded{i}",
            )
            decision = ReviewDecision(
                paper=paper,
                provider="test",
                status=DecisionStatus.DISCARDED,
                tags=["off-topic"],
            )
            session.decisions.append(decision)

        return session

    def test_get_example_decisions(self):
        """Gathers tagged examples correctly."""
        session = self._create_session_with_examples()

        kept, discarded = get_example_decisions(session)

        assert len(kept) == 3
        assert len(discarded) == 3
        assert all(d.status == DecisionStatus.KEPT for d in kept)
        assert all(d.status == DecisionStatus.DISCARDED for d in discarded)

    def test_excludes_untagged_papers(self):
        """Papers without tags are excluded from examples."""
        session = self._create_session_with_examples()

        # Add untagged paper
        paper = Paper(
            title="Untagged Paper",
            authors=["Author"],
            year=2024,
            doi="10.1234/untagged",
        )
        session.decisions.append(ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=[],  # No tags
        ))

        kept, discarded = get_example_decisions(session)

        # Untagged paper should not be included
        assert len(kept) == 3  # Still only the original 3

    def test_prioritizes_corrected_examples(self):
        """Corrected LLM decisions are prioritized."""
        session = ReviewSession(
            query="test",
            providers=["test"],
            timestamp=datetime.now(),
        )

        # Add regular example
        paper1 = Paper(title="Regular", authors=["A"], year=2024, doi="1")
        session.decisions.append(ReviewDecision(
            paper=paper1,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=["good"],
            is_example=False,
        ))

        # Add corrected example
        paper2 = Paper(title="Corrected", authors=["A"], year=2024, doi="2")
        session.decisions.append(ReviewDecision(
            paper=paper2,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=["also-good"],
            is_example=True,  # User corrected LLM
        ))

        kept, _ = get_example_decisions(session)

        # Corrected example should be first
        assert kept[0].is_example is True

    def test_validate_examples_success(self):
        """Validation passes with sufficient examples."""
        kept = [Mock() for _ in range(3)]
        discarded = [Mock() for _ in range(2)]

        is_valid, error = validate_examples(kept, discarded)

        assert is_valid is True
        assert error == ""

    def test_validate_examples_insufficient_total(self):
        """Validation fails with insufficient total examples."""
        kept = [Mock()]
        discarded = [Mock()]

        is_valid, error = validate_examples(kept, discarded)

        assert is_valid is False
        assert "at least 5" in error

    def test_validate_examples_no_kept(self):
        """Validation fails with no kept examples."""
        kept = []
        discarded = [Mock() for _ in range(5)]

        is_valid, error = validate_examples(kept, discarded)

        assert is_valid is False
        assert "kept" in error.lower()

    def test_validate_examples_no_discarded(self):
        """Validation fails with no discarded examples."""
        kept = [Mock() for _ in range(5)]
        discarded = []

        is_valid, error = validate_examples(kept, discarded)

        assert is_valid is False
        assert "discarded" in error.lower()

class TestPromptConstruction:
    """Tests for prompt construction functions."""

    def test_format_paper_for_prompt(self):
        """Papers are formatted correctly for prompts."""
        paper = Paper(
            title="Test Paper",
            authors=["Alice", "Bob", "Charlie", "David"],
            year=2024,
            abstract="This is the abstract.",
            venue="ICML",
        )
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=["ml", "relevant"],
        )

        result = _format_paper_for_prompt(decision)

        assert "Test Paper" in result
        assert "Alice" in result
        assert "et al." in result  # More than 3 authors
        assert "2024" in result
        assert "ICML" in result
        assert "abstract" in result.lower()
        assert "ml, relevant" in result

    def test_format_paper_truncates_long_abstract(self):
        """Long abstracts are truncated."""
        paper = Paper(
            title="Test",
            authors=["A"],
            year=2024,
            abstract="x" * 2000,  # Very long
        )
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=["test"],
        )

        result = _format_paper_for_prompt(decision)

        assert len(result) < 2000
        assert "..." in result

    def test_build_classification_prompt_includes_context(self):
        """Prompt includes research context when provided."""
        paper = Paper(title="Test", authors=["A"], year=2024)
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.PENDING,
            tags=[],
        )

        prompt = build_classification_prompt(
            papers_to_classify=[decision],
            kept_examples=[],
            discarded_examples=[],
            research_context="Focus on privacy-preserving ML.",
        )

        assert "privacy-preserving" in prompt.lower()

    def test_build_classification_prompt_includes_examples(self):
        """Prompt includes kept and discarded examples."""
        paper = Paper(title="Test", authors=["A"], year=2024)
        to_classify = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.PENDING,
            tags=[],
        )

        kept_paper = Paper(title="Kept Example", authors=["B"], year=2024)
        kept_example = ReviewDecision(
            paper=kept_paper,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=["relevant"],
        )

        discarded_paper = Paper(
            title="Discarded Example", authors=["C"], year=2024
        )
        discarded_example = ReviewDecision(
            paper=discarded_paper,
            provider="test",
            status=DecisionStatus.DISCARDED,
            tags=["off-topic"],
        )

        prompt = build_classification_prompt(
            papers_to_classify=[to_classify],
            kept_examples=[kept_example],
            discarded_examples=[discarded_example],
        )

        assert "Kept Example" in prompt
        assert "Discarded Example" in prompt
        assert "KEPT Papers" in prompt
        assert "DISCARDED Papers" in prompt
class TestZeroShotClassification:
    """Tests for classification without example requirements."""

    def test_classify_without_examples_dry_run(self):
        """Zero-shot mode builds a prompt without raising."""
        session = ReviewSession(
            query="test",
            providers=["test"],
            timestamp=datetime.now(),
            research_context="I am studying X.",
        )
        session.decisions.append(
            ReviewDecision(
                paper=Paper(
                    title="Pending",
                    authors=["A"],
                    year=2024,
                    abstract="Abstract.",
                ),
                provider="test",
                status=DecisionStatus.PENDING,
            )
        )

        prompt = classify_papers_with_llm(
            session=session,
            count=1,
            dry_run=True,
            require_examples=False,
        )

        assert "Research Context" in prompt
        assert "Papers to Classify" in prompt
class TestLLMInteraction:
    """Tests for LLM interaction functions."""

    def test_parse_llm_response_json_in_code_block(self):
        """Parses JSON wrapped in markdown code block."""
        paper = Paper(title="Test", authors=["A"], year=2024, doi="1")
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.PENDING,
            tags=[],
        )

        response = '''
Here's my classification:

```json
{
  "classifications": [
    {
      "paper_index": 0,
      "decision": "kept",
      "tags": ["relevant"],
      "confidence": 0.9,
      "reasoning": "Looks good."
    }
  ]
}
```
'''
        results = parse_llm_response(response, [decision])

        assert len(results) == 1
        assert results[0].status == "kept"
        assert results[0].confidence == 0.9

    def test_parse_llm_response_raw_json(self):
        """Parses raw JSON without code block."""
        paper = Paper(title="Test", authors=["A"], year=2024, doi="1")
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.PENDING,
            tags=[],
        )

        response = '''{"classifications": [{"paper_index": 0, "decision": "discarded", "tags": ["off-topic"], "confidence": 0.8, "reasoning": "Not relevant."}]}'''

        results = parse_llm_response(response, [decision])

        assert len(results) == 1
        assert results[0].status == "discarded"

    def test_parse_llm_response_invalid_json(self):
        """Raises error for invalid JSON."""
        paper = Paper(title="Test", authors=["A"], year=2024, doi="1")
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.PENDING,
            tags=[],
        )

        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_llm_response("{invalid json}", [decision])

    def test_parse_llm_response_no_json(self):
        """Raises error when no JSON found."""
        paper = Paper(title="Test", authors=["A"], year=2024, doi="1")
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.PENDING,
            tags=[],
        )

        with pytest.raises(ValueError, match="No JSON found"):
            parse_llm_response("No JSON here", [decision])

    def test_get_papers_needing_enrichment(self):
        """Identifies papers without abstracts."""
        paper_with = Paper(
            title="With", authors=["A"], year=2024,
            abstract="Has abstract"
        )
        paper_without = Paper(
            title="Without", authors=["A"], year=2024,
            abstract=None
        )

        decisions = [
            ReviewDecision(
                paper=paper_with,
                provider="test",
                status=DecisionStatus.PENDING,
            ),
            ReviewDecision(
                paper=paper_without,
                provider="test",
                status=DecisionStatus.PENDING,
            ),
        ]

        needing = get_papers_needing_enrichment(decisions)

        assert len(needing) == 1
        assert needing[0].title == "Without"
class TestDecisionApplication:
    """Tests for decision application functions."""

    def test_apply_llm_decisions(self):
        """LLM decisions are applied correctly."""
        from scholar.notes import get_paper_id

        paper = Paper(
            title="Test", authors=["A"], year=2024, doi="10.1234/test"
        )
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.PENDING,
            tags=[],
        )

        session = ReviewSession(
            query="test",
            providers=["test"],
            timestamp=datetime.now(),
        )
        session.decisions.append(decision)

        # Get the actual paper_id that will be used
        paper_id = get_paper_id(paper)

        # Create LLM result with matching paper_id
        llm_decision = LLMDecision(
            paper_id=paper_id,
            status="kept",
            tags=["relevant"],
            confidence=0.85,
            reasoning="Good paper.",
        )
        batch = LLMBatchResult(
            decisions=[llm_decision],
            model_id="test",
            timestamp="2024-01-01",
        )

        updated = apply_llm_decisions(session, batch)

        # Should update correctly
        assert len(updated) == 1
        assert updated[0].status == DecisionStatus.KEPT
        assert updated[0].source == ReviewSource.LLM_UNREVIEWED
        assert updated[0].llm_confidence == 0.85

    def test_mark_as_reviewed_agrees(self):
        """Marking as reviewed when user agrees."""
        paper = Paper(title="Test", authors=["A"], year=2024)
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=["relevant"],
            source=ReviewSource.LLM_UNREVIEWED,
        )

        mark_as_reviewed(decision, user_agrees=True)

        assert decision.source == ReviewSource.LLM_REVIEWED
        assert decision.is_example is False  # Not an example if agreed

    def test_mark_as_reviewed_disagrees(self):
        """Marking as reviewed when user disagrees becomes example."""
        paper = Paper(title="Test", authors=["A"], year=2024)
        decision = ReviewDecision(
            paper=paper,
            provider="test",
            status=DecisionStatus.KEPT,
            tags=["relevant"],
            source=ReviewSource.LLM_UNREVIEWED,
        )

        mark_as_reviewed(
            decision,
            user_agrees=False,
            new_status=DecisionStatus.DISCARDED,
            new_tags=["off-topic"],
        )

        assert decision.source == ReviewSource.LLM_REVIEWED
        assert decision.is_example is True  # Becomes example
        assert decision.status == DecisionStatus.DISCARDED
        assert decision.tags == ["off-topic"]

    def test_get_unreviewed_llm_decisions(self):
        """Gets unreviewed decisions sorted by confidence."""
        session = ReviewSession(
            query="test",
            providers=["test"],
            timestamp=datetime.now(),
        )

        # Add papers with different confidence levels
        for i, conf in enumerate([0.9, 0.3, 0.7]):
            paper = Paper(title=f"Paper {i}", authors=["A"], year=2024)
            decision = ReviewDecision(
                paper=paper,
                provider="test",
                status=DecisionStatus.KEPT,
                source=ReviewSource.LLM_UNREVIEWED,
                llm_confidence=conf,
            )
            session.decisions.append(decision)

        unreviewed = get_unreviewed_llm_decisions(session)

        assert len(unreviewed) == 3
        # Lowest confidence first
        assert unreviewed[0].llm_confidence == 0.3
        assert unreviewed[1].llm_confidence == 0.7
        assert unreviewed[2].llm_confidence == 0.9
class TestStatistics:
    """Tests for statistics functions."""

    def test_get_review_statistics(self):
        """Computes statistics correctly."""
        session = ReviewSession(
            query="test",
            providers=["test"],
            timestamp=datetime.now(),
        )

        # Add various decisions
        for i in range(3):
            paper = Paper(title=f"Human {i}", authors=["A"], year=2024)
            session.decisions.append(
                ReviewDecision(
                    paper=paper,
                    provider="test",
                    status=DecisionStatus.KEPT,
                    source=ReviewSource.HUMAN,
                )
            )

        for i in range(2):
            paper = Paper(title=f"LLM {i}", authors=["A"], year=2024)
            session.decisions.append(
                ReviewDecision(
                    paper=paper,
                    provider="test",
                    status=DecisionStatus.KEPT,
                    source=ReviewSource.LLM_UNREVIEWED,
                )
            )

        paper = Paper(title="Pending", authors=["A"], year=2024)
        session.decisions.append(
            ReviewDecision(
                paper=paper,
                provider="test",
                status=DecisionStatus.PENDING,
            )
        )

        paper = Paper(title="Example", authors=["A"], year=2024)
        session.decisions.append(
            ReviewDecision(
                paper=paper,
                provider="test",
                status=DecisionStatus.DISCARDED,
                source=ReviewSource.LLM_REVIEWED,
                is_example=True,
            )
        )

        stats = get_review_statistics(session)

        assert stats["human"] == 3
        assert stats["llm_unreviewed"] == 2
        assert stats["llm_reviewed"] == 1
        assert stats["pending"] == 1
        assert stats["examples"] == 1
        assert stats["total"] == 7
