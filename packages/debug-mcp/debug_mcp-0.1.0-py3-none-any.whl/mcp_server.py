"""
Debug Incident MCP Server

Implements Debug Memory MCP tools:
- ranked_solutions (incident search + env-aware solution ranking)
- add_solution
- add_incident (creates new incident + solution + outcome; blocks duplicates)
- record_outcome

Uses Debug Memory edge functions and local embeddings (all-MiniLM-L6-v2).
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Configuration
EDGE_FUNCTION_URL = os.getenv("EDGE_FUNCTION_URL")
WORKSPACE_API_KEY = os.getenv("WORKSPACE_API_KEY")

if not EDGE_FUNCTION_URL:
    raise ValueError("Missing EDGE_FUNCTION_URL environment variable")

if not WORKSPACE_API_KEY:
    raise ValueError("Missing WORKSPACE_API_KEY environment variable")

# MCP server
server = Server("debug-incident")

# Embedding model (lazy loaded)
_embedding_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    """Lazy load the embedding model."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


async def _post_json(path: str, payload: dict) -> httpx.Response:
    """Helper for POST requests."""
    async with httpx.AsyncClient() as client:
        return await client.post(
            f"{EDGE_FUNCTION_URL}{path}",
            json=payload,
            headers={
                "Authorization": f"Bearer {WORKSPACE_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )


async def upload_embeddings(incident_id: str, fields: Dict[str, str]) -> str:
    """Generate and upload embeddings for provided fields."""
    tasks = []
    model = get_embedding_model()

    for field, text in fields.items():
        if not text:
            continue
        embedding = model.encode(text).tolist()
        tasks.append(
            _post_json(
                "/embeddings",
                {
                    "incident_id": incident_id,
                    "field": field,
                    "embedding": embedding,
                },
            )
        )

    if not tasks:
        return ""

    import asyncio

    results = await asyncio.gather(*tasks, return_exceptions=True)
    success = sum(
        1
        for r in results
        if isinstance(r, httpx.Response) and r.status_code == 201
    )
    return f"\nEmbeddings: {success}/{len(tasks)} uploaded"


def _format_next_action(action_type: str, instructions: str) -> dict:
    return {"type": action_type, "instructions": instructions}


@server.list_tools()
async def list_tools() -> List[Tool]:
    """Expose MCP tools."""
    return [
        Tool(
            name="add_solution",
            description="Add a new fix for an existing incident (including env-specific variants).",
            inputSchema={
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string",
                        "description": "Incident id to attach solution",
                    },
                    "steps": {
                        "type": "string",
                        "description": "Steps taken to resolve the issue",
                    },
                    "env": {
                        "type": "object",
                        "description": "Environment context used for bucketing",
                    },
                    "env_bucket": {
                        "type": "string",
                        "description": "Optional env bucket override. If omitted, will be computed from env via /env-bucket.",
                    },
                    "lookup_id": {
                        "type": "string",
                        "description": "Lookup correlation id (optional)",
                    },
                },
                "required": ["incident_id", "steps", "env"],
            },
        ),
        Tool(
            name="add_incident",
            description="Create a new incident + solution + outcome. If an incident already exists, use add_solution instead.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Incident title"},
                    "error_signature": {
                        "type": "string",
                        "description": "Error signature/identifier",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Brief summary",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization",
                    },
                    "steps": {
                        "type": "string",
                        "description": "Steps taken to resolve the issue (solution steps)",
                    },
                    "env": {
                        "type": "object",
                        "description": "Environment context used for bucketing and outcome stats",
                    },
                    "env_bucket": {
                        "type": "string",
                        "description": "Optional env bucket override. If omitted, will be computed from env via /env-bucket.",
                    },
                    "worked": {
                        "type": "boolean",
                        "description": "Whether the solution worked in this environment",
                    },
                    "notes": {
                        "type": "string",
                        "description": "Optional notes for the outcome record",
                    },
                    "lookup_id": {
                        "type": "string",
                        "description": "Lookup correlation id (optional)",
                    },
                },
                "required": ["title", "steps", "env", "worked"],
            },
        ),
        Tool(
            name="record_outcome",
            description="Record whether a solution worked or failed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "solution_id": {
                        "type": "string",
                        "description": "Solution id that was attempted",
                    },
                    "worked": {
                        "type": "boolean",
                        "description": "Whether the solution worked",
                    },
                    "env": {
                        "type": "object",
                        "description": "Environment context used for bucketing and outcome stats",
                    },
                    "env_bucket": {
                        "type": "string",
                        "description": "Optional env bucket override. If omitted, will be computed from env via /env-bucket.",
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional notes (optional)",
                    },
                    "lookup_id": {
                        "type": "string",
                        "description": "Lookup correlation id (optional)",
                    },
                },
                "required": ["solution_id", "worked", "env"],
            },
        ),
        Tool(
            name="ranked_solutions",
            description="Search incidents and return solutions ranked by env similarity, reliability, and recency.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query_text": {
                        "type": "string",
                        "description": "Problem description or error message to search for",
                    },
                    "env": {
                        "type": "object",
                        "description": "Environment context (required for ranking)",
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum solutions to return (default: 5)",
                    },
                },
                "required": ["query_text", "env"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Dispatch tool calls."""
    if name == "add_solution":
        return await add_solution(arguments)
    if name == "add_incident":
        return await add_incident(arguments)
    if name == "record_outcome":
        return await record_outcome(arguments)
    if name == "ranked_solutions":
        return await ranked_solutions(arguments)

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        # Handle trailing Z
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def _jaccard_score(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    a_tokens = set(a.split("|"))
    b_tokens = set(b.split("|"))
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def _reliability_score(worked: int, failed: int) -> float:
    # Smoothed success rate weighted by sample size (caps at 1.0)
    worked = worked or 0
    failed = failed or 0
    total = worked + failed
    if total == 0:
        return 0.0
    success_rate = worked / total
    weight = min(total, 10) / 10  # saturate after ~10 outcomes
    return success_rate * weight


def _recency_boost(last_confirmed_at: Optional[str]) -> float:
    ts = _parse_iso(last_confirmed_at)
    if not ts:
        return 0.0
    days = (datetime.now(timezone.utc) - ts).total_seconds() / 86400.0
    # Linear decay over ~90 days, capped between 0 and 0.2
    factor = max(0.0, 1.0 - min(days / 90.0, 1.0))
    return 0.2 * factor


def _best_env_match(
    query_bucket: str, solution_bucket: Optional[str], stats: List[Dict[str, Any]]
) -> Tuple[str, float, Dict[str, Any]]:
    best_bucket = solution_bucket or ""
    best_score = _jaccard_score(query_bucket, solution_bucket or "")
    best_stat = {}

    for stat in stats:
        bucket = stat.get("env_bucket") or ""
        score = _jaccard_score(query_bucket, bucket)
        if score > best_score:
            best_score = score
            best_bucket = bucket
            best_stat = stat

    return best_bucket, best_score, best_stat


def _extract_outcome_env_fields(env: Dict[str, Any]) -> Dict[str, Any]:
    """Extract known env fields for the outcomes API, without sending unexpected keys."""
    if not isinstance(env, dict):
        return {}
    keys = [
        "os_family",
        "language",
        "language_major",
        "framework",
        "framework_major",
        "runtime",
        "cuda_major",
    ]
    out: Dict[str, Any] = {}
    for k in keys:
        if k in env and env[k] is not None:
            out[k] = env[k]
    return out


async def _get_env_bucket(env: Dict[str, Any], fallback: str = "") -> str:
    """Canonicalize env to env_bucket via /env-bucket."""
    try:
        resp = await _post_json("/env-bucket", {"env": env})
        if resp.status_code == 200:
            return resp.json().get("env_bucket", "") or fallback
    except Exception:
        pass
    return fallback


async def ranked_solutions(arguments: Dict[str, Any]) -> List[TextContent]:
    """Search incidents then rank solutions by env match, reliability, and recency."""
    query_text = arguments.get("query_text")
    env = arguments.get("env")
    limit = int(arguments.get("limit", 5))

    if not query_text:
        return [TextContent(type="text", text="Error: query_text is required")]
    if env is None:
        return [TextContent(type="text", text="Error: env is required for ranking")]

    try:
        model = get_embedding_model()
        query_embedding = model.encode(query_text).tolist()

        # Step A: incident search
        resp = await _post_json(
            "/search",
            {
                "embedding": query_embedding,
                "limit": max(limit * 2, 5),  # get enough incidents to collect solutions
            },
        )
        if resp.status_code != 200:
            return [
                TextContent(
                    type="text",
                    text=f"❌ Search failed (status {resp.status_code})",
                )
            ]

        data = resp.json()
        results = data.get("results", [])
        lookup_id = str(uuid.uuid4())

        if not results:
            next_action = _format_next_action(
                "NO_MATCH_DEBUG_THEN_ADD_INCIDENT",
                "No relevant incidents found. Debug normally. If a fix is found, call add_incident to store the incident + solution + outcome.",
            )
            return [
                TextContent(
                    type="text",
                    text=(
                        f"🔍 No matches found for: \"{query_text}\"\n"
                        f"lookup_id: {lookup_id}\n\n"
                        f"next_action: {next_action}"
                    ),
                )
            ]

        # Step B: collect candidate solutions
        solution_map: Dict[str, Dict[str, Any]] = {}
        incident_titles: Dict[str, str] = {}
        for item in results:
            inc = item.get("incident", {})
            incident_titles[inc.get("id", "")] = inc.get("title", "(no title)")
            for sol in item.get("solutions") or []:
                sid = sol.get("id")
                if sid and sid not in solution_map:
                    solution_map[sid] = sol

        if not solution_map:
            next_action = _format_next_action(
                "NO_SOLUTIONS_ADD_ONE",
                "Incidents were found but no solutions exist. Debug normally. Once you find a fix that works, call add_solution for the best matching incident, then record_outcome.",
            )
            return [
                TextContent(
                    type="text",
                    text=(
                        f"🔍 Incidents found for: \"{query_text}\" but no solutions are recorded.\n"
                        f"lookup_id: {lookup_id}\n\n"
                        f"next_action: {next_action}"
                    ),
                )
            ]

        # Step C: canonicalize env bucket and fetch solution env stats
        env_bucket = await _get_env_bucket(env, fallback="")

        stats_map: Dict[str, List[Dict[str, Any]]] = {}
        try:
            stats_resp = await _post_json(
                "/solution-env-stats", {"solution_ids": list(solution_map.keys())}
            )
            if stats_resp.status_code == 200:
                for row in stats_resp.json().get("stats", []):
                    sid = row.get("solution_id")
                    if sid:
                        stats_map.setdefault(sid, []).append(row)
        except Exception:
            stats_map = {}

        # Step C continued: score each solution
        scored: List[Dict[str, Any]] = []
        for sid, sol in solution_map.items():
            sol_bucket = sol.get("env_bucket")
            best_bucket, env_match_score, best_stat = _best_env_match(
                env_bucket, sol_bucket, stats_map.get(sid, [])
            )
            reliability = _reliability_score(
                best_stat.get("worked_count", 0), best_stat.get("failed_count", 0)
            ) if best_stat else 0.0
            recency = _recency_boost(best_stat.get("last_confirmed_at")) if best_stat else 0.0
            final_score = env_match_score + reliability + recency

            scored.append(
                {
                    "solution_id": sid,
                    "solution": sol,
                    "incident_id": sol.get("incident_id", ""),
                    "best_env_bucket": best_bucket,
                    "env_match_score": env_match_score,
                    "reliability_score": reliability,
                    "recency_boost": recency,
                    "final_score": final_score,
                    "worked_count": best_stat.get("worked_count", 0) if best_stat else 0,
                    "failed_count": best_stat.get("failed_count", 0) if best_stat else 0,
                    "last_confirmed_at": best_stat.get("last_confirmed_at") if best_stat else None,
                }
            )

        scored.sort(key=lambda x: x["final_score"], reverse=True)
        top = scored[:limit]

        recommended = top[0] if top else None
        next_action = _format_next_action(
            "TRY_SOLUTION_AND_RECORD_OUTCOME",
            "Try the recommended solution. After attempting it, call record_outcome with worked=true or false.",
        )

        lines = [
            f"🔍 Ranked solutions for: \"{query_text}\"",
            f"lookup_id: {lookup_id}",
            f"query_env_bucket: {env_bucket or '(none)'}",
            f"incidents_found: {len(results)}",
            f"candidate_solutions: {len(scored)}",
            "",
        ]

        for i, item in enumerate(top, 1):
            sol = item["solution"]
            title = incident_titles.get(item["incident_id"], "(unknown incident)")
            lines.append(
                f"{i}. solution_id: {item['solution_id']} (incident: {title})"
            )
            lines.append(f"   steps: {sol.get('steps','')[:200]}")
            lines.append(
                f"   env_bucket: {item['best_env_bucket'] or sol.get('env_bucket','') or '(none)'} "
                f"(match {item['env_match_score']:.2f})"
            )
            lines.append(
                f"   reliability: {item['reliability_score']:.2f} (worked {item['worked_count']}, failed {item['failed_count']})"
            )
            if item["last_confirmed_at"]:
                lines.append(f"   last_confirmed_at: {item['last_confirmed_at']}")
            lines.append(f"   recency_boost: {item['recency_boost']:.2f}")
            lines.append(f"   final_score: {item['final_score']:.2f}")
            lines.append("")

        if recommended:
            lines.append("Recommended solution to try first:")
            lines.append(f"- solution_id: {recommended['solution_id']}")
            lines.append(f"- steps: {recommended['solution'].get('steps','')}")
            lines.append(
                f"- env_bucket: {recommended['best_env_bucket'] or recommended['solution'].get('env_bucket','') or '(none)'}"
            )
            lines.append(
                f"- scores => env_match: {recommended['env_match_score']:.2f}, "
                f"reliability: {recommended['reliability_score']:.2f}, "
                f"recency: {recommended['recency_boost']:.2f}"
            )
            lines.append("")

        lines.append(f"next_action: {next_action}")

        return [TextContent(type="text", text="\n".join(lines))]

    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def add_solution(arguments: Dict[str, Any]) -> List[TextContent]:
    """Add a new solution to an incident."""
    incident_id = arguments.get("incident_id")
    steps = arguments.get("steps")
    env = arguments.get("env")
    env_bucket_override = arguments.get("env_bucket") or ""

    if not incident_id or not steps:
        return [
            TextContent(
                type="text", text="Error: incident_id and steps are required"
            )
        ]
    if not isinstance(env, dict):
        return [TextContent(type="text", text="Error: env is required and must be an object")]

    env_bucket = await _get_env_bucket(env, fallback=env_bucket_override)

    payload = {
        "incident_id": incident_id,
        "steps": steps,
        "env": env,
        "env_bucket": env_bucket or None,
    }

    resp = await _post_json("/solutions", payload)
    if resp.status_code != 201:
        msg = resp.json().get("error", f"status {resp.status_code}")
        return [TextContent(type="text", text=f"❌ Failed to add solution: {msg}")]

    sol = resp.json().get("solution", {}) or {}
    solution_id = sol.get("id", "unknown")

    next_action = _format_next_action(
        "RECORD_OUTCOME_FOR_NEW_SOLUTION",
        "If you try this solution, call record_outcome with solution_id, worked, and env.",
    )

    return [
        TextContent(
            type="text",
            text=(
                "✅ Solution added\n"
                f"solution_id: {solution_id}\n"
                f"incident_id: {incident_id}\n"
                f"env_bucket: {env_bucket or ''}\n"
                f"next_action: {next_action}"
            ),
        )
    ]


async def add_incident(arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Create a new incident + solution + outcome.
    If an incident already exists, callers should use add_solution (and then record_outcome).
    """
    title = arguments.get("title")
    steps = arguments.get("steps")
    env = arguments.get("env")
    worked = arguments.get("worked")
    notes = arguments.get("notes")
    env_bucket_override = arguments.get("env_bucket") or ""

    if arguments.get("incident_id"):
        return [
            TextContent(
                type="text",
                text="Error: add_incident no longer supports incident_id. Use add_solution for existing incidents.",
            )
        ]

    if not title:
        return [TextContent(type="text", text="Error: title is required")]
    if not steps:
        return [TextContent(type="text", text="Error: steps is required")]
    if not isinstance(env, dict):
        return [TextContent(type="text", text="Error: env is required and must be an object")]
    if worked is None:
        return [TextContent(type="text", text="Error: worked is required")]

    embeddings_info = ""

    # Duplicate guard: block creating a near-identical incident
    try:
        model = get_embedding_model()
        dedupe_text = "\n".join(
            [
                title or "",
                arguments.get("error_signature") or "",
                arguments.get("summary") or "",
            ]
        ).strip()
        if dedupe_text:
            dedupe_embedding = model.encode(dedupe_text).tolist()
            dedupe_resp = await _post_json(
                "/search",
                {
                    "embedding": dedupe_embedding,
                    "limit": 1,
                    "threshold": 0.9,
                },
            )
            if dedupe_resp.status_code == 200:
                maybe = (dedupe_resp.json().get("results") or [])
                if maybe:
                    top = maybe[0]
                    inc = top.get("incident", {}) or {}
                    sim = float(top.get("similarity", 0) or 0)
                    # Defensive: only block on very high similarity
                    if sim >= 0.9 and inc.get("id"):
                        next_action = _format_next_action(
                            "USE_ADD_SOLUTION_FOR_EXISTING_INCIDENT",
                            "An incident already exists. Use add_solution with this incident_id, then record_outcome after you try it.",
                        )
                        return [
                            TextContent(
                                type="text",
                                text=(
                                    "⚠️ Incident appears to already exist (high similarity).\n"
                                    f"existing_incident_id: {inc.get('id')}\n"
                                    f"existing_title: {inc.get('title','')}\n"
                                    f"similarity: {sim:.2f}\n"
                                    f"next_action: {next_action}"
                                ),
                            )
                        ]
    except Exception:
        pass

    # Create incident
    payload = {
        "title": title,
        "summary": arguments.get("summary"),
        "error_signature": arguments.get("error_signature"),
        "tags": arguments.get("tags"),
    }

    resp = await _post_json("/incidents", payload)
    if resp.status_code != 201:
        msg = resp.json().get("error", f"status {resp.status_code}")
        return [TextContent(type="text", text=f"❌ Failed to add incident: {msg}")]

    incident = resp.json().get("incident", {})
    incident_id = incident.get("id", "unknown")

    embeddings_info = await upload_embeddings(
        incident_id,
        {
            "title": title,
            "summary": arguments.get("summary", ""),
            "error_signature": arguments.get("error_signature", ""),
        },
    )

    # Canonicalize env bucket (used for outcomes + ranking stats)
    env_bucket = await _get_env_bucket(env, fallback=env_bucket_override)

    # Create solution
    sol_payload = {
        "incident_id": incident_id,
        "steps": steps,
        "env": env,
        "env_bucket": env_bucket or None,
    }
    sol_resp = await _post_json("/solutions", sol_payload)
    if sol_resp.status_code != 201:
        msg = sol_resp.json().get("error", f"status {sol_resp.status_code}")
        return [TextContent(type="text", text=f"❌ Failed to add solution: {msg}")]

    sol = sol_resp.json().get("solution", {}) or {}
    solution_id = sol.get("id", "unknown")

    # Create outcome for this env
    outcome_payload: Dict[str, Any] = {
        "solution_id": solution_id,
        "worked": worked,
        "notes": notes,
        "env_bucket": env_bucket or None,
        "env_raw": env,
        **_extract_outcome_env_fields(env),
    }
    out_resp = await _post_json("/outcomes", outcome_payload)
    if out_resp.status_code != 201:
        msg = out_resp.json().get("error", f"status {out_resp.status_code}")
        return [TextContent(type="text", text=f"❌ Failed to record outcome: {msg}")]

    next_action = (
        _format_next_action(
            "DONE_OR_ADD_ENV_VARIANT",
            "Done. If this fix works in another environment, add_solution to the same incident and then record_outcome.",
        )
        if worked
        else _format_next_action(
            "DEBUG_FURTHER_THEN_ADD_SOLUTION_OR_INCIDENT",
            "Debug further. If you find a new fix for the same problem, call add_solution (then record_outcome). If the root cause is different, call add_incident to create a new incident.",
        )
    )

    header = "✅ Incident created + solution + outcome"
    return [
        TextContent(
            type="text",
            text=(
                f"{header}\n"
                f"incident_id: {incident_id}\n"
                f"solution_id: {solution_id}\n"
                f"worked: {worked}\n"
                f"env_bucket: {env_bucket or ''}\n"
                f"{embeddings_info}\n"
                f"next_action: {next_action}"
            ),
        )
    ]


async def record_outcome(arguments: Dict[str, Any]) -> List[TextContent]:
    """Record whether a solution worked or failed."""
    solution_id = arguments.get("solution_id")
    worked = arguments.get("worked")
    env = arguments.get("env")
    env_bucket_override = arguments.get("env_bucket") or ""
    notes = arguments.get("notes")

    if solution_id is None or worked is None or not isinstance(env, dict):
        return [
            TextContent(
                type="text",
                text="Error: solution_id and worked are required",
            )
        ]

    env_bucket = await _get_env_bucket(env, fallback=env_bucket_override)

    payload: Dict[str, Any] = {
        "solution_id": solution_id,
        "worked": worked,
        "notes": notes,
        "env_bucket": env_bucket or None,
        "env_raw": env,
        **_extract_outcome_env_fields(env),
    }

    resp = await _post_json("/outcomes", payload)
    if resp.status_code != 201:
        msg = resp.json().get("error", f"status {resp.status_code}")
        return [TextContent(type="text", text=f"❌ Failed to record outcome: {msg}")]

    next_action = (
        _format_next_action(
            "DONE_OR_ADD_ENV_VARIANT",
            "Done. If this fix works in another environment, add_solution to the same incident and then record_outcome.",
        )
        if worked
        else _format_next_action(
            "DEBUG_FURTHER_THEN_ADD_SOLUTION_OR_INCIDENT",
            "Debug further. If you find a new fix for the same incident, call add_solution (then record_outcome). If the root cause is different, call add_incident to create a new incident.",
        )
    )

    outcome = resp.json().get("outcome", {})
    return [
        TextContent(
            type="text",
            text=(
                "✅ Outcome recorded\n"
                f"solution_id: {solution_id}\n"
                f"worked: {worked}\n"
                f"notes: {notes or ''}\n"
                f"next_action: {next_action}"
            ),
        )
    ]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def run() -> None:
    """Console entrypoint for running as an installable CLI."""
    import asyncio

    asyncio.run(main())


if __name__ == "__main__":
    run()

