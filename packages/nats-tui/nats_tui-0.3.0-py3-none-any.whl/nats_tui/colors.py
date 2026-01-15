"""Theme definitions for NATS TUI."""

from textual.theme import Theme as TextualTheme

# NATS brand colors
GREEN = "#27ae60"  # NATS green
BLUE = "#375EAB"  # NATS blue

# Accent colors (from Harlequin)
YELLOW = "#FEFFAC"
PINK = "#FFB6D9"
PURPLE = "#D67BFF"

# Neutral colors
GRAY = "#777777"
DARK_GRAY = "#555555"
BLACK = "#0C0C0C"
WHITE = "#DDDDDD"

# =============================================================================
# OSCAR EDS Brand Colors (from eds-libraries.css)
# =============================================================================
OSCAR_YELLOW = "#FAD22D"  # --brand-yellow (primary accent)
OSCAR_BLUE = "#1174E6"    # --brand-blue
OSCAR_GREEN = "#0FC373"   # --brand-green
OSCAR_RED = "#FF3232"     # --brand-red
OSCAR_ORANGE = "#FF8C0A"  # --brand-orange
OSCAR_PURPLE = "#AF78D2"  # --brand-purple

# OSCAR darker variants (for accents)
OSCAR_YELLOW4 = "#C6A823"  # --brand-yellow4
OSCAR_BLUE4 = "#0069C2"    # --brand-blue4
OSCAR_GREEN4 = "#0C9B5B"   # --brand-green4
OSCAR_RED4 = "#CC2828"     # --brand-red4

# OSCAR lighter variants (for hover/highlights)
OSCAR_YELLOW2 = "#FCE282"  # --brand-yellow2
OSCAR_BLUE2 = "#81BAF3"    # --brand-blue2
OSCAR_GREEN2 = "#70DBAA"   # --brand-green2

# OSCAR grays
OSCAR_BLACK = "#0C0C0C"    # --brand-black
OSCAR_GRAY1 = "#242424"    # --brand-gray1
OSCAR_GRAY1B = "#3A3A3A"   # --brand-gray1b
OSCAR_GRAY2 = "#767676"    # --brand-gray2
OSCAR_GRAY3 = "#A0A0A0"    # --brand-gray3
OSCAR_GRAY4 = "#E0E0E0"    # --brand-gray4
OSCAR_GRAY5 = "#F2F2F2"    # --brand-gray5
OSCAR_WHITE = "#FAFAFA"    # --brand-ericsson-white

# =============================================================================
# OSCAR Theme (dark mode - default)
# =============================================================================
OSCAR_THEME = TextualTheme(
    name="oscar",
    primary=OSCAR_YELLOW,      # Yellow as primary (distinctive!)
    secondary=OSCAR_BLUE,      # Blue for secondary elements
    warning=OSCAR_ORANGE,      # Orange for warnings
    error=OSCAR_RED,           # Red for errors
    success=OSCAR_GREEN,       # Green for success
    accent=OSCAR_BLUE,         # Blue accent
    foreground=OSCAR_GRAY4,    # Light gray text
    background=OSCAR_BLACK,    # Black background
    surface=OSCAR_GRAY1,       # Slightly lighter surface
    panel=OSCAR_GRAY1B,        # Panel color
    dark=True,
)

# OSCAR Theme (light mode)
OSCAR_LIGHT_THEME = TextualTheme(
    name="oscar-light",
    primary=OSCAR_YELLOW4,     # Darker yellow for light mode
    secondary=OSCAR_BLUE,      # Blue secondary
    warning=OSCAR_ORANGE,      # Orange for warnings
    error=OSCAR_RED,           # Red for errors
    success=OSCAR_GREEN4,      # Darker green for light mode
    accent=OSCAR_BLUE,         # Blue accent
    foreground=OSCAR_GRAY1,    # Dark text
    background=OSCAR_GRAY5,    # Light gray background
    surface=OSCAR_WHITE,       # White surface
    panel=OSCAR_GRAY4,         # Light panel
    dark=False,
)

# =============================================================================
# NATS TUI Theme (dark mode)
# =============================================================================
NATS_TUI_TEXTUAL_THEME = TextualTheme(
    name="nats-tui",
    primary=GREEN,
    secondary=BLUE,
    warning=YELLOW,
    error=PINK,
    success=GREEN,
    accent=BLUE,
    foreground=WHITE,
    background=BLACK,
    surface=BLACK,
    panel=GRAY,
    dark=True,
)

# Light mode colors
LIGHT_BG = "#f5f5f5"
LIGHT_SURFACE = "#ffffff"
LIGHT_PANEL = "#e0e0e0"
LIGHT_FG = "#1a1a1a"
LIGHT_WARNING = "#B8860B"  # Dark goldenrod
LIGHT_ERROR = "#DC143C"  # Crimson

# Custom NATS TUI theme (light mode)
NATS_TUI_LIGHT_THEME = TextualTheme(
    name="nats-tui-light",
    primary=GREEN,
    secondary=BLUE,
    warning=LIGHT_WARNING,
    error=LIGHT_ERROR,
    success=GREEN,
    accent=BLUE,
    foreground=LIGHT_FG,
    background=LIGHT_BG,
    surface=LIGHT_SURFACE,
    panel=LIGHT_PANEL,
    dark=False,
)

# Build valid themes dict - start with Textual's built-in themes
# and add our custom themes
try:
    from textual.theme import BUILTIN_THEMES

    VALID_THEMES = BUILTIN_THEMES.copy()
    VALID_THEMES.pop("textual-ansi", None)
except ImportError:
    # Fallback if internal API changes
    VALID_THEMES = {}

# Add custom themes
VALID_THEMES["oscar"] = OSCAR_THEME
VALID_THEMES["oscar-light"] = OSCAR_LIGHT_THEME
VALID_THEMES["nats-tui"] = NATS_TUI_TEXTUAL_THEME
VALID_THEMES["nats-tui-light"] = NATS_TUI_LIGHT_THEME

# Default theme
DEFAULT_THEME = "oscar"
