# Vikui - Knowledge Base System for Matrix Bot

**Version**: 1.0
**Date**: 2025-12-24
**Status**: Planned for V2
**Related**: MATRIX_TRANSPORT_SPEC_V2.md, MATRIX_ROOM_BINDING_MODEL2.md

---

## Overview

**Vikui** is a room-specific knowledge base system that uses RAG (Retrieval-Augmented Generation) to make the bot an expert on different topics depending on which room you're in.

**Etymology**: *vikui* = Vikunja UI/interface (connection to knowledge)

### The Magic Formula

```
PROJECT (Vikunja)     = STATE (tasks, deadlines, status)
+
VIKUI (RAG)           = CONTENT (docs, notes, knowledge)
+
CLAUDE (LLM)          = INTELLIGENCE (reasoning, actions)
=
🎯 CONTEXT-AWARE AI WORKSPACE
```

---

## Core Concept

### Room-Specific Knowledge

Each Matrix room can be bound to a **knowledge base** (vikui) that provides context-specific information:

```
Room #vikunja-support:
  Vikui: vikunja_docs
  → Bot knows Vikunja documentation, API reference, troubleshooting

Room #recipe-testing:
  Vikui: recipes
  → Bot knows recipes, cooking techniques, ingredient substitutions

Room #client-xyz:
  Vikui: client_xyz_notes
  → Bot knows client contacts, meeting notes, project context
```

### Combined with Project Binding

```
Room #client-xyz:
  Project: Client XYZ (Vikunja)        ← STATE
  Vikui: client_xyz_notes              ← CONTENT

  Result: Bot can manage tasks AND answer questions about the client
```

---

## Commands

### The Vik Family

| Command | Behavior | Type |
|---------|----------|------|
| `!vik` | Connect to Vikunja | State |
| `!novik` | Disconnect from Vikunja | State |
| `!viki` | List Vikunja instances | State |
| `!vikui <name>` | Bind room to knowledge base | Content |
| `!vikui` | Show current knowledge base | Content |
| `!novikui` | Remove knowledge base binding | Content |
| `!vikuii` | List available knowledge bases | Content |
| `!viktus` | Show all connection status | Status |

### Room Binding (Room Admins Only)

| Command | Behavior |
|---------|----------|
| `!vikui <name>` | Bind room to knowledge base |
| `!vikui` | Show current binding |
| `!novikui` | Remove binding |
| `!vikuii` | List available knowledge bases |

### Knowledge Base Management (Bot Admins Only)

| Command | Behavior |
|---------|----------|
| `!vikui-create <name>` | Create new knowledge base |
| `!vikui-add <name> <file>` | Add document to knowledge base |
| `!vikui-refresh <name>` | Rebuild embeddings |
| `!vikui-info <name>` | Show knowledge base details |

---

## Architecture

### Data Flow

```
User Question
    ↓
┌─────────────────────────────────────────┐
│ 1. Context Builder                      │
│    - Get room's project (Vikunja)       │
│    - Get room's vikui (RAG)         │
│    - Search vikui for relevant docs │
│    - Build system prompt with context   │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 2. Claude API                           │
│    - System prompt (base + context)     │
│    - User message                       │
│    - Tool registry (58 Vikunja tools)   │
│    - Conversation history               │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 3. Tool Execution                       │
│    - Create/update/search tasks         │
│    - Use Vikunja API                    │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 4. Response                             │
│    - Formatted answer                   │
│    - Citations from Vikui           │
│    - ECO streak footer                  │
└─────────────────────────────────────────┘
```

### Storage Architecture

```
/data/
├── config.yaml                    # User configs, room bindings
│
├── vikunja/                       # State (via API)
│   └── [managed by Vikunja API]
│
└── vikui/                     # Content (RAG)
    ├── chroma/                    # Vector database
    │   ├── vikunja_docs/
    │   ├── recipes/
    │   └── client_xyz_notes/
    │
    └── sources/                   # Original documents
        ├── vikunja_docs/
        │   ├── tasks.md
        │   ├── projects.md
        │   ├── recurring.md
        │   └── api.md
        │
        ├── recipes/
        │   ├── cookies.md
        │   ├── chocolate_cake.md
        │   └── baking_tips.md
        │
        └── client_xyz_notes/
            ├── contacts.md
            ├── meeting_notes.md
            └── project_overview.md
```

---

## Configuration

### config.yaml Structure

