# Telegram Emoji Status

A reusable GitHub Action to update your Telegram account's emoji status using [Telethon](https://github.com/LonamiWebs/Telethon).

Pass your Telegram API credentials, an authenticated session, and a custom emoji ID. The action updates your status whenever a calling workflow runs. It does not define a schedule or trigger.

## Features

- Update your Telegram emoji status from any GitHub Actions workflow.
- Accept a custom emoji document ID as input.
- Use GitHub Actions secrets to protect credentials.
- Support manual runs, scheduled workflows, and other workflow triggers.
- Reuse the same action across multiple repositories.

## Requirements

Before using this action, you need:

- A Telegram API ID and API hash from [my.telegram.org](https://my.telegram.org).
- An authenticated Telethon session file.
- The document ID of the custom emoji you want to use.
- A GitHub repository with Actions enabled.

**Important:** This action uses an existing authenticated session. It does not perform the initial Telegram login or generate a session file.

## Inputs

| Input | Required | Description |
|---|---|---|
| `api_id` | Yes | Telegram API ID. |
| `api_hash` | Yes | Telegram API hash. |
| `session_b64` | Yes | Base64-encoded authenticated Telethon session file. |
| `emoji_id` | Yes | Telegram custom emoji document ID. |

All inputs are required. Store sensitive values in GitHub Actions secrets rather than hardcoding them in workflow files.

## Setup

### 1. Create a Telegram API application

1. Open [my.telegram.org](https://my.telegram.org).
2. Sign in with your Telegram account.
3. Open **API development tools**.
4. Create an application if you do not already have one.
5. Copy your API ID and API hash.

Keep the API hash private.

### 2. Create an authenticated Telethon session

Create a Telethon session on a trusted computer using your Telegram account. Complete the initial login and any required verification.

For example, if you already have a session file named `telegram_status.session`, you can reuse it.

The session file must be compatible with the Telethon version used by this action. Do not upload it to a public repository.

### 3. Encode the session file

Convert the session file to Base64.

On Linux:

```bash
base64 -w 0 telegram_status.session
```

On macOS:

```bash
base64 < telegram_status.session | tr -d '\n'
```

Copy the output and store it as a GitHub Actions secret. Base64 is an encoding format, not encryption.

### 4. Add repository secrets

In the repository that calls this action:

1. Open **Settings → Secrets and variables → Actions**.
2. Select **New repository secret**.
3. Add the following secrets.

| Secret name | Value |
|---|---|
| `TG_API_ID` | Your Telegram API ID |
| `TG_API_HASH` | Your Telegram API hash |
| `TG_SESSION_B64` | The Base64-encoded session file |
| `TG_EMOJI_ID` | The custom emoji document ID |

Use the same secret names in the example workflow below, or change the references to match your own names.

## Usage

Create `.github/workflows/update-telegram-status.yml` in the repository that will use the action.

Replace `YOUR_GITHUB_USERNAME` with the GitHub username or organization that owns this action repository.

```yaml
name: Update Telegram Emoji Status

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  update-status:
    runs-on: ubuntu-latest
    timeout-minutes: 3

    steps:
      - name: Update Telegram emoji status
        uses: YOUR_GITHUB_USERNAME/telegram-emoji-status@v1
        with:
          api_id: ${{ secrets.TG_API_ID }}
          api_hash: ${{ secrets.TG_API_HASH }}
          session_b64: ${{ secrets.TG_SESSION_B64 }}
          emoji_id: ${{ secrets.TG_EMOJI_ID }}
```

Open the **Actions** tab, select **Update Telegram Emoji Status**, and click **Run workflow**.

The workflow will execute the action and update the emoji status associated with the authenticated Telegram account.

### Run every 15 minutes

If you want to update the status automatically, add a schedule to the calling workflow:

```yaml
on:
  schedule:
    - cron: "*/15 * * * *"
  workflow_dispatch:
```

Scheduled workflows use UTC. GitHub may delay scheduled runs during periods of high load.

Scheduling belongs in the calling workflow, not in this action.

## Repository structure

The action repository should contain:

```text
telegram-emoji-status/
├── action.yml
├── update_status.py
├── requirements.txt
└── README.md
```

- `action.yml` defines the action's inputs and execution steps.
- `update_status.py` connects to Telegram and updates the emoji status.
- `requirements.txt` declares the Python dependencies.
- `README.md` documents installation, configuration, and usage.

## Security

Telegram session files grant access to the associated account. Handle them with the same care as passwords.

- Never commit session files, API hashes, or encoded sessions to source control.
- Store credentials in GitHub Actions secrets.
- Never print credentials or session contents in workflow logs.
- Use a dedicated Telegram account if practical.
- Restrict repository access to trusted users.
- Pin third-party actions to full commit SHAs when stronger supply-chain security is required.
- Review and pin Python dependencies to tested versions.
- Revoke the session if you suspect it has been exposed.

Anyone who obtains a valid session file may be able to access the associated Telegram account.

## Troubleshooting

### The session is not authenticated

The session may be invalid, expired, revoked, or incompatible with the installed Telethon version. Generate a new authenticated session and update `TG_SESSION_B64`.

### The emoji status does not change

Check that:

- The emoji ID is a valid Telegram custom emoji document ID.
- The Telegram account can use the specified emoji.
- The workflow uses the correct credentials and session.
- The action completed without a Telegram API error.

### The workflow cannot find a secret

Check the secret name and confirm that it exists in the repository running the workflow. Secrets from another repository are not automatically available.

### The scheduled workflow does not start on time

GitHub Actions schedules are best-effort. Runs can start later than the requested time. Use `workflow_dispatch` to test the action manually.

## Contributing

Contributions and bug reports are welcome. Please include reproduction steps and relevant error messages, but never include API hashes, session files, access tokens, or other credentials.

## License

Choose a license before publishing this action for public reuse. An MIT license is a reasonable option if you want others to use, modify, and redistribute the code with minimal restrictions.
