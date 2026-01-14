#!/usr/bin/env python
"""ViiV - VSCode theme generator.

This module provides functionality to generate customized VSCode themes with
random or configured colors for tokens and workbench elements. It supports
both light and dark themes with automatic contrast ratio adjustments.

Main features:
- Generate random themes with customizable parameters
- Create themes from configuration files
- Automatic contrast ratio optimization
- Support for decoration and highlight colors
- Color palette generation and management
"""

import argparse
import json
import os
import random
import re
import sys
import typing
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from loguru import logger
from peelee import color as C
from peelee import peelee as P

from viiv.generators.nvim import generate_nvim_themes
from viiv.utils import load_config_json, load_json_file

# Load .env file
load_dotenv()

logger.remove()

MAX_ATTEMPTS_CONVERT_TO_BEST_COLOR = 6

# slice colors total
SLICE_COLORS_TOTAL = 100

# reserved constants
TOKEN_COLOR_PREFIX = "T_"
WORKBENCH_COLOR_PREFIX = "W_"
PLACEHOLDER_REGEX = r"C_[a-zA-Z0-9]{2}_[a-zA-Z0-9]{2,4}"
PLACEHOLDER_REGEX_WITHOUT_ALPHA = r"C_[a-zA-Z0-9]{2}_[a-zA-Z0-9]{2}"
PLACEHOLDER_REGEX_WITH_ALPHA = r"C_[a-zA-Z0-9]{2}_[a-zA-Z0-9]{2}[a-zA-Z0-9]{2}"
RGB_HEX_REGEX = r"#[a-zA-Z0-9]{6,8}"
RGB_HEX_REGEX_WITHOUT_ALPHA = r"#[a-zA-Z0-9]{6}"
RGB_HEX_REGEX_WITH_ALPHA = r"#[a-zA-Z0-9]{8}"
LIGHT_BOLD_TOKEN_SCOPE_REGEX_DEFAULT = r".*(keyword|type).*"

HEX_NUMBER_STR_PATTERN = re.compile(r"^0x[0-9a-zA-Z]+$")

THEME_TEMPLATE_JSON_FILE = f"{os.getcwd()}/templates/viiv-color-theme.template.json"
PALETTE_FILE_PATH = f"{os.getcwd()}/output/random-palette.json"
SELECTED_UI_COLOR_FILE_PATH = f"{os.getcwd()}/output/selected-ui-palette.json"
SELECTED_TOKEN_COLOR_FILE_PATH = f"{os.getcwd()}/output/selected-token-palette.json"

DEFAULT_DECORATION_COLORS = ["#ffa500", "#00b300", "#008b8b"]
DEFAULT_HIGHLIGHT_BG_COLORS = ["#ffa500", "#00b300", "#008b8b"]


class ThemeMode(Enum):
    """Enum representing the theme mode."""

    LIGHT = "Light"
    DARK = "Dark"
    RANDOM = "Random"


class ColorComponent(Enum):
    """
    Enum representing different components of a color.

    The enum includes the following values:
        - BASIC: Represents the basic color components (red, green, blue).
        - LIGHT: Represents the components of a lighter version of the color (light red, light green, light blue).
        - ALPHA: Represents the alpha component of the color.
        - ALL: Represents all components of the color.

    Example usage:
        If you want to access the basic color component of a color object:
            color = (255, 128, 0, 255)  # represents a fully opaque orange color
            red_component = color[ColorComponent.BASIC.value]  # returns 255, the value of the red component
    """

    BASIC = 1
    LIGHT = 2
    ALPHA = 3
    ALL = 4


class MatchRule(Enum):
    """Match rule for color range."""

    EXACT = 1
    ENDSWITH = 2
    STARTSWITH = 3
    CONTAINS = 4
    FUZZY = 5


def _to_int(value: str) -> int:
    """Convert string to int, handling hex format.

    Args:
        value: String value to convert, can be hex format (0x...) or regular int.

    Returns:
        Integer value.
    """
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and (HEX_NUMBER_STR_PATTERN.match(value)):
        return int(value, 16)
    return int(value)


def is_property_area(area):
    """Check if the area is a property area.

    Args:
        area: Area name to check.

    Returns:
        bool: True if area is 'background' or 'foreground'.
    """
    return area in ["background", "foreground"]


def normalize_range(range_values: list[str]) -> list[str]:
    """Generate normalized range values with zero-padding.

    Converts a range of integers to zero-padded string format.
    Numbers less than 10 are prefixed with '0'.

    Args:
        range_values: List containing start and end values.

    Returns:
        List of zero-padded string values.

    Example:
        normalize_range([1, 12]) -> ['01', '02', ..., '11']
    """
    _random = []
    _start = _to_int(range_values[0])
    _end = _to_int(range_values[1])
    for i in range(_start, _end):
        _random.append(str(i) if i >= 10 else str("0" + str(i)))
    return _random


class ColorsWrapper(dict):
    """Wrapper class for the generated color identifiers or color 'hex' code.

    The color identifiers or color 'hex' code will be put in the 'colors' list. The color identifiers will be replaced with the actual color values. The 'hex' code could be appened with alpha value(if it doesn't include alpha value) and then used in the final theme directly.
    """

    def __init__(
        self,
        colors: list,
        area: str,
        group: str,
        replace_color_component: Optional[list] = None,
    ):
        self.colors = colors
        self.area = area
        self.group = group
        self.replace_color_component = replace_color_component or [ColorComponent.ALL]
        super().__init__(
            colors=colors,
            group=group,
            area=area,
            replace_color_component=replace_color_component,
        )


class ColorConfig(dict):
    """Wrapper class for color configuraton.

    One color configuration consists of hex, color ranges for basic, light, and alpha.
    If hex is given, then basic and light ranges will be ignored.
    One color can generate multiple colors by using hex or basic and light ranges, together with alpha range.

    If the hex is given, then the generated color hex values could be "#efefef3e". Otherwise, it could be "C_11_343e".
    The first format is used directly in final theme config file.
    The 2nd one is used in theme template file and will be replaced with the auto-generated color hex value.

    The Color is configured in config.json file. It's content could be like:
    {
        "hex": "#008000",
        "alpha_range": [
            "0x99",
            "0xcc"
        ]
    }
    or
    {
        "basic_range": [
            11,
            12
        ],
        "light_range": [
            59,
            60
        ],
        "alpha_range": [
            "0x99",
            "0xcc"
        ]
    }
    """

    def __init__(
        self,
        color_config,
        area,
        group,
        replace_color_component: Optional[typing.List[ColorComponent]] = None,
    ):
        self.color_config = color_config
        self.area = area
        self.group = group
        self.replace_color_component = replace_color_component or [ColorComponent.ALL]
        self.hex = color_config.get("hex", None)
        self.alpha_range = color_config.get("alpha_range", None)
        self.basic_range = color_config.get("basic_range", None)
        self.light_range = color_config.get("light_range", None)
        super().__init__(color_config=self.color_config)

    def __repr__(self):
        return f"Color({self.color_config})"

    def create_colors_wrapper(self) -> ColorsWrapper:
        """Generate colors by using hex or basic and light ranges in the color configuration. This is one of the core functions.

        Here, 'color' could be the 'hex' color code or the color placeholder identifier such as "C_11_343e".
        If the hex is given, then the generated color hex values could be "#efefef3e". Otherwise, it could be "C_11_343e".
        If it's color is a placeholder, then it will be replaced with the generated color. For example, "C_11_343e" could be replaced with "#efefef3e". The color value replacement is generated by Palette from the module 'peelee'.

        If the hex is given, then the generated color hex values could be "#efefef3e". Otherwise, it could be "C_11_343e". The first format is used directly in final theme config file. The 2nd one is used in theme template file and will be replaced with the auto-generated color hex value.

        NOTE: If 'hex' is given, then 'basic_range' and 'light_range' will be ignored.

        The Color is configured in config.json file.

        Example:
        Given the following color configuration:
        {
            "alpha_range": [
                "0x99",
                "0xcc"
            ],
            "basic_range": [
                10,
                12
            ],
            "light_range": [
                50,
                60
            ]
        }
        The generated colors would include the following color identifiers:
        ["C_10_5099", "C_11_5099", "C_11_51aa", "C_12_5099", "C_12_51aa"]
        But it will have much more because the alpha range is from 0x99 to 0xcc, and light range is from 50 to 60.

        """
        has_hex = self.hex is not None
        has_alpha = (
            self.alpha_range is not None and len(self.alpha_range) == 2 and self.alpha_range[0] < self.alpha_range[1]
        )
        has_basic = (
            self.basic_range is not None and len(self.basic_range) == 2 and self.basic_range[0] < self.basic_range[1]
        )
        has_light = (
            self.light_range is not None and len(self.light_range) == 2 and self.light_range[0] < self.light_range[1]
        )

        if has_hex:
            _head = [self.hex]
        elif has_basic and has_light:
            _head = [
                "C_" + basic + "_" + light
                for basic in normalize_range(self.basic_range)
                for light in normalize_range(self.light_range)
            ]
        else:
            _head = ["#000000"]

        if has_alpha:
            _tail = []
            for alpha in normalize_range(self.alpha_range):
                alpha = format(int(alpha), "x")
                if len(alpha) == 1:
                    alpha = "0" + alpha
                _tail.append(alpha)
        else:
            _tail = [""]
        _colors = [f"{head}{tail}" for head in _head for tail in _tail]

        _wrapper = ColorsWrapper(_colors, self.area, self.group, self.replace_color_component)
        return _wrapper


