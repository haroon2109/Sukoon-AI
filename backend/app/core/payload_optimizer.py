import re
import math
from typing import List
from app.domain.schemas.schemas import ExtractedClaim, RetrievedEvidence

def approximate_tokens(text: str) -> int:
    """Heuristic token approximation (avg 4 chars per token)"""
    return math.ceil(len(text) / 4.0)

def strip_html_and_boilerplate(text: str) -> str:
    """Removes HTML, multiple whitespaces, and common boilerplate."""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def deduplicate_lines(text: str) -> str:
    """Removes duplicate lines (useful for OCR repeating tickers)."""
    if not text:
        return ""
    lines = text.split('\n')
    seen = set()
    cleaned = []
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        if line_clean not in seen:
            seen.add(line_clean)
            cleaned.append(line_clean)
    return "\n".join(cleaned)

class PayloadOptimizer:
    @staticmethod
    def optimize_text(text: str, max_chars: int = None) -> str:
        text = strip_html_and_boilerplate(text)
        if max_chars and len(text) > max_chars:
            text = text[:max_chars] + "... [TRUNCATED DUE TO CONTEXT LIMITS]"
        return text

    @staticmethod
    def optimize_evidence_list(claims: List[ExtractedClaim], evidence: List[RetrievedEvidence], max_context_window: int) -> str:
        """
        Truncates the evidence list so it doesn't blow past the max_context_window.
        Allocates ~20% of context to claims, ~80% to evidence.
        """
        claims_text = "\n".join([f"- {c.claim_text}" for c in claims])
        
        # Keep 1000 tokens for system prompt & response
        available_tokens = max(1000, max_context_window - 1000)
        claim_tokens = approximate_tokens(claims_text)
        
        remaining_evidence_tokens = max(500, available_tokens - claim_tokens)
        remaining_chars = remaining_evidence_tokens * 4
        
        optimized_evidence = []
        current_chars = 0
        
        for e in evidence:
            content_stripped = strip_html_and_boilerplate(e.content)
            entry = f"Source: {e.source_url}\n{content_stripped}"
            
            if current_chars + len(entry) <= remaining_chars:
                optimized_evidence.append(entry)
                current_chars += len(entry)
            else:
                # Truncate the last piece of evidence that fits partially
                allowable = remaining_chars - current_chars
                if allowable > 100:
                    optimized_evidence.append(entry[:allowable] + "...[TRUNCATED]")
                break
                
        evidence_text = "\n\n".join(optimized_evidence)
        return f"Claims:\n{claims_text}\n\nEvidence:\n{evidence_text}"
