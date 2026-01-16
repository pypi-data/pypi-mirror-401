"""
TTS Preset Configuration System

Presets define voice, temperature, model, format for specific use cases.
Load from YAML files or define programmatically.

Usage:
    from unified_ai.presets import load_preset, TTSPreset

    # Load from file
    preset = load_preset("gemini/warm_trainer")

    # Or define inline
    preset = TTSPreset(
        provider="gemini",
        model="gemini-2.5-pro-preview-tts",
        voice="Enceladus",
        temperature=1.35,
        output_format="mp3"
    )

    # Use with SDK
    await sdk.generate_speech(text, preset=preset)
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional
import os

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class TTSPreset:
    """TTS configuration preset."""

    provider: str
    model: str
    voice: str
    temperature: float = 1.0
    output_format: str = "mp3"
    streaming: bool = False  # True for long content
    description: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def model_string(self) -> str:
        """Return provider/model format."""
        return f"{self.provider}/{self.model}"

    def to_kwargs(self) -> Dict[str, Any]:
        """Convert to SDK kwargs."""
        kwargs = {
            "voice": self.voice,
            "output_format": self.output_format,
            "provider_params": {
                "temperature": self.temperature,
                "streaming": self.streaming,
                **self.extra
            }
        }
        return kwargs


# Built-in presets
BUILTIN_PRESETS: Dict[str, TTSPreset] = {
    "gemini/warm_trainer": TTSPreset(
        provider="gemini",
        model="gemini-2.5-pro-preview-tts",
        voice="Enceladus",
        temperature=1.35,
        output_format="mp3",
        description="Warm, friendly business trainer voice"
    ),
    "gemini/narrator": TTSPreset(
        provider="gemini",
        model="gemini-2.5-flash-preview-tts",
        voice="Kore",
        temperature=1.0,
        output_format="mp3",
        description="Clear narrator voice, fast generation"
    ),
    "gemini/storyteller": TTSPreset(
        provider="gemini",
        model="gemini-2.5-pro-preview-tts",
        voice="Puck",
        temperature=1.2,
        output_format="mp3",
        description="Expressive storytelling voice"
    ),
    "gemini/news": TTSPreset(
        provider="gemini",
        model="gemini-2.5-flash-preview-tts",
        voice="Charon",
        temperature=0.8,
        output_format="mp3",
        description="Professional news reader, neutral tone"
    ),
}


def _scan_yaml_presets(presets_dir: Path) -> Dict[str, Path]:
    """Scan directory for YAML preset files."""
    found = {}
    if not presets_dir.exists() or not HAS_YAML:
        return found

    for yaml_file in presets_dir.glob("**/*.yaml"):
        # Convert path to preset name: configs/gemini/warm_trainer.yaml -> gemini/warm_trainer
        rel_path = yaml_file.relative_to(presets_dir)
        name = str(rel_path.with_suffix("")).replace("\\", "/")
        found[name] = yaml_file

    for yaml_file in presets_dir.glob("**/*.yml"):
        rel_path = yaml_file.relative_to(presets_dir)
        name = str(rel_path.with_suffix("")).replace("\\", "/")
        found[name] = yaml_file

    return found


def load_preset(name: str, presets_dir: Optional[Path] = None) -> TTSPreset:
    """
    Load a TTS preset by name.

    Args:
        name: Preset name like "gemini/warm_trainer"
              - First checks YAML files in presets_dir/configs/
              - Then checks builtin presets
        presets_dir: Optional directory with preset YAML files

    Returns:
        TTSPreset configuration

    Raises:
        ValueError: If preset not found
    """
    if presets_dir is None:
        presets_dir = Path(__file__).parent / "configs"

    # Scan YAML files first (allows overriding builtins)
    yaml_presets = _scan_yaml_presets(presets_dir)
    if name in yaml_presets:
        with open(yaml_presets[name]) as f:
            data = yaml.safe_load(f)
        return TTSPreset(**data)

    # Fall back to builtin
    if name in BUILTIN_PRESETS:
        return BUILTIN_PRESETS[name]

    available = list(yaml_presets.keys()) + list(BUILTIN_PRESETS.keys())
    raise ValueError(
        f"Preset '{name}' not found. "
        f"Available: {sorted(set(available))}"
    )


def list_presets(presets_dir: Optional[Path] = None) -> Dict[str, str]:
    """List available presets with descriptions."""
    if presets_dir is None:
        presets_dir = Path(__file__).parent / "configs"

    result = {}

    # Add YAML presets
    yaml_presets = _scan_yaml_presets(presets_dir)
    for name, path in yaml_presets.items():
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            result[name] = data.get("description", f"[YAML] {path.name}")
        except Exception:
            result[name] = f"[YAML] {path.name}"

    # Add builtins (YAML can override)
    for name, preset in BUILTIN_PRESETS.items():
        if name not in result:
            result[name] = preset.description

    return result


__all__ = ["TTSPreset", "load_preset", "list_presets", "BUILTIN_PRESETS"]
