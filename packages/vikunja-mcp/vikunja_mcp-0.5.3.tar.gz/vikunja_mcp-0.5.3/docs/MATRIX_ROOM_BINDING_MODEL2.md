# Matrix Room Binding - Model 2 (Shared Context)

**Status**: Future Enhancement (Post-V1)  
**Date**: 2025-12-24  
**Related**: MATRIX_TRANSPORT_SPEC_V2.md

---

## Overview

**Model 2** extends personal room bindings (Model 1) with **shared room context** - allowing room admins to bind a room to a Vikunja scope (instances, projects, subprojects, views) that applies to **all users** in that room.

This creates a **collaborative workspace** where the room itself represents a shared project context.

---

## Conceptual Model

### Model 1 (V1 - Personal Context)
```
Room #client-xyz:
  Alice: !bind Client XYZ
  [Alice's personal config: room → "Client XYZ"]
  
  Alice: !today
  eis: [DMs Alice] 📋 Due Today (Client XYZ): ...
  
  Bob: !today
  eis: [DMs Bob] 📋 Due Today (no project): ...
```

**Each user has their own room→project mapping. Privacy preserved.**

---

### Model 2 (Future - Shared Context)
```
Room #client-xyz:
  Alice (room admin): !bind-room Client XYZ
  [Room itself is bound to "Client XYZ" for everyone]
  
  Alice: !today
  eis: [DMs Alice] 📋 Due Today (Client XYZ): ...
  
  Bob: !today
  eis: [DMs Bob] 📋 Due Today (Client XYZ): ...  # Same project!
```

**Room = workspace = project. All users share the same context.**

---

## Scope Hierarchy

Rooms can be bound to different levels of Vikunja scope:

### 1. Instance Scope
```
!bind-room instance:production
```
- All commands in this room use the "production" Vikunja instance
- Users can still have personal project context within that instance

### 2. Project Scope
```
!bind-room project:Client XYZ
```
- All commands default to "Client XYZ" project
- Most common use case

### 3. Subproject Scope
```
!bind-room subproject:Client XYZ > Q1 Deliverables
```
- Narrow focus to specific subproject
- Useful for sprint rooms, milestone tracking

### 4. View Scope
```
!bind-room view:Sprint Board
```
- Bind to a saved Vikunja view (filter + sort)
- Advanced use case for custom workflows

### 5. Multi-Scope
```
!bind-room instance:production project:Client XYZ
```
- Combine instance + project for full context
- Ensures everyone is on same instance AND project

---

## Permission Model

### Who Can Bind Rooms?

**Room Admins Only** (Matrix power level ≥ 50)

```python
async def can_bind_room(room_id: str, user_id: str) -> bool:
    """Check if user has permission to bind room."""
    
    # Bot admins can always bind
    if user_id in MATRIX_ADMIN_IDS:
        return True
    
    # Check Matrix room power level
    room = await client.get_room(room_id)
    power_levels = room.power_levels
    
    user_level = power_levels.get_user_level(user_id)
    required_level = 50  # Room admin
    
    return user_level >= required_level
```

**Rationale**:
- Prevents chaos (anyone binding/unbinding)
- Aligns with Matrix permission model
- Room admins already manage room purpose/topic

### Bot Admin Special Powers

Bot admins (MATRIX_ADMIN_IDS) can:
- Bind any room (even if not room admin)
- Create **special-purpose rooms** with custom bindings
- Add **room-specific skills** (future: custom tools per room)
- Add **room-specific knowledge bases** (future: RAG per room)

**Example Use Cases**:
```
Room #vikunja-support:
  - Bound to: knowledge_base:vikunja_docs
  - Bot has access to Vikunja documentation
  - Can answer "How do I create a recurring task?"

Room #recipe-testing:
  - Bound to: project:Recipe Testing
  - Bound to: skill:recipe_parser
  - Bot can parse recipe URLs and create tasks
```

---

## Conflict Resolution

### Initial Approach (V2.0)

**Last Admin Wins** - Whoever has admin privilege can change the binding.

