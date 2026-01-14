"""
LLM-assisted paper classification for systematic reviews.

Provides functions for classifying papers using large language models,
learning from human-tagged examples in a round-based workflow.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import json
import logging
import re

from scholar.review import (
    ReviewSession,
    ReviewDecision,
    DecisionStatus,
    ReviewSource,
)
from scholar.scholar import Paper

logger = logging.getLogger(__name__)
# Minimum requirements for LLM classification
MIN_TOTAL_EXAMPLES = 5
MIN_KEPT_EXAMPLES = 1
MIN_DISCARDED_EXAMPLES = 1

# Default batch size for classification
DEFAULT_BATCH_SIZE = 10

# Maximum examples to include in prompt (to manage token limits)
MAX_KEPT_EXAMPLES = 10
MAX_DISCARDED_EXAMPLES = 10


@dataclass
class LLMDecision:
    """
    A single LLM classification decision for a paper.

    Attributes:
        paper_id: Identifier of the classified paper
        status: Classification result ("kept" or "discarded")
        tags: Themes (kept) or motivations (discarded) assigned
        confidence: LLM's confidence in the decision (0.0-1.0)
        reasoning: Brief explanation of the classification
    """

    paper_id: str
    status: str  # "kept" or "discarded"
    tags: list[str]
    confidence: float
    reasoning: str


@dataclass
class LLMBatchResult:
    """
    Results from a batch LLM classification.

    Attributes:
        decisions: List of individual paper decisions
        model_id: Identifier of the LLM model used
        timestamp: When the classification was performed
        prompt_tokens: Optional token count for the prompt
        completion_tokens: Optional token count for the response
    """

    decisions: list[LLMDecision]
    model_id: str
    timestamp: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


def get_example_decisions(
    session: ReviewSession,
    max_kept: int = MAX_KEPT_EXAMPLES,
    max_discarded: int = MAX_DISCARDED_EXAMPLES,
) -> tuple[list[ReviewDecision], list[ReviewDecision]]:
    """
    Gather tagged examples from a review session.

    Prioritizes user-corrected LLM decisions (is_example=True) as these
    represent cases where the LLM's initial classification was wrong.

    Args:
        session: The review session to gather examples from
        max_kept: Maximum number of kept examples to include
        max_discarded: Maximum number of discarded examples to include

    Returns:
        Tuple of (kept_examples, discarded_examples)
    """
    kept_examples: list[ReviewDecision] = []
    discarded_examples: list[ReviewDecision] = []

    for decision in session.decisions:
        # Only include papers with tags (our example requirement)
        if not decision.tags:
            continue

        if decision.status == DecisionStatus.KEPT:
            kept_examples.append(decision)
        elif decision.status == DecisionStatus.DISCARDED:
            discarded_examples.append(decision)

    # Sort to prioritize corrected examples (is_example=True first)
    # Then by confidence (lower first, as these are harder cases)
    def sort_key(d: ReviewDecision) -> tuple[int, float]:
        # is_example=True should come first (0), then False (1)
        example_priority = 0 if d.is_example else 1
        # Lower confidence first (more informative examples)
        confidence = d.llm_confidence if d.llm_confidence is not None else 1.0
        return (example_priority, confidence)

    kept_examples.sort(key=sort_key)
    discarded_examples.sort(key=sort_key)

    # Limit to max and log selected examples
    kept_result = kept_examples[:max_kept]
    discarded_result = discarded_examples[:max_discarded]

    # Log info about selected examples
    if kept_result or discarded_result:
        logger.info(
            f"Selected {len(kept_result)} kept and "
            f"{len(discarded_result)} discarded examples for LLM"
        )
        for example in kept_result:
            logger.info(
                f"  KEPT example: {example.paper.title[:60]}... "
                f"[tags: {', '.join(example.tags)}]"
            )
        for example in discarded_result:
            logger.info(
                f"  DISCARDED example: {example.paper.title[:60]}... "
                f"[tags: {', '.join(example.tags)}]"
            )

    return kept_result, discarded_result


def validate_examples(
    kept_examples: list[ReviewDecision],
    discarded_examples: list[ReviewDecision],
    min_total: int = MIN_TOTAL_EXAMPLES,
    min_kept: int = MIN_KEPT_EXAMPLES,
    min_discarded: int = MIN_DISCARDED_EXAMPLES,
) -> tuple[bool, str]:
    """
    Check if examples meet minimum requirements for LLM classification.

    Args:
        kept_examples: List of kept paper examples
        discarded_examples: List of discarded paper examples
        min_total: Minimum total examples required
        min_kept: Minimum kept examples required
        min_discarded: Minimum discarded examples required

    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string.
    """
    total = len(kept_examples) + len(discarded_examples)

    if total < min_total:
        return False, (
            f"Need at least {min_total} tagged examples, "
            f"but only have {total}."
        )

    if len(kept_examples) < min_kept:
        return False, (
            f"Need at least {min_kept} kept example(s) with tags, "
            f"but only have {len(kept_examples)}."
        )

    if len(discarded_examples) < min_discarded:
        return False, (
            f"Need at least {min_discarded} discarded example(s) with tags, "
            f"but only have {len(discarded_examples)}."
        )

    return True, ""


def _format_paper_for_prompt(
    decision: ReviewDecision,
    include_abstract: bool = True,
) -> str:
    """
    Format a paper decision for inclusion in the prompt.

    Args:
        decision: The review decision containing the paper
        include_abstract: Whether to include the abstract

    Returns:
        Formatted string representation of the paper
    """
    paper = decision.paper
    lines = [
        f"Title: {paper.title}",
        f"Authors: {', '.join(paper.authors[:3])}"
        + (" et al." if len(paper.authors) > 3 else ""),
    ]

    if paper.year:
        lines.append(f"Year: {paper.year}")

    if paper.venue:
        lines.append(f"Venue: {paper.venue}")

    if include_abstract and paper.abstract:
        # Truncate very long abstracts
        abstract = paper.abstract
        if len(abstract) > 1000:
            abstract = abstract[:1000] + "..."
        lines.append(f"Abstract: {abstract}")

    lines.append(f"Tags: {', '.join(decision.tags)}")

    return "\n".join(lines)


def _format_paper_to_classify(
    decision: ReviewDecision,
    index: int,
) -> str:
    """
    Format a paper for classification request.

    Args:
        decision: The review decision containing the paper
        index: Zero-based index for reference in response

    Returns:
        Formatted string representation
    """
    paper = decision.paper
    lines = [
        f"[Paper {index}]",
        f"Title: {paper.title}",
        f"Authors: {', '.join(paper.authors[:3])}"
        + (" et al." if len(paper.authors) > 3 else ""),
    ]

    if paper.year:
        lines.append(f"Year: {paper.year}")

    if paper.venue:
        lines.append(f"Venue: {paper.venue}")

    if paper.abstract:
        abstract = paper.abstract
        if len(abstract) > 1000:
            abstract = abstract[:1000] + "..."
        lines.append(f"Abstract: {abstract}")
    else:
        lines.append("Abstract: [Not available]")

    return "\n".join(lines)


def _collect_available_tags(
    session: ReviewSession,
) -> tuple[set[str], set[str]]:
    """
    Collect all tags used in the session.

    Args:
        session: The review session

    Returns:
        Tuple of (themes_for_kept, motivations_for_discarded)
    """
    themes: set[str] = set()
    motivations: set[str] = set()

    for decision in session.decisions:
        if decision.status == DecisionStatus.KEPT:
            themes.update(decision.tags)
        elif decision.status == DecisionStatus.DISCARDED:
            motivations.update(decision.tags)

    return themes, motivations


def build_classification_prompt(
    papers_to_classify: list[ReviewDecision],
    kept_examples: list[ReviewDecision],
    discarded_examples: list[ReviewDecision],
    research_context: str | None = None,
    available_themes: set[str] | None = None,
    available_motivations: set[str] | None = None,
) -> str:
    """
    Construct the LLM prompt for paper classification.

    Args:
        papers_to_classify: Papers needing classification
        kept_examples: Example papers that were kept
        discarded_examples: Example papers that were discarded
        research_context: Description of the research focus
        available_themes: Tags used for kept papers
        available_motivations: Tags used for discarded papers

    Returns:
        Complete prompt string for the LLM
    """
    sections = []

    # Introduction
    sections.append(
        "You are helping with a systematic literature review. "
        "Your task is to classify papers as 'kept' (relevant to the review) "
        "or 'discarded' (not relevant)."
    )

    # Research context
    if research_context:
        sections.append(f"\n## Research Context\n\n{research_context}")

    # Available tags
    if available_themes:
        themes_list = ", ".join(sorted(available_themes))
        sections.append(
            f"\n## Available Themes (for kept papers)\n\n{themes_list}"
        )

    if available_motivations:
        motivations_list = ", ".join(sorted(available_motivations))
        sections.append(
            f"\n## Available Motivations (for discarded papers)\n\n"
            f"{motivations_list}"
        )

    # Kept examples
    if kept_examples:
        sections.append("\n## Examples of KEPT Papers\n")
        for example in kept_examples:
            sections.append(_format_paper_for_prompt(example))
            sections.append("")

    # Discarded examples
    if discarded_examples:
        sections.append("\n## Examples of DISCARDED Papers\n")
        for example in discarded_examples:
            sections.append(_format_paper_for_prompt(example))
            sections.append("")

    # Papers to classify
    sections.append("\n## Papers to Classify\n")
    for i, decision in enumerate(papers_to_classify):
        sections.append(_format_paper_to_classify(decision, i))
        sections.append("")

    # Instructions
    sections.append(
        """
