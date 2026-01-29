# Debug Memory API

This document describes the API endpoints available for integrating external services (like the Cursor MCP server) with Debug Memory.

## Authentication

All API requests require a workspace API key. You can create API keys from the **API Keys** page in the Debug Memory dashboard (admin access required).

Include the API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

## Base URL

```
https://shcqctifenlhkhwgrksx.supabase.co/functions/v1
```

---

## Incidents

### Create an Incident

**POST** `/incidents`

Creates a new incident in the workspace associated with the API key.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | ✅ | Short description of the incident |
| `summary` | string | | Detailed summary of what happened |
| `error_signature` | string | | The error type/message for matching similar incidents |
| `tags` | string[] | | Tags for categorization |

#### Example Request

```bash
curl -X POST https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/incidents \
  -H "Authorization: Bearer dm_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "TypeError: Cannot read property of undefined",
    "summary": "Attempted to access .map() on an undefined array in UserList component",
    "error_signature": "TypeError: Cannot read property '\''map'\'' of undefined",
    "tags": ["react", "typescript", "null-check"]
  }'
```

#### Response

**201 Created**

```json
{
  "success": true,
  "incident": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "workspace_id": "...",
    "title": "TypeError: Cannot read property of undefined",
    "summary": "...",
    "error_signature": "...",
    "tags": ["react", "typescript", "null-check"],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### List Incidents

**GET** `/incidents`

Retrieves incidents for the workspace associated with the API key.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | number | 50 | Maximum number of incidents to return |
| `offset` | number | 0 | Number of incidents to skip (for pagination) |

#### Example Request

```bash
curl "https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/incidents?limit=10&offset=0" \
  -H "Authorization: Bearer dm_abc123..."
```

#### Response

**200 OK**

```json
{
  "incidents": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "TypeError: Cannot read property of undefined",
      "summary": "...",
      "created_at": "2024-01-15T10:30:00Z",
      ...
    }
  ],
  "total": 42
}
```

---

## Solutions

### Create a Solution

**POST** `/solutions`

Creates a new solution for an incident. Solutions contain the fix steps.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `incident_id` | string (UUID) | ✅ | The incident this solution is for |
| `steps` | string | | Steps taken to resolve the issue |
| `steps_hash` | string | | Hash of steps for deduplication |

#### Example Request

```bash
curl -X POST https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/solutions \
  -H "Authorization: Bearer dm_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": "550e8400-e29b-41d4-a716-446655440000",
    "steps": "Added null check before mapping: users?.map(...)",
    "steps_hash": "abc123def456"
  }'
```

#### Response

**201 Created**

```json
{
  "success": true,
  "solution": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "workspace_id": "...",
    "incident_id": "550e8400-e29b-41d4-a716-446655440000",
    "steps": "Added null check before mapping: users?.map(...)",
    "steps_hash": "abc123def456",
    "created_at": "2024-01-15T10:35:00Z"
  }
}
```

---

### List Solutions

**GET** `/solutions`

Retrieves solutions for the workspace. Optionally filter by incident.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `incident_id` | string (UUID) | | Filter to solutions for a specific incident |
| `limit` | number | 50 | Maximum number of solutions to return |
| `offset` | number | 0 | Number of solutions to skip (for pagination) |

#### Example Request

```bash
curl "https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/solutions?incident_id=550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer dm_abc123..."
```

#### Response

**200 OK**

```json
{
  "solutions": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "incident_id": "550e8400-e29b-41d4-a716-446655440000",
      "steps": "Added null check before mapping",
      "steps_hash": "abc123def456",
      "created_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 1
}
```

---

## Embeddings

### Add Embedding

**POST** `/embeddings`

Adds a pre-computed embedding for an incident field. Embeddings should be generated externally using `all-MiniLM-L6-v2` (384 dimensions).

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `incident_id` | string (UUID) | ✅ | The incident to associate the embedding with |
| `field` | string | ✅ | The field name this embedding represents (e.g., `"title"`, `"summary"`, `"error_signature"`) |
| `embedding` | number[] | ✅ | 384-dimensional embedding vector |

#### Example Request

```bash
curl -X POST https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/embeddings \
  -H "Authorization: Bearer dm_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": "550e8400-e29b-41d4-a716-446655440000",
    "field": "title",
    "embedding": [0.123, -0.456, 0.789, ...]
  }'