```yaml
vikui:
  knowledge_bases:
    vikunja_docs:
      path: /data/vikui/sources/vikunja_docs
      description: "Vikunja documentation and API reference"
      created_by: "@admin:matrix.factumerit.app"
      created_at: "2025-12-24T10:00:00Z"
      documents:
        - tasks.md
        - projects.md
        - recurring.md
        - api.md
      embedding_model: "text-embedding-3-small"
      chunk_size: 500
      chunk_overlap: 50
      last_indexed: "2025-12-24T10:30:00Z"
    
    recipes:
      path: /data/vikui/sources/recipes
      description: "Tested recipes and cooking techniques"
      created_by: "@admin:matrix.factumerit.app"
      created_at: "2025-12-24T11:00:00Z"
      documents:
        - cookies.md
        - chocolate_cake.md
        - baking_tips.md
      embedding_model: "text-embedding-3-small"
      chunk_size: 500
      chunk_overlap: 50
      last_indexed: "2025-12-24T11:15:00Z"
  
  room_bindings:
    "!abc123:matrix.factumerit.app": "vikunja_docs"
    "!def456:matrix.factumerit.app": "recipes"
    "!ghi789:matrix.factumerit.app": "client_xyz_notes"
```

---

## Implementation

### Vector Database: ChromaDB

**Why ChromaDB:**
- ✅ Local, no external dependencies
- ✅ Simple Python API
- ✅ Built-in embedding support
- ✅ Persistent storage
- ✅ Fast similarity search

**Installation:**
```bash
pip install chromadb openai
```

### Core Functions

#### 1. Initialize ChromaDB Client

```python
import chromadb
from chromadb.utils import embedding_functions

# Initialize persistent client
chroma_client = chromadb.PersistentClient(path="/data/vikui/chroma")

# OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)
```

#### 2. Index Knowledge Base

```python
async def index_vikui(kb_name: str) -> dict:
    """Index all documents in a knowledge base.

    Args:
        kb_name: Name of knowledge base to index

    Returns:
        dict with indexing stats
    """
    config = _load_config()
    kb_config = config['vikui']['knowledge_bases'][kb_name]
    kb_path = kb_config['path']

    # Get or create collection
    collection = chroma_client.get_or_create_collection(
        name=kb_name,
        embedding_function=openai_ef,
        metadata={"description": kb_config['description']}
    )

    # Clear existing documents
    try:
        collection.delete()
    except:
        pass

    # Re-create collection
    collection = chroma_client.create_collection(
        name=kb_name,
        embedding_function=openai_ef,
        metadata={"description": kb_config['description']}
    )

    # Index all documents
    documents = []
    metadatas = []
    ids = []

    chunk_size = kb_config.get('chunk_size', 500)
    chunk_overlap = kb_config.get('chunk_overlap', 50)

    for doc_file in kb_config['documents']:
        doc_path = os.path.join(kb_path, doc_file)

        # Read document
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Chunk document
        chunks = _chunk_text(content, chunk_size, chunk_overlap)

        for i, chunk in enumerate(chunks):
            if chunk.strip():
                documents.append(chunk)
                metadatas.append({
                    'source': doc_file,
                    'chunk_index': i,
                    'kb_name': kb_name
                })
                ids.append(f"{kb_name}_{doc_file}_{i}")

    # Add to collection
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    # Update last_indexed timestamp
    config['vikui']['knowledge_bases'][kb_name]['last_indexed'] = datetime.now().isoformat()
    _save_config(config)

    return {
        'kb_name': kb_name,
        'documents': len(kb_config['documents']),
        'chunks': len(documents),
        'indexed_at': config['vikui']['knowledge_bases'][kb_name]['last_indexed']
    }


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks.

    Args:
        text: Text to chunk
        chunk_size: Target chunk size in characters
        overlap: Overlap between chunks in characters

    Returns:
        List of text chunks
    """
    # Simple chunking by paragraphs, then by size
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
```

#### 3. Search Knowledge Base

```python
async def search_vikui(kb_name: str, query: str, top_k: int = 5) -> list[dict]:
    """Search knowledge base for relevant chunks.

    Args:
        kb_name: Name of knowledge base to search
        query: Search query
        top_k: Number of results to return

    Returns:
        List of dicts with 'content', 'source', 'score'
    """
    try:
        collection = chroma_client.get_collection(
            name=kb_name,
            embedding_function=openai_ef
        )
    except:
        logger.warning(f"Knowledge base '{kb_name}' not found")
        return []

    # Search
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    # Format results
    chunks = []
    if results['documents'] and results['documents'][0]:
        for i, doc in enumerate(results['documents'][0]):
            chunks.append({
                'content': doc,
                'source': results['metadatas'][0][i]['source'],
                'score': results['distances'][0][i] if results['distances'] else 0,
                'chunk_index': results['metadatas'][0][i].get('chunk_index', 0)
            })

    return chunks
```

#### 4. Build System Prompt with Context