## Instructions

For each paper above, classify it as 'kept' or 'discarded'.
Respond with a JSON object in exactly this format:

```json
{
  "classifications": [
    {
      "paper_index": 0,
      "decision": "kept",
      "tags": ["theme1", "theme2"],
      "confidence": 0.85,
      "reasoning": "Brief explanation of why this paper is relevant."
    },
    {
      "paper_index": 1,
      "decision": "discarded",
      "tags": ["motivation1"],
      "confidence": 0.90,
      "reasoning": "Brief explanation of why this paper is not relevant."
    }
  ]
}
```

Guidelines:
- Use existing themes/motivations when appropriate
- Create new tags only when existing ones don't fit
- Confidence should reflect how certain you are (0.0 to 1.0)
- Keep reasoning brief (1-2 sentences)
- Every discarded paper MUST have at least one motivation tag
"""
    )

    return "\n".join(sections)


def parse_llm_response(
    response_text: str,
    papers: list[ReviewDecision],
) -> list[LLMDecision]:
    """
    Parse JSON response from LLM into decisions.

    Args:
        response_text: Raw text response from LLM
        papers: The papers that were classified (for ID lookup)

    Returns:
        List of LLMDecision objects

    Raises:
        ValueError: If response cannot be parsed
    """
    from scholar.notes import get_paper_id

    # Extract JSON from response (may be wrapped in markdown code block)
    json_match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        response_text,
        re.DOTALL,
    )
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find raw JSON
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            raise ValueError("No JSON found in LLM response")

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in LLM response: {e}")

    if "classifications" not in data:
        raise ValueError("Response missing 'classifications' key")

    decisions = []
    for item in data["classifications"]:
        paper_index = item.get("paper_index", 0)
        if paper_index < 0 or paper_index >= len(papers):
            logger.warning(f"Invalid paper_index {paper_index}, skipping")
            continue

        paper_decision = papers[paper_index]
        paper_id = get_paper_id(paper_decision.paper)

        # Validate status
        status = item.get("decision", "").lower()
        if status not in ("kept", "discarded"):
            logger.warning(f"Invalid decision '{status}', defaulting to kept")
            status = "kept"

        # Ensure tags are present
        tags = item.get("tags", [])
        if not isinstance(tags, list):
            tags = [str(tags)]

        # Validate confidence
        confidence = item.get("confidence", 0.5)
        try:
            confidence = float(confidence)
            confidence = max(0.0, min(1.0, confidence))
        except (TypeError, ValueError):
            confidence = 0.5

        decisions.append(
            LLMDecision(
                paper_id=paper_id,
                status=status,
                tags=tags,
                confidence=confidence,
                reasoning=item.get("reasoning", ""),
            )
        )

    return decisions


def get_papers_needing_enrichment(
    papers: list[ReviewDecision],
) -> list[Paper]:
    """
    Return papers that lack abstracts (required for LLM classification).

    Args:
        papers: List of review decisions to check

    Returns:
        List of Paper objects that need enrichment
    """
    return [
        decision.paper for decision in papers if not decision.paper.abstract
    ]


def classify_papers_with_llm(
    session: ReviewSession,
    count: int = DEFAULT_BATCH_SIZE,
    model_id: str | None = None,
    enrich_missing: bool = True,
    dry_run: bool = False,
    require_examples: bool = True,
) -> LLMBatchResult | str:
    """
    Classify pending papers using LLM.

    This is the main entry point for LLM-assisted classification. It:
    1. Optionally gathers training examples from human-reviewed papers
    2. Optionally validates minimum example requirements
    3. Optionally enriches papers lacking abstracts
    4. Constructs a prompt with examples and papers to classify
    5. Invokes the LLM and parses the response

    Args:
        session: The review session
        count: Number of papers to classify in this batch
        model_id: LLM model to use (uses llm default if None)
        enrich_missing: Whether to auto-enrich papers without abstracts
        dry_run: If True, return the prompt without calling LLM
        require_examples: If True (default), require tagged example papers
            before classification. Set False for zero-shot classification
            using only the research context.

    Returns:
        LLMBatchResult with decisions, or prompt string if dry_run=True

    Raises:
        ValueError: If there are no papers to classify, or if
            require_examples=True and there are insufficient examples
        ImportError: If llm package is not installed
    """
    # Gather examples (optional)
    if require_examples:
        kept_examples, discarded_examples = get_example_decisions(session)

        # Validate
        is_valid, error = validate_examples(kept_examples, discarded_examples)
        if not is_valid:
            raise ValueError(error)
    else:
        kept_examples = []
        discarded_examples = []

    # Get pending papers
    pending = [
        d for d in session.decisions if d.status == DecisionStatus.PENDING
    ]

    if not pending:
        raise ValueError("No pending papers to classify")

    # Limit to requested count
    to_classify = pending[:count]

    # Check for papers needing enrichment
    if enrich_missing:
        needing_enrichment = get_papers_needing_enrichment(to_classify)
        if needing_enrichment:
            try:
                from scholar.enrich import enrich_papers

                logger.info(
                    f"Enriching {len(needing_enrichment)} papers "
                    "before classification"
                )
                enrich_papers(needing_enrichment)
            except ImportError:
                logger.warning(
                    "Enrich module not available, "
                    "some papers may lack abstracts"
                )

    # Collect available tags
    themes, motivations = _collect_available_tags(session)

    # Build prompt
    prompt = build_classification_prompt(
        papers_to_classify=to_classify,
        kept_examples=kept_examples,
        discarded_examples=discarded_examples,
        research_context=session.research_context,
        available_themes=themes,
        available_motivations=motivations,
    )

    if dry_run:
        return prompt

    # Import llm and call
    try:
        import llm
    except ImportError:
        raise ImportError(
            "The 'llm' package is required for LLM classification. "
            "Install it with: pip install llm"
        )

    model = llm.get_model(model_id) if model_id else llm.get_model()
    logger.info(
        f"Classifying {len(to_classify)} papers with {model.model_id}"
    )

    # Log papers being sent for classification
    logger.info("Papers to classify:")
    for i, decision in enumerate(to_classify):
        abstract_status = (
            "with abstract" if decision.paper.abstract else "NO ABSTRACT"
        )
        logger.info(
            f"  [{i}] {decision.paper.title[:50]}... ({abstract_status})"
        )

    response = model.prompt(prompt)
    response_text = response.text()

    # Parse response
    decisions = parse_llm_response(response_text, to_classify)

    return LLMBatchResult(
        decisions=decisions,
        model_id=model.model_id,
        timestamp=datetime.now().isoformat(),
        prompt_tokens=getattr(response, "prompt_tokens", None),
        completion_tokens=getattr(response, "completion_tokens", None),
    )


def _build_paper_id_lookup(
    session: ReviewSession,
) -> dict[str, ReviewDecision]:
    """Build a lookup dict from paper_id to decision."""
    from scholar.notes import get_paper_id

    return {get_paper_id(d.paper): d for d in session.decisions}


def apply_llm_decisions(
    session: ReviewSession,
    batch_result: LLMBatchResult,
) -> list[ReviewDecision]:
    """
    Apply LLM decisions to session, marking as LLM_UNREVIEWED.

    Args:
        session: The review session to update
        batch_result: Results from LLM classification

    Returns:
        List of ReviewDecision objects that were updated
    """
    updated = []

    # Build lookup for efficient paper_id matching
    paper_id_lookup = _build_paper_id_lookup(session)

    logger.info(
        f"Applying LLM decisions for {len(batch_result.decisions)} papers"
    )

    for llm_decision in batch_result.decisions:
        if llm_decision.paper_id not in paper_id_lookup:
            logger.warning(
                f"Paper {llm_decision.paper_id} not in session, skipping"
            )
            continue

        decision = paper_id_lookup[llm_decision.paper_id]

        # Only update pending papers
        if decision.status != DecisionStatus.PENDING:
            logger.debug(
                f"Paper {llm_decision.paper_id} already decided, skipping"
            )
            continue

        # Apply LLM decision
        decision.status = (
            DecisionStatus.KEPT
            if llm_decision.status == "kept"
            else DecisionStatus.DISCARDED
        )
        decision.tags = llm_decision.tags
        decision.source = ReviewSource.LLM_UNREVIEWED
        decision.llm_confidence = llm_decision.confidence
        decision.is_example = False  # Not an example until user reviews

        # Log info about each paper's review outcome
        status_str = "KEPT" if llm_decision.status == "kept" else "DISCARDED"
        logger.info(
            f"  {status_str} (conf={llm_decision.confidence:.2f}): "
            f"{decision.paper.title[:50]}..."
        )
        logger.info(f"    Tags: {', '.join(llm_decision.tags)}")
        if llm_decision.reasoning:
            logger.info(f"    Reason: {llm_decision.reasoning[:80]}...")

        updated.append(decision)

    logger.info(f"Applied LLM decisions to {len(updated)} papers")
    return updated


def mark_as_reviewed(
    decision: ReviewDecision,
    user_agrees: bool,
    new_status: DecisionStatus | None = None,
    new_tags: list[str] | None = None,
) -> None:
    """
    Mark an LLM decision as reviewed by user.

    If the user changed the decision (disagrees), the paper becomes a
    training example for future LLM rounds.

    Args:
        decision: The decision to mark as reviewed
        user_agrees: Whether user agrees with LLM classification
        new_status: New status if user disagrees (ignored if agrees)
        new_tags: New tags if user disagrees (ignored if agrees)
    """
    if decision.source != ReviewSource.LLM_UNREVIEWED:
        logger.warning("Decision is not LLM_UNREVIEWED, nothing to mark")
        return

    decision.source = ReviewSource.LLM_REVIEWED

    if not user_agrees:
        # User corrected the LLM - this becomes an example
        decision.is_example = True

        if new_status is not None:
            decision.status = new_status

        if new_tags is not None:
            decision.tags = new_tags


def get_unreviewed_llm_decisions(
    session: ReviewSession,
    sort_by_confidence: bool = True,
) -> list[ReviewDecision]:
    """
    Get LLM decisions that haven't been reviewed by user.

    Args:
        session: The review session
        sort_by_confidence: If True, sort by confidence (lowest first)
            so users review uncertain decisions first

    Returns:
        List of ReviewDecision objects pending user review
    """
    unreviewed = [
        d
        for d in session.decisions
        if d.source == ReviewSource.LLM_UNREVIEWED
    ]

    if sort_by_confidence:
        # Sort by confidence, lowest first (most uncertain)
        unreviewed.sort(
            key=lambda d: d.llm_confidence if d.llm_confidence else 0.5
        )

    return unreviewed


def get_review_statistics(session: ReviewSession) -> dict[str, int]:
    """
    Get counts of decisions by source and status.

    Args:
        session: The review session

    Returns:
        Dictionary with counts:
        - human: Decisions made by human directly
        - llm_unreviewed: LLM decisions pending review
        - llm_reviewed: LLM decisions reviewed by user
        - examples: Papers marked as training examples
        - pending: Papers not yet decided
        - total: Total papers in session
    """
    stats = {
        "human": 0,
        "llm_unreviewed": 0,
        "llm_reviewed": 0,
        "examples": 0,
        "pending": 0,
        "total": len(session.decisions),
    }

    for decision in session.decisions:
        if decision.status == DecisionStatus.PENDING:
            stats["pending"] += 1
        elif decision.source == ReviewSource.HUMAN:
            stats["human"] += 1
        elif decision.source == ReviewSource.LLM_UNREVIEWED:
            stats["llm_unreviewed"] += 1
        elif decision.source == ReviewSource.LLM_REVIEWED:
            stats["llm_reviewed"] += 1

        if decision.is_example:
            stats["examples"] += 1

    return stats
