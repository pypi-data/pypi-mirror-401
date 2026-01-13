"""
RAG ingestability computation for CGD documents.

Per VALIDATOR_REFERENCE.md §6.2:
rag-ingestable = (clarity-status == CLEAR)
             AND (hitl-status == REVIEWED)
             AND (exclusion_block_count == 0)
"""

from ..types import ClarityStatus, HITLStatus


def compute_rag_ingestable(
    clarity_status: ClarityStatus,
    hitl_status: HITLStatus,
    exclusion_block_count: int,
) -> bool:
    """
    Compute rag-ingestable value.

    A document is safe for RAG ingestion only when:
    - clarity-status is CLEAR (no epistemic concerns)
    - hitl-status is REVIEWED (human has verified)
    - No exclusion blocks exist (nothing needs to be hidden)
    """
    return (
        clarity_status == "CLEAR"
        and hitl_status == "REVIEWED"
        and exclusion_block_count == 0
    )


def compute_rag_ingestable_with_version(
    clarity_status: ClarityStatus,
    hitl_status: HITLStatus,
    exclusion_block_count: int,
    major_version: int,
) -> bool:
    """
    Compute rag-ingestable with forward compatibility.

    If major version is unknown (> current), force false.
    """
    # Unknown major version = not safe to ingest
    if major_version > 1:
        return False

    return compute_rag_ingestable(clarity_status, hitl_status, exclusion_block_count)