class Config(dict):
    """Wrapper class for color config

    Read and parse config.json file located in the current directory.
    """

    def __init__(self, config_path=None):
        """Read config.json file and initialize."""
        if config_path is None:
            config_path = os.getenv("VIIV_CONFIG_PATH")
        if config_path is None:
            self.config = load_config_json()
        else:
            self.config = load_json_file(config_path)
        self.areas = list(filter(lambda k: k not in ["options", "themes"], self.config.keys()))
        # global default, token default, decoration default
        default_color_config = list(
            filter(
                lambda x: "default" in x["groups"],
                self.config["default"],
            )
        )[0]
        default_token_color_config = list(
            filter(
                lambda x: len(x["groups"]) == 1 and x["groups"][0] == "default",
                self.config["token"],
            )
        )[0]
        default_decoration_color_config = list(
            filter(
                lambda x: len(x["groups"]) == 1 and x["groups"][0] == "default",
                self.config["decoration"],
            )
        )[0]
        default_highlight_background_color_config = list(
            filter(
                lambda x: len(x["groups"]) == 1 and x["groups"][0] == "default",
                self.config["highlight_background"],
            )
        )[0]
        self.default_color_config = ColorConfig(
            default_color_config["color"], "default", default_color_config["groups"][0]
        )
        self.default_token_color_config = ColorConfig(
            default_token_color_config["color"],
            "token",
            default_token_color_config["groups"][0],
        )
        self.default_decoration_color_config = ColorConfig(
            default_decoration_color_config["color"],
            "decoration",
            default_decoration_color_config["groups"][0],
        )
        self.default_highlight_background_color_config = ColorConfig(
            default_highlight_background_color_config["color"],
            "highlight_background",
            default_highlight_background_color_config["groups"][0],
        )
        assert (
            self.default_decoration_color_config.basic_range is not None
            and len(self.default_decoration_color_config.basic_range) == 2
        ), "Basic range of the default group of 'decoration' area is not configured."
        # the maximum end value of basic range of the default group of
        # 'decoration' area is the sum value of the token colors total and the
        # workbench colors total as it could be the result of the random int
        # and it will be used as the start value of the basic range of the
        # default group of 'decoration' area and plus 1 to it will be used as
        # the end value of the basic range of the default group of
        # 'decoration' area - this will make the decoration color be static in basic color range - we want to have the same decoration color
        # decoration color in config.json file is use to control the color of the decoration group, it's value will be used to set the groups in 'decoration' area
        random_decoration_basic_range_min = random.randint(
            self.default_decoration_color_config.basic_range[0],
            self.default_decoration_color_config.basic_range[1],
        )
        self.default_decoration_color_config.basic_range = [
            random_decoration_basic_range_min,
            random_decoration_basic_range_min + 1,
        ]
        self.options = self.config["options"]
        self.decoration_groups = []
        self.highlight_background_groups = []
        self.ansi_groups = []
        for area in self.areas:
            for color_config in self.config[area]:
                groups = color_config["groups"]
                if "decoration" in groups:
                    self.decoration_groups.extend(groups)
                elif "highlight_background" in groups:
                    self.highlight_background_groups.extend(groups)
        for area in self.areas:
            for color_config in self.config[area]:
                groups = color_config["groups"]
                ansi_groups = list(filter(lambda x: x.startswith("ansi"), groups))
                if len(ansi_groups) > 0:
                    self.ansi_groups.extend(groups)

        super().__init__(
            config=self.config,
            areas=self.areas,
            default_color=self.default_color_config,
            default_token_color=self.default_token_color_config,
            decoration_groups=self.decoration_groups,
            highlight_background_groups=self.highlight_background_groups,
            ansi_groups=self.ansi_groups,
        )

    def get_color_wrappers(self, target_property, target_area=None) -> list:
        """Go through the config items in the basic groups and set the color by checking if the given 'group' contains the key of the groups.

        content example of basic groups:
        {
            "group": [
                "success",
                "add"
            ],
            "color": {
                "hex": "#008000",
                "alpha_range": [
                    "0x99",
                    "0xcc"
                ]
            }
        }

        Parameters:
            target (str): target group or target color perperty


        Retrun :
            Color object include area info, only those color perperty belong to that area can use that color. Color for backkground cannot be used by foreground color perperty.
            If not found, return the default color.
        """
        _matched_color_configs = self._find_matched_color_configs(target_property, target_area)
        color_wrappers = self._create_color_wrappers_from_configs(_matched_color_configs)

        if len(color_wrappers) > 0:
            return color_wrappers

        return self._get_default_color_wrappers(target_area)

    def _find_matched_color_configs(self, target_property, target_area):
        """Find matched color configurations for the target property."""
        _matched_color_configs = []
        for area in self.areas:
            if target_area and area != target_area:
                continue
            if is_property_area(area) and target_property.lower().find(area) == -1:
                continue
            # try to find the configured color in the matching order
            _matched_color_config_dict = self._get_color(area, target_property)

            if _matched_color_config_dict and _matched_color_config_dict not in _matched_color_configs:
                _matched_color_configs.append(_matched_color_config_dict)
        return _matched_color_configs

    def _create_color_wrappers_from_configs(self, _matched_color_configs):
        """Create color wrappers from matched configurations."""
        color_wrappers = []
        if _matched_color_configs:
            default_area_matched_color_configs = list(filter(lambda x: x["area"] == "default", _matched_color_configs))
            if default_area_matched_color_configs:
                _matched_color_configs = default_area_matched_color_configs

            # clever code?
            most_matched_color_config = min(
                list(
                    filter(
                        lambda c: c["color_config"] is not None,
                        _matched_color_configs,
                    )
                ),
                key=lambda x: x["match_rule"].value,
            )

            if most_matched_color_config:
                color_wrappers.append(most_matched_color_config["color_config"].create_colors_wrapper())
        return color_wrappers

    def _get_default_color_wrappers(self, target_area):
        """Get default color wrappers based on target area."""
        color_wrappers = []
        if target_area is None or target_area != "token":
            color_wrappers.append(self.default_color_config.create_colors_wrapper())
        else:
            color_wrappers.append(self.default_token_color_config.create_colors_wrapper())
        assert len(color_wrappers) > 0, f"no color found ({target_area})"
        return color_wrappers

    def match(self, groups, target_property):
        """Match the target property with the group.

        By using all MatchRules to check if the target property matches any group in the groups.
        If multiple groups matched the target property, then pick up the one using match rule having the least value(which means highest priority).

        Parameters:
            group (str): group name
            target_property (str): target property

        Returns:
            dict: the matched group and the matched rule

            Example of the return value:
                {
                    "match_rule": MatchRule.FUZZY,
                    "group": "success"
                }
        """
        matched_groups = []
        groups = sorted(groups, reverse=True)
        for match_rule in MatchRule:
            for group in groups:
                if (
                    match_rule == MatchRule.EXACT
                    and target_property.lower() == group.lower()
                    or match_rule == MatchRule.ENDSWITH
                    and target_property.lower().endswith(f".{group.lower()}")
                    or match_rule == MatchRule.STARTSWITH
                    and target_property.lower().startswith(f"{group.lower()}.")
                    or match_rule == MatchRule.CONTAINS
                    and target_property.lower().find(group.lower()) != -1
                    or match_rule == MatchRule.FUZZY
                    and re.match(group, target_property, re.IGNORECASE)
                ):
                    matched_groups.append({"match_rule": match_rule, "group": group})
        if not matched_groups:
            return None

        return min(matched_groups, key=lambda x: x["match_rule"].value)

    def _get_replace_color_component(self, area, groups_config):
        """Get the replace color component.

        replace_color_component is a list of ColorComponent. it's an optional property of the groups config. by default, for all areas except for 'default', it's set to [ColorComponent.ALL] and for 'default' area, it's set to [ColorComponent.ALPHA].
        """
        replace_color_component = groups_config.get("replace_color_component")
        if replace_color_component is not None and isinstance(replace_color_component, list):
            replace_color_component = [ColorComponent[_component] for _component in replace_color_component]
        else:
            replace_color_component = [ColorComponent.ALL] if area != "default" else [ColorComponent.ALPHA]
        return replace_color_component

    def _get_color(self, area, target_property) -> dict:
        """Get the color config.

        Each area has many color configurations for different groups.
        Each group could match one or many different color properties.
        By going through all color configurations in the given area,
        and then check if any group in each color configuration matched
        the target property by using different matching rules.
        Finally, if multiple groups matched the target property,
        then pick up the one using match rule having the least matching
        rule value (which means highest priority).
        If no any group matched the target property,
        then return None which means there is no color config matching
        the target property in this area. For example, 'background' area
        cannot have any color config to match 'activityBar.foreground'.

        Matching rule will be returned also. Then if many areas have matched
        color config for the target property, then pick up the one with
        the least matching rule. If the same, then print warning for duplicated
        configuration and pickup the first one.

        Parameters:

            area (str): area name
            target_property (str): target property

        Returns:
            dict: the matched group and the matched rule
        """
        area_config = self.config[area]
        _matches = []
        for groups_config in area_config:
            enabled = groups_config.get("enabled", True)
            if not enabled:
                continue
            groups = groups_config["groups"]
            groups.sort(reverse=True)
            _match = self.match(groups, target_property)
            if _match:
                color = groups_config["color"]
                replace_color_component = self._get_replace_color_component(area, groups_config)
                _match["color"] = color
                _match["replace_color_component"] = replace_color_component
                _matches.append(_match)

        if not _matches:
            return {}

        _most_matched_config = min(_matches, key=lambda x: x["match_rule"].value)
        color = _most_matched_config["color"]
        group = _most_matched_config["group"]
        # decoration groups will use default decoration color's hex and basic
        # range if they are not configured specicifically
        if group in self.decoration_groups:
            color["hex"] = color.get("hex", self.default_decoration_color_config.hex)
            color["basic_range"] = color.get("basic_range", self.default_decoration_color_config.basic_range)
        elif group in self.highlight_background_groups:
            color["hex"] = color.get("hex", self.default_highlight_background_color_config.hex)
            color["basic_range"] = color.get(
                "basic_range",
                self.default_highlight_background_color_config.basic_range,
            )

        replace_color_component = _most_matched_config["replace_color_component"]
        color_config = ColorConfig(color, area, group, replace_color_component)
        return {
            "color_config": color_config,
            "match_rule": _most_matched_config["match_rule"],
            "area": area,
        }