```python
async def build_system_prompt(room_id: str, user_id: str, message: str) -> str:
    """Build context-aware system prompt.

    Args:
        room_id: Matrix room ID
        user_id: Matrix user ID
        message: User's message (for Vikui search)

    Returns:
        System prompt with project + Vikui context
    """
    # Base prompt
    prompt = """You are eis, a helpful Vikunja task management assistant.
You have access to 58 Vikunja tools to help users manage their tasks.
Be helpful, playful, and encouraging.

Use playful language:
- "Oops!" for overdue tasks
- "Fire drill!" for urgent tasks
- "Zen mode" for focus
- Celebrate ECO streaks 🌿"""

    # Add project context (STATE from Vikunja)
    project = get_room_project(room_id, user_id)
    if project:
        prompt += f"\n\n📌 **Current Project Context:** {project}"
        prompt += f"\nAll task operations should default to this project unless user specifies otherwise."

    # Add Vikui context (CONTENT from RAG)
    vikui_kb = _get_room_vikui(room_id)
    if vikui_kb:
        # Search knowledge base
        chunks = await search_vikui(vikui_kb, message, top_k=5)

        if chunks:
            prompt += f"\n\n📚 **Vikui Knowledge Base:** {vikui_kb}\n\n"
            prompt += "You have access to the following relevant information:\n\n"

            for i, chunk in enumerate(chunks, 1):
                prompt += f"**[{i}] {chunk['source']}**\n"
                prompt += f"{chunk['content']}\n\n"

            prompt += (
                "\nUse this knowledge to provide better answers. "
                "Cite sources when using Vikui information. "
                "Format citations as: [Source: filename.md]"
            )

    # Add user preferences
    user_config = _get_user_config(user_id)
    timezone = user_config.get('timezone', 'UTC')
    prompt += f"\n\n⏰ **User Timezone:** {timezone}"

    return prompt


def _get_room_vikui(room_id: str) -> Optional[str]:
    """Get room's Vikui binding.

    Args:
        room_id: Matrix room ID

    Returns:
        Knowledge base name or None
    """
    config = _load_config()
    return config.get('vikui', {}).get('room_bindings', {}).get(room_id)
```

#### 5. Command Implementations