```

#### Response

**201 Created**

```json
{
  "success": true,
  "embedding": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "incident_id": "550e8400-e29b-41d4-a716-446655440000",
    "workspace_id": "...",
    "field": "title",
    "embedding": "[0.123,-0.456,0.789,...]",
    "created_at": "2024-01-15T10:35:00Z"
  }
}
```

---

### Get Embeddings for an Incident

**GET** `/embeddings?incident_id={incident_id}`

Retrieves all embeddings for a specific incident.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `incident_id` | string (UUID) | ✅ | The incident ID to fetch embeddings for |

#### Example Request

```bash
curl "https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/embeddings?incident_id=550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer dm_abc123..."
```

#### Response

**200 OK**

```json
{
  "embeddings": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "incident_id": "550e8400-e29b-41d4-a716-446655440000",
      "field": "title",
      "embedding": "[0.123,-0.456,0.789,...]",
      "created_at": "2024-01-15T10:35:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "incident_id": "550e8400-e29b-41d4-a716-446655440000",
      "field": "summary",
      "embedding": "[0.234,-0.567,0.890,...]",
      "created_at": "2024-01-15T10:36:00Z"
    }
  ]
}
```

---

## Search

### Semantic Search for Similar Incidents

**POST** `/search`

Searches for similar incidents using vector similarity on pre-computed embeddings. Returns incidents ranked by relevance, including their solutions.

#### Request Body

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `embedding` | number[] | ✅ | | 384-dimensional query embedding vector |
| `limit` | number | | 10 | Maximum number of results to return |
| `threshold` | number | | 0.7 | Minimum similarity score (0-1) to include in results |
| `field` | string | | | Filter to search only specific field embeddings (e.g., `"title"`, `"summary"`) |

#### Example Request

```bash
curl -X POST https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/search \
  -H "Authorization: Bearer dm_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "embedding": [0.123, -0.456, 0.789, ...],
    "limit": 5,
    "threshold": 0.75
  }'
```

#### Response

**200 OK**

```json
{
  "results": [
    {
      "incident_id": "550e8400-e29b-41d4-a716-446655440000",
      "similarity": 0.92,
      "field": "error_signature",
      "incident": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "TypeError: Cannot read property of undefined",
        "summary": "...",
        ...
      },
      "solutions": [
        {
          "id": "660e8400-e29b-41d4-a716-446655440000",
          "steps": "Added null check before mapping"
        }
      ]
    }
  ],
  "count": 1
}
```

#### Usage Notes

1. Generate query embeddings using the same model as stored embeddings (`all-MiniLM-L6-v2`)
2. Higher `threshold` values return fewer but more relevant results
3. Use `field` filter to search only specific types of embeddings

---

## Outcomes

### Record an Outcome

**POST** `/outcomes`

Records whether a solution worked or failed in a specific environment. This creates an outcome record and automatically updates the `solution_env_stats` table via database trigger.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `solution_id` | string (UUID) | ✅ | The solution this outcome is for |
| `worked` | boolean | ✅ | Whether the fix worked (`true`) or failed (`false`) |
| `notes` | string | | Additional notes about the outcome |
| `os_family` | string | | Operating system: `linux`, `macos`, `windows` |
| `language` | string | | Programming language: `python`, `node`, `go`, etc. |
| `language_major` | integer | | Major version of the language (e.g., `3` for Python 3.x) |
| `framework` | string | | Framework: `pytorch`, `tensorflow`, `fastapi`, `react`, etc. |
| `framework_major` | integer | | Major version of the framework |
| `runtime` | string | | Runtime environment: `docker`, `k8s`, `bare`, `conda`, `venv` |
| `cuda_major` | integer | | CUDA major version (nullable) |
| `env_bucket` | string | | Environment bucket for grouping (e.g., `linux|py3|torch2|cuda12|docker`) |
| `env_raw` | object | | Optional raw environment JSON for additional context |

#### Example Request

```bash
curl -X POST https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/outcomes \
  -H "Authorization: Bearer dm_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "solution_id": "660e8400-e29b-41d4-a716-446655440000",
    "worked": true,
    "notes": "Fix verified in production after deploying v2.3.1",
    "os_family": "linux",
    "language": "python",
    "language_major": 3,
    "framework": "pytorch",
    "framework_major": 2,
    "runtime": "docker",
    "cuda_major": 12,
    "env_bucket": "linux|py3|torch2|cuda12|docker"
  }'
