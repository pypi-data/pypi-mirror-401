import tomllib
from pathlib import Path
from platformdirs import user_config_dir

CONFIG_DIR = Path(user_config_dir("mercedtodo"))
CONFIG_FILE = CONFIG_DIR / "config.toml"

def load_config():
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}

def get_theme_css():
    config = load_config()
    theme = config.get("theme", {})
    # Simple example: override background colors
    css = ""
    if "background" in theme:
        css += f"Screen {{ background: {theme['background']}; }}\n"
    if "primary" in theme:
        css += f"Button.primary {{ background: {theme['primary']}; }}\n"
    return css