```python
async def _vikui_bind_impl(room_id: str, user_id: str, kb_name: str) -> dict:
    """Bind room to Vikui knowledge base.

    Args:
        room_id: Matrix room ID
        user_id: Matrix user ID (for permission check)
        kb_name: Knowledge base name

    Returns:
        dict with success message
    """
    # Check permission (room admin or bot admin)
    if not await can_bind_room(room_id, user_id):
        raise PermissionError("Only room admins can bind Vikui")

    # Check if knowledge base exists
    config = _load_config()
    if kb_name not in config.get('vikui', {}).get('knowledge_bases', {}):
        available = list(config.get('vikui', {}).get('knowledge_bases', {}).keys())
        raise ValueError(
            f"Knowledge base '{kb_name}' not found.\n\n"
            f"Available: {', '.join(available)}\n\n"
            f"Use !vikui-list to see all knowledge bases."
        )

    # Bind room
    if 'vikui' not in config:
        config['vikui'] = {}
    if 'room_bindings' not in config['vikui']:
        config['vikui']['room_bindings'] = {}

    config['vikui']['room_bindings'][room_id] = kb_name
    _save_config(config)

    kb_config = config['vikui']['knowledge_bases'][kb_name]

    return {
        'message': (
            f"📚 **Vikui Activated!**\n\n"
            f"This room is now bound to: **{kb_name}**\n\n"
            f"{kb_config['description']}\n\n"
            f"📄 Documents: {len(kb_config['documents'])}\n"
            f"🔄 Last indexed: {kb_config.get('last_indexed', 'Never')}\n\n"
            f"Ask me anything related to this knowledge base!"
        )
    }


async def _vikui_unbind_impl(room_id: str, user_id: str) -> dict:
    """Remove Vikui binding from room.

    Args:
        room_id: Matrix room ID
        user_id: Matrix user ID (for permission check)

    Returns:
        dict with success message
    """
    # Check permission
    if not await can_bind_room(room_id, user_id):
        raise PermissionError("Only room admins can unbind Vikui")

    config = _load_config()

    if room_id not in config.get('vikui', {}).get('room_bindings', {}):
        return {'message': "❌ This room is not bound to any Vikui knowledge base."}

    kb_name = config['vikui']['room_bindings'][room_id]
    del config['vikui']['room_bindings'][room_id]
    _save_config(config)

    return {
        'message': f"✅ Removed Vikui binding to '{kb_name}'"
    }


async def _vikuii_list_impl(user_id: str) -> dict:
    """List all available Vikui knowledge bases.

    Args:
        user_id: Matrix user ID (for admin check)

    Returns:
        dict with knowledge base list
    """
    config = _load_config()
    kbs = config.get('vikui', {}).get('knowledge_bases', {})

    if not kbs:
        return {'message': "📚 No Vikuii available yet."}

    lines = ["📚 **Available Vikuii**\n"]

    for kb_name, kb_config in kbs.items():
        lines.append(f"**{kb_name}**")
        lines.append(f"  {kb_config['description']}")
        lines.append(f"  📄 {len(kb_config['documents'])} documents")
        lines.append(f"  🔄 Last indexed: {kb_config.get('last_indexed', 'Never')}")
        lines.append("")

    lines.append("Use `!vikui <name>` to bind this room to a knowledge base.")

    return {'message': '\n'.join(lines)}


async def _vikui_create_impl(user_id: str, kb_name: str) -> dict:
    """Create new Vikui knowledge base.

    Args:
        user_id: Matrix user ID (must be bot admin)
        kb_name: Name for new knowledge base

    Returns:
        dict with success message
    """
    # Check admin permission
    if user_id not in MATRIX_ADMIN_IDS:
        raise PermissionError("Only bot admins can create knowledge bases")

    config = _load_config()

    if 'vikui' not in config:
        config['vikui'] = {'knowledge_bases': {}, 'room_bindings': {}}

    if kb_name in config['vikui']['knowledge_bases']:
        raise ValueError(f"Knowledge base '{kb_name}' already exists")

    # Create directory
    kb_path = f"/data/vikui/sources/{kb_name}"
    os.makedirs(kb_path, exist_ok=True)

    # Add to config
    config['vikui']['knowledge_bases'][kb_name] = {
        'path': kb_path,
        'description': f"Knowledge base: {kb_name}",
        'created_by': user_id,
        'created_at': datetime.now().isoformat(),
        'documents': [],
        'embedding_model': 'text-embedding-3-small',
        'chunk_size': 500,
        'chunk_overlap': 50,
        'last_indexed': None
    }
    _save_config(config)

    return {
        'message': (
            f"✅ Created Vikui knowledge base: **{kb_name}**\n\n"
            f"📁 Path: {kb_path}\n\n"
            f"Next steps:\n"
            f"1. Add markdown files to {kb_path}/\n"
            f"2. Run `!vikui-refresh {kb_name}` to index\n"
            f"3. Bind rooms with `!vikui {kb_name}`"
        )
    }


async def _vikui_refresh_impl(user_id: str, kb_name: str) -> dict:
    """Rebuild embeddings for knowledge base.

    Args:
        user_id: Matrix user ID (must be bot admin)
        kb_name: Knowledge base name

    Returns:
        dict with indexing stats
    """
    # Check admin permission
    if user_id not in MATRIX_ADMIN_IDS:
        raise PermissionError("Only bot admins can refresh knowledge bases")

    config = _load_config()

    if kb_name not in config.get('vikui', {}).get('knowledge_bases', {}):
        raise ValueError(f"Knowledge base '{kb_name}' not found")

    # Scan directory for markdown files
    kb_path = config['vikui']['knowledge_bases'][kb_name]['path']
    md_files = [f for f in os.listdir(kb_path) if f.endswith('.md')]

    if not md_files:
        return {
            'message': (
                f"⚠️ No markdown files found in {kb_path}\n\n"
                f"Add .md files to the directory and try again."
            )
        }

    # Update document list
    config['vikui']['knowledge_bases'][kb_name]['documents'] = md_files
    _save_config(config)

    # Index
    stats = await index_vikui(kb_name)

    return {
        'message': (
            f"✅ **Vikui Refreshed: {kb_name}**\n\n"
            f"📄 Documents: {stats['documents']}\n"
            f"📦 Chunks: {stats['chunks']}\n"
            f"🔄 Indexed: {stats['indexed_at']}\n\n"
            f"Knowledge base is ready to use!"
        )
    }


async def _viktus_impl(user_id: str, room_id: str) -> dict:
    """Show comprehensive connection status (viktus = having been connected).

    Args:
        user_id: Matrix user ID
        room_id: Matrix room ID

    Returns:
        dict with status dashboard
    """
    config = _load_config()
    user_config = config.get('users', {}).get(user_id, {})

    # Vikunja connection status
    vikunja_status = "❌ Not connected"
    vikunja_details = ""

    if _is_user_connected(user_id):
        instance = _get_current_instance(user_id)
        vikunja_status = f"✓ Connected to: {instance['name']}"
        vikunja_details = f"   📍 {instance['url']}\n   🔑 Token: Valid"

    # Vikui (knowledge base) status
    vikui_status = "❌ No knowledge base"
    vikui_details = ""

    room_vikui = _get_room_vikui(room_id)
    if room_vikui:
        kb_config = config.get('vikui', {}).get('knowledge_bases', {}).get(room_vikui, {})
        vikui_status = f"✓ Connected to: {room_vikui}"
        vikui_details = (
            f"   📄 {len(kb_config.get('documents', []))} documents\n"
            f"   🔄 Last indexed: {_format_time_ago(kb_config.get('last_indexed'))}"
        )

    # Context status
    project = get_room_project(room_id, user_id)
    project_status = f"Project: {project}" if project else "Project: None (use !project or !bind)"

    timezone = user_config.get('timezone', 'UTC')
    timezone_status = f"Timezone: {timezone}"
    if timezone == 'UTC':
        timezone_status += " (use !timezone to set)"

    # ECO streak
    streak = _get_eco_streak(user_id)
    tokens_saved = streak * 500
    eco_status = f"{streak} commands | ~{tokens_saved:,} tokens saved"

    # Add milestone if applicable
    eco_milestone = ""
    if streak >= 50:
        eco_milestone = "\n   🏆 ECO legend!"
    elif streak >= 25:
        eco_milestone = "\n   🌳 Token-saving champion!"
    elif streak >= 10:
        eco_milestone = "\n   🌿 ECO warrior!"
    elif streak >= 5:
        eco_milestone = "\n   🌱 You're getting the hang of this!"

    # Usage stats
    usage = _get_user_usage(user_id)
    monthly_cost = usage.get('monthly_cost', 0)
    monthly_limit = usage.get('monthly_limit', 20)
    monthly_tokens = usage.get('monthly_tokens', 0)
    percentage = (monthly_cost / monthly_limit * 100) if monthly_limit > 0 else 0

    # Build status message
    status = f"""📊 **Viktus - Connection Status**

🔗 **Vikunja (State):**
   {vikunja_status}
{vikunja_details}

📚 **Vikui (Knowledge):**
   {vikui_status}
{vikui_details}

📌 **Context:**
   {project_status}
   {timezone_status}

🌿 **ECO Streak:**
   {eco_status}{eco_milestone}

💰 **Usage (This Month):**
   ${monthly_cost:.2f} / ${monthly_limit:.2f} ({percentage:.1f}%)
   ~{monthly_tokens:,} tokens used

✨ **You're all set!**"""

    return {'message': status}


def _format_time_ago(timestamp: str) -> str:
    """Format timestamp as relative time.

    Args:
        timestamp: ISO format timestamp

    Returns:
        Human-readable relative time (e.g., "2 hours ago")
    """
    if not timestamp:
        return "Never"

    from datetime import datetime, timezone

    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = now - dt

        seconds = diff.total_seconds()

        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    except:
        return timestamp
```

