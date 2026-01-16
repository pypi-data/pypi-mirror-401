#!/usr/bin/env python3

import argparse
import getpass
import json
import shutil
import subprocess
import sys
import webbrowser
import re

SSO_URL_PATTERN = re.compile(
    r"^(https://(?:keepersecurity\.(?:com|eu|ca|jp)|keepersecurity\.com\.au|govcloud\.keepersecurity\.us)/api/rest/sso/\S+)$"
)

DEFAULT_FIELDS_BY_TYPE = {
    "api": "API Key",
    "login": "password",
    "secure note": "password",
}

KEEPER_COMMANDER = "keeper"


def run_keeper_command(cmd: list[str], debug: bool = False) -> tuple[int, str, str]:
    """Run a keeper command with SSO handling.

    Returns: (returncode, stdout, stderr)
    """
    if debug:
        print(f"Running: {' '.join(cmd)}", file=sys.stderr)

    # Run keeper with piped stdin so we can send commands for SSO automation
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if debug:
        print("Process started, reading stdout...", file=sys.stderr)

    # Read stdout line by line to detect SSO URL and automate login
    stdout_lines = []
    sso_handled = False
    for line in process.stdout:
        if debug:
            print(f"Got line: {line!r}", file=sys.stderr)
        stdout_lines.append(line)

        if not sso_handled:
            sso_match = SSO_URL_PATTERN.search(line.strip())
            if sso_match:
                sso_url = sso_match.group(1)
                webbrowser.open(sso_url)

                # Read token from user (hidden input)
                # Write prompt to stderr so it works when stdout is piped
                try:
                    token = getpass.getpass(
                        "Paste the login token: ", stream=sys.stderr
                    )
                except OSError:
                    # Not running in a terminal - can't do interactive SSO
                    print("SSO login required but no TTY available.", file=sys.stderr)
                    sys.exit(1)

                # Send token directly to keeper
                if token:
                    process.stdin.write(token + "\n")
                    process.stdin.flush()
                sso_handled = True

    process.wait()
    stdout = "".join(stdout_lines)

    # Read stderr
    stderr_lines = []
    for line in process.stderr:
        if debug:
            print(f"Got stderr line: {line!r}", file=sys.stderr)
        stderr_lines.append(line)
    stderr = "".join(stderr_lines)

    return process.returncode, stdout, stderr