CONFIG = Config()

DARK_MODE_WORKBENCH_FOREGROUND_COLOR_MIN_CONTRAST_RATIO = CONFIG.options[
    "dark_mode_workbench_foreground_color_min_contrast_ratio"
]
DARK_MODE_WORKBENCH_FOREGROUND_COLOR_MAX_CONTRAST_RATIO = CONFIG.options[
    "dark_mode_workbench_foreground_color_max_contrast_ratio"
]
TOKEN_FOREGROUND_COLOR_MIN_CONTRAST_RATIO = CONFIG.options["token_foreground_color_min_contrast_ratio"]
TOKEN_FOREGROUND_COLOR_MAX_CONTRAST_RATIO = CONFIG.options["token_foreground_color_max_contrast_ratio"]
WORKBENCH_BACKGROUND_COLOR_MIN_CONTRAST_RATIO = CONFIG.options["highlight_background_color_min_contrast_ratio"]
WORKBENCH_BACKGROUND_COLOR_MAX_CONTRAST_RATIO = CONFIG.options["highlight_background_color_max_contrast_ratio"]
DARK_MODE_BACKGROUND_COLOR_MIN_CONTRAST_RATIO = CONFIG.options["dark_mode_background_color_min_contrast_ratio"]
DARK_MODE_BACKGROUND_COLOR_MAX_CONTRAST_RATIO = CONFIG.options["dark_mode_background_color_max_contrast_ratio"]
LIGHT_MODE_WORKBENCH_FOREGROUND_COLOR_MIN_CONTRAST_RATIO = CONFIG.options[
    "light_mode_workbench_foreground_color_min_contrast_ratio"
]
LIGHT_MODE_WORKBENCH_FOREGROUND_COLOR_MAX_CONTRAST_RATIO = CONFIG.options[
    "light_mode_workbench_foreground_color_max_contrast_ratio"
]
LIGHT_MODE_BACKGROUND_COLOR_MIN_CONTRAST_RATIO = CONFIG.options["light_mode_background_color_min_contrast_ratio"]
LIGHT_MODE_BACKGROUND_COLOR_MAX_CONTRAST_RATIO = CONFIG.options["light_mode_background_color_max_contrast_ratio"]
DECORATION_COLOR_CONTRAST_RATIO_MIN = CONFIG.options["decoration_color_contrast_ratio_min"]
DECORATION_COLOR_CONTRAST_RATIO_MAX = CONFIG.options["decoration_color_contrast_ratio_max"]
DEBUG_PROPERTIES = CONFIG.options["debug_properties"]
DEBUG_GROUPS = CONFIG.options["debug_groups"]
IS_AUTO_ADJUST_CONTRAST_RADIO_ENABLED = CONFIG.options["is_auto_adjust_contrast_radio_enabled"]
AUTO_TUNE_EDITOR_BACKGROUND_RATIO = CONFIG.options.get("auto_tune_editor_background_ratio", False)


def log_property_trace(property_name: str, *args) -> None:
    """Log trace information for properties if enabled in DEBUG_PROPERTIES.

    Args:
        property_name: The property name to check against DEBUG_PROPERTIES.
        *args: Additional arguments to log.
    """
    if property_name in DEBUG_PROPERTIES:
        logger.trace(f"{property_name}, {args}")


logger.add(
    sys.stderr,
    level=os.getenv("LOG_LEVEL", CONFIG.options.get("log_level", "INFO")).upper(),
    colorize=True,
)