---

## User Experience Examples

### Example 0: Viktus Status Dashboard

```
Alice: !viktus
eis: 📊 **Viktus - Connection Status**

     🔗 **Vikunja (State):**
        ✓ Connected to: production
        📍 https://vikunja.example.com
        🔑 Token: Valid

     📚 **Vikui (Knowledge):**
        ✓ Connected to: vikunja_docs
        📄 4 documents
        🔄 Last indexed: 2 hours ago

     📌 **Context:**
        Project: None (use !project or !bind)
        Timezone: UTC (use !timezone to set)

     🌿 **ECO Streak:**
        12 commands | ~6,000 tokens saved
        🌿 ECO warrior!

     💰 **Usage (This Month):**
        $2.34 / $20.00 (11.7%)
        ~15,000 tokens used

     ✨ **You're all set!**
```

**What is Viktus?**
- **viktus** = Latin passive perfect participle ("having been connected")
- Shows the **state of being connected** - all your connections at a glance
- One command to see: Vikunja, Vikui, project, timezone, ECO streak, usage

---

### Example 1: Vikunja Support Room

```
Room #vikunja-support:
  Admin: !vikui vikunja_docs
  eis: 📚 **Vikui Activated!**

       This room is now bound to: **vikunja_docs**

       Vikunja documentation and API reference

       📄 Documents: 4
       🔄 Last indexed: 2025-12-24T10:30:00Z

       Ask me anything related to this knowledge base!

---

  Alice: @eis How do I create a recurring task?

  eis: [Searches Vikui for "recurring task"]
       [Finds relevant chunks from recurring.md]

       📚 **From Vikui: vikunja_docs**

       To create a recurring task:

       1. Open task details
       2. Click "Repeat" section
       3. Choose frequency (daily, weekly, monthly, yearly)
       4. Set repeat pattern
       5. Optional: Set end date
       6. Save

       **Example - Weekly Task:**
       - Frequency: Weekly
       - Days: Monday, Wednesday, Friday
       - Repeat: Every 1 week

       The task will automatically regenerate after completion.

       [Source: recurring.md]

       Want me to create a recurring task for you?

---

  Bob: @eis What's the API endpoint for creating tasks?

  eis: [Searches Vikui for "API" + "create task"]
       [Finds relevant chunks from api.md]

       📚 **From Vikui: vikunja_docs**

       **Create Task API Endpoint:**

       ```
       POST /api/v1/projects/{projectId}/tasks
       ```

       **Headers:**
       - `Authorization: Bearer <token>`
       - `Content-Type: application/json`

       **Request Body:**
       ```json
       {
         "title": "Task title",
         "description": "Task description",
         "due_date": "2025-12-31T23:59:59Z",
         "priority": 3
       }
       ```

       **Response:** 201 Created
       ```json
       {
         "id": 123,
         "title": "Task title",
         ...
       }
       ```

       [Source: api.md]

       Need help with authentication or other endpoints?
```

