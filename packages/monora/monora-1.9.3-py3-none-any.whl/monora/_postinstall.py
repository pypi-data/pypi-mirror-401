"""Post-installation message and setup prompt for Monora SDK."""
from __future__ import annotations

import os
import sys
import subprocess


def is_ci() -> bool:
    """Check if running in a CI environment."""
    ci_env_vars = [
        "CI",
        "CONTINUOUS_INTEGRATION",
        "BUILD_NUMBER",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "CIRCLECI",
        "TRAVIS",
        "JENKINS_URL",
        "MONORA_SKIP_POSTINSTALL",
    ]
    return any(os.environ.get(var) for var in ci_env_vars)


def is_interactive() -> bool:
    """Check if running in an interactive terminal."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def config_exists() -> bool:
    """Check if a Monora config file already exists."""
    config_files = [
        "monora.yml",
        "monora.yaml",
        "monora.json",
        ".monora.yml",
        ".monora.yaml",
        ".monora.json",
    ]
    return any(os.path.exists(f) for f in config_files)


def show_quick_start() -> None:
    """Display quick start information."""
    print("\n📦 Monora SDK installed successfully!")
    print("")
    print("Quick Start:")
    print("  1. Run: monora init")
    print("  2. Or use zero-config in your code:")
    print("     import monora")
    print("     monora.init()")
    print("")


def run_wizard() -> None:
    """Run the setup wizard with smart defaults."""
    try:
        subprocess.run(
            [sys.executable, "-m", "monora.cli.report", "init", "--yes"],
            check=False,
        )
    except Exception:
        show_quick_start()


def post_install() -> None:
    """Main post-installation routine."""
    # Skip in CI environments
    if is_ci():
        print("\n📦 Monora SDK installed successfully.")
        print("   Run 'monora init' to configure.\n")
        return

    # Check if config already exists
    if config_exists():
        print("\n✅ Monora SDK installed. Existing configuration detected.\n")
        return

    # Non-interactive terminal - show quick start
    if not is_interactive():
        show_quick_start()
        return

    # Interactive terminal - run setup wizard
    print("\n🚀 Monora SDK installed! Starting setup wizard...\n")
    run_wizard()


if __name__ == "__main__":
    post_install()