class Template(dict):
    """Wrapper class for template config."""

    def __init__(self, template_path=None):
        if template_path is None:
            template_path = THEME_TEMPLATE_JSON_FILE
        self.template_path = template_path
        self.template = load_json_file(template_path)
        self.color_properties = list(self.template["colors"].keys())
        super().__init__(config_path=template_path)

    def append_or_replace_alpha(self, old_color, new_color, component: ColorComponent):
        """
        Append or replace the alpha component of a color.

        Args:
            old_color (str): The original color string.
            new_color (str): The new color string.
            component (ColorComponent): The color component to be replaced or appended.

        Returns:
            str: The updated color string.

        """
        _color = None
        if component == ColorComponent.ALPHA:
            _color = old_color[0:7] + new_color[7:9]
        elif re.match(RGB_HEX_REGEX, old_color):
            # if it's already RGB HEX color, then cannot replace basic and light color with color placeholder. so, return directly
            return old_color
        elif component == ColorComponent.LIGHT:
            _color = old_color[0:5] + new_color[5:7] + old_color[7:]
        elif component == ColorComponent.BASIC:
            _color = old_color[0:2] + new_color[2:5] + old_color[5:]

        return _color

    def generate_template(self, config: Optional[Config] = None, **kwargs):
        """
        Generates a template based on the provided configuration.

        Args:
            config (Config, optional): The configuration object. Defaults to None.

        Returns:
            None
        """
        if config is None:
            config = Config()

        workbench_colors: dict = {}
        default_processed_properties: list[str] = []
        customized_properties: list[str] = []
        used_groups: list[str] = []

        # Setup decoration and highlight colors
        decoration_hex_color, highlight_background_color = self._setup_override_colors(kwargs)

        # Process workbench colors
        self._process_workbench_colors(
            config,
            workbench_colors,
            default_processed_properties,
            customized_properties,
            used_groups,
            decoration_hex_color,
            highlight_background_color,
        )

        workbench_colors = dict(sorted(workbench_colors.items(), key=lambda x: x[0]))
        self.template["colors"] = workbench_colors

        # Process token colors
        self._process_token_colors(config, used_groups)

        # Save results
        output_dir = kwargs.get("output_dir", None)
        theme_name = kwargs.get("theme_name", "default")
        self._save_template_results(config, used_groups, output_dir=output_dir, theme_name=theme_name)

    def _setup_override_colors(self, kwargs):
        """Setup decoration and highlight background override colors."""
        decoration_hex_colors = kwargs.get("decoration_hex_colores", None)
        if kwargs.get("use_default_decoration_hex_colores", False):
            decoration_hex_colors = DEFAULT_DECORATION_COLORS
        decoration_hex_color = None
        if decoration_hex_colors:
            if isinstance(decoration_hex_colors, str):
                decoration_hex_color = decoration_hex_colors
            elif isinstance(decoration_hex_colors, list):
                decoration_hex_color = random.choice(decoration_hex_colors)

        highlight_background = kwargs.get("highlight_background", None)
        if kwargs.get("use_default_highlight_background", False):
            highlight_background = DEFAULT_HIGHLIGHT_BG_COLORS
        highlight_background_color = None
        if highlight_background:
            if isinstance(highlight_background, str):
                highlight_background_color = highlight_background
            elif isinstance(highlight_background, list):
                highlight_background_color = random.choice(highlight_background)

        return decoration_hex_color, highlight_background_color

    def _process_workbench_colors(
        self,
        config,
        workbench_colors,
        default_processed_properties,
        customized_properties,
        used_groups,
        decoration_hex_color,
        highlight_background_color,
    ):
        """Process workbench colors from template."""
        for property_name in self.color_properties:
            color_wrappers = config.get_color_wrappers(property_name)
            if color_wrappers is None or not isinstance(color_wrappers, list):
                continue
            color_wrappers_areas = [w.area for w in color_wrappers]
            if property_name in default_processed_properties and "default" not in color_wrappers_areas:
                continue

            self._process_single_workbench_color(
                property_name,
                color_wrappers,
                config,
                workbench_colors,
                default_processed_properties,
                customized_properties,
                used_groups,
                decoration_hex_color,
                highlight_background_color,
            )

    def _process_single_workbench_color(
        self,
        property_name,
        color_wrappers,
        config,
        workbench_colors,
        default_processed_properties,
        customized_properties,
        used_groups,
        decoration_hex_color,
        highlight_background_color,
    ):
        """Process a single workbench color property."""
        debug_property_counter = 0
        debug_group_counter = 0
        for wrapper in color_wrappers:
            colors = wrapper.colors
            replace_color_component = wrapper.replace_color_component
            group = wrapper.group
            area = wrapper.area
            # we are not processing the token color here
            if area == "token":
                continue

            # if group is in decoration groups, and decoration color is passed
            # by argument, then use it to override the configuration
            color = colors[random.randint(0, len(colors) - 1)]
            color = self._apply_color_overrides(color, group, config, decoration_hex_color, highlight_background_color)
            color_orig = color

            color = self._handle_existing_workbench_color(
                property_name,
                workbench_colors,
                color,
                color_orig,
                replace_color_component,
                area,
                customized_properties,
                group,
            )

            self._log_debug_info(
                property_name,
                area,
                group,
                color,
                replace_color_component,
                color_wrappers,
                debug_property_counter,
                debug_group_counter,
            )

            self._update_processing_lists(
                property_name,
                area,
                group,
                default_processed_properties,
                customized_properties,
                used_groups,
            )

            workbench_colors[property_name] = color

    def _apply_color_overrides(self, color, group, config, decoration_hex_color, highlight_background_color):
        """Apply color overrides for decoration and highlight background groups."""
        if (
            group in config.decoration_groups
            and decoration_hex_color
            and re.match(RGB_HEX_REGEX_WITHOUT_ALPHA, decoration_hex_color)
        ):
            color = decoration_hex_color + color[7:9]
        elif (
            group in config.highlight_background_groups
            and highlight_background_color
            and re.match(RGB_HEX_REGEX_WITHOUT_ALPHA, highlight_background_color)
        ):
            color = highlight_background_color + color[7:9]
        return color

    def _handle_existing_workbench_color(
        self,
        property_name,
        workbench_colors,
        color,
        color_orig,
        replace_color_component,
        area,
        customized_properties,
        group,
    ):
        """Handle existing workbench color replacement logic."""
        if property_name in workbench_colors:
            if property_name in customized_properties:
                return color
            if area not in ["default", "token"]:
                return color
            old_color = workbench_colors[property_name]
            _changed = False
            if ColorComponent.BASIC in replace_color_component:
                color = self.append_or_replace_alpha(
                    old_color if not _changed else color,
                    color_orig,
                    ColorComponent.BASIC,
                )
                _changed = True
            if ColorComponent.LIGHT in replace_color_component:
                color = self.append_or_replace_alpha(
                    old_color if not _changed else color,
                    color_orig,
                    ColorComponent.LIGHT,
                )
                _changed = True
            if ColorComponent.ALPHA in replace_color_component:
                color = self.append_or_replace_alpha(
                    old_color if not _changed else color,
                    color_orig,
                    ColorComponent.ALPHA,
                )
                _changed = True
            if ColorComponent.ALL in replace_color_component or property_name == group:
                color = color_orig
        return color

    def _log_debug_info(
        self,
        property_name,
        area,
        group,
        color,
        replace_color_component,
        color_wrappers,
        debug_property_counter,
        debug_group_counter,
    ):
        """Log debug information for color processing."""
        if property_name in DEBUG_PROPERTIES:
            debug_property_counter += 1
            logger.debug(
                f"DEBUG_PROPERTY[{debug_property_counter}]: {property_name} -> {area} -> {group} -> {color} -> {replace_color_component} -> {len(color_wrappers)}"
            )
        if group in DEBUG_GROUPS:
            debug_group_counter += 1
            logger.debug(
                f"DEBUG_GROUP[{debug_group_counter}]: {group} -> {property_name} -> {area} -> {color} -> {replace_color_component} -> {len(color_wrappers)}"
            )

    def _update_processing_lists(
        self,
        property_name,
        area,
        group,
        default_processed_properties,
        customized_properties,
        used_groups,
    ):
        """Update processing tracking lists."""
        if area == "default" and group != "default":
            default_processed_properties.append(property_name)
        if group == property_name:
            customized_properties.append(property_name)
        if group not in used_groups:
            used_groups.append(group)

    def _process_token_colors(self, config, used_groups):
        """Process token colors from template."""
        token_configs = self.template["tokenColors"]
        new_token_configs = []
        for token_config in token_configs:
            scope = token_config["scope"]
            color_wrappers = config.get_color_wrappers(scope, target_area="token")
            assert len(color_wrappers) == 1, f"how can we get multiple color wrappers for token ({scope})?"
            color_wrapper = color_wrappers[0]
            _colors = color_wrapper.colors
            new_color = _colors[random.randint(0, len(_colors) - 1)]
            new_token_configs.append({"scope": scope, "settings": {"foreground": new_color}})
            group = color_wrapper.group
            if group not in used_groups:
                used_groups.append(group)

        new_token_configs.sort(key=lambda x: x["scope"])
        self.template["tokenColors"] = new_token_configs

    def _save_template_results(
        self,
        config,
        used_groups,
        output_dir,
        theme_name="default",
        palette_root_dir=None,
    ):
        """Save template and related files."""
        if palette_root_dir is None:
            palette_root_dir = f"{output_dir}/tmp/" if output_dir else "./"

        if not os.path.exists(palette_root_dir):
            os.makedirs(palette_root_dir, exist_ok=True)

        _dump_json_file(self.template_path, self.template)

        lower_theme_name = theme_name.lower().replace(" ", "-")
        _dump_json_file(f"{palette_root_dir}{lower_theme_name}-used_groups.json", used_groups)

        # clever code?!
        all_groups = sorted(list(set((c for a in config.areas for g in config.config[a] for c in g["groups"]))))
        _dump_json_file(f"{palette_root_dir}{lower_theme_name}-all_groups.json", all_groups)

        # good auto-completion
        _dump_json_file(
            f"{palette_root_dir}{lower_theme_name}-not_used_groups.json",
            [x for x in all_groups if x not in used_groups],
        )


def _dump_json_file(json_file_path, json_data):
    """Write JSON data to file.

    Args:
        json_file_path: Path to the JSON file.
        json_data: Data to write to the file.
    """
    if not os.path.exists(os.path.dirname(json_file_path)):
        parent_path = Path(json_file_path).parent
        os.makedirs(parent_path, exist_ok=True)
        if not os.path.exists(parent_path):
            logger.error("Failed to create output directory '%s'.", parent_path)
            return
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)
    logger.info(f"Dump file: {json_file_path}")


def show_theme_colors(filter_value, theme="random", themes_dir=None):
    """Display theme colors to console.

    Args:
        filter_value: Filter string to match color names.
        theme: Theme name to display colors from.
        themes_dir: Directory path where theme files are located.
    """
    assert theme is not None, "Please provide theme name."

    if themes_dir is None:
        themes_dir = os.path.join(os.path.dirname(__file__), "..", "themes")

    theme_json_file_path = f"{themes_dir}/{theme}-color-theme.json"
    random_theme_json = load_json_file(theme_json_file_path)
    theme_template_json = load_json_file(THEME_TEMPLATE_JSON_FILE)
    colors = random_theme_json["colors"]
    for k, v in colors.items():
        if k.lower().find(filter_value) != -1 or re.match(f".*{filter_value}.*", k, re.IGNORECASE):
            logger.info(P.bg(v, f"{k}: {v} ({theme_template_json['colors'][k]})"))


