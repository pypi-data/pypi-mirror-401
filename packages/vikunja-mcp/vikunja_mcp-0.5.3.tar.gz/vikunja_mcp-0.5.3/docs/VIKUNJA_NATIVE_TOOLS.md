# Vikunja-Native @eis Tool Registry

**Principle:** @eis can do anything WITHIN a project it's invited to, but cannot access other projects or perform admin operations.

## Included Tools (43)

### Task Operations (5)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `create_task` | Create a new task in the project | None |
| `get_task` | Get task details by ID | None |
| `complete_task` | Mark a task as complete | None |
| `delete_task` | Delete a task | **Always** |
| `set_reminders` | Set reminder times for a task | None |

### Batch Operations (3)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `batch_create_tasks` | Create multiple tasks at once | >10 items |
| `batch_update_tasks` | Update multiple tasks at once | >5 items |
| `complete_tasks_by_label` | Complete all tasks with a label | **Always** |

### Labels (6)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `add_label_to_task` | Add a label to a task | None |
| `create_label` | Create a new label | None |
| `delete_label` | Delete a label | **Always** |
| `list_labels` | List all labels in the project | None |
| `bulk_create_labels` | Create multiple labels at once | None |
| `bulk_relabel_tasks` | Add/remove labels from multiple tasks | >5 items |

### Buckets / Kanban (6)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `create_bucket` | Create a new kanban bucket | None |
| `delete_bucket` | Delete a bucket | **Always** |
| `list_buckets` | List all buckets in a view | None |
| `sort_bucket` | Sort tasks within a bucket | None |
| `move_tasks_by_label_to_buckets` | Move tasks to buckets based on labels | >5 items |
| `list_tasks_by_bucket` | List tasks grouped by bucket | None |

### Views (7)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `create_view` | Create a new view (list, kanban, etc.) | None |
| `create_filtered_view` | Create a view with filters | None |
| `delete_view` | Delete a view | **Always** |
| `list_views` | List all views in the project | None |
| `get_view_tasks` | Get tasks from a specific view | None |
| `get_kanban_view` | Get kanban board layout | None |
| `setup_kanban_board` | Set up a kanban board with buckets | None |

### Task Relations (2)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `create_task_relation` | Create relation (subtask, blocks, etc.) | None |
| `list_task_relations` | List relations for a task | None |

### Assignment (2)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `assign_user` | Assign a user to a task | None |
| `unassign_user` | Remove a user from a task | None |

### Queries (8)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `list_tasks` | List tasks in the project | None |
| `due_today` | Get tasks due today | None |
| `due_this_week` | Get tasks due this week | None |
| `overdue_tasks` | Get overdue tasks | None |
| `high_priority_tasks` | Get high priority tasks | None |
| `upcoming_deadlines` | Get tasks with upcoming deadlines | None |
| `unscheduled_tasks` | Get tasks without due dates | None |
| `focus_now` | Get suggested task to focus on | None |

### Positioning (4)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `set_task_position` | Set task position in a view | None |
| `bulk_set_task_positions` | Set positions for multiple tasks | None |
| `batch_set_positions` | Batch update task positions | None |
| `set_view_position` | Set view position in project | None |

---

## Excluded Tools (35)

### Cross-Project Operations

| Tool | Rationale |
|------|-----------|
| `move_task_to_project` | Would allow moving tasks outside the project scope |
| `move_task_to_project_by_name` | Same - cross-project move |
| `move_tasks_by_label` | Bulk cross-project move |
| `list_all_projects` | Exposes projects user may not have shared with @eis |
| `list_all_tasks` | Cross-project task access |
| `search_all` | Cross-project search |
| `export_all_projects` | Admin-level export |

### Project-Level Operations

| Tool | Rationale |
|------|-----------|
| `create_project` | @eis shouldn't create projects on behalf of users |
| `delete_project` | Destructive, irreversible at project level |
| `update_project` | Project settings should be user-controlled |
| `get_project` | Use `list_tasks` or `task_summary` instead |
| `list_projects` | Cross-project access |
| `setup_project` | Admin setup operation |

### Instance Management

| Tool | Rationale |
|------|-----------|
| `connect_instance` | Multi-instance management is user-level |
| `disconnect_instance` | Could break user's setup |
| `list_instances` | Exposes user's Vikunja instances |
| `rename_instance` | User preference |
| `switch_instance` | User preference |

### Context (Claude Code Specific)

| Tool | Rationale |
|------|-----------|
| `get_context` | Claude Code IDE integration, not applicable |
| `get_active_context` | Claude Code IDE integration |
| `set_active_context` | Claude Code IDE integration |

### Calendar Integration

| Tool | Rationale |
|------|-----------|
| `add_to_calendar` | External service integration |
| `get_calendar_url` | Exposes user's calendar tokens |
| `get_ics_feed` | External service integration |

### Project Configuration

| Tool | Rationale |
|------|-----------|
| `get_project_config` | Admin-level configuration |
| `set_project_config` | Could change project behavior unexpectedly |
| `delete_project_config` | Could break project setup |
| `list_project_configs` | Admin-level access |

### Templates

| Tool | Rationale |
|------|-----------|
| `create_from_template` | Templates may reference other projects |

### XQ (Queue Management)

| Tool | Rationale |
|------|-----------|
| `check_xq` | XQ is a separate system, not Vikunja-native |
| `claim_xq_task` | XQ queue management |
| `complete_xq_task` | XQ queue management |
| `setup_xq` | XQ setup |

### Admin / Health

| Tool | Rationale |
|------|-----------|
| `check_token_health` | Exposes token status, admin concern |
| `analyze_project_dimensions` | Expensive LLM operation, use `task_summary` instead |

---

## Confirmation Levels

| Level | When Used | Examples |
|-------|-----------|----------|
| **ALWAYS** | Destructive/irreversible operations | `delete_task`, `delete_bucket`, `delete_view`, `delete_label`, `complete_tasks_by_label` |
| **COUNT** | Bulk operations affecting >N items | `batch_update_tasks` (>5), `batch_create_tasks` (>10), `bulk_relabel_tasks` (>5) |
| **NONE** | Safe, reversible, single-item operations | Most read operations, single creates |

### Confirmation UX

When confirmation is required, @eis will:
1. Describe the operation and affected items
2. Show estimated cost (if LLM involved)
3. Ask user to reply `@eis yes` to confirm

Example:
```
@eis reorganize by priority

→ This will move 47 tasks across 4 buckets.
  Estimated cost: ~2¢
  Reply "@eis yes" to confirm.
```

---

## Design Decisions

### Why project-scoped?

1. **Security**: Users explicitly invite @eis to projects they want automated
2. **Clarity**: No ambiguity about what @eis can access
3. **Trust**: Users maintain control over their workspace

### Why confirmation for deletes?

1. **Irreversible**: Deleted items cannot be recovered
2. **User intent**: Ensures user really meant to delete
3. **Audit trail**: Confirmation creates a clear record

### Why exclude cross-project moves?

1. **Scope creep**: @eis in Project A shouldn't affect Project B
2. **Permission model**: User may have different collaborators per project
3. **Simplicity**: Keeps @eis behavior predictable

---

*Last updated: 2025-12-31*
*Bead: solutions-2gvm*
