# Debug Memory Workflow

This document explains **how debugging decisions are made** in the system:
- when to search
- when to record outcomes
- when to add solutions
- when to create new incidents

This workflow applies to:
- humans using the system
- LLM agents calling MCP tools
- future contributors

---

## Core Idea

Debugging produces **three kinds of information**:

1. **Incident** — what kind of problem this is  
2. **Solution** — how it was fixed in a specific environment  
3. **Outcome** — whether the fix actually worked  

The system only stores new data **when something new is learned**.

---

## Always Start With Search

When a new debugging issue appears:

1. Always search existing incidents first  
2. Never immediately create a new incident  

This prevents duplicate knowledge.

---

## What Happens After Search

### If no relevant incident is found
- Debug normally
- If a fix is discovered:
  - call `add_incident` (without `incident_id`) to create the incident + solution + outcome in one step
- If no fix is found:
  - do nothing

---

### If a relevant incident is found
- Use env-aware ranking: the system canonicalizes the provided env, pulls solution_env_stats for all solutions under the matched incidents, and ranks solutions by env match + reliability + recency
- Selects the solution with the highest final score (env match + reliability + recency)
- Returns the best matching solution as the recommended solution
- Try the solution
- **Always record an outcome**

Recording outcomes is mandatory whenever a solution is attempted.

**Note:** Env-aware ranking relies on solution_env_stats and env bucket canonicalization to prioritize solutions proven in similar environments.

---

## After Trying a Solution: One Question

After attempting a solution, ask:

> **Did I learn something new?**

The answer determines what to store.

---

### Case A — Nothing new learned
- The solution worked
- Same fix, same environment
- Same root cause

**Action:**
- Record outcome only

This is the most common case.

---

### Case B — New fix, same problem
- Existing solution failed
- You found a different fix
- Root cause is the same

**Action:**
- Call `add_solution` to attach the new solution to the existing incident
- Then call `record_outcome` after you try it

---

### Case C — Different root cause
- Issue looked similar but wasn’t
- Different subsystem or failure mode
- You would explain it as a different story

**Action:**
- Call `add_incident` (without `incident_id`) to create a new incident + solution + outcome

---

## How to Tell “Same Incident” vs “New Incident”

### Same incident if:
- Same subsystem/component
- Same failure mode
- Only env, version, or config differs

### New incident if:
- Different subsystem
- Different failure mode
- Different lifecycle phase
- Different root cause explanation

Rule of thumb:
> If you’d explain it differently to a teammate, it’s a new incident.

---

## Non-Negotiable Rules

- Always search first
- Always record outcomes
- Never create incidents casually
- Never skip evidence

Following these keeps the system clean and scalable.
