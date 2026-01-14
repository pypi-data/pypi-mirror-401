#!/usr/bin/env python3
"""Refineo CLI entry point."""

import subprocess
import sys
import platform
from pathlib import Path

from .config import load_credentials, clear_credentials
from .api import start_device_code_flow, poll_for_token, humanize, get_usage

VERSION = "0.0.6"

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RED = "\033[31m"


def print_error(message: str) -> None:
    """Print error message."""
    print(f"{RED}Error:{RESET} {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print success message."""
    print(f"{GREEN}✓{RESET} {message}")


def open_browser(url: str) -> None:
    """Open URL in default browser."""
    system = platform.system()

    try:
        if system == "Darwin":
            subprocess.run(["open", url], check=True, capture_output=True)
        elif system == "Windows":
            subprocess.run(["start", "", url], check=True, capture_output=True, shell=True)
        else:
            subprocess.run(["xdg-open", url], check=True, capture_output=True)
    except Exception:
        print(f"Please open this URL in your browser: {url}")


def login_command() -> None:
    """Login command."""
    existing = load_credentials()
    if existing:
        print(f"Already logged in as {CYAN}{existing['user']['email']}{RESET}")
        print(f"Tier: {BOLD}{existing['user']['tier']}{RESET}")
        print(f"\nRun {DIM}refineo logout{RESET} to switch accounts.")
        return

    print(f"{BOLD}Refineo CLI Login{RESET}\n")

    try:
        device_code = start_device_code_flow()

        print(f"Your code: {BOLD}{CYAN}{device_code['user_code']}{RESET}\n")
        print("Opening browser to authorize...")
        print(f"{DIM}{device_code['verification_uri_complete']}{RESET}\n")

        open_browser(device_code["verification_uri_complete"])

        print("Waiting for authorization...", end="", flush=True)

        dots = [0]

        def on_poll() -> None:
            dots[0] = (dots[0] % 3) + 1
            print(f"\rWaiting for authorization{'.' * dots[0]}   ", end="", flush=True)

        credentials = poll_for_token(
            device_code["device_code"],
            device_code["interval"],
            device_code["expires_in"],
            on_poll,
        )

        print("\r                                    \r", end="")
        print_success(f"Logged in as {CYAN}{credentials['user']['email']}{RESET}")
        print(f"Tier: {BOLD}{credentials['user']['tier']}{RESET}")

    except Exception as e:
        print()
        print_error(str(e))
        sys.exit(1)


def logout_command() -> None:
    """Logout command."""
    credentials = load_credentials()

    if not credentials:
        print("Not logged in.")
        return

    clear_credentials()
    print_success(f"Logged out from {credentials['user']['email']}")


def stats_command() -> None:
    """Stats command."""
    credentials = load_credentials()

    if not credentials:
        print_error("Not logged in. Run: refineo login")
        sys.exit(1)

    try:
        usage = get_usage()

        print(f"{BOLD}Refineo Usage{RESET}\n")
        print(f"Account: {CYAN}{credentials['user']['email']}{RESET}")
        print(f"Plan: {BOLD}{usage['tier']}{RESET}")
        print()

        if usage["limit"] == -1:
            print(f"Requests: {GREEN}Unlimited{RESET}")
            if usage.get("rateLimit"):
                print(f"Rate limit: {usage['rateLimit']} requests/hour")
        else:
            percentage = round((usage["used"] / usage["limit"]) * 100)
            color = RED if percentage >= 90 else YELLOW if percentage >= 70 else GREEN
            print(f"Requests: {color}{usage['used']}{RESET} / {usage['limit']} ({percentage}%)")
            print(f"Remaining: {usage['remaining']}")

        print(f"Word limit: {usage['wordLimit']} words/request")

        if usage.get("resetDate"):
            print(f"Resets: {usage['resetDate']}")

    except Exception as e:
        print_error(str(e))
        sys.exit(1)


def humanize_command(args: list[str]) -> None:
    """Humanize command."""
    credentials = load_credentials()

    if not credentials:
        print_error("Not logged in. Run: refineo login")
        sys.exit(1)

    # Parse arguments
    text = ""
    model = "enhanced"
    input_file = ""
    output_file = ""

    i = 0
    while i < len(args):
        arg = args[i]

        if arg in ("--model", "-m"):
            i += 1
            if i < len(args):
                value = args[i]
                if value in ("standard", "enhanced"):
                    model = value
                else:
                    print_error('Model must be "standard" or "enhanced"')
                    sys.exit(1)
        elif arg in ("--file", "-f"):
            i += 1
            if i < len(args):
                input_file = args[i]
        elif arg in ("--output", "-o"):
            i += 1
            if i < len(args):
                output_file = args[i]
        elif not arg.startswith("-"):
            text = arg

        i += 1

    # Read from file if specified
    if input_file:
        path = Path(input_file)
        if not path.exists():
            print_error(f"File not found: {input_file}")
            sys.exit(1)
        text = path.read_text()

    # Read from stdin if no text provided
    if not text:
        if sys.stdin.isatty():
            print_error(
                'No text provided. Usage: refineo humanize "your text" or echo "text" | refineo humanize'
            )
            sys.exit(1)
        text = sys.stdin.read().strip()

    if not text:
        print_error("No text provided")
        sys.exit(1)

    try:
        result = humanize(text, model)

        if output_file:
            Path(output_file).write_text(result["humanizedText"])
            print_success(f"Output written to {output_file}")
        else:
            print(result["humanizedText"])

    except Exception as e:
        print_error(str(e))
        sys.exit(1)


def help_command() -> None:
    """Help command."""
    print(f"""
{BOLD}Refineo CLI{RESET} - AI Text Humanizer
Version {VERSION}

{BOLD}Usage:{RESET}
  refineo <command> [options]

{BOLD}Commands:{RESET}
  login              Authenticate with your Refineo account
  logout             Clear stored credentials
  stats              Show usage statistics
  humanize <text>    Humanize AI-generated text

{BOLD}Humanize Options:{RESET}
  -m, --model <model>   Model: "standard" or "enhanced" (default: enhanced)
  -f, --file <path>     Read input from file
  -o, --output <path>   Write output to file

{BOLD}Examples:{RESET}
  {DIM}# Login to your account{RESET}
  refineo login

  {DIM}# Humanize text directly{RESET}
  refineo humanize "The results indicate a significant correlation."

  {DIM}# Use standard model{RESET}
  refineo humanize "Text here" --model standard

  {DIM}# Read from file{RESET}
  refineo humanize --file input.txt --output output.txt

  {DIM}# Pipe from stdin{RESET}
  echo "AI-generated text" | refineo humanize

  {DIM}# Check usage{RESET}
  refineo stats

{BOLD}More Info:{RESET}
  https://www.refineo.app/docs/cli
""")


def version_command() -> None:
    """Version command."""
    print(f"refineo {VERSION}")


def main() -> None:
    """Main entry point."""
    args = sys.argv[1:]
    command = args[0] if args else None

    if command == "login":
        login_command()
    elif command == "logout":
        logout_command()
    elif command == "stats":
        stats_command()
    elif command == "humanize":
        humanize_command(args[1:])
    elif command in ("help", "--help", "-h"):
        help_command()
    elif command in ("version", "--version", "-v"):
        version_command()
    elif command is None:
        help_command()
    else:
        print_error(f"Unknown command: {command}")
        print(f"Run {DIM}refineo help{RESET} for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
