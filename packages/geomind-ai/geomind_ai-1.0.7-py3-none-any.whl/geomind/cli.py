"""
Command-line interface for GeoMind.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional

from .agent import GeoMindAgent


# Config file path for storing API key
CONFIG_DIR = Path.home() / ".geomind"
CONFIG_FILE = CONFIG_DIR / "config"


def get_saved_api_key() -> Optional[str]:
    """Get API key saved on user's PC."""
    if CONFIG_FILE.exists():
        try:
            return CONFIG_FILE.read_text().strip()
        except Exception:
            return None
    return None


def save_api_key(api_key: str) -> bool:
    """Save API key to user's PC."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(api_key)
        return True
    except Exception:
        return False


def main():
    """Main CLI entry point for the geomind package."""
    parser = argparse.ArgumentParser(
        description="GeoMind - AI agent for geospatial analysis with Sentinel-2 imagery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  geomind

  # Single query
  geomind --query "Find recent imagery of Paris"

  # With custom model
  geomind --model "anthropic/claude-3.5-sonnet"

  # With API key
  geomind --api-key "your-openrouter-api-key"

  # Clear saved API key
  geomind --clear-key

Environment Variables:
  OPENROUTER_API_KEY    Your OpenRouter API key
  OPENROUTER_MODEL      Model to use (default: xiaomi/mimo-v2-flash:free)
  OPENROUTER_API_URL    API endpoint (default: https://openrouter.ai/api/v1)
        """,
    )

    parser.add_argument(
        "--query",
        "-q",
        type=str,
        help="Single query to run (if not provided, starts interactive mode)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        help="Model name to use (e.g., 'anthropic/claude-3.5-sonnet')",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        type=str,
        help="OpenRouter API key (or set OPENROUTER_API_KEY env variable)",
    )
    parser.add_argument(
        "--version", "-v", action="store_true", help="Show version and exit"
    )
    parser.add_argument("--clear-key", action="store_true", help="Clear saved API key")

    args = parser.parse_args()

    if args.clear_key:
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
            print("✅ Saved API key cleared.")
        else:
            print("ℹ️ No saved API key found.")
        sys.exit(0)

    if args.version:
        from . import __version__

        print(f"GeoMind version {__version__}")
        sys.exit(0)

    # Start interactive or single-query mode
    try:
        if args.query:
            # Single query mode - also use saved key
            api_key = args.api_key or get_saved_api_key()
            if not api_key:
                print("❌ No API key found. Run 'geomind' first to set up.")
                sys.exit(1)
            agent = GeoMindAgent(model=args.model, api_key=api_key)
            agent.chat(args.query)
        else:
            # Interactive mode
            run_interactive(model=args.model, api_key=args.api_key)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def run_interactive(model: Optional[str] = None, api_key: Optional[str] = None):
    """Run interactive CLI mode."""
    from . import __version__

    print("=" * 60)
    print("🌍 GeoMind - Geospatial AI Agent")
    print("=" * 60)
    print(f"Version: {__version__} | Author: Harsh Shinde")
    print("Type 'quit' or 'exit' to end the session")
    print("Type 'reset' to start a new conversation")
    print("=" * 60)

    # Check for API key in order: argument > env > saved file
    from .config import OPENROUTER_API_KEY

    if not api_key:
        api_key = OPENROUTER_API_KEY

    if not api_key:
        api_key = get_saved_api_key()

    if not api_key:
        print("\n🔑 OpenRouter API key required (FREE)")
        print("   Get yours at: https://openrouter.ai/settings/keys\n")
        api_key = input("   Enter your API key: ").strip()

        if not api_key:
            print("\n❌ No API key provided. Exiting.")
            return

        # Save the key for future use
        if save_api_key(api_key):
            print("   ✅ API key saved! You won't need to enter it again.\n")
        else:
            print("   ⚠️ Could not save API key. You'll need to enter it next time.\n")

    agent = GeoMindAgent(model=model, api_key=api_key)

    while True:
        try:
            user_input = input("\n💬 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye!")
                break

            if user_input.lower() == "reset":
                agent.reset()
                continue

            agent.chat(user_input)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
