# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| v1      | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please **do not** open a public issue.

Instead, please send an email to Amirhossein Alibakhshi at **amir78729@gmail.com** or use GitHub's private vulnerability reporting feature under the **Security** tab of this repository.

Please include:
- A description of the issue and potential impact.
- Steps to reproduce the issue.
- Any suggested fixes or mitigations.

## Security Best Practices for Users

1. **Protect Your Telegram Session:** A Telegram session string or file grants access to the associated Telegram account. Treat your `TG_SESSION_B64` value with the same confidentiality as a master password.
2. **Never Commit Secrets:** Do not commit `.session` files, API hashes, or base64 session strings to git repositories. Always use GitHub Actions Secrets.
3. **Revocation:** If you suspect a session has been compromised, immediately terminate it from the Telegram app under **Settings → Devices → Active Sessions**.