def run_keeper_get(record_name: str, debug: bool = False) -> dict:
    """Run keeper get command and return parsed JSON, handling SSO if needed."""
    cmd = [KEEPER_COMMANDER, "get", record_name, "--format", "json"]

    returncode, stdout, stderr = run_keeper_command(cmd, debug=debug)

    if returncode != 0:
        if returncode == 1 and "Cannot find any object with UID" in stderr:
            print("Cannot find any object with UID", file=sys.stderr)
        sys.exit(returncode)

    # Extract JSON from output (may contain SSO prompts before the JSON)
    json_start = stdout.find("{")
    if json_start == -1:
        print("No JSON found in keeper output", file=sys.stderr)
        if debug:
            print(f"Output was: {stdout}", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(stdout[json_start:])
    except json.JSONDecodeError as e:
        print(f"Failed to parse keeper output: {e}", file=sys.stderr)
        if debug:
            print(f"Output was: {stdout}", file=sys.stderr)
        sys.exit(1)


def extract_field_value(record: dict, field_name: str | None) -> str:
    """Extract field value from record, using smart defaults based on record type."""
    record_type = record.get("type", "").lower()

    # Determine which field to extract
    if field_name is None:
        field_name = DEFAULT_FIELDS_BY_TYPE.get(record_type)
        if field_name is None:
            print(
                f"No default field for record type '{record_type}'. Please specify --field.",
                file=sys.stderr,
            )
            sys.exit(1)

    # Search in fields array
    fields = record.get("fields", [])
    for field in fields:
        field_type = field.get("type", "")
        field_label = field.get("label", "")

        # For text fields, match by label
        if field_type == "text":
            if field_label.lower() == field_name.lower():
                values = field.get("value", [])
                return values[0] if values else ""
        # For other fields, match by type
        elif field_type.lower() == field_name.lower():
            values = field.get("value", [])
            return values[0] if values else ""

    # Search in custom fields
    custom_fields = record.get("custom", [])
    for field in custom_fields:
        field_type = field.get("type", "")
        field_label = field.get("label", "")

        if field_type == "text":
            if field_label.lower() == field_name.lower():
                values = field.get("value", [])
                return values[0] if values else ""
        elif field_type.lower() == field_name.lower():
            values = field.get("value", [])
            return values[0] if values else ""
        # Also check label for non-text fields
        elif field_label.lower() == field_name.lower():
            values = field.get("value", [])
            return values[0] if values else ""

    print(f"Field '{field_name}' not found in record.", file=sys.stderr)
    sys.exit(1)


def parse_insert_path(path: str) -> tuple[str, str]:
    """Parse insert path into folder and secret name.

    Examples:
        'infra\\gitlab\\project\\secret' -> ('infra\\gitlab\\project', 'secret')
        'infra\\gitlab' -> ('infra', 'gitlab')
        'gitlab' -> ('', 'gitlab')
    """
    # Normalize to use backslashes (Keeper format)
    normalized_path = path.replace("/", "\\")

    # Split on last backslash to separate folder path from secret name
    if "\\" in normalized_path:
        parts = normalized_path.rsplit("\\", 1)
        return parts[0], parts[1]
    else:
        return "", normalized_path


def run_keeper_add(
    title: str, folder: str, fields: list[str], debug: bool = False
) -> None:
    """Run keeper record-add command to create a new secret, handling SSO if needed."""
    cmd = [
        KEEPER_COMMANDER,
        "record-add",
        "--title",
        title,
        "--record-type",
        "login",
    ]

    if folder:
        cmd.extend(["--folder", folder])

    # Add fields
    cmd.extend(fields)

    returncode, stdout, stderr = run_keeper_command(cmd, debug=debug)

    if returncode != 0:
        print(f"Error creating record: {stderr}", file=sys.stderr)
        sys.exit(returncode)


def collect_field_input() -> list[str]:
    """Collect field input from user interactively.

    User enters fields like 'login=foo password=bar' and presses Enter to finish.
    """
    print(
        "Enter login fields (e.g., 'login=foo password=bar url=https://acme.com') and press Enter:",
        file=sys.stderr,
    )
    try:
        user_input = input().strip()
    except EOFError:
        return []

    if not user_input:
        return []

    # Split by spaces to get individual field=value pairs
    return user_input.split()


def main():
    if shutil.which(KEEPER_COMMANDER) is None:
        print(
            f"Error: {KEEPER_COMMANDER} command not found. Please install Keeper Commander.",
            file=sys.stderr,
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(
        prog="keys",
        description="KEYS: Straightforward CLI wrapper for Keeper Commander",
        epilog="Example: export OPENAPI_API_KEY=\"$(keys 'OpenAI')\"",
    )
    parser.add_argument(
        "record", help="Record name or path to fetch/insert from Keeper"
    )
    parser.add_argument(
        "--field", "-f", help="Field to extract (defaults based on record type)"
    )
    parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug output"
    )
    parser.add_argument(
        "--insert", "-i", action="store_true", help="Insert a new secret"
    )

    args = parser.parse_args()

    if args.insert:
        # Insert mode
        fields = collect_field_input()
        folder, secret_name = parse_insert_path(args.record)
        run_keeper_add(secret_name, folder, fields, debug=args.debug)
    else:
        # Get mode (original functionality)
        record = run_keeper_get(args.record, debug=args.debug)
        value = extract_field_value(record, args.field)
        print(value, end="")


if __name__ == "__main__":
    main()
