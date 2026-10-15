import asyncio
import base64
import os
import tempfile
from pathlib import Path

from telethon import TelegramClient, functions, types


async def main() -> None:
    api_id = int(os.environ["TG_API_ID"])
    api_hash = os.environ["TG_API_HASH"]
    session_b64 = os.environ["TG_SESSION_B64"]
    emoji_id = int(os.environ["TG_EMOJI_ID"])

    session_data = base64.b64decode(session_b64, validate=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        session_path = Path(temp_dir) / "telegram_status.session"
        session_path.write_bytes(session_data)
        session_path.chmod(0o600)

        client = TelegramClient(str(session_path), api_id, api_hash)

        try:
            await client.connect()

            if not await client.is_user_authorized():
                raise RuntimeError(
                    "The Telegram session is not authenticated."
                )

            await client(
                functions.account.UpdateEmojiStatusRequest(
                    emoji_status=types.EmojiStatus(
                        document_id=emoji_id
                    )
                )
            )

            print("Telegram emoji status updated successfully.")

        finally:
            await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
