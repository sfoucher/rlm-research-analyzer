---
name: nlm-research-analyzer
description: "Use this skill whenever the user wants to synthesize, review, or analyze papers in a NotebookLM notebook. Trigger on phrases like: 'review my NotebookLM notebook on X', 'analyze the papers in my notebook', 'do a lit review from my NotebookLM', 'summarize the research in my notebook on X', 'query my NotebookLM collection about X'. Do NOT trigger for Zotero collections — use rlm-research-analyzer for those."
---

# NLM Research Analyzer

## Prerequisites

| Requirement | Role | Required? |
|-------------|------|-----------|
| **notebooklm-mcp** MCP server | Provides all `mcp__notebooklm__*` tools | **Required** |
| **NotebookLM notebook** registered in notebooklm-mcp library | Source for synthesis | **Required** |
| **Python packages: `weasyprint`, `markdown`** | PDF generation in Stage 6 | Optional — skipped gracefully if absent |

If notebooklm-mcp tools are unavailable, stop and print:
```
NLM Research Analyzer requires the notebooklm-mcp MCP server.
See: https://github.com/PleasePrompto/notebooklm-mcp
```

## Arguments

Format: `"Notebook Name"` or `"Notebook Name" focus question`

- **Notebook name:** the first double-quoted string. If no quotes, treat the entire argument as the notebook name.
- **Focus question:** everything after the closing quote (trimmed). Empty if absent.
- **`<notebook-slug>`:** notebook name lowercased, spaces → hyphens, non-alphanumeric chars removed. Example: `"Air Pollution India 2024"` → `air-pollution-india-2024`.
- **`<working_dir>`:** `<project_root>/nlm-runs/<notebook-slug>/` where `<project_root>` is resolved via `pwd` at invocation time.
- **`<skill_dir>`:** the base directory shown in the system reminder at invocation: "Base directory for this skill: <path>".

## Stage 1 — Initialize

1. Resolve `<working_dir>`:
   ```bash
   pwd
   ```
   Construct `<working_dir>` as `<pwd result>/nlm-runs/<notebook-slug>/`.

2. Verify authentication:
   - Call `mcp__notebooklm__get_health`.
   - If `authenticated: false`: call `mcp__notebooklm__setup_auth` and wait for it to return `authenticated: true`. If it fails, stop and ask the user to complete authentication.

3. Find the notebook:
   - Call `mcp__notebooklm__list_notebooks`.
   - Find the entry whose `name` matches `<Notebook Name>` (case-insensitive).
   - If no exact match: call `mcp__notebooklm__search_notebooks` with `<Notebook Name>` as the query.
   - If still no match, print:
     ```
     Notebook "<name>" not found in the notebooklm-mcp library.
     Registered notebooks:
     - <list all names from list_notebooks>

     To register it: share the notebook URL from notebooklm.google.com and use add_notebook.
     ```
     Then stop.
   - Record matched notebook's `id` as `<notebook_id>` and `url` as `<notebook_url>`.

4. Activate the notebook:
   - Call `mcp__notebooklm__select_notebook` with `id: <notebook_id>`.

5. Enumerate sources (best-effort):
   - Call `mcp__notebooklm__ask_question` with:
     - `notebook_id: <notebook_id>`
     - `question: "Please list all papers and sources in this notebook. For each one provide: title, authors, year (if available), and a 2–3 sentence summary of its main contribution."`
   - Save the response as `<source_list>`.
   - If the response is empty or under 100 characters: set `<source_list>` to `"Source enumeration unavailable — index will be minimal."` and add a note to the index.
   - Save the returned `session_id` (if any) as `<enum_session_id>` for possible reuse in Stage 2.

6. Apply focus question filter (if provided):
   - Call `mcp__notebooklm__ask_question` with:
     - `notebook_id: <notebook_id>`
     - `question: "Which papers or sources in this notebook are most relevant to: <focus question>? List their titles and briefly explain why each is relevant."`
   - Save the response as `<focus_filter>`.
   - If no focus question: set `<focus_filter>` to `"N/A"`.

7. Create the run directory:
   ```bash
   mkdir -p <working_dir>
   ```

8. Write `<working_dir>/nlm_index_<notebook-slug>.md`:
   ```markdown
   # Index: <Notebook Name>
   Generated: <today's date>
   Notebook ID: <notebook_id>
   Notebook URL: <notebook_url>
   Focus question: <focus question or "none">

   ## Sources (as reported by notebook)

   <source_list>

   ## Focus Filter Results

   <focus_filter>
   ```

## Stage 2 — Plan

1. Read `<working_dir>/nlm_index_<notebook-slug>.md`.

2. Derive the research scope and present it to the user. Wait for approval before continuing.

   Present exactly this structure:
   ```
   ## Research Scope

   **Notebook:** <name>
   **Focus question:** <question or "open synthesis">

   **Key research questions:**
   1. <specific, answerable question derived from focus question or inferred from source list>
   2. <question>
   (2–5 questions total)

   Research questions must be: (a) answerable from notebook content; (b) specific enough to yield a clear answered/unresolved verdict; (c) aligned with the focus question if provided.

   **Anticipated output sections:**
   - Themes likely to emerge: <list based on source summaries>
   - Source categories present: <empirical / review / theoretical / mixed>

   **Note:** Source index is best-effort — NotebookLM may not have enumerated all sources completely.

   **Verification checklist (to be completed before delivery):**
   - [ ] All research questions answered or marked unresolved with reason
   - [ ] Every major claim traceable to a cited source
   - [ ] No single-source dependencies for key conclusions

   Proceed with this scope? (yes / adjust)
   ```

3. If the user requests changes: apply them and re-present the updated scope. Repeat up to 3 rounds. After 3 rounds without approval, ask: "Proceed with the current scope, or stop?"

4. Once approved: assign one batch number per research question (Batch 1 = Question 1, Batch 2 = Question 2, etc.). Compute a canonical short label (≤8 words) per question.

5. Write `<working_dir>/nlm_plan_<notebook-slug>.md`:
   ```markdown
   # Plan: <Notebook Name>
   Approved: <date>
   Notebook ID: <notebook_id>

   ## Research Questions
   1. <question> — status: pending — label: <label>
   2. <question> — status: pending — label: <label>

   ## Batches

   ### Batch 1
   **Research question:** <question 1>
   **Label:** <label 1>

   ### Batch 2
   **Research question:** <question 2>
   **Label:** <label 2>

   (one batch section per question)

   ## Warnings
   ```

## Stage 3 — Delegate

Read `<working_dir>/nlm_plan_<notebook-slug>.md` to retrieve: research questions, canonical labels, `<notebook_id>`, and any existing warnings.

Read the worker prompt template from `<skill_dir>/references/worker-prompt.md`. For each batch, fill in all placeholders:
- `<working_dir>` → absolute run directory
- `<N>` → batch number
- `<notebook_id>` → from plan file
- `<question>` → the research question text for this batch
- `<label>` → the canonical label for this batch

Spawn one `Agent` subagent per batch **in parallel** (all batches in a single message with multiple Agent tool calls). Set each worker's `description` to `"Question N — <label>"` (substitute actual values) and `model` to `"haiku"`.

After all subagents return:
- If a subagent's return value does not contain the text `"Question <N> complete"`, treat it as failed. Open `<working_dir>/nlm_plan_<notebook-slug>.md` and append under `## Warnings`:
  ```
  - Question <N> failed or returned empty: <question text>
  ```
- Continue regardless. Failed questions will be marked Unresolved in Stage 4.
