# Database Schema

Complete database schema documentation for Debug Memory.

## Enums

### `app_role`
User roles within a workspace.
- `admin` - Full access, can manage members and settings
- `member` - Standard access to workspace resources

### `redaction_level`
Level of automatic PII redaction for incidents.
- `none` - No redaction
- `basic` - Basic PII redaction
- `strict` - Aggressive redaction

---

## Tables

### `workspaces`
Top-level organizational unit.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `name` | text | No | - | Workspace name |
| `plan` | text | No | `'free'` | Subscription plan |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |

---

### `workspace_members`
Links users to workspaces with roles.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `user_id` | uuid | No | - | FK to auth.users |
| `role` | app_role | No | `'member'` | User's role |
| `created_at` | timestamptz | No | `now()` | Join timestamp |

**Unique constraint**: `(workspace_id, user_id)`

---

### `workspace_api_keys`
API keys for server-to-server authentication (MCP integration).

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `name` | text | No | - | Key name/label |
| `key_hash` | text | No | - | SHA-256 hash of API key |
| `is_active` | boolean | No | `true` | Whether key is active |
| `last_used_at` | timestamptz | Yes | - | Last usage timestamp |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |

**Note**: The actual API key is only shown once at creation. Only the hash is stored.

---

### `workspace_settings`
Per-workspace configuration.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `workspace_id` | uuid | No | - | PK, FK to workspaces |
| `auto_capture_enabled` | boolean | No | `true` | Auto-capture incidents |
| `retention_days` | integer | No | `30` | Data retention period |
| `redaction_level` | redaction_level | No | `'basic'` | PII redaction level |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |
| `updated_at` | timestamptz | No | `now()` | Last update timestamp |

---

### `incidents`
Core incident records created by MCP or manually.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `title` | text | No | - | Incident title |
| `summary` | text | Yes | - | Brief description |
| `error_signature` | text | Yes | - | Unique error identifier |
| `tags` | text[] | Yes | `'{}'` | Categorization tags |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |
| `updated_at` | timestamptz | No | `now()` | Last update timestamp |

---

### `solutions`
Proposed fixes for incidents.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `incident_id` | uuid | No | - | FK to incidents |
| `steps` | text | Yes | - | Resolution steps |
| `steps_hash` | text | Yes | - | Hash for deduplication |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |

---

### `outcomes`
Records whether a solution worked or failed, with environment context.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `solution_id` | uuid | No | - | FK to solutions |
| `worked` | boolean | No | - | Whether fix succeeded |
| `notes` | text | Yes | - | Additional notes |
| `os_family` | text | Yes | - | OS: `linux`, `macos`, `windows` |
| `language` | text | Yes | - | Language: `python`, `node`, `go`, etc. |
| `language_major` | integer | Yes | - | Language major version |
| `framework` | text | Yes | - | Framework: `pytorch`, `tensorflow`, `react`, etc. |
| `framework_major` | integer | Yes | - | Framework major version |
| `runtime` | text | Yes | - | Runtime: `docker`, `k8s`, `bare`, `conda`, `venv` |
| `cuda_major` | integer | Yes | - | CUDA major version |
| `env_bucket` | text | Yes | - | Environment bucket (e.g., `linux|py3|torch2|cuda12|docker`) |
| `env_raw` | jsonb | Yes | - | Raw environment data |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |

---

### `solution_env_stats`
Aggregated success/failure stats per solution per environment bucket. Automatically updated via trigger.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `solution_id` | uuid | No | - | FK to solutions |
| `env_bucket` | text | No | - | Environment bucket string |
| `worked_count` | integer | No | `0` | Times fix succeeded |
| `failed_count` | integer | No | `0` | Times fix failed |
| `last_confirmed_at` | timestamptz | Yes | - | Last success timestamp |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |
| `updated_at` | timestamptz | No | `now()` | Last update timestamp |

**Unique constraint**: `(solution_id, env_bucket)`

---

### `incident_embeddings`
Vector embeddings for semantic search on incidents.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `incident_id` | uuid | No | - | FK to incidents |
| `field` | text | No | - | Which field was embedded |
| `embedding` | vector(384) | Yes | - | pgvector embedding |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |

---

### `solution_embeddings`
Vector embeddings for semantic search on solutions (e.g., environment context).

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `solution_id` | uuid | No | - | FK to solutions |
| `field` | text | No | - | Which field was embedded (e.g., `env`) |
| `embedding` | vector(384) | Yes | - | pgvector embedding |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |

