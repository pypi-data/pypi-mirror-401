"""
Staged signup workflow for beta users.

This module implements a multi-stage signup process with explicit checkpoints
to avoid race conditions when provisioning bot accounts and sharing projects.

Bead: solutions-xk9l
"""

import logging
import os
import time
from dataclasses import dataclass
from typing import Optional
import requests

from .bot_provisioning import BotCredentials, ProvisioningError

logger = logging.getLogger(__name__)


@dataclass
class SignupState:
    """State object tracking progress through signup stages."""
    
    # User info
    email: str
    username: str  # Sanitized username for Vikunja (no + or .)
    registration_code: str
    
    # Vikunja user account
    vikunja_user_id: Optional[int] = None
    vikunja_jwt_token: Optional[str] = None
    
    # Bot account
    bot_credentials: Optional[BotCredentials] = None
    bot_verified: bool = False
    
    # Projects
    inbox_project_id: Optional[int] = None
    inbox_shared: bool = False
    
    # Completion
    welcome_task_created: bool = False
    password_reset_sent: bool = False


class SignupWorkflow:
    """Manages the staged signup workflow with explicit verification steps."""
    
    def __init__(self, vikunja_url: str):
        self.vikunja_url = vikunja_url
    
    def stage_1_create_user(self, state: SignupState, password: str) -> SignupState:
        """
        Stage 1: Create Vikunja user account.

        Returns updated state with vikunja_user_id and vikunja_jwt_token.
        Raises exception on failure.
        """
        logger.info(f"[Stage 1] Creating Vikunja user {state.username} for {state.email}")
        print(f"[STAGE 1] Creating user {state.username}", flush=True)

        try:
            # Get admin token for nginx auth (defense in depth)
            vikunja_admin_token = os.environ.get("VIKUNJA_ADMIN_TOKEN", "")
            headers = {"X-Admin-Token": vikunja_admin_token} if vikunja_admin_token else {}

            # Register user with sanitized username (passed from server.py)
            register_resp = requests.post(
                f"{self.vikunja_url}/api/v1/register",
                headers=headers,
                json={"username": state.username, "email": state.email, "password": password},
                timeout=30
            )

            if register_resp.status_code == 200:
                data = register_resp.json()
                state.vikunja_user_id = data.get("id")
                state.vikunja_jwt_token = data.get("token")

                # If no JWT token (email verification enabled), login to get one
                if not state.vikunja_jwt_token:
                    logger.info(f"[Stage 1] No JWT from registration, logging in...")
                    login_resp = requests.post(
                        f"{self.vikunja_url}/api/v1/login",
                        json={"username": state.username, "password": password},
                        timeout=10
                    )
                    if login_resp.status_code == 200:
                        login_data = login_resp.json()
                        state.vikunja_jwt_token = login_data.get("token")
                        state.vikunja_user_id = login_data.get("id") or state.vikunja_user_id
                    else:
                        logger.warning(f"[Stage 1] Login failed: {login_resp.status_code}")

                logger.info(f"[Stage 1] ✓ User created: id={state.vikunja_user_id}")
                return state
            else:
                error_text = register_resp.text
                if "user already exists" in error_text.lower() or "email already" in error_text.lower():
                    raise Exception("An account with this email already exists. Try logging in instead.")
                raise Exception(f"Registration failed: {register_resp.status_code} - {error_text}")

        except Exception as e:
            logger.error(f"[Stage 1] ✗ Failed to create user: {e}")
            raise
    
    def stage_2_provision_bot(self, state: SignupState) -> SignupState:
        """
        Stage 2: Provision personal bot account.

        Returns updated state with bot_credentials.
        Non-fatal - returns state unchanged if bot provisioning fails.
        """
        logger.info(f"[Stage 2] Provisioning bot for {state.username}")
        print(f"[STAGE 2] Provisioning bot", flush=True)

        try:
            from .bot_provisioning import provision_personal_bot, store_bot_credentials

            bot_creds = provision_personal_bot(
                username=state.username,  # Parameter not actually used, bot username is random
                vikunja_url=self.vikunja_url
            )

            # Store bot credentials in database (needed for later retrieval)
            user_id = f"vikunja:{state.username}"
            store_bot_credentials(
                user_id=user_id,
                credentials=bot_creds,
                owner_vikunja_user_id=state.vikunja_user_id,
                owner_vikunja_token=state.vikunja_jwt_token
            )

            state.bot_credentials = bot_creds
            logger.info(f"[Stage 2] ✓ Bot provisioned and stored: {bot_creds.username}")
            print(f"[STAGE 2] ✓ Bot created: {bot_creds.username} (Vikunja ID: {bot_creds.vikunja_user_id})", flush=True)
            return state
            
        except ProvisioningError as e:
            logger.warning(f"[Stage 2] ⚠ Bot provisioning failed (non-fatal): {e}")
            return state
        except Exception as e:
            logger.warning(f"[Stage 2] ⚠ Unexpected error provisioning bot (non-fatal): {e}")
            return state
    
    def stage_3_verify_bot(self, state: SignupState, max_retries: int = 3, retry_delay: float = 1.0) -> SignupState:
        """
        Stage 3: Verify bot account is visible in Vikunja database.
        
        This is the critical checkpoint that ensures the bot is fully committed
        to the database before we try to share projects with it.
        
        Returns updated state with bot_verified=True.
        Non-fatal - returns state unchanged if verification fails.
        """
        if not state.bot_credentials:
            logger.info("[Stage 3] ⊘ Skipping bot verification (no bot credentials)")
            return state
        
        logger.info(f"[Stage 3] Verifying bot {state.bot_credentials.username} is visible in database")
        
        for attempt in range(1, max_retries + 1):
            try:
                # Try to login as the bot - this proves the user exists and is active
                login_resp = requests.post(
                    f"{self.vikunja_url}/api/v1/login",
                    json={
                        "username": state.bot_credentials.username,
                        "password": state.bot_credentials.password
                    },
                    timeout=10
                )
                
                if login_resp.status_code == 200:
                    bot_data = login_resp.json()
                    logger.info(f"[Stage 3] ✓ Bot verified (attempt {attempt}/{max_retries}): "
                               f"id={bot_data.get('id')}, username={bot_data.get('username')}")
                    state.bot_verified = True
                    return state
                else:
                    logger.warning(f"[Stage 3] Bot login failed (attempt {attempt}/{max_retries}): "
                                 f"{login_resp.status_code} - {login_resp.text[:200]}")
                    
            except Exception as e:
                logger.warning(f"[Stage 3] Bot verification error (attempt {attempt}/{max_retries}): {e}")
            
            # Wait before retry (except on last attempt)
            if attempt < max_retries:
                time.sleep(retry_delay)
        
        logger.warning(f"[Stage 3] ⚠ Bot verification failed after {max_retries} attempts (non-fatal)")
        return state

    def stage_4_find_inbox(self, state: SignupState) -> SignupState:
        """
        Stage 4: Find user's Inbox project.

        Returns updated state with inbox_project_id.
        Non-fatal - returns state unchanged if Inbox not found.
        """
        logger.info(f"[Stage 4] Finding Inbox project for {state.email}")

        try:
            projects_resp = requests.get(
                f"{self.vikunja_url}/api/v1/projects",
                headers={"Authorization": f"Bearer {state.vikunja_jwt_token}"},
                timeout=10
            )

            if projects_resp.status_code == 200:
                projects = projects_resp.json()
                logger.info(f"[Stage 4] Found {len(projects)} projects: {[p.get('title') for p in projects]}")

                # Find Inbox (usually titled "Inbox")
                inbox = next((p for p in projects if p.get("title") == "Inbox"), None)

                if inbox:
                    state.inbox_project_id = inbox.get("id")
                    logger.info(f"[Stage 4] ✓ Found Inbox: id={state.inbox_project_id}")
                else:
                    logger.warning(f"[Stage 4] ⚠ No Inbox project found")
            else:
                logger.warning(f"[Stage 4] ⚠ Failed to list projects: {projects_resp.status_code}")

        except Exception as e:
            logger.warning(f"[Stage 4] ⚠ Error finding Inbox (non-fatal): {e}")

        return state

    def stage_5_share_inbox(self, state: SignupState, max_retries: int = 3, retry_delay: float = 1.0) -> SignupState:
        """
        Stage 5: Share Inbox with bot (requires bot_verified=True).

        This is where the race condition was happening. We now only attempt this
        after explicitly verifying the bot exists in stage 3.

        Returns updated state with inbox_shared=True.
        Non-fatal - returns state unchanged if sharing fails.
        """
        if not state.bot_verified:
            logger.info("[Stage 5] ⊘ Skipping Inbox sharing (bot not verified)")
            return state

        if not state.inbox_project_id:
            logger.info("[Stage 5] ⊘ Skipping Inbox sharing (no Inbox found)")
            return state

        logger.info(f"[Stage 5] Sharing Inbox {state.inbox_project_id} with bot {state.bot_credentials.username}")

        for attempt in range(1, max_retries + 1):
            try:
                payload = {
                    "username": state.bot_credentials.username,
                    "right": 1  # Read & Write (0=read, 1=read/write, 2=admin)
                }
                logger.info(f"[Stage 5] DEBUG: Sending payload: {payload}")
                print(f"[STAGE 5] Payload: {payload}", flush=True)

                share_resp = requests.put(
                    f"{self.vikunja_url}/api/v1/projects/{state.inbox_project_id}/users",
                    headers={"Authorization": f"Bearer {state.vikunja_jwt_token}"},
                    json=payload,
                    timeout=10
                )

                if share_resp.status_code == 201:
                    logger.info(f"[Stage 5] ✓ Inbox shared with bot (attempt {attempt}/{max_retries})")
                    state.inbox_shared = True
                    return state
                else:
                    logger.warning(f"[Stage 5] Share failed (attempt {attempt}/{max_retries}): "
                                 f"{share_resp.status_code} - {share_resp.text[:200]}")

            except Exception as e:
                logger.warning(f"[Stage 5] Share error (attempt {attempt}/{max_retries}): {e}")

            # Wait before retry (except on last attempt)
            if attempt < max_retries:
                time.sleep(retry_delay)

        logger.warning(f"[Stage 5] ⚠ Inbox sharing failed after {max_retries} attempts (non-fatal)")
        return state

    def stage_6_create_welcome_task(self, state: SignupState) -> SignupState:
        """
        Stage 6: Create welcome task in Inbox.

        Returns updated state with welcome_task_created=True.
        Non-fatal - returns state unchanged if task creation fails.
        """
        if not state.inbox_project_id:
            logger.info("[Stage 6] ⊘ Skipping welcome task (no Inbox)")
            return state

        logger.info(f"[Stage 6] Creating welcome task in Inbox {state.inbox_project_id}")

        try:
            # Users @mention @eis (dispatcher model) - personal bot is behind the scenes
            bot_mention = "@eis"

            # Build activation link
            activation_link = f"https://mcp.factumerit.app/activate-bot?user={state.username}"

            # HTML description (Vikunja requires HTML, not Markdown)
            description_html = f"""<p>👋 <strong>Welcome to Factumerit!</strong></p>

<p>Your AI assistant <strong>{bot_mention}</strong> is ready to help you manage tasks.</p>

<div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px; margin: 16px 0; border-radius: 4px;">
    <p style="margin: 0 0 12px 0;"><strong>⚡ Activate Your Bot</strong></p>
    <p style="margin: 0 0 12px 0;">Click the link below to connect your bot to this Inbox:</p>
    <p style="margin: 0;"><a href="{activation_link}" style="color: #0284c7; font-weight: 600;">Activate {bot_mention}</a></p>
</div>

<p><strong>After activation, try these commands:</strong></p>
<ul>
    <li><code>{bot_mention} !help</code> - See all commands</li>
    <li><code>{bot_mention} !w Seattle</code> - Weather</li>
    <li><code>{bot_mention} !list</code> - Your tasks</li>
</ul>

<p style="font-size: 14px; color: #666;">Use <code>!</code> commands in any task comment to get help!</p>"""

            task_resp = requests.put(
                f"{self.vikunja_url}/api/v1/projects/{state.inbox_project_id}/tasks",
                headers={"Authorization": f"Bearer {state.vikunja_jwt_token}"},
                json={
                    "title": f"👋 Welcome! Activate your AI assistant {bot_mention}",
                    "description": description_html
                },
                timeout=10
            )

            if task_resp.status_code == 201:
                logger.info(f"[Stage 6] ✓ Welcome task created with activation link")
                state.welcome_task_created = True
            else:
                logger.warning(f"[Stage 6] ⚠ Failed to create welcome task: {task_resp.status_code}")

        except Exception as e:
            logger.warning(f"[Stage 6] ⚠ Error creating welcome task (non-fatal): {e}")

        return state

    def stage_7_send_onboarding_email(self, state: SignupState, password: str) -> SignupState:
        """
        Stage 7: Send onboarding email with credentials.

        Sends branded Factumerit welcome email with login credentials.
        This replaces Vikunja's built-in welcome email.

        Bead: fa-kwoh (smooth onboarding)

        Returns state with password_reset_sent=True on success.
        Non-fatal - returns state unchanged if email fails.
        """
        logger.info(f"[Stage 7] Sending onboarding email to {state.email}")
        print(f"[STAGE 7] Sending onboarding email", flush=True)

        try:
            from .email_service import send_onboarding_email

            user_id = f"vikunja:{state.username}"
            result = send_onboarding_email(
                to_email=state.email,
                username=state.username,
                password=password,
                user_id=user_id,
            )

            if result.success:
                logger.info(f"[Stage 7] ✓ Onboarding email sent: {result.message_id}")
                state.password_reset_sent = True
            else:
                logger.warning(f"[Stage 7] ⚠ Email failed: {result.error}")

        except Exception as e:
            logger.warning(f"[Stage 7] ⚠ Error sending email (non-fatal): {e}")

        return state

    def stage_7_skip_email(self, state: SignupState, temp_password: str) -> SignupState:
        """
        Stage 7 (DEPRECATED): Skip email sending.

        Use stage_7_send_onboarding_email instead.
        Kept for backwards compatibility during transition.
        """
        logger.info(f"[Stage 7] Email sending disabled - user can login with temp password")
        state.password_reset_sent = False
        return state

    def run_full_workflow(self, email: str, username: str, registration_code: str, password: str) -> SignupState:
        """
        Run the complete signup workflow with all stages.

        Returns final state object with completion status of each stage.
        Only stage 1 (user creation) is fatal - all other stages are best-effort.
        """
        logger.info(f"=== Starting signup workflow for {email} (username: {username}) ===")
        logger.info(f"[DEBUG] CODE VERSION: Using 'right' field (commit b4c2fc7)")
        print(f"[SIGNUP WORKFLOW] COMMIT b4c2fc7 - Using 'right' field", flush=True)

        state = SignupState(email=email, username=username, registration_code=registration_code)

        # Stage 1: Create user (FATAL - must succeed)
        state = self.stage_1_create_user(state, password)

        # Stage 2: Provision bot (non-fatal)
        state = self.stage_2_provision_bot(state)

        # Stage 3: Verify bot exists (non-fatal, but required for stage 5)
        # Increased to 10 retries × 2.5s = 25s total to handle database replication lag
        state = self.stage_3_verify_bot(state, max_retries=10, retry_delay=2.5)

        # Stage 4: Find Inbox (non-fatal)
        state = self.stage_4_find_inbox(state)

        # Stage 5: SKIPPED - Sharing moved to /activate-bot endpoint
        # This avoids database replication race conditions during signup
        # User clicks activation link in welcome task to complete bot setup
        logger.info(f"[Stage 5] Skipping Inbox sharing - deferred to activation endpoint")

        # Stage 6: Create welcome task with activation link (non-fatal)
        state = self.stage_6_create_welcome_task(state)

        # Stage 7: Send onboarding email with credentials (non-fatal)
        # Bead: fa-kwoh - replaces Vikunja's built-in welcome email
        state = self.stage_7_send_onboarding_email(state, password)

        logger.info(f"=== Signup workflow complete for {email} ===")
        logger.info(f"    User created: ✓")
        logger.info(f"    Bot provisioned: {'✓' if state.bot_credentials else '✗'}")
        logger.info(f"    Bot verified: {'✓' if state.bot_verified else '✗'}")
        logger.info(f"    Inbox found: {'✓' if state.inbox_project_id else '✗'}")
        logger.info(f"    Inbox shared: {'✓' if state.inbox_shared else '✗'}")
        logger.info(f"    Welcome task: {'✓' if state.welcome_task_created else '✗'}")
        logger.info(f"    Password reset: {'✓' if state.password_reset_sent else '✗'}")

        return state