### Example 2: Recipe Testing Room

```
Room #recipe-testing:
  Admin: !vikui recipes
  eis: 📚 **Vikui Activated!**

       This room is now bound to: **recipes**

       Tested recipes and cooking techniques

       📄 Documents: 3
       🔄 Last indexed: 2025-12-24T11:15:00Z

       Ask me anything related to this knowledge base!

---

  Charlie: @eis chocolate chip cookie recipe

  eis: [Searches Vikui for "chocolate chip cookie"]
       [Finds recipe from cookies.md]

       📚 **From Vikui: recipes**

       **Classic Chocolate Chip Cookies**

       **Ingredients:**
       - 2¼ cups all-purpose flour
       - 1 tsp baking soda
       - 1 tsp salt
       - 1 cup butter, softened
       - ¾ cup granulated sugar
       - ¾ cup packed brown sugar
       - 2 large eggs
       - 2 tsp vanilla extract
       - 2 cups chocolate chips

       **Instructions:**
       1. Preheat oven to 375°F
       2. Mix flour, baking soda, salt
       3. Beat butter and sugars until creamy
       4. Add eggs and vanilla
       5. Gradually blend in flour mixture
       6. Stir in chocolate chips
       7. Drop by rounded tablespoon onto ungreased cookie sheets
       8. Bake 9-11 minutes or until golden brown
       9. Cool on baking sheet 2 minutes
       10. Remove to wire rack

       **Yield:** 5 dozen cookies
       **Prep time:** 15 min | **Bake time:** 11 min

       [Source: cookies.md]

       Want me to create Vikunja tasks for each step?

---

  Charlie: @eis yes, create tasks for this weekend

  eis: [Creates tasks in Vikunja "Recipe Testing" project]
       [Uses Vikui recipe as source]

       ✅ Created 10 tasks in "Recipe Testing" project:

       🛒 **Shopping (Friday):**
       [#101] Buy cookie ingredients

       👨‍🍳 **Prep (Saturday 2pm):**
       [#102] Preheat oven to 375°F
       [#103] Mix dry ingredients
       [#104] Cream butter and sugars
       [#105] Add eggs and vanilla
       [#106] Blend in flour mixture
       [#107] Stir in chocolate chips

       🍪 **Bake (Saturday 2:30pm):**
       [#108] Drop dough on cookie sheets
       [#109] Bake 9-11 minutes
       [#110] Cool and enjoy!

       All tasks scheduled for this weekend.
       React ✅ as you complete each step!
```

### Example 3: Client Project Room

```
Room #client-xyz:
  Admin: !bind Client XYZ
  Admin: !vikui client_xyz_notes

  eis: ✅ Room configured!

       📌 Project: Client XYZ (Vikunja)
       📚 Vikui: client_xyz_notes

       I now have access to:
       - Your tasks, deadlines, and status (from Vikunja)
       - Client notes, meeting minutes, contacts (from Vikui)

       Ask me anything!

---

  Dana: @eis Who's the main contact at Client XYZ?

  eis: [Searches Vikui for "contact" + "Client XYZ"]
       [Finds info from contacts.md]

       📚 **From Vikui: client_xyz_notes**

       **Main Contact:**
       Jane Smith
       - Title: VP of Engineering
       - Email: jane.smith@clientxyz.com
       - Phone: (555) 123-4567
       - Timezone: America/New_York (EST)
       - Best time to reach: 10am-4pm EST

       **Secondary Contact:**
       Bob Johnson
       - Title: Project Manager
       - Email: bob.johnson@clientxyz.com
       - Phone: (555) 234-5678

       [Source: contacts.md]

       Want me to create a task to contact Jane?

---

  Dana: @eis What did we decide in the last meeting?

  eis: [Searches Vikui for "meeting" + "decision"]
       [Finds latest meeting notes]

       📚 **From Vikui: client_xyz_notes**

       **Meeting Notes - Dec 20, 2025**

       **Attendees:** Jane Smith, Bob Johnson, Dana (us)

       **Decisions:**
       1. ✅ Move deadline to Jan 15 (approved by Jane)
       2. ✅ Add user authentication feature to scope
       3. ✅ Weekly check-ins every Friday 2pm EST

       **Action Items:**
       - Dana: Update project timeline → Due Dec 22
       - Bob: Draft auth spec → Due Dec 27
       - Jane: Review and approve → Due Jan 3

       [Source: meeting_notes.md]

       I can create Vikunja tasks for these action items if you'd like!

---

  Dana: @eis yes, create tasks for my action items

  eis: [Creates tasks in Vikunja "Client XYZ" project]
       [Uses meeting notes from Vikui]

       ✅ Created 1 task in "Client XYZ" project:

       [#201] Update project timeline
       - Due: Dec 22, 2025
       - Priority: 4 (high)
       - Assignee: Dana
       - Context: Per Dec 20 meeting with Jane & Bob

       Note: Bob's task (Draft auth spec) is assigned to him.
       I can only create tasks for you unless you're an admin.
```

