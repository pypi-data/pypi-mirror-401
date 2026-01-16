"""
Logowatch preset configurations.

Presets are stored as actual YAML files and copied to user's CWD during init.
"""

from pathlib import Path
from importlib import resources


def get_preset_path(preset_name: str) -> Path | None:
    """Get the path to a preset YAML file.

    Args:
        preset_name: Name of the preset (e.g., 'mcp', 'claude-session', 'docker')

    Returns:
        Path to the preset file, or None if not found
    """
    preset_file = f"{preset_name}.yaml"
    preset_dir = Path(__file__).parent
    preset_path = preset_dir / preset_file

    if preset_path.exists():
        return preset_path
    return None


def list_presets() -> dict[str, dict]:
    """List all available presets with their metadata.

    Returns:
        Dict mapping preset name to metadata (name, description, path)
    """
    preset_dir = Path(__file__).parent
    presets = {}

    for yaml_file in preset_dir.glob("*.yaml"):
        preset_name = yaml_file.stem
        # Parse first few lines for comments to get description
        content = yaml_file.read_text()
        lines = content.split("\n")

        # Extract title from first comment line
        title = preset_name
        description = ""

        for line in lines[:5]:
            if line.startswith("# LOGOWATCH PRESET:"):
                title = line.replace("# LOGOWATCH PRESET:", "").strip()
            elif line.startswith("#") and not line.startswith("# LOGOWATCH"):
                desc = line.lstrip("# ").strip()
                if desc and not description:
                    description = desc
                    break

        presets[preset_name] = {
            "name": title,
            "description": description,
            "path": yaml_file,
        }

    return presets


def get_preset_content(preset_name: str) -> str | None:
    """Get the content of a preset YAML file.

    Args:
        preset_name: Name of the preset

    Returns:
        Content of the preset file, or None if not found
    """
    preset_path = get_preset_path(preset_name)
    if preset_path:
        return preset_path.read_text()
    return None