```
Room #client-xyz:
  Alice (admin): !bind-room Client XYZ
  eis: ✅ Room bound to "Client XYZ"
  
  [2 hours later]
  Bob (admin): !bind-room Internal Ops
  eis: ⚠️ Room was bound to "Client XYZ" by @alice
       Change to "Internal Ops"? React ✅ to confirm.
  
  Bob: [reacts ✅]
  eis: ✅ Room rebound to "Internal Ops"
```

**Concerns**:
- **Race conditions** - Two admins binding simultaneously
- **Accidental changes** - Admin doesn't realize room is already bound
- **No audit trail** - Who changed what when?

### Future Enhancements (V2.1+)

#### Option A: Require Unbind First
```
Bob (admin): !bind-room Internal Ops
eis: ❌ Room already bound to "Client XYZ" by @alice
     Use !unbind-room first, then !bind-room
```

**Pros**: Explicit, prevents accidents  
**Cons**: Extra step, annoying for legitimate changes

#### Option B: Confirmation with History
```
Bob (admin): !bind-room Internal Ops
eis: ⚠️ Room binding history:
     - 2025-12-20: Bound to "Client XYZ" by @alice
     - 2025-12-15: Bound to "Q4 Planning" by @charlie
     
     Change to "Internal Ops"? React ✅ to confirm.
```

**Pros**: Informed decision, audit trail  
**Cons**: More complex, requires history storage

#### Option C: Multi-Admin Consensus
```
Bob (admin): !bind-room Internal Ops
eis: 📊 Binding change proposed by @bob
     Current: "Client XYZ"
     Proposed: "Internal Ops"
     
     Room admins, react ✅ to approve (2/3 required)
```

**Pros**: Democratic, prevents unilateral changes  
**Cons**: Slow, requires multiple admins online

#### Option D: Lock Bindings
```
Alice (admin): !bind-room Client XYZ --lock
eis: ✅ Room bound to "Client XYZ" (locked)

Bob (admin): !bind-room Internal Ops
eis: ❌ Room binding is locked by @alice
     Only @alice or bot admins can change it
```

**Pros**: Prevents accidental changes  
**Cons**: Requires lock management, can be abused

---

## Storage Model

### Room Bindings Table

```yaml
# config.yaml
room_bindings:
  "!abc123:matrix.factumerit.app":
    scope:
      instance: "production"
      project: "Client XYZ"
      subproject: null
      view: null
    bound_by: "@alice:matrix.factumerit.app"
    bound_at: "2025-12-24T10:30:00Z"
    locked: false
    history:
      - timestamp: "2025-12-24T10:30:00Z"
        user: "@alice:matrix.factumerit.app"
        action: "bind"
        scope: {project: "Client XYZ"}
      - timestamp: "2025-12-20T14:15:00Z"
        user: "@charlie:matrix.factumerit.app"
        action: "bind"
        scope: {project: "Q4 Planning"}

users:
  "@alice:matrix.factumerit.app":
    room_bindings:  # Personal bindings (Model 1)
      "!xyz789:matrix.factumerit.app": "Personal Project"
```

### Precedence Rules

When determining project context:

1. **Personal override** - User's `!project X` command (session-only)
2. **Personal room binding** - User's `!bind X` (Model 1)
3. **Shared room binding** - Room's `!bind-room X` (Model 2)
4. **No context** - User must specify project

```python
def get_effective_project(room_id: str, user_id: str) -> Optional[str]:
    """Get effective project context with precedence."""
    
    # 1. Check session override (!project command)
    session_project = _get_session_project(user_id)
    if session_project:
        return session_project
    
    # 2. Check personal room binding (Model 1)
    personal_binding = _get_personal_room_binding(room_id, user_id)
    if personal_binding:
        return personal_binding
    
    # 3. Check shared room binding (Model 2)
    room_binding = _get_room_binding(room_id)
    if room_binding:
        return room_binding.get("scope", {}).get("project")
    
    # 4. No context
    return None
```

---

## User Experience

### Room Join Notification

When a user joins a bound room:

```
Alice joins #client-xyz

eis: 👋 Welcome @alice!
     
     This room is bound to:
     📌 Project: Client XYZ
     🏢 Instance: production
     
     All commands in this room will default to this context.
     Use !binding to see details.
```

### Room Topic Integration

Update room topic to show binding:

```
Before: "Client XYZ project discussion"
After:  "Client XYZ project discussion | 📌 Vikunja: Client XYZ"
```

