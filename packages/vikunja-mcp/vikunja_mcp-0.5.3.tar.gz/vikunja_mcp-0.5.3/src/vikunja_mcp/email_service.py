"""
Email Service for Factumerit.

Sends transactional emails via Resend API.

Bead: solutions-cmzu
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

import resend

logger = logging.getLogger(__name__)


@dataclass
class EmailResult:
    """Result of sending an email."""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None


def _get_resend_client():
    """Get Resend client if API key is configured."""
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        return None
    resend.api_key = api_key
    return resend


def send_welcome_email(
    to_email: str,
    reset_token: str,
    user_name: Optional[str] = None,
) -> EmailResult:
    """Send welcome email to new user.

    Args:
        to_email: Recipient email address
        reset_token: Password reset token from Vikunja
        user_name: Optional name for personalization

    Returns:
        EmailResult with success status
    """
    client = _get_resend_client()
    if not client:
        logger.warning("RESEND_API_KEY not configured, skipping email")
        return EmailResult(success=False, error="Email not configured")

    # Build reset URL
    reset_url = f"https://vikunja.factumerit.app/user/settings/general?passwordConfirmToken={reset_token}"

    # Personalize greeting
    greeting = f"Hi {user_name}," if user_name else "Hi there,"

    # HTML email body
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #2563eb; }}
        .button {{ display: inline-block; background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
        .button:hover {{ background: #1d4ed8; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 14px; color: #666; }}
        .tip {{ background: #f0f9ff; border-left: 4px solid #2563eb; padding: 12px 16px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">FACTUM ERIT</div>
    </div>

    <p>{greeting}</p>

    <p>Welcome to FACTUM ERIT! Your account is ready.</p>

    <p>Click the button below to set your password and start using your AI-powered task assistant:</p>

    <p style="text-align: center;">
        <a href="{reset_url}" class="button">Set Your Password</a>
    </p>

    <div class="tip">
        <strong>Quick tip:</strong> After logging in, try creating a task with <code>@eis</code> in the title:
        <br><br>
        <code>@eis remind me to check email tomorrow</code>
    </div>

    <p>Your personal AI assistant <strong>@eis</strong> is already set up in your project. Just mention @eis in any task to get help with:</p>
    <ul>
        <li>Creating and organizing tasks</li>
        <li>Setting reminders and due dates</li>
        <li>Getting weather, stocks, and news</li>
        <li>AI-powered task planning</li>
    </ul>

    <p>Questions? Just reply to this email.</p>

    <p>— The FACTUM ERIT Team</p>

    <div class="footer">
        <p>This link expires in 72 hours. If you didn't request this account, you can ignore this email.</p>
        <p style="margin-top: 20px;">
            <strong>FACTUM ERIT</strong><br>
            <em>"it will have been done"</em>
        </p>
        <p><a href="https://factumerit.app">factumerit.app</a></p>
    </div>
</body>
</html>
"""

    # Plain text fallback
    text_body = f"""{greeting}

Welcome to FACTUM ERIT! Your account is ready.

Set your password here:
{reset_url}

After logging in, try creating a task with @eis in the title:
  @eis remind me to check email tomorrow

Your AI assistant @eis can help with:
- Creating and organizing tasks
- Setting reminders and due dates
- Getting weather, stocks, and news
- AI-powered task planning

Questions? Just reply to this email.

— The FACTUM ERIT Team

This link expires in 72 hours.

FACTUM ERIT
"it will have been done"
"""

    try:
        response = resend.Emails.send({
            "from": "FACTUM ERIT <hello@factumerit.app>",
            "to": [to_email],
            "subject": "Your FACTUM ERIT account is ready",
            "html": html_body,
            "text": text_body,
        })

        logger.info(f"Welcome email sent to {to_email}: {response.get('id')}")
        return EmailResult(success=True, message_id=response.get("id"))

    except Exception as e:
        logger.exception(f"Failed to send welcome email to {to_email}")
        return EmailResult(success=False, error=str(e))