def show_palette(filter_value=None, palette_root_dir=None, theme_name="default"):
    """Display color palettes to console.

    Shows random palette, selected UI palette, and selected token palette.

    Args:
        filter_value: Optional filter to match specific colors.
        palette_root_dir: Directory path where palette files are located.
        theme_name: Theme name to use in file naming.
    """
    if filter_value is not None and len(filter_value.strip()) == 0:
        filter_value = None

    if palette_root_dir is None:
        palette_root_dir = os.path.join(os.path.dirname(__file__), "..", "..", "tmp")
    if not os.path.exists(palette_root_dir):
        logger.error("Palette root directory '%s' does not exist.", palette_root_dir)
        return
    lower_theme_name = theme_name.lower().replace(" ", "-")

    palette_json_file = f"{palette_root_dir}/{lower_theme_name}-palette.json"
    with open(palette_json_file, "r", encoding="utf-8") as file:
        random_palette_json = json.load(file)
    for k, v in random_palette_json.items():
        if filter_value and k != filter_value and not re.match(f".*{filter_value}.*", k, re.IGNORECASE):
            continue
        logger.info(P.bg(v["hex"], f"{k}: {v}"))

    logger.info("\nSelected UI Palette:")
    selected_ui_file_path = f"{palette_root_dir}/{lower_theme_name}-selected-ui-palette.json"
    with open(selected_ui_file_path, encoding="utf-8") as selected_ui_file:
        selected_ui_palette_json = json.load(selected_ui_file)
        for k, v in selected_ui_palette_json.items():
            if filter_value and k != filter_value and not re.match(f".*{filter_value}.*", k, re.IGNORECASE):
                continue
            logger.info(P.bg(list(v.values())[0]["hex"], f"{k}: {v}"))

    logger.info("\nSelected Token Palette:")
    selected_token_file_path = f"{palette_root_dir}/{lower_theme_name}-selected-token-palette.json"
    with open(selected_token_file_path, encoding="utf-8") as selected_token_file:
        selected_token_palette_json = json.load(selected_token_file)
        for k, v in selected_token_palette_json.items():
            if filter_value and k != filter_value and not re.match(f".*{filter_value}.*", k, re.IGNORECASE):
                continue
            logger.info(P.bg(list(v.values())[0]["hex"], f"{k}: {v}"))


# Note: convert_to_best_light_color and convert_to_best_dark_color functions
# are now imported from peelee.color to ensure consistency with b.themes
# frontend and preview theme generation


def _is_debug_property(property_name: str) -> bool:
    """Check if property is in DEBUG_PROPERTIES using fuzzy matching.

    Args:
        property_name: Property name to check.

    Returns:
        bool: True if property matches any DEBUG_PROPERTIES pattern.
    """
    return any(re.match(debug_prop, property_name, re.IGNORECASE) for debug_prop in DEBUG_PROPERTIES)


def is_foreground_property(property_name):
    """Check if property is a foreground property.

    Args:
        property_name: Property name to check.

    Returns:
        bool: True if property is a foreground property.
    """
    if _is_debug_property(property_name):
        logger.debug(f"Checking is_foreground_property for DEBUG_PROPERTY: {property_name}")

    _match = CONFIG.match(CONFIG.options["workbench_foreground_properties"], property_name)

    if _is_debug_property(property_name):
        logger.debug(f"DEBUG_PROPERTY {property_name} foreground match result: {_match}")

    return _match is not None


def is_background_property(property_name):
    """Check if property is a workbench background property.

    Args:
        property_name: Property name to check.

    Returns:
        bool: True if property is a workbench background property.
    """
    if _is_debug_property(property_name):
        logger.debug(f"Checking is_background_property for DEBUG_PROPERTY: {property_name}")

    _match = CONFIG.match(CONFIG.options["workbench_background_properties"], property_name)

    if _is_debug_property(property_name):
        logger.debug(f"DEBUG_PROPERTY {property_name} background match result: {_match}")

    return _match is not None


def is_highlight_background_property(property_name):
    """Check if property is a highlight background property.

    Args:
        property_name: Property name to check.

    Returns:
        bool: True if property is a highlight background property.
    """
    if _is_debug_property(property_name):
        logger.debug(f"Checking is_highlight_background_property for DEBUG_PROPERTY: {property_name}")

    for group in CONFIG.highlight_background_groups:
        if re.match(group, property_name, re.IGNORECASE):
            if _is_debug_property(property_name):
                logger.debug(f"DEBUG_PROPERTY {property_name} matched highlight_background group: {group}")
            return True
    return False


def is_exemption_property(property_name):
    """Check if property is exempt from contrast ratio adjustment.

    Args:
        property_name: Property name to check.

    Returns:
        bool: True if property is exempt from contrast adjustment.
    """
    if _is_debug_property(property_name):
        logger.debug(f"Checking is_exemption_property for DEBUG_PROPERTY: {property_name}")

    _match = list(
        filter(
            lambda x: re.match(x, property_name, re.IGNORECASE),
            CONFIG.options["exemption_contrast_ratio_adjustment_properties"],
        )
    )

    if _is_debug_property(property_name):
        logger.debug(f"DEBUG_PROPERTY {property_name} exemption matches: {_match}")

    return len(_match) > 0


def is_decoration_property(property_name):
    """Check if property is a decoration property.

    Args:
        property_name: Property name to check.

    Returns:
        bool: True if property is a decoration property.
    """
    if _is_debug_property(property_name):
        logger.debug(f"Checking is_decoration_property for DEBUG_PROPERTY: {property_name}")

    for group in CONFIG.decoration_groups:
        if re.match(group, property_name, re.IGNORECASE):
            if _is_debug_property(property_name):
                logger.debug(f"DEBUG_PROPERTY {property_name} matched decoration group: {group}")
            return True
    return False


def _determine_theme_mode(theme_mode_input: Optional[str]) -> ThemeMode:
    """Determine theme mode from input string.

    Args:
        theme_mode_input: Theme mode string input (can be None).

    Returns:
        ThemeMode: Determined theme mode (DARK, LIGHT, or randomly chosen).
    """
    if theme_mode_input is not None:
        theme_mode_input = theme_mode_input.upper()

    if theme_mode_input is None or ThemeMode[theme_mode_input] is ThemeMode.RANDOM:
        return ThemeMode.DARK if random.randint(0, 9999) % 2 == 0 else ThemeMode.LIGHT

    return ThemeMode[theme_mode_input]


