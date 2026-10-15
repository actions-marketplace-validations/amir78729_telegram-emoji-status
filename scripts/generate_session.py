#!/usr/bin/env python3
"""
Helper script to generate a Base64-encoded Telethon session string
for use with the Telegram Emoji Status GitHub Action.
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

try:
    from telethon import TelegramClient
except ImportError:
    print("Error: Telethon is not installed.")
    print("Install it by running: pip install -r requirements.txt")
    sys.exit(1)


def main() -> None:
    print("==================================================")
    print("  Telegram Emoji Status - Session Generator")
    print("==================================================")
    print("This script logs into your Telegram account once")
    print("and generates a Base64-encoded session string")
    print("to use as the TG_SESSION_B64 GitHub Secret.\n")

    api_id_input = os.environ.get("TG_API_ID") or input("Enter your Telegram API ID: ").strip()
    try:
        api_id = int(api_id_input)
    except ValueError:
        print("Error: API ID must be an integer.")
        sys.exit(1)

    api_hash = (
        os.environ.get("TG_API_HASH")
        or input("Enter your Telegram API Hash: ").strip()
    )

    if not api_hash:
        print("Error: API Hash cannot be empty.")
        sys.exit(1)

    print("\nStarting Telethon authentication...")
    print("You will be asked for your phone number, the verification code,")
    print("and your 2FA password (if enabled).\n")

    with tempfile.TemporaryDirectory() as temp_dir:
        session_file = Path(temp_dir) / "temp_session"
        client = TelegramClient(str(session_file), api_id, api_hash)

        try:
            client.start()
        except Exception as e:  # noqa: BLE001
            print(f"\nAuthentication failed: {e}")
            sys.exit(1)

        # Telethon writes SQLite session with .session extension
        actual_session_path = session_file.with_suffix(".session")
        if not actual_session_path.exists():
            print("Error: Session file was not generated.")
            sys.exit(1)

        session_bytes = actual_session_path.read_bytes()
        client.disconnect()

        encoded_session = base64.b64encode(session_bytes).decode("ascii")

    print("\n" + "=" * 60)
    print("SUCCESS! Here is your Base64-encoded session string:")
    print("=" * 60 + "\n")
    print(encoded_session)
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Copy the string above (it is one continuous line).")
    print("2. In your GitHub repository, go to:")
    print("   Settings -> Secrets and variables -> Actions -> New repository secret")
    print("3. Set the Name to: TG_SESSION_B64")
    print("4. Paste the string into Secret value and click 'Add secret'.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