def send_onboarding_email(
    to_email: str,
    username: str,
    password: Optional[str] = None,
    user_id: Optional[str] = None,
    user_name: Optional[str] = None,
    auth_method: str = "password",
) -> EmailResult:
    """
    Send onboarding email - unified for both password and Google users.

    This replaces Vikunja's built-in welcome email with a branded
    Factumerit experience. The only difference between password and
    Google users is the credentials section.

    Bead: fa-kwoh (smooth onboarding)
    Bead: fa-8g1r (Welcome message for Google users)

    Args:
        to_email: Recipient email address
        username: Vikunja username for login
        password: Generated password (only for password auth)
        user_id: User ID for action token generation (e.g., "vikunja:alice")
        user_name: Optional display name for personalization
        auth_method: "password" or "google"

    Returns:
        EmailResult with success status
    """
    client = _get_resend_client()
    if not client:
        logger.warning("RESEND_API_KEY not configured, skipping email")
        return EmailResult(success=False, error="Email not configured")

    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    # Personalize greeting
    greeting = f"Hi {user_name}," if user_name else "Hi there,"
    display_name = user_name or username

    # Auth-specific sections
    if auth_method == "google":
        intro_text = "Welcome to FACTUM ERIT! Your account is ready and linked to your Google account."
        credentials_html = """
        <div class="auth-info">
            <span style="color: #666;">Sign in anytime with</span>
            <strong style="color: #4285f4;">G</strong><strong style="color: #ea4335;">o</strong><strong style="color: #fbbc05;">o</strong><strong style="color: #4285f4;">g</strong><strong style="color: #34a853;">l</strong><strong style="color: #ea4335;">e</strong>
        </div>
"""
        credentials_text = f"""Sign in anytime at: {vikunja_url}
(Just click "Continue with Google")"""
        footer_text = "You can sign in anytime using your Google account."
        button_text = "Open FACTUM ERIT"
    else:
        intro_text = "Welcome to FACTUM ERIT! Your account is ready. Here are your login credentials:"
        credentials_html = f"""
        <div class="credentials">
            <div class="credentials-row">
                <span class="credentials-label">Username:</span>
                <span class="credentials-value">{username}</span>
            </div>
            <div class="credentials-row">
                <span class="credentials-label">Password:</span>
                <span class="credentials-value">{password}</span>
            </div>
        </div>
"""
        credentials_text = f"""YOUR LOGIN CREDENTIALS
----------------------
Username: {username}
Password: {password}

Log in at: {vikunja_url}"""
        footer_text = "Save this email - you'll need your password to log in.<br>You can change your password after logging in at Settings &rarr; General."
        button_text = "Log In to FACTUM ERIT"

    # HTML email body (unified template)
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }}
        .logo {{
            font-size: 28px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .credentials {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin: 24px 0;
        }}
        .credentials-row {{
            display: flex;
            margin: 8px 0;
        }}
        .credentials-label {{
            color: #666;
            width: 100px;
            flex-shrink: 0;
        }}
        .credentials-value {{
            font-family: 'Monaco', 'Menlo', monospace;
            font-weight: 600;
            color: #333;
        }}
        .auth-info {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 24px 0;
            text-align: center;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            padding: 14px 28px;
            text-decoration: none;
            border-radius: 8px;
            margin: 8px 4px;
            font-weight: 500;
        }}
        .button:hover {{
            opacity: 0.9;
        }}
        .button-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .tip {{
            background: #f0f9ff;
            border-left: 4px solid #667eea;
            padding: 16px 20px;
            margin: 24px 0;
            border-radius: 0 8px 8px 0;
        }}
        .tip-title {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 8px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 14px;
            color: #666;
            text-align: center;
        }}
        code {{
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">FACTUM ERIT</div>
            <p style="color: #666; margin: 10px 0 0 0;">Your AI-powered task assistant</p>
        </div>

        <p>{greeting}</p>

        <p>{intro_text}</p>

        {credentials_html}

        <div class="button-container">
            <a href="{vikunja_url}" class="button">{button_text}</a>
        </div>

        <div class="tip">
            <div class="tip-title">Getting Started</div>
            <p style="margin: 0;">Try these commands in any task comment:</p>
            <p style="margin: 10px 0 0 0;"><code>@eis !help</code> · <code>@eis !w Seattle</code> · <code>@eis !list</code></p>
        </div>

        <p>Your assistant <strong>@eis</strong> responds to <code>!</code> commands:</p>
        <ul>
            <li><code>!help</code> - See all available commands</li>
            <li><code>!w [city]</code> - Weather forecast</li>
            <li><code>!list</code> - View your tasks</li>
        </ul>

        <p>Questions? Reply to this email anytime.</p>

        <p style="margin-top: 30px;">— The FACTUM ERIT Team</p>

        <div class="footer">
            <p>{footer_text}</p>
            <p style="margin-top: 20px;">
                <strong>FACTUM ERIT</strong><br>
                <em>"it will have been done"</em>
            </p>
            <p><a href="https://factumerit.app" style="color: #667eea;">factumerit.app</a></p>
        </div>
    </div>
</body>
</html>
"""

    # Plain text fallback
    text_body = f"""{greeting}

{intro_text}

{credentials_text}

GETTING STARTED
---------------
Try these commands in any task comment:
  @eis !help  |  @eis !w Seattle  |  @eis !list

Your assistant @eis responds to ! commands:
- !help - See all available commands
- !w [city] - Weather forecast
- !list - View your tasks

Questions? Reply to this email anytime.

— The FACTUM ERIT Team

FACTUM ERIT
"it will have been done"
"""

    try:
        response = resend.Emails.send({
            "from": "FACTUM ERIT <hello@factumerit.app>",
            "to": [to_email],
            "subject": f"Welcome to FACTUM ERIT, {display_name}!",
            "html": html_body,
            "text": text_body,
        })

        logger.info(f"Onboarding email ({auth_method}) sent to {to_email}: {response.get('id')}")
        return EmailResult(success=True, message_id=response.get("id"))

    except Exception as e:
        logger.exception(f"Failed to send onboarding email to {to_email}")
        return EmailResult(success=False, error=str(e))


def send_google_welcome_email(
    to_email: str,
    user_name: Optional[str] = None,
) -> EmailResult:
    """
    Send welcome email for Google OAuth users.

    Wrapper around send_onboarding_email for backwards compatibility.

    Bead: fa-8g1r (Welcome message missing for Google Login users)
    """
    # Extract username from email for display
    username = to_email.split("@")[0]
    return send_onboarding_email(
        to_email=to_email,
        username=username,
        password=None,
        user_name=user_name,
        auth_method="google",
    )


def send_test_email(to_email: str) -> EmailResult:
    """Send a test email to verify configuration.

    Args:
        to_email: Recipient email address

    Returns:
        EmailResult with success status
    """
    client = _get_resend_client()
    if not client:
        return EmailResult(success=False, error="RESEND_API_KEY not configured")

    try:
        response = resend.Emails.send({
            "from": "FACTUM ERIT <hello@factumerit.app>",
            "to": [to_email],
            "subject": "Test email from FACTUM ERIT",
            "text": "This is a test email. If you received it, email is working!",
        })

        return EmailResult(success=True, message_id=response.get("id"))

    except Exception as e:
        return EmailResult(success=False, error=str(e))


def send_claude_config_email(
    to_email: str,
    api_token: str,
    vikunja_url: str = "https://vikunja.factumerit.app",
    user_name: Optional[str] = None,
) -> EmailResult:
    """
    Send Claude Desktop MCP configuration email after bot activation.

    This email contains the API token and setup instructions that users
    need to connect Claude Desktop to their Vikunja account.

    Sent during bot activation (after user clicks activate link).
    Bypasses WAF issues that blocked the welcome task creation.

    Args:
        to_email: Recipient email address
        api_token: Vikunja API token for Claude Desktop
        vikunja_url: Vikunja instance URL
        user_name: Optional name for personalization

    Returns:
        EmailResult with success status
    """
    import json

    client = _get_resend_client()
    if not client:
        logger.warning("RESEND_API_KEY not configured, skipping Claude config email")
        return EmailResult(success=False, error="Email not configured")

    greeting = f"Hi {user_name}," if user_name else "Hi there,"

    # Build platform-specific MCP configs with full paths
    # (Claude Desktop doesn't inherit shell PATH, so full paths required)
    # Use @latest to ensure users get newest version without cache issues
    mac_config = f'''{{"mcpServers": {{
  "vikunja": {{
    "command": "/Users/YOUR_USERNAME/.local/bin/uvx",
    "args": ["vikunja-mcp@latest"],
    "env": {{
      "VIKUNJA_URL": "{vikunja_url}",
      "VIKUNJA_TOKEN": "{api_token}"
    }}
  }}
}}}}'''

    win_config = f'''{{"mcpServers": {{
  "vikunja": {{
    "command": "C:\\\\Users\\\\YOUR_USERNAME\\\\.local\\\\bin\\\\uvx.exe",
    "args": ["vikunja-mcp@latest"],
    "env": {{
      "VIKUNJA_URL": "{vikunja_url}",
      "VIKUNJA_TOKEN": "{api_token}"
    }}
  }}
}}}}'''

    # HTML email
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #2563eb; }}
        .step {{ background: #f8fafc; border-radius: 8px; padding: 16px; margin: 16px 0; }}
        .step-number {{ display: inline-block; width: 28px; height: 28px; background: #2563eb; color: white; border-radius: 50%; text-align: center; line-height: 28px; font-weight: bold; margin-right: 8px; }}
        pre {{ background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; }}
        code {{ font-family: 'SF Mono', Monaco, monospace; }}
        .config-box {{ background: #0f172a; color: #22d3ee; padding: 16px; border-radius: 8px; font-family: monospace; font-size: 12px; white-space: pre-wrap; word-break: break-all; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 14px; color: #666; text-align: center; }}
        .token-hint {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px 16px; margin: 16px 0; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🤖 Claude Desktop Setup</div>
    </div>

    <p>{greeting}</p>

    <p>Your AI assistant is activated! Here's how to connect Claude Desktop to your Vikunja tasks.</p>

    <div class="step">
        <span class="step-number">1</span>
        <strong>Install uv (one-time)</strong>
        <p style="margin: 8px 0 0 36px; font-size: 14px;">
            <strong>macOS/Linux:</strong><br>
            <code>curl -LsSf https://astral.sh/uv/install.sh | sh</code>
        </p>
        <p style="margin: 8px 0 0 36px; font-size: 14px;">
            <strong>Windows (PowerShell):</strong><br>
            <code>powershell -c "irm https://astral.sh/uv/install.ps1 | iex"</code>
        </p>
    </div>

    <div class="step">
        <span class="step-number">2</span>
        <strong>Add to Claude Desktop config</strong>
        <p style="margin: 8px 0 0 36px; font-size: 14px;">
            Find your config file:<br>
            • <strong>macOS:</strong> <code>~/Library/Application Support/Claude/claude_desktop_config.json</code><br>
            • <strong>Windows:</strong> <code>%APPDATA%\\Claude\\claude_desktop_config.json</code>
        </p>
        <p style="margin: 12px 0 4px 36px; font-size: 14px;"><strong>macOS/Linux config</strong> (replace YOUR_USERNAME):</p>
        <div class="config-box">{mac_config}</div>
        <p style="margin: 12px 0 4px 36px; font-size: 14px;"><strong>Windows config</strong> (replace YOUR_USERNAME):</p>
        <div class="config-box">{win_config}</div>
        <p style="margin: 8px 0 0 36px; font-size: 13px; color: #666;">
            💡 To find your username, run <code>whoami</code> in Terminal (Mac) or PowerShell (Windows)
        </p>
    </div>

    <div class="step">
        <span class="step-number">3</span>
        <strong>Restart Claude Desktop</strong>
        <p style="margin: 8px 0 0 36px; font-size: 14px;">
            <strong>macOS:</strong> Cmd+Q, then reopen<br>
            <strong>Windows:</strong> Close Claude, open Task Manager, end "Claude" processes, reopen
        </p>
    </div>

    <div class="step">
        <span class="step-number">4</span>
        <strong>Test it!</strong>
        <p style="margin: 8px 0 0 36px; font-size: 14px;">
            Ask Claude: <em>"What's on my todo list?"</em>
        </p>
    </div>

    <div class="token-hint">
        <strong>🔐 Your API token starts with:</strong> <code>{api_token[:16]}...</code><br>
        <span style="font-size: 12px;">Keep this email - you'll need the token if you set up another device.</span>
    </div>

    <div class="footer">
        <p>📖 <a href="https://github.com/ivantohelpyou/vikunja-mcp">Full documentation</a></p>
        <p style="color: #999; font-size: 12px;">FACTUM ERIT<br><em>"it will have been done"</em></p>
    </div>
</body>
</html>
"""

    # Plain text version
    text_body = f"""{greeting}

Your AI assistant is activated! Here's how to connect Claude Desktop to your Vikunja tasks.

STEP 1: Install uv (one-time)
-----------------------------
macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

STEP 2: Add to Claude Desktop config
-------------------------------------
Find your config file:
- macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
- Windows: %APPDATA%\\Claude\\claude_desktop_config.json

macOS/Linux config (replace YOUR_USERNAME with your username):

{mac_config}

Windows config (replace YOUR_USERNAME with your username):

{win_config}

To find your username, run: whoami

STEP 3: Restart Claude Desktop
------------------------------
macOS: Cmd+Q, then reopen
Windows: Close Claude, open Task Manager, end "Claude" processes, reopen

STEP 4: Test it!
----------------
Ask Claude: "What's on my todo list?"

---
Your API token starts with: {api_token[:16]}...
Keep this email - you'll need the token if you set up another device.

Full docs: https://github.com/ivantohelpyou/vikunja-mcp

FACTUM ERIT
"it will have been done"
"""

    try:
        response = resend.Emails.send({
            "from": "FACTUM ERIT <hello@factumerit.app>",
            "to": [to_email],
            "subject": "🔧 Your Claude Desktop Setup Instructions",
            "html": html_body,
            "text": text_body,
        })

        logger.info(f"Sent Claude config email to {to_email}, message_id={response.get('id')}")
        return EmailResult(success=True, message_id=response.get("id"))

    except Exception as e:
        logger.error(f"Failed to send Claude config email to {to_email}: {e}")
        return EmailResult(success=False, error=str(e))