def generate_random_theme_file(  # noqa: C901
    token_colors_total=7,
    token_colors_gradations_total=60,
    token_colors_min=120,
    token_colors_max=180,
    token_colors_saturation=0.35,
    token_colors_lightness=0.15,
    workbench_colors_total=7,
    workbench_colors_gradations_total=60,
    workbench_colors_min=19,
    workbench_colors_max=20,
    workbench_colors_saturation=0.2,
    workbench_colors_lightness=0.09,
    output_dir=None,
    **kwargs,
):
    """
    Generates a random theme file with specified parameters.

    Args:
        colors_total (int): The total number of colors.
        gradations_total (int): The total number of color gradations.
        dark_color_gradations_total (int): The total number of dark color gradations.
        general_min_color (int): The minimum color value. Best value: 60.
        general_max_color (int): The maximum color value. Best value: 180.
        dark_color_min (int): The minimum dark color value.
        dark_color_max (int): The maximum dark color value.
        dark_colors_total (int): The total number of dark colors.
        dark_base_colors (list): The list of dark base colors.
        theme_filename_prefix (str): The prefix for the theme filename.

    Best value values for general min and max: 60, 180.This range can generate
    full color used for token colors. Therefore, no need to change them or pass
    other values unless you know what you are doing.

    Good valus for dark colors min and max: 5, 15. The maximum value of dark colors max should be 30. No bigger value should be used unless for light-mode theme. When the range is changed, the values used in config.json might be tuned accordingly. With the configuration in v0.2.31, the best values are 15,20.

    Returns:
        None
    """
    if not output_dir:
        raise ValueError("output_dir is required and cannot be None or empty")
    if not os.path.exists(output_dir):
        raise ValueError(f"output_dir does not exist: {output_dir}")
    if not os.path.isdir(output_dir):
        raise ValueError(f"output_dir is not a directory: {output_dir}")

    # Determine theme mode
    theme_mode = _determine_theme_mode(kwargs.get("theme_mode"))
    random_int = random.randint(0, 9999)
    theme_name = kwargs.get("theme_name", f"ViiV-Random-{theme_mode.value}-{P.padding(random_int, 4)}")
    # Ensure theme_name is never None
    if theme_name is None:
        theme_name = f"ViiV-Random-{theme_mode.value}-{P.padding(random_int, 4)}"
    logger.info("")
    logger.info(f" >>>>>> GENERATING {theme_name} <<<<<<")
    logger.info((theme_name, theme_mode, type(theme_mode)))

    # it's possible that user pass decoration hex color
    decoration_hex_colores = kwargs.get("decoration_hex_colores")

    template_path = kwargs.get("template_path", None)
    template_config = Template(template_path=template_path)
    template_config.generate_template(
        decoration_hex_colores=decoration_hex_colores,
        output_dir=output_dir,
        theme_name=theme_name,
    )
    template_config_data = template_config.template
    workbench_base_background_color_name = kwargs.get("workbench_base_background_color_name", "RANDOM")
    workbench_colors_hue = kwargs.get("workbench_colors_hue")
    workbench_editor_background_color = kwargs.get("workbench_editor_background_color")
    workbench_editor_foreground_color = kwargs.get("workbench_editor_foreground_color")
    workbench_editor_background_color_id = kwargs.get("workbench_editor_background_color_id")
    # if theme mode is light, then set workbench_editor_background_color_id as value of light_mode_workbench_editor_background_color_id
    if theme_mode is ThemeMode.LIGHT:
        workbench_editor_background_color_id = kwargs.get("light_mode_workbench_editor_background_color_id")
        workbench_editor_background_color_id = P.padding(workbench_editor_background_color_id)
    workbench_editor_foreground_color_id = kwargs.get("workbench_editor_foreground_color_id")
    workbench_editor_foreground_color_id = P.padding(workbench_editor_foreground_color_id)
    color_gradations_division_rate = kwargs.get("color_gradations_division_rate")
    reversed_color_offset_rate = kwargs.get("reversed_color_offset_rate")
    dark_mode_background_color_min_contrast_ratio = kwargs.get("dark_mode_background_color_min_contrast_ratio")
    dark_mode_background_color_max_contrast_ratio = kwargs.get("dark_mode_background_color_max_contrast_ratio")
    highlight_background_color_max_contrast_ratio = kwargs.get("highlight_background_color_max_contrast_ratio")
    highlight_background_color_min_contrast_ratio = kwargs.get("highlight_background_color_min_contrast_ratio")
    light_mode_background_color_min_contrast_ratio = kwargs.get("light_mode_background_color_min_contrast_ratio")
    light_mode_background_color_max_contrast_ratio = kwargs.get("light_mode_background_color_max_contrast_ratio")
    dark_mode_workbench_foreground_color_min_contrast_ratio = kwargs.get(
        "dark_mode_workbench_foreground_color_min_contrast_ratio"
    )
    dark_mode_workbench_foreground_color_max_contrast_ratio = kwargs.get(
        "dark_mode_workbench_foreground_color_max_contrast_ratio"
    )
    light_mode_workbench_foreground_color_min_contrast_ratio = kwargs.get(
        "light_mode_workbench_foreground_color_min_contrast_ratio"
    )
    light_mode_workbench_foreground_color_max_contrast_ratio = kwargs.get(
        "light_mode_workbench_foreground_color_max_contrast_ratio"
    )
    token_foreground_color_min_contrast_ratio = kwargs.get("token_foreground_color_min_contrast_ratio")
    token_foreground_color_max_contrast_ratio = kwargs.get("token_foreground_color_max_contrast_ratio")
    decoration_color_contrast_ratio_min = kwargs.get("decoration_color_contrast_ratio_min", 6)
    decoration_color_contrast_ratio_max = kwargs.get("decoration_color_contrast_ratio_max", 9)
    is_auto_adjust_contrast_radio_enabled = kwargs.get("is_auto_adjust_contrast_radio_enabled")
    auto_tune_editor_background_ratio = kwargs.get("auto_tune_editor_background_ratio", False)
    force_to_use_workbench_editor_background_color = kwargs.get("force_to_use_workbench_editor_background_color")
    bold_token_scopes = kwargs.get("bold_token_scopes", [".*(keyword|type).*"])
    all_base_colors_total = token_colors_total + workbench_colors_total
    # NOTE: the theme mode value passed to Palette is str(ThemeMode.name) rather than Enum(ThemeMode)
    palette_color = kwargs.get("palette_color")
    palette_data = (
        palette_color
        or P.Palette(
            colors_total=token_colors_total,
            colors_gradations_total=token_colors_gradations_total,
            colors_min=token_colors_min,
            colors_max=token_colors_max,
            colors_saturation=token_colors_saturation,
            colors_lightness=token_colors_lightness,
            dark_colors_total=workbench_colors_total,
            dark_colors_gradations_total=workbench_colors_gradations_total,
            dark_colors_min=workbench_colors_min,
            dark_colors_max=workbench_colors_max,
            dark_colors_hue=workbench_colors_hue,
            dark_colors_saturation=workbench_colors_saturation,
            dark_colors_lightness=workbench_colors_lightness,
            dark_base_color=workbench_editor_background_color,
            dark_base_color_name=workbench_base_background_color_name,
            color_gradations_division_rate=color_gradations_division_rate,
            reversed_color_offset_rate=reversed_color_offset_rate,
            palette_mode=theme_mode.name,
        ).generate_palette()
    )
    orig_palette_data = palette_data.copy()

    # reverse the last 10 dark colors except for the last one, if the theme is
    # LIGHT then to have the effect that the title bar and activity bar are
    # darker than side bar and editor background
    # keeping the last one because it will be used as the border color
    # the side effect is that the editor background will be darker
    # this is a good solution
    # if theme_mode == ThemeMode.LIGHT:
    #    list_items = list(palette_data.items())
    #    last_10_without_last = list_items[-11:]
    #    last_10_without_last_keys = [item[0] for item in last_10_without_last]
    #    last_10_without_last_values = [item[1] for item in last_10_without_last]
    #    last_10_without_last_values.reverse()
    #    last_10_without_last_reversed = dict(
    #        zip(last_10_without_last_keys, last_10_without_last_values)
    #    )
    #    palette_data = {
    #        **dict(list_items[0:-10]),
    #        **dict(last_10_without_last_reversed),
    #    }

    # if foreground color is not configured, use the one in generated palette
    # read it out here and be prepared to use for edito background tuning -
    # the specified editor background color should have tuned contrast ratio
    # according to the editor foreground color.
    if not workbench_editor_foreground_color:
        assert (
            workbench_editor_foreground_color_id is not None
        ), "Neither workbench_editor_foreground_color nor workbench_editor_foreground_color_id is configured. Please configure at least one of them."
        workbench_editor_foreground_color_id = P.padding(workbench_editor_foreground_color_id)
        workbench_editor_foreground_color_identifier = (
            f"C_{all_base_colors_total}_{workbench_editor_foreground_color_id}"
        )
        workbench_editor_foreground_color = palette_data[workbench_editor_foreground_color_identifier]

    logger.debug(
        (
            "1. workbench_editor_background_color: ",
            workbench_editor_background_color,
            " >> workbench_editor_foreground_color:",
            workbench_editor_foreground_color,
        )
    )

    # workbench_editor_background_color is customized and won't use the one in
    # generated palette but it must be tuned according to the editor
    # foreground and the configured contrast ratio, unless the user want
    # to use the original configured editor background color forcely.
    if workbench_editor_background_color:
        # if the workbench editor background color is too dark, then select the
        # darkest lighter color in acceptable contrast ratio scope as the
        # editor background
        logger.debug(
            (
                "workbench_editor_background_color: ",
                workbench_editor_background_color,
                " >> workbench_editor_foreground_color:",
                workbench_editor_foreground_color,
            )
        )
        orig_workbench_editor_background_color = workbench_editor_background_color
        if auto_tune_editor_background_ratio:
            if theme_mode == ThemeMode.DARK:
                workbench_editor_background_color = C.convert_to_best_dark_color(
                    workbench_editor_background_color,
                    workbench_editor_foreground_color,
                    dark_mode_background_color_min_contrast_ratio,
                    dark_mode_background_color_max_contrast_ratio,
                    choose_darkest=True,
                )
            else:
                workbench_editor_background_color = C.convert_to_best_light_color(
                    workbench_editor_background_color,
                    workbench_editor_foreground_color,
                    light_mode_background_color_min_contrast_ratio,
                    light_mode_background_color_max_contrast_ratio,
                    choose_lightest=True,
                )

        # if force_to_use_workbench_editor_background_color is set as true, then use workbench_editor_background_color as the editor background
        if force_to_use_workbench_editor_background_color:
            str_workbench_edtor_color_id = (
                f"C_{all_base_colors_total}_{P.padding(workbench_editor_background_color_id)}"
            )
            palette_data[str_workbench_edtor_color_id] = orig_workbench_editor_background_color

        else:
            workbench_editor_background_color = palette_data[
                f"C_{all_base_colors_total}_{P.padding(workbench_editor_background_color_id)}"
            ]
    else:
        # if the workbench editor background color is not configured, use the
        # one in generated palette
        assert (
            workbench_editor_background_color_id is not None
        ), "Neither workbench_editor_background_color nor workbench_editor_background_color_id is configured. Please configure at least one of them."
        workbench_editor_background_color_identifier = (
            f"C_{all_base_colors_total}_{workbench_editor_background_color_id}"
        )
        workbench_editor_background_color = palette_data[workbench_editor_background_color_identifier]
        logger.info(
            f"Read workbench_editor_background_color from palette_data by id: {workbench_editor_background_color_identifier}"
        )

    logger.debug(
        (
            "2. workbench_editor_background_color: ",
            workbench_editor_background_color,
            " >> workbench_editor_foreground_color:",
            workbench_editor_foreground_color,
        )
    )

    token_color_contrast_ratio = None
    for _basic in range(1, token_colors_total + 1):
        for _light in range(0, token_colors_gradations_total):
            _basic = P.padding(_basic)
            _light = P.padding(_light)
            color_code = f"C_{_basic}_{_light}"
            token_color = palette_data[color_code]
            if theme_mode == ThemeMode.LIGHT:
                token_color_contrast_ratio = C.calculate_contrast_ratio(workbench_editor_background_color, token_color)
            else:
                token_color_contrast_ratio = C.calculate_contrast_ratio(token_color, workbench_editor_background_color)
            palette_data[color_code] = {
                "hex": token_color,
                "contrast_ratio": token_color_contrast_ratio,
            }

    workbench_color_contrast_ratio = None
    for _basic in range(token_colors_total + 1, all_base_colors_total + 1):
        for _light in range(0, workbench_colors_gradations_total):
            _basic = P.padding(_basic)
            _light = P.padding(_light)
            color_code = f"C_{_basic}_{_light}"
            workbench_color = palette_data[color_code]
            if theme_mode == ThemeMode.LIGHT:
                workbench_color_contrast_ratio = C.calculate_contrast_ratio(
                    workbench_editor_background_color, workbench_color
                )
            else:
                workbench_color_contrast_ratio = C.calculate_contrast_ratio(
                    workbench_color, workbench_editor_background_color
                )
            palette_data[color_code] = {
                "hex": workbench_color,
                "contrast_ratio": workbench_color_contrast_ratio,
            }

    selected_ui_color = {}
    selected_token_color = {}

    # workbench colors
    for property_name, color_placeholder in template_config_data["colors"].items():
        color_placeholder = template_config_data["colors"][property_name]
        color_code = color_placeholder[0:7]
        color_alpha = color_placeholder[7:9]

        if color_code in palette_data:
            hex_color = palette_data[color_code]["hex"]
        else:
            # some configuration use hex color code, for example ansi colors,
            # are static and not provided by palette
            if re.match(RGB_HEX_REGEX, color_placeholder, re.IGNORECASE):
                hex_color = color_placeholder[0:7]
            else:
                raise ValueError(
                    f"Color {color_placeholder} for {property_name} not found in palette and it's not an ansi color."
                )

        converted_hex_color = None
        original_contrast_ratio = None
        # auto adjust the contrast ratio to tune the hex color to the best
        if is_auto_adjust_contrast_radio_enabled and not is_exemption_property(property_name):
            # Read original contrast ratio from palette data
            if color_code in palette_data and isinstance(palette_data[color_code], dict):
                original_contrast_ratio = palette_data[color_code].get("contrast_ratio")

            # Skip conversion if original_contrast_ratio is None
            if original_contrast_ratio is None:
                converted_hex_color = hex_color
            elif theme_mode == ThemeMode.DARK:
                if is_decoration_property(property_name):
                    log_property_trace(
                        property_name,
                        theme_mode,
                        hex_color,
                        property_name,
                        f"is used as decoration color. Original contrast ratio: {original_contrast_ratio}. To get best light color for workbench editor background color {workbench_editor_background_color}.",
                    )
                    converted_hex_color = C.convert_to_best_light_color(
                        hex_color,
                        workbench_editor_background_color,
                        decoration_color_contrast_ratio_min,
                        decoration_color_contrast_ratio_max,
                    )
                    converted_contrast_ratio = C.calculate_contrast_ratio(
                        converted_hex_color, workbench_editor_background_color
                    )
                elif is_foreground_property(property_name):
                    log_property_trace(
                        property_name,
                        theme_mode,
                        hex_color,
                        property_name,
                        f"is used as foreground color. Original contrast ratio: {original_contrast_ratio}. To get best light color for workbench editor background color {workbench_editor_background_color}.",
                    )
                    converted_hex_color = C.convert_to_best_light_color(
                        hex_color,
                        workbench_editor_background_color,
                        dark_mode_workbench_foreground_color_min_contrast_ratio,
                        dark_mode_workbench_foreground_color_max_contrast_ratio,
                        choose_lightest=True,
                    )
                    converted_contrast_ratio = C.calculate_contrast_ratio(
                        converted_hex_color, workbench_editor_background_color
                    )
                elif is_background_property(property_name):
                    log_property_trace(
                        property_name,
                        theme_mode,
                        hex_color,
                        property_name,
                        f"is used as background color. Original contrast ratio: {original_contrast_ratio}. To get best dark color for workbench editor foreground color {workbench_editor_foreground_color}.",
                    )
                    converted_hex_color = C.convert_to_best_dark_color(
                        hex_color,
                        workbench_editor_foreground_color,
                        dark_mode_background_color_min_contrast_ratio,
                        dark_mode_background_color_max_contrast_ratio,
                    )
                    converted_contrast_ratio = C.calculate_contrast_ratio(
                        workbench_editor_foreground_color, converted_hex_color
                    )
                elif is_highlight_background_property(property_name):
                    log_property_trace(
                        property_name,
                        theme_mode,
                        hex_color,
                        property_name,
                        f"is used as highlight background color. Original contrast ratio: {original_contrast_ratio}. To get best light color for workbench editor background color {workbench_editor_background_color}.",
                    )
                    converted_hex_color = C.convert_to_best_light_color(
                        hex_color,
                        workbench_editor_background_color,
                        highlight_background_color_min_contrast_ratio,
                        highlight_background_color_max_contrast_ratio,
                    )
                    converted_contrast_ratio = C.calculate_contrast_ratio(
                        converted_hex_color, workbench_editor_background_color
                    )
                else:
                    converted_hex_color = hex_color
                    converted_contrast_ratio = original_contrast_ratio
                    log_property_trace(
                        property_name,
                        f"Dark mode: Unknown property type, using original color: {hex_color}",
                    )
            else:
                # LIGHT MODE
                if is_decoration_property(property_name):
                    log_property_trace(
                        property_name,
                        theme_mode,
                        hex_color,
                        property_name,
                        f"is used as decoration color. Original contrast ratio: {original_contrast_ratio}. To get best dark color for workbench editor background color {workbench_editor_background_color}.",
                    )
                    converted_hex_color = C.convert_to_best_dark_color(
                        hex_color,
                        workbench_editor_background_color,
                        decoration_color_contrast_ratio_min,
                        decoration_color_contrast_ratio_max,
                    )
                    converted_contrast_ratio = C.calculate_contrast_ratio(
                        converted_hex_color, workbench_editor_background_color
                    )
                    log_property_trace(
                        property_name,
                        f"converted to {converted_hex_color} with contrast ratio {converted_contrast_ratio}",
                    )
                elif is_foreground_property(property_name):
                    log_property_trace(
                        property_name,
                        theme_mode,
                        hex_color,
                        property_name,
                        f"is used as foreground color. Original contrast ratio: {original_contrast_ratio}. To get best dark color for workbench editor background color {workbench_editor_background_color}.",
                    )
                    converted_hex_color = C.convert_to_best_dark_color(
                        hex_color,
                        workbench_editor_background_color,
                        light_mode_workbench_foreground_color_min_contrast_ratio,
                        light_mode_workbench_foreground_color_max_contrast_ratio,
                    )
                    converted_contrast_ratio = C.calculate_contrast_ratio(
                        workbench_editor_background_color, converted_hex_color
                    )
                elif is_background_property(property_name):
                    log_property_trace(
                        property_name,
                        theme_mode,
                        hex_color,
                        property_name,
                        f"is used as background color. Original contrast ratio: {original_contrast_ratio}. To get best light color for workbench editor foreground color {workbench_editor_foreground_color}.",
                    )
                    converted_hex_color = C.convert_to_best_light_color(
                        hex_color,
                        workbench_editor_foreground_color,
                        light_mode_background_color_min_contrast_ratio,
                        light_mode_background_color_max_contrast_ratio,
                    )
                    converted_contrast_ratio = C.calculate_contrast_ratio(
                        converted_hex_color, workbench_editor_foreground_color
                    )
                else:
                    converted_hex_color = hex_color
                    converted_contrast_ratio = original_contrast_ratio
                    log_property_trace(
                        property_name,
                        f"Light mode: Unknown property type, using original color: {hex_color}",
                    )
        else:
            converted_hex_color = hex_color
            converted_contrast_ratio = original_contrast_ratio
            log_property_trace(
                property_name,
                f"No conversion applied, using original color: {hex_color}",
            )

        final_hex_color = converted_hex_color + color_alpha
        template_config_data["colors"][property_name] = final_hex_color
        selected_ui_color[property_name] = {
            color_placeholder: {
                "hex": hex_color,
                "converted_hex": converted_hex_color,
                "original_contrast_ratio": original_contrast_ratio,
                "converted_contrast_ratio": converted_contrast_ratio,
                "hls": P.hex2hls(final_hex_color),
                "id": color_code,
            }
        }
        log_property_trace(
            property_name,
            f"{converted_hex_color} - New color: {selected_ui_color[property_name]}",
        )

    # token colors - naturally being foreground color
    for token_color in template_config_data["tokenColors"]:
        scope = token_color["scope"]
        foreground = token_color["settings"]["foreground"]
        color_code = foreground[0:7]
        alpha = foreground[7:9]
        if re.match(RGB_HEX_REGEX, color_code, re.IGNORECASE):
            hex_token_color = color_code
        elif re.match(PLACEHOLDER_REGEX, color_code, re.IGNORECASE):
            hex_token_color = palette_data[color_code]["hex"]
        else:
            raise ValueError(
                f"Color {color_code} for token color {token_color} is neither hex color code ({RGB_HEX_REGEX}) nor placeholder({PLACEHOLDER_REGEX})."
            )
        # auto adjust the contrast ratio to tune the hex color to the best
        # re-generate colors and choose the best one if the current color
        # contrast ratio is too low
        original_token_contrast_ratio = None
        if color_code in palette_data and isinstance(palette_data[color_code], dict):
            original_token_contrast_ratio = palette_data[color_code].get("contrast_ratio")

        if (
            is_auto_adjust_contrast_radio_enabled
            and not is_exemption_property(scope)
            and original_token_contrast_ratio is not None
        ):
            if theme_mode == ThemeMode.LIGHT:
                hex_token_color = C.convert_to_best_dark_color(
                    hex_token_color,
                    workbench_editor_background_color,
                    token_foreground_color_min_contrast_ratio,
                    token_foreground_color_max_contrast_ratio,
                )
            else:
                hex_token_color = C.convert_to_best_light_color(
                    hex_token_color,
                    workbench_editor_background_color,
                    token_foreground_color_min_contrast_ratio,
                    token_foreground_color_max_contrast_ratio,
                )
        if theme_mode == ThemeMode.LIGHT:
            converted_token_contrast_ratio = C.calculate_contrast_ratio(
                workbench_editor_background_color, hex_token_color
            )
        else:
            converted_token_contrast_ratio = C.calculate_contrast_ratio(
                hex_token_color, workbench_editor_background_color
            )

        final_hex_token_color = hex_token_color + alpha
        token_color["settings"]["foreground"] = final_hex_token_color

        # bold the token if they match the configured regex and the theme
        # mode is LIGHT in which bold fonts are necessary to make the code
        # more readable
        token_scope = token_color["scope"]
        to_be_bold = None
        for bold_token_scope in bold_token_scopes:
            to_be_bold = re.match(bold_token_scope, token_scope, re.IGNORECASE)
            if to_be_bold:
                break
        if theme_mode == ThemeMode.LIGHT and to_be_bold:
            token_color["settings"]["fontStyle"] = "bold"

        selected_token_color[scope] = {
            color_code: {
                "hex": final_hex_token_color,
                "original_contrast_ratio": original_token_contrast_ratio,
                "converted_contrast_ratio": converted_token_contrast_ratio,
            }
        }

    lower_theme_name = theme_name.lower().replace(" ", "-")

    # theme file should be saved under themes/ sub-directory, if the directory does not exist, create it
    themes_subfolder_path = f"{output_dir}/themes/"
    if not os.path.exists(themes_subfolder_path):
        os.makedirs(themes_subfolder_path, exist_ok=True)
    random_theme_path = f"{themes_subfolder_path}{lower_theme_name}-color-theme.json"

    # other files should be saved under output/tmp sub-directory, if the directory does not exist, create it
    tmp_subfolder_path = f"{output_dir}/tmp/"
    if not os.path.exists(tmp_subfolder_path):
        os.makedirs(tmp_subfolder_path, exist_ok=True)
    _dump_json_file(f"{tmp_subfolder_path}{lower_theme_name}-palette.json", palette_data)
    _dump_json_file(f"{tmp_subfolder_path}{lower_theme_name}-orig-palette.json", orig_palette_data)
    _dump_json_file(random_theme_path, template_config_data)
    _dump_json_file(
        f"{tmp_subfolder_path}{lower_theme_name}-selected-ui-palette.json",
        selected_ui_color,
    )
    _dump_json_file(
        f"{tmp_subfolder_path}{lower_theme_name}-selected-token-palette.json",
        selected_token_color,
    )

    logger.info(f" >>>>>> END ({theme_name}) <<<<<<")