---

## Admin Workflow

### Creating a New Knowledge Base

```
Admin: !vikui-create company_policies

eis: ✅ Created Vikui knowledge base: **company_policies**

     📁 Path: /data/vikui/sources/company_policies

     Next steps:
     1. Add markdown files to /data/vikui/sources/company_policies/
     2. Run `!vikui-refresh company_policies` to index
     3. Bind rooms with `!vikui company_policies`

---

[Admin adds files via SSH/SFTP:]
$ cd /data/vikui/sources/company_policies
$ ls
pto_policy.md
remote_work.md
expense_reimbursement.md
code_of_conduct.md

---

Admin: !vikui-refresh company_policies

eis: ✅ **Vikui Refreshed: company_policies**

     📄 Documents: 4
     📦 Chunks: 47
     🔄 Indexed: 2025-12-24T15:30:00Z

     Knowledge base is ready to use!

---

Admin: !vikui-list

eis: 📚 **Available Vikui Knowledge Bases**

     **vikunja_docs**
       Vikunja documentation and API reference
       📄 4 documents
       🔄 Last indexed: 2025-12-24T10:30:00Z

     **recipes**
       Tested recipes and cooking techniques
       📄 3 documents
       🔄 Last indexed: 2025-12-24T11:15:00Z

     **client_xyz_notes**
       Client XYZ project notes and contacts
       📄 3 documents
       🔄 Last indexed: 2025-12-24T14:00:00Z

     **company_policies**
       Company policies and procedures
       📄 4 documents
       🔄 Last indexed: 2025-12-24T15:30:00Z

     Use `!vikui <name>` to bind a room to a knowledge base.
```

---

## Technical Details

### Embedding Model

**OpenAI text-embedding-3-small**
- Cost: $0.02 / 1M tokens
- Dimensions: 1536
- Performance: Excellent for semantic search
- Speed: Fast (~100ms per request)

**Cost Estimate:**
- 1000 chunks × 500 chars = 500K chars ≈ 125K tokens
- Embedding cost: $0.0025 (one-time)
- Search cost: Negligible (embeddings cached)

### Chunking Strategy

**Paragraph-based with overlap:**
- Chunk size: 500 characters (≈125 tokens)
- Overlap: 50 characters (≈12 tokens)
- Preserves context across chunk boundaries
- Good balance between granularity and coherence

**Alternative strategies:**
- Sentence-based: More precise, but loses context
- Semantic chunking: Better quality, but slower
- Fixed-size: Simple, but may split mid-sentence

### Search Parameters

**Top K = 5:**
- Provides enough context without overwhelming Claude
- Typical chunk: 500 chars × 5 = 2500 chars ≈ 625 tokens
- Leaves room for conversation history + tools

**Distance Threshold:**
- ChromaDB uses cosine distance (0-2)
- Typical good match: < 0.5
- Can filter results by distance if needed

### Performance

**Indexing:**
- 100 documents × 10 chunks = 1000 chunks
- Embedding time: ~10 seconds (parallel batching)
- Storage: ~10MB (embeddings + metadata)

**Search:**
- Query time: ~100ms (embedding + search)
- Acceptable for real-time chat
- Can cache frequent queries if needed

---

## Phased Rollout

### Phase 1: Core Implementation (V2.0)
- ✅ ChromaDB integration
- ✅ Basic indexing (markdown files)
- ✅ Search functionality
- ✅ Room binding
- ✅ Admin commands
- ✅ System prompt injection

**Timeline:** 2-3 days

### Phase 2: Enhanced Features (V2.1)
- 📄 Support for other file types (PDF, DOCX, TXT)
- 🔄 Auto-refresh on file changes (file watcher)
- 📊 Search analytics (what users ask about)
- 🎯 Relevance tuning (adjust top_k, distance threshold)
- 💾 Search result caching

**Timeline:** 1 week

### Phase 3: User Contributions (V2.2)
- 👥 Users can suggest additions to knowledge bases
- ✅ Approval workflow for new content
- 📝 Version control for documents (git integration)
- 🔍 Full-text search (in addition to semantic)
- 📈 Usage metrics per knowledge base

**Timeline:** 2 weeks

---

## Testing Strategy

