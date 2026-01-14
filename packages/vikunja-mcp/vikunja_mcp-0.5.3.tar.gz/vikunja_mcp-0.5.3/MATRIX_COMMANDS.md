# Matrix Bot Commands Reference

## Quick Filter Commands (ECO Mode - No AI Cost)

### Task Filters by Due Date
- `!oops` / `!overdue` - Show overdue tasks
- `!now` / `!today` - Show tasks due today
- `!week` - Show tasks due this week
- `!maybe` / `!unscheduled` - Show tasks with no due date

### Task Filters by Priority
- `!fire` / `!urgent` - Show priority 5 (urgent) tasks
- `!vip` / `!priority` - Show high priority tasks (3+)

### Task Filters by Focus
- `!zen` / `!focus` - Show focus mode tasks (high priority + due soon)

### All Tasks
- `!tasks` / `!list` - Show all active tasks

## Task Management Commands

### Complete Tasks
- `!done <title>` - Mark task as complete by title (fuzzy match)
- `!complete <title>` - Alias for `!done`
- `!finish <title>` - Alias for `!done`
- `!check <title>` - Alias for `!done`

## Connection Commands

### Connect to Vikunja
- `!vik <token>` - Connect to Vikunja with API token
  - Example: `!vik tk_abc123...`
  - Token is stored encrypted in PostgreSQL
  - Auto-sets active instance for first-time users

### View Connections
- `!viki` - List all connected Vikunja instances
- `!instances` - Alias for `!viki`
- `!connections` - Alias for `!viki`
- Shows:
  - Instance name
  - URL
  - Active instance (marked with ✓)
  - Source (config vs user token)

### Disconnect
- `!novik [instance]` - Disconnect from Vikunja instance
- `!disconnect [instance]` - Alias for `!novik`
- Defaults to "default" instance if not specified

### Test Connection
- `!test` - Test Vikunja connection and show diagnostics
- Shows:
  - Git version (deployment hash)
  - Project count
  - Active instance
  - Token status
  - First 10 active tasks preview

## Information Commands

### Statistics
- `!stats` - Show task summary statistics
  - Total tasks
  - By priority
  - By due date
  - Unscheduled count

## Settings Commands

### Timezone
- `!tz` - View current timezone
- `!tz <timezone>` - Set timezone
  - Example: `!tz America/Los_Angeles`
  - Example: `!tz Europe/London`
- `!timezone` - Alias for `!tz`

### AI Model
- `!model` - View current AI model
- `!model <name>` - Change AI model
  - Available models depend on configuration

### API Key
- `!apikey` - View API key status
- `!apikey <key>` - Set API key (isolated instances only)

### Credits
- `!credits` - Check AI usage and remaining credits

## Context Commands

### Instance Context
- `!switch` - View current Vikunja instance
- `!switch <instance>` - Switch to different instance
- `!instance` - Alias for `!switch`

### Project Context
- `!project` - View active project
- `!project <name>` - Set active project
  - Filters all commands to this project

### View All Context
- `!context` - Show current instance, project, and timezone

## Room Binding Commands (Rooms Only)

### Bind Room to Project
- `!bind <project>` - Bind current room to a Vikunja project
  - All tasks created in this room go to the bound project
  - Only works in rooms, not DMs

### View Binding
- `!binding` - Show current room's project binding

### Remove Binding
- `!unbind` - Remove room's project binding

## Help

- `!help` - Show command list
- `!h` - Alias for `!help`
- `!?` - Alias for `!help`

## Natural Language

You can also just type naturally! The AI will:
- Parse your intent
- Execute the appropriate Vikunja API calls
- Format the response

Examples:
- "Show me my tasks for tomorrow"
- "Create a task to buy groceries due Friday"
- "What's on my plate this week?"
- "Mark 'write report' as done"

---

## Implementation Notes

### ECO Mode
Commands marked "ECO Mode" execute directly without AI processing, saving API costs.

### Token Storage
- User tokens stored encrypted in PostgreSQL
- Uses Fernet encryption (AES-128-CBC)
- Auto-expires based on Vikunja token expiration

### Multi-Instance Support
- Users can connect to multiple Vikunja instances
- Switch between instances with `!switch`
- Each instance has separate token storage

### Room Binding
- Binds Matrix rooms to Vikunja projects
- Stored in PostgreSQL `room_bindings` table
- Only works in rooms, not DMs