def generate_themes(target_theme=None, themes=CONFIG.config["themes"], output_dir=None):
    """Generate configured themes.

    Args:
        target_theme: Specific theme to generate (optional).
        themes: List of theme configurations to process.
        output_dir: Directory to save generated themes.
    """
    for theme_config in themes:
        # Handle theme mode conversion
        theme_mode = theme_config.get("theme_mode", "RANDOM").upper()

        theme_name = theme_config.get("name", theme_config.get("label"))
        if target_theme and (
            theme_name != target_theme and not re.match(f".*{target_theme}.*", theme_name, re.IGNORECASE)
        ):
            continue

        # Start with global config options as base
        options = CONFIG.options.copy()

        # Override with theme-specific configurations
        options.update(theme_config)

        # Set required parameters
        options["output_dir"] = output_dir
        options["theme_name"] = theme_name
        options["theme_mode"] = theme_mode

        generate_random_theme_file(**options)


def generate_random_theme(
    workbench_editor_background_color: Optional[str] = None,
    theme_name: Optional[str] = None,
    output_dir: Optional[str] = None,
    **kwargs,
):
    """
    Creates a random theme file with configuration options.

    Args:
        workbench_editor_background_color (str, optional): The workbench editor background color.
            If provided, uses this color; otherwise uses the CONFIG value.
        theme_name (str, optional): Custom theme name. If provided, uses this name;
            otherwise generates a random name or uses CONFIG value.
        output_dir (str, optional): Directory to save the generated theme file.
            If provided, saves theme to this directory; otherwise uses default location.
        **kwargs: Additional options that override CONFIG.options values.
    """
    config_options = CONFIG.options.copy()
    config_theme_name = config_options.get("theme_name")
    if config_theme_name and not theme_name:
        logger.info(f"Using configured theme name from CONFIG.options: {config_theme_name}")
        return generate_themes(config_theme_name, output_dir=output_dir)

    # Override with any kwargs provided
    config_options.update(kwargs)

    # Add required parameters
    config_options["workbench_editor_background_color"] = (
        workbench_editor_background_color
        if workbench_editor_background_color
        else config_options.get("workbench_editor_background_color")
    )
    config_options["theme_name"] = theme_name
    config_options["output_dir"] = output_dir

    generate_random_theme_file(**config_options)


