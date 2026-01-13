"""Configuration management for sbc.

Loads configuration from multiple sources in priority order:
1. Default values (hardcoded)
2. User config: ~/.sbc.toml or ~/.config/sbc/config.toml
3. Project config: .sbc.toml (in current directory)
4. Environment variables (SBC_*)

Configuration structure:
    [jupyterhub]
    base_url = "https://jh-01.cheme.cmu.edu"
    dev_url = "https://jupyterhub-dev.cheme.cmu.edu"

    [course]
    name = "f25-06623"
    semester = "f25"
    course_number = "06623"
    github_org = "jkitchin"
    github_repo = "f25-06623"
    github_branch = "main"

    [paths]
    source_root = "~/f25-06623-source"
    dest_root = "~/f25-06623-source/f25-06623/assignments"
    notebook_root = "~/s25-06623"
    search_db = "~/db.chromadb"
    search_collection = "ipynb"

    [search]
    include_pattern = "**/*.ipynb"
    exclude_patterns = ["assignment"]
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Fallback for older Python


class Config:
    """Configuration container with dot-notation access."""

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self._data = data or {}

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            return object.__getattribute__(self, name)

        value = self._data.get(name)
        if isinstance(value, dict):
            return Config(value)
        return value

    def __getitem__(self, name: str) -> Any:
        return self._data[name]

    def get(self, name: str, default: Any = None) -> Any:
        """Get a value with optional default."""
        return self._data.get(name, default)

    def update(self, other: Dict[str, Any]) -> None:
        """Deep update configuration."""
        self._deep_update(self._data, other)

    @staticmethod
    def _deep_update(base: Dict, update: Dict) -> None:
        """Recursively update nested dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                Config._deep_update(base[key], value)
            else:
                base[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """Convert to plain dictionary."""
        return self._data.copy()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration values."""
    return {
        'jupyterhub': {
            'base_url': 'https://jh-01.cheme.cmu.edu',
            'dev_url': 'https://jupyterhub-dev.cheme.cmu.edu',
        },
        'course': {
            'name': 'f25-06623',
            'semester': 'f25',
            'course_number': '06623',
            'github_org': 'jkitchin',
            'github_repo': 'f25-06623',
            'github_branch': 'main',
        },
        'paths': {
            'source_root': '~/f25-06623-source',
            'dest_root': '~/f25-06623-source/f25-06623/assignments',
            'notebook_root': '~/s25-06623',
            'search_db': '~/db.chromadb',
            'search_collection': 'ipynb',
        },
        'search': {
            'include_pattern': '**/*.ipynb',
            'exclude_patterns': ['assignment'],
        },
        'nbgitpuller': {
            'url_template': '{jupyterhub_url}/hub/user-redirect/git-pull?repo=https%3A//{github_repo}&urlpath=lab/tree/{course_name}/{path}&branch={branch}',
        },
    }


def load_toml_file(path: Path) -> Optional[Dict[str, Any]]:
    """Load a TOML file if it exists."""
    if not path.exists():
        return None

    try:
        with open(path, 'rb') as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"Warning: Failed to load config from {path}: {e}")
        return None


def load_env_overrides() -> Dict[str, Any]:
    """Load configuration overrides from environment variables.

    Environment variables should be prefixed with SBC_ and use double underscores
    to indicate nesting. For example:
        SBC_JUPYTERHUB__BASE_URL=https://example.com
        SBC_COURSE__NAME=s25-06623
    """
    config = {}
    prefix = 'SBC_'

    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue

        # Remove prefix and split on double underscores
        parts = key[len(prefix):].lower().split('__')

        # Build nested dictionary
        current = config
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Handle lists (comma-separated values)
        if ',' in value:
            current[parts[-1]] = [v.strip() for v in value.split(',')]
        else:
            current[parts[-1]] = value

    return config


def get_config_paths() -> List[Path]:
    """Get list of possible configuration file paths in priority order."""
    paths = []

    # User config in home directory
    home = Path.home()
    paths.append(home / '.sbc.toml')

    # XDG config directory
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_home:
        paths.append(Path(xdg_config_home) / 'sbc' / 'config.toml')
    else:
        paths.append(home / '.config' / 'sbc' / 'config.toml')

    # Project-specific config in current directory
    paths.append(Path.cwd() / '.sbc.toml')

    return paths


def load_config() -> Config:
    """Load configuration from all sources."""
    # Start with defaults
    config_dict = get_default_config()

    # Load from config files in priority order
    for path in get_config_paths():
        file_config = load_toml_file(path)
        if file_config:
            Config._deep_update(config_dict, file_config)

    # Apply environment variable overrides
    env_config = load_env_overrides()
    if env_config:
        Config._deep_update(config_dict, env_config)

    return Config(config_dict)


def save_config_template(path: Path, include_defaults: bool = True) -> None:
    """Save a configuration template file.

    Args:
        path: Path to save the template
        include_defaults: If True, include default values as comments
    """
    template = '''# SBC Configuration File
# See documentation for all available options

[jupyterhub]
base_url = "https://jh-01.cheme.cmu.edu"
dev_url = "https://jupyterhub-dev.cheme.cmu.edu"

[course]
name = "f25-06623"
semester = "f25"
course_number = "06623"
github_org = "jkitchin"
github_repo = "f25-06623"
github_branch = "main"

[paths]
source_root = "~/f25-06623-source"
dest_root = "~/f25-06623-source/f25-06623/assignments"
notebook_root = "~/s25-06623"
search_db = "~/db.chromadb"
search_collection = "ipynb"

[search]
include_pattern = "**/*.ipynb"
exclude_patterns = ["assignment"]

[nbgitpuller]
url_template = "{jupyterhub_url}/hub/user-redirect/git-pull?repo=https%3A//{github_repo}&urlpath=lab/tree/{course_name}/{path}&branch={branch}"
'''

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(template)


# Global configuration instance
config = load_config()


def reload_config() -> Config:
    """Reload configuration from all sources."""
    global config
    config = load_config()
    return config
