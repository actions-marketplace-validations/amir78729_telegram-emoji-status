# Telegram Emoji Status

[![Marketplace](https://img.shields.io/badge/Marketplace-Telegram%20Emoji%20Status-blue?logo=github&style=flat-square)](https://github.com/marketplace/actions/telegram-emoji-status)
[![Latest Release](https://img.shields.io/github/v/release/amir78729/telegram-emoji-status?style=flat-square)](https://github.com/amir78729/telegram-emoji-status/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white&style=flat-square)](https://www.python.org/)

A reusable GitHub Action to update your Telegram account's custom emoji status using [Telethon](https://github.com/LonamiWebs/Telethon).

Pass your Telegram API credentials, an authenticated session, and a custom emoji ID. The action updates your status whenever a calling workflow runs.

---

## Features

- **Automated status updates:** Update your Telegram emoji status from any GitHub Actions workflow.
- **Custom emoji support:** Accepts any Telegram custom emoji document ID.
- **Secure:** Runs securely using GitHub Actions Secrets with zero credential leaks.
- **Flexible triggering:** Support for manual triggers (`workflow_dispatch`), cron schedules, and event-driven updates.
- **Zero workspace bloat:** Composite action runs cleanly without needing to checkout caller repositories.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| `api_id` | **Yes** | Telegram API ID from [my.telegram.org](https://my.telegram.org). |
| `api_hash` | **Yes** | Telegram API hash from [my.telegram.org](https://my.telegram.org). |
| `session_b64` | **Yes** | Base64-encoded authenticated Telethon session file. |
| `emoji_id` | **Yes** | Telegram custom emoji document ID. |

---

## Setup Guide

### 1. Get Telegram API Credentials

1. Go to [my.telegram.org](https://my.telegram.org) and sign in.
2. Select **API development tools**.
3. Create an application if you have not already.
4. Copy your **API ID** and **API Hash**.

### 2. Generate Your Base64 Session

You need an authenticated session string to authorize Telegram. You can generate one easily using the included helper script:

```bash
# Clone the repository and install dependencies
git clone https://github.com/amir78729/telegram-emoji-status.git
cd telegram-emoji-status
pip install -r requirements.txt

# Run the interactive generator
python scripts/generate_session.py
```

The script will prompt for your API ID, API Hash, and phone number, verify the login code, and print out a clean `TG_SESSION_B64` value ready for GitHub Secrets.

<details>
<summary>Manual session creation (Alternative)</summary>

If you already have a Telethon session file (e.g. `telegram_status.session`):

- **macOS:**
  ```bash
  base64 < telegram_status.session | tr -d '\n'
  ```
- **Linux:**
  ```bash
  base64 -w 0 telegram_status.session
  ```
</details>

### 3. How to Find Custom Emoji IDs

To find the document ID of a custom emoji:
1. In Telegram, forward a message containing the custom emoji to a bot like [@ShowJsonBot](https://t.me/ShowJsonBot) or [@getidsbot](https://t.me/getidsbot).
2. Look for `custom_emoji_id` or `document_id` in the returned JSON (e.g. `5373141891138497672`).

### 4. Configure GitHub Repository Secrets

In the GitHub repository that will run the workflow:

1. Navigate to **Settings → Secrets and variables → Actions**.
2. Click **New repository secret** and add the following:

| Secret Name | Description |
|---|---|
| `TG_API_ID` | Your Telegram API ID |
| `TG_API_HASH` | Your Telegram API Hash |
| `TG_SESSION_B64` | The Base64-encoded session string from Step 2 |
| `TG_EMOJI_ID` | The custom emoji document ID from Step 3 |

---

## Usage

Create `.github/workflows/update-telegram-status.yml` in your target repository:

```yaml
name: Update Telegram Emoji Status

on:
  workflow_dispatch:
  # Optional: Run automatically every hour
  # schedule:
  #   - cron: "0 * * * *"

permissions:
  contents: read

jobs:
  update-status:
    runs-on: ubuntu-latest
    timeout-minutes: 3

    steps:
      - name: Update Telegram emoji status
        uses: amir78729/telegram-emoji-status@v1
        with:
          api_id: ${{ secrets.TG_API_ID }}
          api_hash: ${{ secrets.TG_API_HASH }}
          session_b64: ${{ secrets.TG_SESSION_B64 }}
          emoji_id: ${{ secrets.TG_EMOJI_ID }}
```

---

## Repository Structure

```text
telegram-emoji-status/
├── .github/
│   ├── dependabot.yml       # Automated dependency updates
│   └── workflows/
│       └── ci.yml           # Code linting & validation
├── scripts/
│   └── generate_session.py  # User helper to generate TG_SESSION_B64
├── action.yml               # Action definition and composite steps
├── update_status.py         # Telethon status updater logic
├── requirements.txt         # Python dependencies
├── SECURITY.md              # Security and vulnerability reporting
├── LICENSE                  # MIT License
└── README.md                # Documentation
```

---

## Security

Telegram session credentials grant access to your account.
- **Never** commit `.session` files or raw Base64 strings to public repositories.
- Always use **GitHub Secrets** for credentials.
- If you believe a session was compromised, revoke it immediately in the Telegram app via **Settings → Devices → Terminate Session**.
- For more information, see [SECURITY.md](SECURITY.md).

---

## Contributing

Contributions and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).