def get_all_built_in_themes():
    """Get all built-in theme names.

    Returns:
        List of built-in theme labels.
    """
    root_path = os.getcwd() + os.sep
    package_file_path = root_path + "package.json"
    package_data = load_json_file(package_file_path)
    themes = package_data["contributes"]["themes"]
    themes_labels = [t["label"] for t in themes]
    logger.info(themes_labels)
    return themes_labels


def main():
    """Parse command line arguments and generate themes or display colors.

    Supports the following command line arguments:
    - --random_theme/-r: Generate random theme
    - --generate/-g: Generate default themes
    - --print_colors/-p: Print theme colors with filter
    - --theme/-t: Specify target theme
    - --print_palette/-P: Print palette colors with filter
    """
    parser = argparse.ArgumentParser(description="ViiV - VSCode theme generator")
    parser.add_argument("-r", "--random_theme", action="store_true", help="Generate random theme")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate default themes")
    parser.add_argument("-p", "--print_colors", metavar="FILTER", help="Print theme colors with filter")
    parser.add_argument("-t", "--theme", metavar="THEME", help="Specify target theme")
    parser.add_argument("-T", "--get_themes", action="store_true", help="Get all built-in themes")
    parser.add_argument("-N", "--nvim", action="store_true", help="Generate Neovim themes")
    parser.add_argument("--nvim-repo", metavar="PATH", help="Path to viiv.nvim repository")
    parser.add_argument(
        "-P",
        "--print_palette",
        metavar="FILTER",
        help="Print palette colors with filter",
    )
    parser.add_argument(
        "-D",
        "--palette-root-dir",
        metavar="PATH",
        help="Directory path where palette files are located",
    )
    parser.add_argument(
        "-d",
        "--themes-dir",
        metavar="PATH",
        help="Directory path where theme files are located",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        metavar="PATH",
        help="Output directory for generated themes",
        default=".",
    )
    parser.add_argument(
        "-b",
        "--background",
        metavar="COLOR",
        help="Workbench editor background color",
    )

    args = parser.parse_args()

    if args.random_theme:
        generate_random_theme(
            workbench_editor_background_color=args.background,
            output_dir=args.output_dir,
        )

    if args.get_themes:
        get_all_built_in_themes()

    if args.nvim:
        generate_nvim_themes(args.nvim_repo)

    if args.print_palette:
        show_palette(
            args.print_palette,
            getattr(args, "palette_root_dir", None),
            args.theme or "default",
        )

    if args.generate:
        generate_themes(args.theme, output_dir=args.output_dir)

    if args.print_colors:
        show_theme_colors(args.print_colors, args.theme, getattr(args, "themes_dir", None))


if __name__ == "__main__":
    main()
