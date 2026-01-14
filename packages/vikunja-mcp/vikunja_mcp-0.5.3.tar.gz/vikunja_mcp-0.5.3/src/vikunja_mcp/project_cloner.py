"""
Project Cloner - Clone Vikunja projects between accounts.

Solves the bot project sharing bug (solutions-2x6i) by:
1. Bot creates project in its own account
2. Bot exports project data (structure, tasks, views, buckets)
3. Bot creates identical project in user's account
4. Bot deletes original project from bot's account

This avoids the ownership problem where bot-created projects
can't be shared with users via the normal API.

Full cloning includes:
- Project metadata (title, description, color)
- Tasks (all fields including dates, priority, done status)
- Task labels
- Task relationships (subtasks, blocking, related, etc.)
- Task assignees
- Task comments
- Task attachments (files)
- Custom views (kanban, list, etc.)
- Buckets (kanban columns)
- Bucket task assignments (via position API)

Bead: solutions-2x6i
"""

import os
import logging
import httpx
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


def clone_project_to_user(
    bot_project_id: int,
    target_user_token: str,
    bot_token: str,
    parent_project_id: Optional[int] = None,
    vikunja_url: str = None,
    delete_original: bool = True,
) -> Dict[str, Any]:
    """
    Clone a bot-created project to a user's account with full fidelity.

    Flow:
    1. Export project data from bot's account (using bot token)
    2. Create identical project in user's account (using user token)
    3. Clone all tasks with full metadata
    4. Clone task labels
    5. Clone task relationships (subtasks, blocking, related, etc.)
    6. Clone task assignees
    7. Clone task comments
    8. Clone task attachments (files)
    9. Clone views (kanban, list, etc.)
    10. Clone buckets (kanban columns)
    11. Assign tasks to correct buckets
    12. Optionally delete original project from bot's account

    Args:
        bot_project_id: ID of project in bot's account
        target_user_token: User's JWT token (to create project in their account)
        bot_token: Bot's API token (to read bot's project)
        parent_project_id: Optional parent project ID in user's account
        vikunja_url: Vikunja instance URL
        delete_original: Whether to delete bot's original project (default: True)

    Returns:
        {
            "success": bool,
            "user_project_id": int,
            "cloned_tasks": int,
            "cloned_views": int,
            "cloned_buckets": int,
            "cloned_relations": int,
            "cloned_assignees": int,
            "cloned_comments": int,
            "cloned_attachments": int,
            "bucket_assignments": int,
            "error": str (if failed)
        }
    """
    if not vikunja_url:
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    result = {
        "success": False,
        "user_project_id": None,
        "cloned_tasks": 0,
        "cloned_views": 0,
        "cloned_buckets": 0,
        "cloned_relations": 0,
        "cloned_assignees": 0,
        "cloned_comments": 0,
        "cloned_attachments": 0,
        "bucket_assignments": 0,
    }

    try:
        # Step 1: Fetch project data from bot's account
        logger.info(f"[clone] Fetching bot project {bot_project_id}")
        project_resp = httpx.get(
            f"{vikunja_url}/api/v1/projects/{bot_project_id}",
            headers={"Authorization": f"Bearer {bot_token}"},
            timeout=10,
        )
        project_resp.raise_for_status()
        bot_project = project_resp.json()

        # Step 2: Fetch all tasks from bot's project
        tasks_resp = httpx.get(
            f"{vikunja_url}/api/v1/projects/{bot_project_id}/tasks",
            headers={"Authorization": f"Bearer {bot_token}"},
            timeout=10,
        )
        tasks_resp.raise_for_status()
        bot_tasks = tasks_resp.json()

        # Step 3: Create project in user's account
        logger.info(f"[clone] Creating project in user account: {bot_project['title']}")
        new_project_resp = httpx.post(
            f"{vikunja_url}/api/v1/projects",
            headers={"Authorization": f"Bearer {target_user_token}"},
            json={
                "title": bot_project["title"],
                "description": bot_project.get("description", ""),
                "hex_color": bot_project.get("hex_color", ""),
                "parent_project_id": parent_project_id or 0,
            },
            timeout=10,
        )
        new_project_resp.raise_for_status()
        new_project = new_project_resp.json()
        new_project_id = new_project["id"]
        result["user_project_id"] = new_project_id

        logger.info(f"[clone] Created user project {new_project_id}")

        # Step 4: Clone all tasks with labels
        task_count = 0
        task_id_map = {}  # Map bot task IDs to user task IDs

        for task in bot_tasks:
            try:
                # Create task
                task_resp = httpx.put(
                    f"{vikunja_url}/api/v1/projects/{new_project_id}/tasks",
                    headers={"Authorization": f"Bearer {target_user_token}"},
                    json={
                        "title": task["title"],
                        "description": task.get("description", ""),
                        "done": task.get("done", False),
                        "priority": task.get("priority", 0),
                        "due_date": task.get("due_date"),
                        "start_date": task.get("start_date"),
                        "end_date": task.get("end_date"),
                    },
                    timeout=10,
                )
                task_resp.raise_for_status()
                new_task = task_resp.json()
                new_task_id = new_task["id"]
                task_id_map[task["id"]] = new_task_id

                # Clone labels if present
                labels = task.get("labels", [])
                if labels:
                    for label in labels:
                        try:
                            # Add label to new task
                            httpx.put(
                                f"{vikunja_url}/api/v1/tasks/{new_task_id}/labels",
                                headers={"Authorization": f"Bearer {target_user_token}"},
                                json={"label_id": label["id"]},
                                timeout=10,
                            )
                        except Exception as e:
                            logger.warning(f"[clone] Failed to add label {label.get('title')} to task: {e}")

                task_count += 1
            except Exception as e:
                logger.warning(f"[clone] Failed to clone task '{task['title']}': {e}")

        result["cloned_tasks"] = task_count
        logger.info(f"[clone] Cloned {task_count} tasks with labels")

        # Step 5: Clone task relationships (subtasks, blocking, etc.)
        relation_count = 0
        for old_task_id, new_task_id in task_id_map.items():
            try:
                # Get task details which includes related_tasks
                task_resp = httpx.get(
                    f"{vikunja_url}/api/v1/tasks/{old_task_id}",
                    headers={"Authorization": f"Bearer {bot_token}"},
                    timeout=10,
                )
                task_resp.raise_for_status()
                task_data = task_resp.json()

                related_tasks = task_data.get("related_tasks", {})
                if related_tasks:
                    for relation_kind, tasks in related_tasks.items():
                        if tasks:
                            for related_task in tasks:
                                old_other_task_id = related_task["id"]
                                # Only create relation if the other task was also cloned
                                if old_other_task_id in task_id_map:
                                    new_other_task_id = task_id_map[old_other_task_id]
                                    try:
                                        httpx.put(
                                            f"{vikunja_url}/api/v1/tasks/{new_task_id}/relations/{relation_kind}/{new_other_task_id}",
                                            headers={"Authorization": f"Bearer {target_user_token}"},
                                            timeout=10,
                                        )
                                        relation_count += 1
                                    except Exception as e:
                                        logger.warning(f"[clone] Failed to create relation {relation_kind} between tasks: {e}")
            except Exception as e:
                logger.warning(f"[clone] Failed to fetch relations for task {old_task_id}: {e}")

        result["cloned_relations"] = relation_count
        logger.info(f"[clone] Cloned {relation_count} task relationships")

        # Step 6: Clone task assignees
        assignee_count = 0
        for old_task_id, new_task_id in task_id_map.items():
            try:
                # Get original task to check assignees
                task_resp = httpx.get(
                    f"{vikunja_url}/api/v1/tasks/{old_task_id}",
                    headers={"Authorization": f"Bearer {bot_token}"},
                    timeout=10,
                )
                task_resp.raise_for_status()
                task_data = task_resp.json()

                assignees = task_data.get("assignees", [])
                if assignees:
                    for assignee in assignees:
                        try:
                            # Assign user to new task
                            httpx.put(
                                f"{vikunja_url}/api/v1/tasks/{new_task_id}/assignees",
                                headers={"Authorization": f"Bearer {target_user_token}"},
                                json={"user_id": assignee["id"]},
                                timeout=10,
                            )
                            assignee_count += 1
                        except Exception as e:
                            logger.warning(f"[clone] Failed to assign user {assignee.get('username')} to task: {e}")
            except Exception as e:
                logger.warning(f"[clone] Failed to fetch assignees for task {old_task_id}: {e}")

        result["cloned_assignees"] = assignee_count
        logger.info(f"[clone] Cloned {assignee_count} task assignees")

        # Step 7: Clone task comments
        comment_count = 0
        for old_task_id, new_task_id in task_id_map.items():
            try:
                # Get comments from original task
                comments_resp = httpx.get(
                    f"{vikunja_url}/api/v1/tasks/{old_task_id}/comments",
                    headers={"Authorization": f"Bearer {bot_token}"},
                    timeout=10,
                )
                comments_resp.raise_for_status()
                comments = comments_resp.json()

                if comments:
                    # Sort by created date to preserve order
                    sorted_comments = sorted(comments, key=lambda c: c.get("created", ""))
                    for comment in sorted_comments:
                        try:
                            # Add comment to new task
                            httpx.put(
                                f"{vikunja_url}/api/v1/tasks/{new_task_id}/comments",
                                headers={"Authorization": f"Bearer {target_user_token}"},
                                json={"comment": comment.get("comment", "")},
                                timeout=10,
                            )
                            comment_count += 1
                        except Exception as e:
                            logger.warning(f"[clone] Failed to clone comment: {e}")
            except Exception as e:
                logger.warning(f"[clone] Failed to fetch comments for task {old_task_id}: {e}")

        result["cloned_comments"] = comment_count
        logger.info(f"[clone] Cloned {comment_count} task comments")

        # Step 8: Clone task attachments
        attachment_count = 0
        for old_task_id, new_task_id in task_id_map.items():
            try:
                # Get attachments from original task
                task_resp = httpx.get(
                    f"{vikunja_url}/api/v1/tasks/{old_task_id}",
                    headers={"Authorization": f"Bearer {bot_token}"},
                    timeout=10,
                )
                task_resp.raise_for_status()
                task_data = task_resp.json()

                attachments = task_data.get("attachments", [])
                if attachments:
                    for attachment in attachments:
                        try:
                            # Download attachment content
                            attachment_id = attachment["id"]
                            content_resp = httpx.get(
                                f"{vikunja_url}/api/v1/tasks/{old_task_id}/attachments/{attachment_id}",
                                headers={"Authorization": f"Bearer {bot_token}"},
                                timeout=30,  # Longer timeout for file downloads
                            )
                            content_resp.raise_for_status()

                            # Upload to new task
                            files = {"files": (attachment.get("file", {}).get("name", "attachment"), content_resp.content, attachment.get("file", {}).get("mime", "application/octet-stream"))}
                            httpx.put(
                                f"{vikunja_url}/api/v1/tasks/{new_task_id}/attachments",
                                headers={"Authorization": f"Bearer {target_user_token}"},
                                files=files,
                                timeout=30,
                            )
                            attachment_count += 1
                        except Exception as e:
                            logger.warning(f"[clone] Failed to clone attachment {attachment.get('file', {}).get('name', 'unknown')}: {e}")
            except Exception as e:
                logger.warning(f"[clone] Failed to fetch attachments for task {old_task_id}: {e}")

        result["cloned_attachments"] = attachment_count
        logger.info(f"[clone] Cloned {attachment_count} task attachments")

        # Step 10: Clone views and buckets
        view_count = 0
        bucket_count = 0
        view_id_map = {}  # Map bot view IDs to user view IDs
        bucket_id_map = {}  # Map bot bucket IDs to user bucket IDs

        try:
            # Fetch views from bot's project
            views_resp = httpx.get(
                f"{vikunja_url}/api/v1/projects/{bot_project_id}/views",
                headers={"Authorization": f"Bearer {bot_token}"},
                timeout=10,
            )
            views_resp.raise_for_status()
            bot_views = views_resp.json()

            # Clone ALL views (including default ones) to preserve exact structure
            # User project gets default views on creation, but we need to map them
            for view in bot_views:
                try:
                    # Check if user already has a view of this kind (default views)
                    user_views_resp = httpx.get(
                        f"{vikunja_url}/api/v1/projects/{new_project_id}/views",
                        headers={"Authorization": f"Bearer {target_user_token}"},
                        timeout=10,
                    )
                    user_views_resp.raise_for_status()
                    user_views = user_views_resp.json()

                    # Try to find matching view by kind and title
                    matching_view = None
                    for uv in user_views:
                        if uv.get("view_kind") == view.get("view_kind") and uv.get("title") == view.get("title"):
                            matching_view = uv
                            break

                    if matching_view:
                        # Use existing view
                        new_view_id = matching_view["id"]
                        view_id_map[view["id"]] = new_view_id
                        logger.info(f"[clone] Using existing view: {view['title']}")
                    else:
                        # Create new view
                        view_data = {
                            "title": view["title"],
                            "view_kind": view["view_kind"],
                        }

                        # Add bucket configuration for kanban views
                        if view["view_kind"] == "kanban":
                            view_data["bucket_configuration_mode"] = "manual"

                        view_resp = httpx.put(
                            f"{vikunja_url}/api/v1/projects/{new_project_id}/views",
                            headers={"Authorization": f"Bearer {target_user_token}"},
                            json=view_data,
                            timeout=10,
                        )
                        view_resp.raise_for_status()
                        new_view = view_resp.json()
                        new_view_id = new_view["id"]
                        view_id_map[view["id"]] = new_view_id
                        view_count += 1

                    # Clone buckets if this is a kanban view
                    if view["view_kind"] == "kanban":
                        try:
                            buckets_resp = httpx.get(
                                f"{vikunja_url}/api/v1/projects/{bot_project_id}/views/{view['id']}/buckets",
                                headers={"Authorization": f"Bearer {bot_token}"},
                                timeout=10,
                            )
                            buckets_resp.raise_for_status()
                            bot_buckets = buckets_resp.json()

                            for bucket in bot_buckets:
                                try:
                                    bucket_resp = httpx.put(
                                        f"{vikunja_url}/api/v1/projects/{new_project_id}/views/{new_view_id}/buckets",
                                        headers={"Authorization": f"Bearer {target_user_token}"},
                                        json={
                                            "title": bucket["title"],
                                            "position": bucket.get("position", 0),
                                            "limit": bucket.get("limit", 0),
                                        },
                                        timeout=10,
                                    )
                                    bucket_resp.raise_for_status()
                                    new_bucket = bucket_resp.json()
                                    bucket_id_map[bucket["id"]] = new_bucket["id"]
                                    bucket_count += 1
                                except Exception as e:
                                    logger.warning(f"[clone] Failed to clone bucket '{bucket['title']}': {e}")
                        except Exception as e:
                            logger.warning(f"[clone] Failed to fetch buckets for view '{view['title']}': {e}")

                except Exception as e:
                    logger.warning(f"[clone] Failed to clone view '{view['title']}': {e}")

            result["cloned_views"] = view_count
            result["cloned_buckets"] = bucket_count
            logger.info(f"[clone] Cloned {view_count} views and {bucket_count} buckets")
        except Exception as e:
            logger.warning(f"[clone] Failed to clone views/buckets: {e}")

        # Step 11: Assign tasks to buckets (using position API)
        # This must be done after all buckets are created
        bucket_assignment_count = 0
        try:
            # For each view, get task bucket assignments from bot's project
            for bot_view_id, new_view_id in view_id_map.items():
                try:
                    # Get task positions/bucket assignments from bot's view
                    # Note: In Vikunja 0.24+, bucket assignments are stored in task_buckets table
                    # We need to fetch tasks and check their bucket assignments
                    for old_task_id, new_task_id in task_id_map.items():
                        try:
                            # Get original task details
                            task_resp = httpx.get(
                                f"{vikunja_url}/api/v1/tasks/{old_task_id}",
                                headers={"Authorization": f"Bearer {bot_token}"},
                                timeout=10,
                            )
                            task_resp.raise_for_status()
                            task_data = task_resp.json()

                            # Check if task has bucket_id (may be 0 or null)
                            old_bucket_id = task_data.get("bucket_id", 0)

                            # If task was in a bucket and we cloned that bucket
                            if old_bucket_id and old_bucket_id in bucket_id_map:
                                new_bucket_id = bucket_id_map[old_bucket_id]
                                try:
                                    # Assign task to bucket using position API
                                    httpx.post(
                                        f"{vikunja_url}/api/v1/tasks/{new_task_id}/position",
                                        headers={"Authorization": f"Bearer {target_user_token}"},
                                        json={
                                            "project_view_id": new_view_id,
                                            "bucket_id": new_bucket_id,
                                            "position": task_data.get("position", 0),
                                        },
                                        timeout=10,
                                    )
                                    bucket_assignment_count += 1
                                except Exception as e:
                                    logger.warning(f"[clone] Failed to assign task {new_task_id} to bucket: {e}")
                        except Exception as e:
                            logger.warning(f"[clone] Failed to check bucket assignment for task {old_task_id}: {e}")
                except Exception as e:
                    logger.warning(f"[clone] Failed to process bucket assignments for view {bot_view_id}: {e}")

            result["bucket_assignments"] = bucket_assignment_count
            logger.info(f"[clone] Assigned {bucket_assignment_count} tasks to buckets")
        except Exception as e:
            logger.warning(f"[clone] Failed to assign tasks to buckets: {e}")

        # Step 12: Delete original project from bot's account
        if delete_original:
            logger.info(f"[clone] Deleting original bot project {bot_project_id}")
            try:
                httpx.delete(
                    f"{vikunja_url}/api/v1/projects/{bot_project_id}",
                    headers={"Authorization": f"Bearer {bot_token}"},
                    timeout=10,
                )
                logger.info(f"[clone] Deleted original bot project {bot_project_id}")
            except Exception as e:
                logger.warning(f"[clone] Failed to delete original project: {e}")

        result["success"] = True
        logger.info(f"[clone] Successfully cloned project {bot_project_id} → {new_project_id}")
        logger.info(f"[clone] Summary: {task_count} tasks, {relation_count} relations, {assignee_count} assignees, {comment_count} comments, {attachment_count} attachments, {view_count} views, {bucket_count} buckets, {bucket_assignment_count} bucket assignments")
        return result

    except Exception as e:
        logger.error(f"[clone] Failed to clone project: {e}")
        result["error"] = str(e)
        return result