---

### `profiles`
User profile information (synced from auth.users).

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | - | PK, matches auth.users.id |
| `email` | text | Yes | - | User email |
| `full_name` | text | Yes | - | Display name |
| `created_at` | timestamptz | No | `now()` | Creation timestamp |

**Trigger**: `handle_new_user()` auto-creates profile on signup.

---

### `pending_invites`
Workspace invitations for users who haven't signed up yet.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | No | `gen_random_uuid()` | Primary key |
| `workspace_id` | uuid | No | - | FK to workspaces |
| `email` | text | No | - | Invitee email |
| `role` | app_role | No | `'member'` | Role to assign |
| `invited_by` | uuid | No | - | FK to auth.users |
| `created_at` | timestamptz | No | `now()` | Invite timestamp |

**Trigger**: `handle_pending_invites()` processes invites when user signs up.

---

## Database Functions

### `is_workspace_member(workspace_id, user_id)`
Returns `boolean`. Checks if user is a member of the workspace.

### `is_workspace_admin(workspace_id, user_id)`
Returns `boolean`. Checks if user is an admin of the workspace.

### `search_similar_incidents(query_embedding, workspace_uuid, match_threshold, match_count, field_filter)`
Performs vector similarity search on incident embeddings.

**Parameters:**
- `query_embedding` (text) - JSON string of 384-dimension vector
- `workspace_uuid` (uuid) - Workspace to search within
- `match_threshold` (float, default 0.7) - Minimum similarity score
- `match_count` (int, default 10) - Maximum results to return
- `field_filter` (text, optional) - Filter by embedding field type

**Returns:** Table of `(incident_id, field, similarity)` - does not include embedding vectors.

### `search_similar_solutions(query_embedding, workspace_uuid, match_count, field_filter)`
Performs vector similarity search on solution embeddings, returning ranked results without a threshold.

**Parameters:**
- `query_embedding` (text) - JSON string of 384-dimension vector
- `workspace_uuid` (uuid) - Workspace to search within
- `match_count` (int, default 10) - Maximum results to return
- `field_filter` (text, optional) - Filter by embedding field type (e.g., `env`)

**Returns:** Table of `(solution_id, field, similarity)` - ranked by similarity, does not include embedding vectors.

### `update_solution_env_stats()`
Trigger function. Automatically updates `solution_env_stats` when a new outcome is inserted. Aggregates `worked_count` and `failed_count` per `solution_id` and `env_bucket`.

### `handle_new_user()`
Trigger function. Creates profile row when new user signs up.

### `handle_pending_invites()`
Trigger function. Converts pending invites to workspace memberships on signup.

### `update_updated_at_column()`
Trigger function. Auto-updates `updated_at` on row modification.

---

## Entity Relationship Diagram

```
workspaces
    │
    ├──< workspace_members >── profiles (via user_id → auth.users)
    │
    ├──< workspace_api_keys
    │
    ├──< workspace_settings
    │
    ├──< incidents
    │       │
    │       ├──< solutions
    │       │       │
    │       │       ├──< outcomes
    │       │       │
    │       │       └──< solution_env_stats
    │       │
    │       └──< incident_embeddings
    │
    ├──< solutions
    │       │
    │       └──< solution_embeddings
    │
    └──< pending_invites
```

---

## Data Hierarchy

The incident tracking system uses a four-tier structure:

1. **Incidents** - Core issue metadata (title, summary, error signature)
2. **Solutions** - Specific fix steps for an incident
3. **Outcomes** - Individual records tracking if a solution worked or failed, with full environment context
4. **Solution Env Stats** - Aggregated success metrics per solution per environment bucket

This allows multiple proposed fixes per incident, each with independent success metrics across different environments.

---

## MCP Integration Notes

When inserting data from MCP:

1. **Authentication**: Use API key in `Authorization: Bearer <key>` header
2. **Workspace Resolution**: Edge functions hash your key and look up `workspace_id` from `workspace_api_keys`

### Creating Incidents
- **Required**: `title`
- **Recommended**: `error_signature` (for deduplication), `summary`

### Creating Solutions
- **Required**: `incident_id`
- **Recommended**: `steps`, `steps_hash`

### Recording Outcomes
- **Required**: `solution_id`, `worked`
- **Recommended**: `os_family`, `language`, `framework`, `runtime`, `env_bucket`
- **Optional**: `notes`, `language_major`, `framework_major`, `cuda_major`, `env_raw`
s