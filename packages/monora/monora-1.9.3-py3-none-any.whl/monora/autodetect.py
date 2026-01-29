"""Auto-detection utilities for zero-config initialization."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


def detect_installed_sdks() -> List[str]:
    """Detect which LLM SDKs are installed.

    Returns:
        List of installed SDK names: 'openai', 'anthropic', 'langchain'
    """
    sdks: List[str] = []

    sdk_modules = {
        'openai': 'openai',
        'anthropic': 'anthropic',
        'langchain': 'langchain',
    }

    for sdk_name, module_name in sdk_modules.items():
        if importlib.util.find_spec(module_name) is not None:
            sdks.append(sdk_name)

    return sdks


def detect_environment() -> str:
    """Detect the current environment (dev, staging, production).

    Checks environment variables and CI/CD indicators.

    Returns:
        Environment name: 'dev', 'staging', or 'production'
    """
    # Check explicit environment variables
    env_vars = [
        'MONORA_ENV',
        'ENVIRONMENT',
        'ENV',
        'NODE_ENV',
        'PYTHON_ENV',
        'FLASK_ENV',
        'DJANGO_ENV',
        'RAILS_ENV',
    ]

    for var in env_vars:
        value = os.environ.get(var, '').lower()
        if value in ('production', 'prod'):
            return 'production'
        if value in ('staging', 'stage', 'stg'):
            return 'staging'
        if value in ('development', 'dev', 'local'):
            return 'dev'

    # Check CI/CD indicators (typically production-like)
    ci_indicators = [
        'CI',
        'CONTINUOUS_INTEGRATION',
        'GITHUB_ACTIONS',
        'GITLAB_CI',
        'CIRCLECI',
        'JENKINS_URL',
        'TRAVIS',
        'BUILDKITE',
    ]

    for indicator in ci_indicators:
        if os.environ.get(indicator):
            # CI environments are usually staging or production
            return 'staging'

    # Check for production indicators
    production_indicators = [
        'KUBERNETES_SERVICE_HOST',  # Running in Kubernetes
        'ECS_CONTAINER_METADATA_URI',  # Running in AWS ECS
        'DYNO',  # Running on Heroku
    ]

    for indicator in production_indicators:
        if os.environ.get(indicator):
            return 'production'

    # Default to dev
    return 'dev'


def detect_service_name() -> Optional[str]:
    """Detect the service name from project files or directory.

    Checks pyproject.toml, setup.py, package.json, then falls back to directory name.

    Returns:
        Detected service name or None
    """
    cwd = Path.cwd()

    # Try pyproject.toml
    pyproject = cwd / 'pyproject.toml'
    if pyproject.exists():
        name = _parse_pyproject_name(pyproject)
        if name:
            return name

    # Try setup.py
    setup_py = cwd / 'setup.py'
    if setup_py.exists():
        name = _parse_setup_py_name(setup_py)
        if name:
            return name

    # Try package.json
    package_json = cwd / 'package.json'
    if package_json.exists():
        name = _parse_package_json_name(package_json)
        if name:
            return name

    # Fall back to directory name
    dir_name = cwd.name
    if dir_name and dir_name not in ('.', '..', ''):
        return dir_name

    return None


def _parse_pyproject_name(path: Path) -> Optional[str]:
    """Extract project name from pyproject.toml."""
    try:
        content = path.read_text(encoding='utf-8')
        # Simple parsing without toml dependency
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('name'):
                # Handle: name = "project-name"
                parts = line.split('=', 1)
                if len(parts) == 2:
                    value = parts[1].strip().strip('"').strip("'")
                    if value:
                        return value
    except Exception:
        pass
    return None


def _parse_setup_py_name(path: Path) -> Optional[str]:
    """Extract project name from setup.py."""
    try:
        content = path.read_text(encoding='utf-8')
        # Look for name='...' or name="..."
        import re
        match = re.search(r"name\s*=\s*['\"]([^'\"]+)['\"]", content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def _parse_package_json_name(path: Path) -> Optional[str]:
    """Extract project name from package.json."""
    try:
        import json
        content = path.read_text(encoding='utf-8')
        data = json.loads(content)
        name = data.get('name')
        if name and isinstance(name, str):
            # Strip scope from scoped packages (@org/name -> name)
            if name.startswith('@') and '/' in name:
                name = name.split('/', 1)[1]
            return name
    except Exception:
        pass
    return None


def auto_detect_config() -> Dict[str, Any]:
    """Auto-detect configuration based on environment.

    Returns:
        Configuration overrides based on detected environment
    """
    env = detect_environment()
    service_name = detect_service_name()
    installed_sdks = detect_installed_sdks()

    config: Dict[str, Any] = {
        'defaults': {
            'environment': env,
        },
    }

    if service_name:
        config['defaults']['service_name'] = service_name

    # Enable auto-instrumentation if SDKs are detected
    if installed_sdks:
        config['instrumentation'] = {
            'enabled': True,
            'targets': installed_sdks,
        }

    return config


def select_preset_for_environment(env: str) -> str:
    """Select the appropriate preset based on environment.

    Args:
        env: Environment name (dev, staging, production)

    Returns:
        Preset name to use
    """
    preset_map = {
        'dev': 'development',
        'development': 'development',
        'local': 'development',
        'staging': 'production',
        'stage': 'production',
        'stg': 'production',
        'production': 'production',
        'prod': 'production',
    }

    return preset_map.get(env.lower(), 'development')