### Unit Tests

```python
# test_vikui.py

async def test_index_knowledge_base():
    """Test indexing a knowledge base."""
    kb_name = "test_kb"
    # Create test KB with sample docs
    # Index
    # Verify chunks created
    pass

async def test_search_knowledge_base():
    """Test searching a knowledge base."""
    kb_name = "test_kb"
    query = "How do I create a task?"
    results = await search_vikui(kb_name, query, top_k=3)
    assert len(results) <= 3
    assert all('content' in r for r in results)
    assert all('source' in r for r in results)

async def test_build_system_prompt_with_vikui():
    """Test system prompt includes Vikui context."""
    room_id = "!test:matrix.factumerit.app"
    user_id = "@alice:matrix.factumerit.app"
    message = "How do I create a recurring task?"

    # Bind room to vikui
    # Build prompt
    prompt = await build_system_prompt(room_id, user_id, message)

    assert "Vikui Knowledge Base" in prompt
    assert "recurring" in prompt.lower()
```

### Integration Tests

```python
# test_vikui_integration.py

async def test_full_flow():
    """Test: User asks question → Vikui search → Claude response."""
    # Setup room with vikui binding
    # Send message
    # Verify response includes Vikui citation
    pass

async def test_combined_project_vikui():
    """Test: Room bound to both project and vikui."""
    # Bind room to project
    # Bind room to vikui
    # Ask question that needs both contexts
    # Verify response uses both
    pass
```

### Manual Testing Checklist

- [ ] Create knowledge base
- [ ] Add documents
- [ ] Refresh/index
- [ ] Bind room to knowledge base
- [ ] Ask question → get relevant answer
- [ ] Verify citations included
- [ ] Test with multiple knowledge bases
- [ ] Test combined project + vikui
- [ ] Test admin commands (list, create, refresh)
- [ ] Test permission checks (room admin, bot admin)

---

## Security & Privacy

### Access Control

**Room Bindings:**
- Only room admins can bind/unbind Vikui
- Prevents unauthorized access to sensitive knowledge bases

**Knowledge Base Creation:**
- Only bot admins can create/refresh knowledge bases
- Prevents users from polluting the system

**Data Isolation:**
- Each knowledge base is separate
- No cross-contamination between rooms

### Sensitive Information

**Best Practices:**
- Don't store passwords, API keys, or secrets in Vikui
- Use environment variables for sensitive config
- Audit knowledge base contents regularly
- Consider encryption for highly sensitive data

**PII Handling:**
- Be mindful of personal information in knowledge bases
- Follow GDPR/privacy regulations
- Provide way to delete/redact information

---

## Cost Analysis

### OpenAI Costs

**Embedding (one-time per document):**
- text-embedding-3-small: $0.02 / 1M tokens
- 1000 chunks × 125 tokens = 125K tokens
- Cost: $0.0025 per knowledge base

**Search (per query):**
- Query embedding: 1 query × 25 tokens = 25 tokens
- Cost: $0.0000005 per search (negligible)

**Claude API (per conversation):**
- System prompt with Vikui: +625 tokens (5 chunks)
- Additional cost: ~$0.0002 per message (haiku)
- Worth it for better context!

### Storage Costs

**ChromaDB:**
- Embeddings: ~10MB per 1000 chunks
- Metadata: ~1MB per 1000 chunks
- Total: ~11MB per knowledge base
- Negligible on modern systems

---

## Future Enhancements

### V3.0: Advanced RAG

- **Hybrid search:** Combine semantic + keyword search
- **Re-ranking:** Use cross-encoder to re-rank results
- **Query expansion:** Expand user query with synonyms
- **Multi-hop reasoning:** Chain multiple searches

### V3.1: Dynamic Knowledge

- **Web scraping:** Auto-fetch and index URLs
- **API integration:** Pull from Confluence, Notion, etc.
- **Real-time updates:** Watch files for changes
- **Scheduled refresh:** Auto-refresh daily/weekly

### V3.2: Collaborative Knowledge

- **User contributions:** Users can add to knowledge bases
- **Voting system:** Upvote/downvote content quality
- **Version control:** Track changes over time
- **Conflict resolution:** Handle concurrent edits

---

## Summary

**Vikui** transforms the Matrix bot from a task manager into a **context-aware AI workspace** by combining:

1. **STATE** (Vikunja) - Tasks, deadlines, status
2. **CONTENT** (Vikui/RAG) - Docs, notes, knowledge
3. **INTELLIGENCE** (Claude) - Reasoning, actions

**Key Benefits:**
- 🎯 Room-specific expertise
- 📚 Instant access to knowledge
- 🔗 Seamless integration with tasks
- 💡 Better answers with context
- 🚀 Scalable to any domain

**Ready for implementation in V2!** 🎉

---

**End of Vikui Specification**


