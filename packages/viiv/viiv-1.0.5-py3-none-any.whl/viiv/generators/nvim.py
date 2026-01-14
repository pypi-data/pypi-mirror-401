"""Neovim theme generator module."""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def load_nvim_themes_config() -> Dict[str, str]:
    """Load Neovim theme configurations from nvim-themes.json.

    Returns:
        Mapping of theme names to their base colors.
    """
    config_path = Path(__file__).parent.parent / "conf" / "nvim-themes.json"
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        return config["themes"]


def generate_nvim_themes(nvim_repo_path: Optional[str] = None) -> None:
    """Generate Neovim themes using nvim-themes.json configuration.

    Args:
        nvim_repo_path: Path to viiv.nvim repository (optional).
    """
    from viiv.viiv import generate_random_theme_file

    nvim_themes = load_nvim_themes_config()

    for theme_name, dark_base_color in nvim_themes.items():
        logger.info(f"Generating Neovim theme: {theme_name}")

        # Generate theme using existing viiv logic
        generate_random_theme_file(
            theme_name=theme_name,
            theme_mode="DARK",
            workbench_base_background_color=dark_base_color,
            color_gradations_division_rate=0.9,
            reversed_color_offset_rate=0.5,
            output_dir=nvim_repo_path,
        )

    logger.info(f"Generated {len(nvim_themes)} Neovim themes")