**Implementation**:
```python
async def update_room_topic(room_id: str, binding: dict):
    """Add binding info to room topic."""
    
    room = await client.get_room(room_id)
    current_topic = room.topic or ""
    
    # Remove old binding marker
    topic = re.sub(r'\s*\|\s*📌 Vikunja:.*$', '', current_topic)
    
    # Add new binding marker
    project = binding.get("scope", {}).get("project")
    if project:
        topic += f" | 📌 Vikunja: {project}"
    
    await client.set_room_topic(room_id, topic)
```

---

## Advanced Use Cases

### 1. Room-Specific Skills

Bot admins can add custom tools that only work in specific rooms:

```
Room #recipe-testing:
  !bind-room skill:recipe_parser
  
  Alice: @eis https://example.com/chocolate-cake
  eis: 🍰 Parsed recipe: Chocolate Cake
       Created 8 tasks:
       - Preheat oven to 350°F
       - Mix dry ingredients
       - ...
```

**Implementation**: Extend TOOL_REGISTRY with room-specific tools.

### 2. Room-Specific Knowledge Bases

Bot admins can add RAG (Retrieval-Augmented Generation) per room:

```
Room #vikunja-support:
  !bind-room knowledge:vikunja_docs
  
  Alice: @eis How do I create a recurring task?
  eis: [Searches vikunja_docs knowledge base]
       📚 To create a recurring task:
       1. Open task details
       2. Click "Repeat" section
       3. ...
```

**Implementation**: Inject room-specific context into Claude system prompt.

### 3. Multi-Project Rooms

Some rooms need access to multiple projects:

```
Room #sprint-planning:
  !bind-room projects:Client XYZ,Internal Ops,Marketing
  
  Alice: !today
  eis: 📋 Due Today (3 projects):
       
       Client XYZ:
       - Task 1
       
       Internal Ops:
       - Task 2
       
       Marketing:
       - Task 3
```

**Implementation**: Extend scope to support multiple projects.

---

## Migration Path

### Phase 1: V1 Launch (Model 1 Only)
- Personal room bindings (`!bind`)
- No shared context
- Simple, privacy-preserving

### Phase 2: V2.0 (Add Model 2)
- Shared room bindings (`!bind-room`)
- Room admin permissions
- Last admin wins conflict resolution
- Room topic integration

### Phase 3: V2.1 (Enhanced Conflict Resolution)
- Binding history
- Confirmation prompts
- Audit trail

### Phase 4: V2.2 (Advanced Features)
- Room-specific skills
- Room-specific knowledge bases
- Multi-project bindings
- Lock bindings

---

## Open Questions

1. **Race Conditions**: How to handle two admins binding simultaneously?
   - Use database transactions?
   - Optimistic locking with version numbers?
   - Accept last-write-wins?

2. **Community Management**: What rules define the experience?
   - Should there be a "binding cooldown" (can't change for X hours)?
   - Should binding changes notify all room members?
   - Should there be a binding change log visible to all?

3. **Personal Override in Shared Rooms**: If room is bound, can users override?
   - Current answer: Yes (personal binding > room binding)
   - Alternative: Room binding is absolute (no personal override)
   - Hybrid: Room admin can set "strict mode" (no overrides allowed)

4. **DM Behavior**: What if user DMs bot from a bound room?
   - Does room binding apply to DM?
   - Or does DM always use personal context?
   - Current answer: DM uses personal context only

5. **Unrelated Bots**: What if room has multiple bots with different contexts?
   - Not our problem (each bot has own bindings)
   - But could be confusing for users
   - Document best practices?

---

## Implementation Checklist (Future)

- [ ] Add `room_bindings` table to config.yaml
- [ ] Implement `can_bind_room()` permission check
- [ ] Implement `!bind-room` command
- [ ] Implement `!unbind-room` command
- [ ] Implement `!room-binding` command (show current)
- [ ] Add room join notification
- [ ] Add room topic integration
- [ ] Add binding history tracking
- [ ] Add confirmation prompts for changes
- [ ] Implement precedence rules (personal > room)
- [ ] Write tests for conflict scenarios
- [ ] Document best practices for room admins

---

**End of Model 2 Concept Document**