```

#### Response

**201 Created**

```json
{
  "outcome": {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "solution_id": "660e8400-e29b-41d4-a716-446655440000",
    "workspace_id": "...",
    "worked": true,
    "notes": "Fix verified in production after deploying v2.3.1",
    "os_family": "linux",
    "language": "python",
    "language_major": 3,
    "framework": "pytorch",
    "framework_major": 2,
    "runtime": "docker",
    "cuda_major": 12,
    "env_bucket": "linux|py3|torch2|cuda12|docker",
    "env_raw": null,
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

---

### List Outcomes

**GET** `/outcomes`

Retrieves outcomes for the workspace. Optionally filter by solution.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `solution_id` | string (UUID) | | Filter to outcomes for a specific solution |
| `limit` | number | 50 | Maximum number of outcomes to return |
| `offset` | number | 0 | Number of outcomes to skip (for pagination) |

#### Example Request

```bash
curl "https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/outcomes?solution_id=660e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer dm_abc123..."
```

#### Response

**200 OK**

```json
{
  "outcomes": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "solution_id": "660e8400-e29b-41d4-a716-446655440000",
      "worked": true,
      "notes": "Fix verified in production",
      "os_family": "linux",
      "language": "python",
      "env_bucket": "linux|py3|torch2|cuda12|docker",
      "created_at": "2024-01-15T12:00:00Z"
    }
  ],
  "total": 1
}
```

---

## Solution Environment Stats

The `solution_env_stats` table is automatically updated via database trigger when outcomes are created. It aggregates worked/failed counts per solution per environment bucket.

### Schema

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | Primary key |
| `workspace_id` | uuid | Workspace reference |
| `solution_id` | uuid | Solution reference |
| `env_bucket` | text | Environment bucket string |
| `worked_count` | integer | Number of successful outcomes |
| `failed_count` | integer | Number of failed outcomes |
| `last_confirmed_at` | timestamptz | Last successful outcome timestamp |
| `created_at` | timestamptz | Row creation timestamp |
| `updated_at` | timestamptz | Last update timestamp |

This table enables querying solution effectiveness across different environments without scanning all outcomes.

---

## Solution Stats

### Get Solution Environment Stats

**GET** `/solution-stats`

Retrieves aggregated success/failure statistics for solutions across different environments.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `solution_id` | string (UUID) | | Filter to stats for a specific solution |
| `env_bucket` | string | | Filter to stats for a specific environment bucket |
| `limit` | number | 100 | Maximum number of stats to return |
| `offset` | number | 0 | Number of stats to skip (for pagination) |

#### Example Request

```bash
curl "https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/solution-stats?solution_id=660e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer dm_abc123..."
```

#### Response

**200 OK**

```json
{
  "stats": [
    {
      "id": "880e8400-e29b-41d4-a716-446655440000",
      "solution_id": "660e8400-e29b-41d4-a716-446655440000",
      "workspace_id": "...",
      "env_bucket": "linux|py3|torch2|cuda12|docker",
      "worked_count": 15,
      "failed_count": 2,
      "last_confirmed_at": "2024-01-15T14:30:00Z",
      "created_at": "2024-01-10T10:00:00Z",
      "updated_at": "2024-01-15T14:30:00Z"
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440001",
      "solution_id": "660e8400-e29b-41d4-a716-446655440000",
      "workspace_id": "...",
      "env_bucket": "macos|py3|torch2|bare",
      "worked_count": 5,
      "failed_count": 0,
      "last_confirmed_at": "2024-01-14T09:00:00Z",
      "created_at": "2024-01-12T11:00:00Z",
      "updated_at": "2024-01-14T09:00:00Z"
    }
  ],
  "solution": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "incident_id": "550e8400-e29b-41d4-a716-446655440000",
    "steps": "Added null check before mapping",
    "steps_hash": "abc123",
    "created_at": "2024-01-10T10:00:00Z",
    "incidents": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "TypeError: Cannot read property of undefined",
      "error_signature": "TypeError: Cannot read property 'map' of undefined"
    }
  },
  "total": 2
}
```

#### Usage Notes

1. When `solution_id` is provided, the response includes the full solution with its incident details
2. Stats are ordered by `updated_at` descending (most recently updated first)
3. Use `env_bucket` filter to find stats for a specific environment configuration

---

## Bulk Solution Environment Stats

### Fetch Stats for Multiple Solutions

**POST** `/solution-env-stats`

Bulk-fetches environment stats for multiple solutions in one round-trip. Useful when you have a set of candidate solutions and need to evaluate their effectiveness across environments.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `solution_ids` | string[] (UUIDs) | ✅ | Array of solution IDs to fetch stats for (max 100) |

#### Example Request

```bash
curl -X POST https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/solution-env-stats \
  -H "Authorization: Bearer dm_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "solution_ids": [
      "660e8400-e29b-41d4-a716-446655440000",
      "660e8400-e29b-41d4-a716-446655440001",
      "660e8400-e29b-41d4-a716-446655440002"
    ]
  }'
```

#### Response

**200 OK**

```json
{
  "stats": [
    {
      "solution_id": "660e8400-e29b-41d4-a716-446655440000",
      "env_bucket": "linux|py3|torch2|cuda12|docker",
      "worked_count": 15,
      "failed_count": 2,
      "last_confirmed_at": "2024-01-15T14:30:00Z"
    },
    {
      "solution_id": "660e8400-e29b-41d4-a716-446655440000",
      "env_bucket": "macos|py3|torch2|bare",
      "worked_count": 5,
      "failed_count": 0,
      "last_confirmed_at": "2024-01-14T09:00:00Z"
    },
    {
      "solution_id": "660e8400-e29b-41d4-a716-446655440001",
      "env_bucket": "linux|py3|torch2|cuda11|docker",
      "worked_count": 8,
      "failed_count": 1,
      "last_confirmed_at": "2024-01-13T11:00:00Z"
    }
  ]
}
```

#### Usage Notes

1. Maximum 100 solution IDs per request
2. Returns stats for all matching solutions in the workspace
3. Solutions without any recorded outcomes will have no entries in the response

---

## Environment Bucket

### Canonicalize Environment to Bucket

**POST** `/env-bucket`

Canonicalizes an environment object to the standard bucket string format used in `solution_env_stats`. Use this to ensure consistent bucketing between your client and the server.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `env` | object | ✅ | Environment object to canonicalize |

**Environment object fields:**

| Field | Type | Description |
|-------|------|-------------|
| `os_family` | string | Operating system: `linux`, `macos`, `windows` |
| `language` | string | Programming language: `python`, `node`, `go`, etc. |
| `language_major` | number | Major version of the language |
| `framework` | string | Framework: `pytorch`, `tensorflow`, `react`, etc. |
| `framework_major` | number | Major version of the framework |
| `cuda_major` | number | CUDA major version (if applicable) |
| `runtime` | string | Runtime environment: `docker`, `k8s`, `conda`, `venv`, `bare` |

#### Example Request

```bash
curl -X POST https://shcqctifenlhkhwgrksx.supabase.co/functions/v1/env-bucket \
  -H "Content-Type: application/json" \
  -d '{
    "env": {
      "os_family": "linux",
      "language": "python",
      "language_major": 3,
      "framework": "pytorch",
      "framework_major": 2,
      "cuda_major": 12,
      "runtime": "docker"
    }
  }'
```

#### Response

**200 OK**

```json
{
  "env_bucket": "linux|py3|torch2|cuda12|docker"
}
```

#### Bucket Format

The bucket string is constructed as: `os_family|language+major|framework+major|cuda_major|runtime`

- All parts are lowercase
- Empty/null parts are omitted
- Common abbreviations: `python` → `py`, `pytorch` → `torch`, `tensorflow` → `tf`

**Examples:**
- `linux|py3|torch2|cuda12|docker`
- `macos|py3|torch2|bare`
- `windows|node20|react18`
- `linux|go1|docker`

#### Usage Notes

1. No authentication required (public endpoint for convenience)
2. Use the returned `env_bucket` when calling `/outcomes` to ensure consistency
3. The same bucketing logic is used server-side when aggregating stats

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "error": "Error message description"
}
```

### Common Status Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Missing required fields |
| 401 | Unauthorized - Invalid or missing API key |
| 405 | Method Not Allowed |
| 500 | Internal Server Error |

---

## Rate Limits

There are currently no rate limits enforced, but please be reasonable with your API usage.

---

## MCP Server Integration

When integrating with a Cursor MCP server, you can use these endpoints to:

1. **Capture incidents** - When the MCP server encounters an error, POST it to `/incidents`
2. **Add solutions** - When a fix is found, POST it to `/solutions` linked to the incident
3. **Search for solutions** - POST to `/search` with an embedding to find similar past incidents and their solutions
4. **Record outcomes** - POST to `/outcomes` with full environment context to track whether solutions worked
5. **Query stats** - GET `/solution-stats` to retrieve aggregated success/failure metrics per solution and environment

### Example MCP Handler (TypeScript)

```typescript
const API_KEY = process.env.DEBUG_MEMORY_API_KEY;
const BASE_URL = "https://shcqctifenlhkhwgrksx.supabase.co/functions/v1";

async function captureIncident(incident: {
  title: string;
  summary?: string;
  error_signature?: string;
  tags?: string[];
}) {
  const response = await fetch(`${BASE_URL}/incidents`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(incident),
  });
  
  return response.json();
}

async function addSolution(solution: {
  incident_id: string;
  steps: string;
  steps_hash?: string;
}) {
  const response = await fetch(`${BASE_URL}/solutions`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(solution),
  });
  
  return response.json();
}

async function recordOutcome(
  solutionId: string,
  worked: boolean,
  env: {
    os_family?: string;
    language?: string;
    language_major?: number;
    framework?: string;
    framework_major?: number;
    runtime?: string;
    cuda_major?: number;
    env_bucket?: string;
  },
  notes?: string
) {
  const response = await fetch(`${BASE_URL}/outcomes`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      solution_id: solutionId,
      worked,
      notes,
      ...env,
    }),
  });
  
  return response.json();
}
```
