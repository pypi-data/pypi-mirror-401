# MCP Tool Specification

This document defines **each MCP tool**, its purpose, and what it should return
to naturally guide the LLM into the correct next action.

The MCP server enforces workflow through **tool outputs**, not just documentation.

---

## Tool 1: ranked_solutions
Purpose

Search incidents, gather all candidate solutions, and rank them using environment similarity plus reliability and recency from solution_env_stats.

When to use

- Always the first tool for any new debug context

Input

- query_text (string)
- env (object, required) — environment context used for bucket canonicalization and matching
- limit (optional int) — number of solutions to return (default 5)

Returns

- lookup_id (string)
- incidents (array of matches from incident search)
- ranked_solutions (array, sorted by final_score)
  - best_env_bucket_match
  - env_match_score
  - reliability_score
  - recency_boost
  - final_solution_score
- recommended_solution (top-ranked solution)
- next_action (object)

### next_action behavior (all cases)

**Case: no incident matches**

```json
{
  "type": "NO_MATCH_DEBUG_THEN_ADD_INCIDENT",
  "instructions": "No relevant incidents found. Debug normally. If a fix is found, call add_incident to store the incident + solution + outcome."
}
```

**Case: incidents found, but none have solutions**

```json
{
  "type": "NO_SOLUTIONS_ADD_ONE",
  "instructions": "Incidents were found but no solutions exist. Debug normally. Once you find a fix that works, call add_solution for the best matching incident, then record_outcome."
}
```

**Case: solutions ranked successfully**

```json
{
  "type": "TRY_SOLUTION_AND_RECORD_OUTCOME",
  "instructions": "Try the recommended solution. After attempting it, call record_outcome with worked=true or false."
}
```

---

Tool 2: record_outcome
Purpose

Record whether a solution worked or failed.

When to use

Every time a solution is attempted

Input

lookup_id (optional)

solution_id

worked (boolean)

env (object)

env_bucket (optional)

notes (optional)

Returns

ok (boolean)

updated solution stats

next_action (object)

### next_action behavior (all cases)

**Case: worked = true**

```json
{
  "type": "DONE_OR_ADD_ENV_VARIANT",
  "instructions": "Done. If this fix works in another environment, add_solution to the same incident and then record_outcome."
}
```


**Case: worked = false**

```json
{
  "type": "DEBUG_FURTHER_THEN_ADD_SOLUTION_OR_INCIDENT",
  "instructions": "Debug further. If you find a new fix for the same incident, call add_solution (then record_outcome). If the root cause is different, call add_incident to create a new incident."
}
```

Tool 3: add_solution
Purpose

Add a new fix for an existing incident (including env-specific variants). This stores the proposed fix steps; evidence is added later via record_outcome.

When to use

- Same incident, new fix
- Same incident, new environment variant (even if steps are the same)

Input

- incident_id (required)
- steps (required)
- env (required)
- env_bucket (optional)
- lookup_id (optional)

Returns

- solution_id
- env_bucket
- next_action

### next_action behavior (all cases)

**Case: solution created**

```json
{
  "type": "RECORD_OUTCOME_FOR_NEW_SOLUTION",
  "instructions": "If you try this solution, call record_outcome with solution_id, worked, and env."
}
```

Tool 4: add_incident
Purpose

Create a new incident + solution + outcome. If the incident already exists, use add_solution instead.

When to use

- No matching incident exists and you found a fix (create new incident)

Input

title (required)

error_signature

summary

tags (optional)

lookup_id (optional)

steps (required)

env (required)

env_bucket (optional)

worked (required boolean)

notes (optional)

Returns

incident_id

solution_id

outcome_id (if returned by API)

next_action

### next_action behavior (all cases)

**Case: an incident already exists (duplicate guard triggers)**

```json
{
  "type": "USE_ADD_SOLUTION_FOR_EXISTING_INCIDENT",
  "instructions": "An incident already exists. Use add_solution with this incident_id, then record_outcome after you try it."
}
```

**Case: incident + solution + outcome created AND worked = true**

```json
{
  "type": "DONE_OR_ADD_ENV_VARIANT",
  "instructions": "Done. If this fix works in another environment, add_solution to the same incident and then record_outcome."
}
```

**Case: incident + solution + outcome created AND worked = false**

```json
{
  "type": "DEBUG_FURTHER_THEN_ADD_SOLUTION_OR_INCIDENT",
  "instructions": "Debug further. If you find a new fix for the same incident, call add_solution (then record_outcome). If the root cause is different, call add_incident to create a new incident."
}
```

---

Design Principles

Tools represent intent, not database operations

Tool outputs always suggest the next step

LLMs are guided, not trusted blindly

Evidence (outcomes) drives confidence

Summary

ranked_solutions → pick best solution

record_outcome → learn from evidence

add_solution → store a new proposed fix under an existing incident

add_incident → learn a new incident (creates incident + solution + outcome)

This keeps debug memory accurate and useful over time.