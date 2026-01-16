import subprocess
import sys


def install_playwright() -> bool:
    """Install Playwright Chromium browser if not already installed."""
    try:
        # Ensure playwright CLI exists
        subprocess.run(
            ["playwright", "--version"],
            capture_output=True,
            check=True,
            text=True,
        )

        print("Installing Playwright Chromium browser...")
        subprocess.run(
            ["playwright", "install", "chromium"],
            check=True,
        )

        print("✓ Playwright Chromium installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(
            f"Warning: Failed to install Playwright browsers: {e}",
            file=sys.stderr,
        )
        return False

    except FileNotFoundError:
        print(
            "Error: playwright command not found. Is Playwright installed?",
            file=sys.stderr,
        )
        return False
