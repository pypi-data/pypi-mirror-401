from enum import Enum

from pydantic import BaseModel
from src.core.rag.base import ChunkingConfig


class PresetName(str, Enum):
    GENERAL = "general"
    LEGAL = "legal"
    PODCAST = "podcast"


class PipelinePreset(BaseModel):
    name: PresetName
    description: str
    chunking_config: ChunkingConfig


# --- Pre-defined Presets ---

GENERAL_PRESET = PipelinePreset(
    name=PresetName.GENERAL,
    description="Balanced configuration suitable for most audio content. Uses hybrid rule-based chunking.",
    chunking_config=ChunkingConfig(
        strategy_name="recursive",  # or "rule_based" if we want to differentiate
        chunk_size=1000,
        chunk_overlap=200,
    ),
)

LEGAL_PRESET = PipelinePreset(
    name=PresetName.LEGAL,
    description="High-precision semantic chunking for dense information. Smaller chunks with high semantic coherence.",
    chunking_config=ChunkingConfig(
        strategy_name="semantic",
        chunk_size=500,  # Target smaller chunks
        chunk_overlap=100,
        threshold_type="percentile",
        threshold_amount=90.0,  # Strict threshold for semantic shift
    ),
)

PODCAST_PRESET = PipelinePreset(
    name=PresetName.PODCAST,
    description="Optimized for long-form conversational content. Larger chunks to capture full context of discussions.",
    chunking_config=ChunkingConfig(
        strategy_name="semantic",
        chunk_size=1500,  # Larger chunks
        chunk_overlap=300,
        threshold_type="standard_deviation",
        threshold_amount=1.5,  # Looser threshold
    ),
)


def get_preset(name: str | PresetName) -> PipelinePreset:
    """Get a preset by name."""
    if isinstance(name, str):
        try:
            name = PresetName(name.lower())
        except ValueError:
            # Fallback to general if unknown, or raise?
            # Let's default to general for robustness, or we could raise to be explicit.
            # Plan said "Input models accept preset", checking validation there is better.
            # For now, let's return GENERAL if not found is safer?
            # Actually, Pydantic will validate the Enum in the API layer.
            # So here we assume valid index access or we return default.
            return GENERAL_PRESET

    if name == PresetName.LEGAL:
        return LEGAL_PRESET
    if name == PresetName.PODCAST:
        return PODCAST_PRESET

    return GENERAL_PRESET
