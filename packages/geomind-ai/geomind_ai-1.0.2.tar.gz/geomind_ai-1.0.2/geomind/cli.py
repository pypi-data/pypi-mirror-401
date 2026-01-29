"""
Command-line interface for GeoMind.
"""

import sys
import argparse
from typing import Optional

from .agent import GeoMindAgent


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

    args = parser.parse_args()

    if args.version:
        from . import __version__

        print(f"GeoMind version {__version__}")
        sys.exit(0)

    # Start interactive or single-query mode
    try:
        if args.query:
            # Single query mode
            agent = GeoMindAgent(model=args.model, api_key=args.api_key)
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
    print("=" * 60)
    print("🌍 GeoMind - Geospatial AI Agent")
    print("=" * 60)
    print("Powered by OpenRouter | Sentinel-2 Imagery")
    print("Type 'quit' or 'exit' to end the session")
    print("Type 'reset' to start a new conversation")
    print("=" * 60)

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
