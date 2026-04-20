---
name: rlm-research-analyzer
description: "Use this skill whenever the user wants to synthesize, review, or analyze papers in a Zotero collection — even if they don't say 'literature review'. Trigger on phrases like: 'review the papers in my X collection', 'analyze my Zotero collection on X', 'do a lit review on X', 'summarize the research on X from Zotero', 'what does the literature say about X', or any request to make sense of a body of papers. Runs a 6-stage pipeline: indexes the collection, derives research questions with user approval, delegates parallel Haiku workers for full-text extraction, aggregates into a cross-paper synthesis with themes/agreements/contradictions, runs two adversarial review passes, and delivers Markdown + PDF + Zotero notes per paper."
---

# RLM Research Analyzer

## Prerequisites

Before invoking this skill, ensure the following are in place:

| Requirement | Role | Required? |
|-------------|------|-----------|
| **zotero-mcp** MCP server | Provides all `zotero_*` tools (collection listing, metadata, full-text retrieval) | **Required** |
| **Zotero desktop app** running locally | zotero-mcp reads the local SQLite database | **Required** |
| **GEMINI_API_KEY** env var (or OpenAI equivalent) | Powers semantic search filtering when a focus question is provided | Optional — focus-question filtering is skipped if unavailable |
| **Python packages: `weasyprint`, `markdown`** | PDF generation in Stage 6 | Optional — Stage 6 skips PDF gracefully if absent; install with `pip install weasyprint markdown` |

If zotero-mcp is not configured, stop immediately and print:
```
RLM Research Analyzer requires the zotero-mcp MCP server.
See: https://github.com/ussoftwareassociation/zotero-mcp
```

## Arguments

`$ARGUMENTS` format: `"Collection Name"` or `"Collection Name" focus question`

To include a focus question, the collection name MUST be quoted.

Parse `$ARGUMENTS` as follows:
- **Collection name:** the first double-quoted string in `$ARGUMENTS`. If no quotes are present, treat the entire `$ARGUMENTS` string as the collection name (no focus question).
- **Focus question:** everything after the closing quote of the collection name (trimmed). If absent, leave empty.
- **`<collection-slug>`:** collection name lowercased, spaces replaced by hyphens, all characters that are not letters, digits, or hyphens removed. Example: `"Neuro Papers (2024)"` → `neuro-papers-2024`.
- **`<working_dir>`:** `<project_root>/rlm-runs/<collection-slug>/` where `<project_root>` is the absolute path of the current working directory at the time the skill is invoked (i.e. the directory Claude Code was opened in). Use the Bash tool to resolve it: `pwd`. Example: if `pwd` returns `/home/user/myproject`, then `<working_dir>` is `/home/user/myproject/rlm-runs/my-collection/`.

## Stage 1 — Initialize

1. Call `zotero_get_collections` to list all collections in the library.
2. Find the collection whose name matches `<collection name>` (case-insensitive). If no match is found, print:
   ```
   Collection "<name>" not found. Available collections:
   - <list all collection names>
   ```
   Then stop.
3. Call `zotero_get_collection_items` with the matched collection key. Retrieve metadata only: title, abstract, authors, year, tags, item key. Do NOT fetch full text at this stage.
4. If a focus question is provided:
   - Call `zotero_semantic_search` with the focus question.
   - If the tool raises any error (e.g., API key not configured, network failure): skip filtering entirely, proceed with the full working item set, and add a note to the index: "Semantic filter unavailable — using full collection."
   - If results are returned: restrict the working item set to keys that appear in BOTH the step-3 collection result AND the semantic search result. Note any collection items excluded by this filter and the reason ("not matched by semantic filter").
   - If no results overlap with the collection: proceed with the full collection and add a note: "Semantic filter returned no matches within this collection — using full collection."
5. Count the working item set. If count > 50 AND no focus question was provided, ask the user:
   > "This collection has N items. Synthesize all, or provide a focus question to filter first?"
   Wait for their response before continuing.
6. Create the run directory:
   ```bash
   mkdir -p <working_dir>
   ```
7. Write `<working_dir>/rlm_index_<collection-slug>.md` with this structure:
   ```markdown
   # Index: <Collection Name>
   Generated: <today's date>
   Focus question: <focus question or "none">
   Total items: N

   ## Items

   ### 1. <Title> (<Authors>, <Year>)
   **Key:** ABC123
   **Tags:** tag1, tag2
   **Abstract:** <abstract text>

   ### 2. <Title> (<Authors>, <Year>)
   **Key:** DEF456
   **Tags:** tag3
   **Abstract:** <abstract text>

   ## Excluded Items
   | Key | Title | Reason |
   |-----|-------|--------|
   ```

   If no items were excluded from the working set, write `None.` under the `## Excluded Items` heading instead of the empty table.

   `Total items` must be the full collection count from step 3 (`zotero_get_collection_items`), before any exclusions from semantic filtering or manual removal. Items excluded from the working set are logged in the `## Excluded Items` table but still counted in `Total items`.

## Stage 2 — Plan

1. Read `<working_dir>/rlm_index_<collection-slug>.md`.
2. Derive the research scope and present it to the user. Wait for approval before continuing.

   Present exactly this structure (fill in the values):
   ```
   ## Research Scope

   **Collection:** <name>
   **Focus question:** <question or "open synthesis">
   **Items to process:** N

   **Key research questions:**
   1. <question derived from focus question or inferred from collection title/abstracts>
   2. <question>
   (2–5 questions total)
   
   Research questions must be: (a) answerable from the paper content, not rhetorical; (b) specific enough to produce a clear 'answered/unresolved' verdict; (c) aligned with the focus question if provided.

   **Anticipated output sections:**
   - Themes likely to emerge: <list based on abstracts>
   - Source categories present: <empirical / review / theoretical / mixed methods>

   **Items included:** N
   **Items excluded:** N (reason: <semantic filter / manual>)

   **Verification checklist (to be completed before delivery):**
   - [ ] All items processed or skipped with reason logged
   - [ ] Every major claim traceable to at least one named paper
   - [ ] No single-source dependencies for key conclusions
   - [ ] Research question status accounted for

   Proceed with this scope? (yes / adjust)
   ```

3. If the user requests changes: apply their changes to the scope. Mutable fields are: research questions (add/remove/reword), items to include/exclude, and anticipated sections. Re-present the updated scope. Repeat until approved, up to 3 rounds (to avoid infinite loops). After 3 rounds without approval, ask: "Should I proceed with the current scope, or stop?"
4. Once approved: group the included items into batches of ~5 items each. Number batches from 1. If the last batch would contain only 1 item, merge it into the previous batch instead.
5. Write `<working_dir>/rlm_plan_<collection-slug>.md`:
   ```markdown
   # Plan: <Collection Name>
   Approved: <date>

   ## Research Scope
   **Collection:** <name>
   **Focus question:** <question or "open synthesis">
   **Items to process:** N
   **Items included:** N
   **Items excluded:** N (reason: <semantic filter / manual / none>)

   **Anticipated output sections:**
   - Themes likely to emerge: <list based on abstracts>
   - Source categories present: <empirical / review / theoretical / mixed methods>

   **Verification checklist:**
   - [ ] All items processed or skipped with reason logged
   - [ ] Every major claim traceable to at least one named paper
   - [ ] No single-source dependencies for key conclusions
   - [ ] Research question status accounted for

   ## Research Questions
   1. <question> — status: pending
   2. <question> — status: pending

   ## Batches

   ### Batch 1

   #### Item 1
   **Key:** ABC123
   **Title:** Title here
   **Authors:** Smith et al.
   **Year:** 2023
   **Abstract:** Full abstract text here.

   #### Item 2
   **Key:** DEF456
   **Title:** Title here
   **Authors:** Jones et al.
   **Year:** 2024
   **Abstract:** Full abstract text here.

   ### Batch 2
   ...

   ## Warnings
   (populated during Stage 3 if any worker fails)
   ```

## Stage 3 — Delegate

Before spawning workers, pre-compute one canonical short label per research question (≤8 words each). Use these exact labels in every worker prompt's Research question status lines. Example: if the question is 'What machine learning methods were used for early detection of Alzheimer's disease?', the label might be 'ML methods for Alzheimer's early detection'. Before spawning any workers, persist the labels into the plan file: for each research question line in `## Research Questions`, append ` — label: <computed label>` so the line reads `1. <question> — status: pending — label: <computed label>`. Stage 4 reads these labels from the plan file.

Read `references/worker-prompt.md` from this skill's base directory. Use its content as the worker prompt template. Replace ALL placeholders with actual values (working_dir, batch number N, research questions and their labels, and all item fields sourced from the plan file) before spawning.

Spawn one `Agent` subagent per batch **in parallel** (all batches at once, in a single message with multiple Agent tool calls). Set each worker's `description` to `"Batch N — process papers"` and `model` to `"haiku"`.

After all subagents return:
- If a subagent's return value does not contain the text `Batch <N> complete` (where N is the batch number), treat it as failed. Open the plan file and append under `## Warnings`:
  ```
  - Batch <N> failed or returned empty. Items skipped: <list titles>.
  ```
- Continue regardless. Skipped batches will be noted in the final answer.

## Stage 4 — Aggregate

0. Read the plan file to retrieve: (a) the authoritative list of research questions and their canonical labels; (b) any warnings logged during Stage 3. Count the batches listed in the plan file. Verify that `<working_dir>/slice_*.md` files exist for each batch number. If any batch number is missing, treat it as failed and append a warning: `Batch <N> — no slice file found.` For each existing slice file, verify it contains at least one `###` heading. If a file is empty or has no `###` headings, treat it as failed: append a warning (`Batch <N> — slice file exists but is empty`) and exclude it from aggregation.
1. Read all `<working_dir>/slice_*.md` files.
2. Consolidate research question status across all slices using these rules:
   - **Answered:** ≥2 papers marked the question "answered".
   - **Partially answered:** exactly 1 paper marked it "answered", or ≥1 marked it "partially answered".
   - **Unresolved:** ≥1 paper explicitly marked the question "unresolved", and no paper marked it "answered" or "partially answered". Note "open problem" in the summary.
   - **Not addressed:** no paper's Research question status lines mentioned this question at all. Treat the same as Unresolved but note "no coverage" in the summary.
   - **Superseded:** any paper marked it "superseded" — note the paper title and year.
   Apply rules in priority order: Superseded > Answered > Partially answered > Unresolved > Not addressed.
   If ≥1 paper marked it "answered" and ≥1 marked it "partially answered", the stronger verdict prevails: treat as Answered, unless the only answered source is marked [abstract only], in which case treat as Partially Answered.
   **Label matching:** match each slice's Research question status lines against the canonical labels from the plan file using exact string match first. If no exact match is found for a line, attempt a fuzzy match (the label from the plan file is a substring of the slice line, or vice versa). If a fuzzy match succeeds, use that verdict. If no match at all is found, treat as "not addressed" for that question and append a warning: `Label mismatch in slice_<N>.md — could not match: "<unmatched label text>".`
3. Write `<working_dir>/rlm_answer_<collection-slug>.md` with this exact structure:

   ```markdown
   # Synthesis: <Collection Name>
   Focus question: <question or "open synthesis">
   Date: <today's date>

   ## Per-Paper Summaries

   [All per-paper summaries from all slice files, sorted by first author surname, then year. Preserve the exact format from the workers: ### heading, Key findings, Methods, Conclusions, Coverage. Omit the Research question status lines — those are consolidated below.]

   ## Cross-Paper Synthesis

   ### Themes
   [3–7 themes, each supported by ≥2 papers. For each: 1–2 sentences and the papers supporting it, e.g. "(Smith 2023, Jones 2022)". If fewer than 3 themes meet the ≥2-paper threshold, note "Insufficient cross-paper convergence for N theme(s)" rather than including single-paper themes.]

   ### Agreements
   [Findings where ≥2 papers converge. Cite the papers by author and year.]

   ### Contradictions
   [Findings where papers studied comparable phenomena under similar conditions and reached opposing conclusions. Name the papers and the nature of the disagreement. Do not list differences explained by different populations, methods, or time frames — place those in Gaps & Open Questions instead. If no genuine contradictions are identified, write: "No genuine contradictions were identified. Apparent discrepancies are attributable to differences in [populations / methods / time frames / geographies] and are noted in Gaps & Open Questions."]

   ### Gaps & Open Questions
   [Topics not addressed by any paper. Non-critical reviewer issues from Stage 5 will be appended here.]

   ## Research Questions Status

   ### Answered
   - **<Q label>:** <summary of answer across papers> (Sources: Author Year, Author Year)

   ### Partially Answered
   - **<Q label>:** <what was found and what remains unclear> (Source: Author Year only)

   ### Unresolved
   - **<Q label>:** <why it remains unresolved>

   ### Superseded
   - **<Q label>:** <what was superseded and by what finding> (Source: Author Year)
   ```

   Omit any Research Questions Status subsection that has no questions assigned to it.

If any batches were skipped (i.e., `## Warnings` in the plan file contains a line matching "failed or returned empty" or "no slice file found"), insert the following block immediately before the `## Cross-Paper Synthesis` heading in the answer file:
```
> **Skipped items:** <list titles of skipped items from plan file warnings>
```
If no batches were skipped, do not add this block.

## Stage 5 — Verify

1. Read `references/reviewer-prompt.md` from this skill's base directory. Substitute `<working_dir>`, `<collection-slug>`, and `<Collection Name>` with actual values. Spawn one `Agent` subagent using the substituted prompt. Set `description` to `"Review synthesis pass 1"` and `model` to `"sonnet"`.

2. After the reviewer returns, read `<working_dir>/rlm_review_<collection-slug>.md`. If the reviewer's return value does not match the pattern `Review complete: N fatal, N major, N minor.`, treat as 0 issues found, log a warning to the plan file under `## Warnings`, and continue to Stage 6.
3. For each **FATAL or MAJOR issue**: edit the answer file to fix it using the inline annotation in Part 2 of the review to locate the exact passage:
   - Unsupported statement: add a citation or soften the claim to a hypothesis.
   - Single-source dependency: note "(single source)" after the citation, or move the claim to Gaps & Open Questions.
   - Logical break: correct the reasoning or remove the unsupported conclusion.
   - Obsolete claim: move to Gaps & Open Questions.
   - Overstated conclusion: replace with language that accurately reflects what the cited papers demonstrated.
   - Vague praise: add a specific metric, finding, or citation, or remove the claim.
   - If an issue has no corresponding inline annotation in Part 2, locate the passage directly using the first 25 words from the Claim column via Read and search.
4. For each **MINOR issue**: append a bullet to the "Gaps & Open Questions" section of the answer file:
   ```
   - [Reviewer note] <description of the minor issue>
   ```
5. If any FATAL or MAJOR issues were fixed: read the review file's `## Summary` block and append the pass-1 tallies to `## Warnings` in the plan file:
   ```
   - Pass 1 review: N fatal, N major, N minor (all fixed before pass 2)
   ```
   Spawn the reviewer subagent once more with the same already-substituted prompt (set `description` to `"Review synthesis pass 2"`, `model` to `"sonnet"`). The reviewer will overwrite the existing review file. If it returns 0 fatal and 0 major issues, continue to Stage 6. If FATAL or MAJOR issues remain after the second pass, append them as bullets to "Gaps & Open Questions" with the prefix `[Unresolved reviewer issue]` and continue to Stage 6 — do not loop again.

## Stage 6 — Deliver

1. Count the final tallies by reading the previously written files:
   - **Total in collection:** from the "Total items: N" line in the index file
   - **Reviewed (full text):** count `###` headings in all `slice_*.md` files whose heading line does NOT contain `[abstract only]` and does NOT contain `[skipped`
   - **Reviewed (abstract only):** count `###` headings in all `slice_*.md` files whose heading line DOES contain `[abstract only]`
   - **Skipped (no content):** count `###` headings in all `slice_*.md` files whose heading line contains `[skipped`
   - **Excluded:** count of rows in the "## Excluded Items" table in the index file
   - **Reviewer pass 1 — fatal/major:** Look for a line matching `- Pass 1 review: N fatal, N major, N minor` in `## Warnings` of the plan file. Extract those counts.
   - **Reviewer pass 2 — fatal/major:** Sum "Fatal issues found: N" and "Major issues found: N" from the `## Summary` block of the final review file. If the file does not exist or its Summary block is absent, record 'N/A'.
   - If no pass-1 warning line exists (only one reviewer pass ran), treat pass 1 and pass 2 as the same run and record counts once under pass 1; leave pass 2 as "not run".

2. Post-process the answer file to add a Table of Contents and a Sources section:

   **a. Fetch full metadata for each working-set item.**
   Read item keys from the Batches section of the plan file. For each key, call `zotero_get_item_metadata` to retrieve: journal/publication name, volume, issue, pages, DOI, URL. These calls are independent and can be made in parallel. If a key's metadata call fails, use the fields already available from the plan file (title, authors, year) and omit missing fields.

   **b. Build the sorted reference list.**
   Sort all working-set items alphabetically by first author surname, then by year for ties. Format each entry as:
   ```
   Surname, F.I.; Surname2, F.I.; Surname3, F.I.; et al. (Year). Title. *Journal Name*, Volume(Issue), Pages. [DOI: xxxxx](https://doi.org/xxxxx)
   ```
   Rules:
   - List up to three authors by surname + initials separated by `;`. If more than three authors, write the first three followed by `et al.`
   - Italicize journal name with `*...*`
   - If DOI is available, format as a markdown hyperlink `[DOI: xxxxx](https://doi.org/xxxxx)`
   - If DOI is unavailable but a URL is present, use `[Link](url)` instead
   - If neither DOI nor URL is available, omit the link entirely
   - Omit volume/issue/pages if not available

   **c. Generate a Table of Contents.**
   Scan the answer file for headings. Include all `## ` headings. For `### ` headings, include only those within `## Cross-Paper Synthesis` and `## Research Questions Status` — skip all `### ` headings inside `## Per-Paper Summaries`. Build the ToC in this format:
   ```markdown
   ## Table of Contents
   - [Section Name](#anchor)
     - [Subsection Name](#anchor)
   ```
   Anchors follow GitHub-flavored Markdown: heading text lowercased, spaces replaced by hyphens, all characters that are not letters, digits, or hyphens removed.

   **d. Update the answer file.**
   1. Insert the Table of Contents block immediately after the `Date:` line (the third line of the file).
   2. Append the Sources section to the end of the file:
      ```markdown
      ---

      ## Sources

      Surname, F.I.; ... (Year). Title. *Journal*. [DOI: xxx](url)
      (one entry per working-set item, alphabetical order)
      ```
   3. Write the updated file.

3. Generate a PDF version of the answer file. Locate the skill's base directory from the "Base directory for this skill:" line in your system context. Then run:
   ```bash
   python "<skill_base_dir>/scripts/make_pdf.py" \
     --collection "<Collection Name>" \
     --date "<today's date>" \
     --input "<working_dir>/rlm_answer_<collection-slug>.md" \
     --output "<working_dir>/rlm_answer_<collection-slug>.pdf"
   ```
   If the script exits successfully, note the PDF path in the delivery output.
   If it fails (e.g., `weasyprint` not installed), print:
   ```
   [Warning] PDF generation skipped — weasyprint not available. Install with: pip install weasyprint markdown
   ```
   and continue to step 4.

4. Write `<working_dir>/rlm_provenance_<collection-slug>.md`:
   ```markdown
   # Provenance: <Collection Name>
   Completed: <today's date>

   ## Scope
   - Focus question: <focus question or "open synthesis">
   - Items in working set: N (of N total in collection)
   - Batches processed: N

   ## Sources
   - Total in collection: N
   - Reviewed (full text): N
   - Reviewed (abstract only): N
   - Skipped (no content): N
   - Excluded: N

   ## Excluded Items
   | Title | Reason |
   |-------|--------|
   | <title> | <reason> |

   ## Verification
   - Reviewer pass 1: N fatal, N major (all fixed before pass 2)
   - Reviewer pass 2: N fatal, N major (fixed before delivery / "not run" if only one pass)
   - Remaining minor issues: <if any minor issues were recorded: "N — see Gaps & Open Questions in answer file"; otherwise: "None">

   ## Research Files Consulted
   - rlm_index_<collection-slug>.md
   - rlm_plan_<collection-slug>.md
   - (list each slice_*.md file that actually exists in `<working_dir>`, one per line)
   - rlm_review_<collection-slug>.md

   ## Outputs
   - rlm_answer_<collection-slug>.md
   - rlm_answer_<collection-slug>.pdf  (or "not generated — weasyprint unavailable")
   ```

   If the Excluded Items table in the index has no data rows, write `None.` under the `## Excluded Items` heading instead of a table.

5. Create Zotero notes for each processed item:
   - Read the Batches section of the plan file to collect all `(key, title)` pairs in order.
   - Read all `slice_*.md` files into memory.
   - For each `(key, title)` pair:
     a. Search the slice files for a `###` heading whose text contains the first 40 characters of the title (case-insensitive). Take the first match.
     b. If found, extract the full summary block: from that `###` heading line up to (but not including) the next `###` heading or end of file.
     c. Skip items whose heading contains `[skipped — no content available]` — do not create a note for them.
     d. Format the note as:
        ```
        ## RLM Summary — <Collection Name>
        *Generated: <today's date>*

        <full extracted summary block>
        ```
     e. Call `zotero_create_note` with `item_key=<key>` and the formatted note content. If the call fails, log the failure but continue to the next item.
   - After all items are processed, report: "Zotero notes: N created, M failed." If M > 0, list the failed item keys.
   - If `zotero_create_note` is not available (tool not found), skip this step silently and add: "[Zotero notes skipped — zotero_create_note unavailable]".

6. Print a delivery summary — do NOT print the full answer file, as it can be very large:
   ```
   Synthesis complete for "<Collection Name>"
   - Items: N reviewed (N full text, N abstract only, N skipped), N excluded
   - Themes: <list theme titles>
   - Research questions: <one line per question — label: verdict>
   - Reviewer: pass 1 (N fatal, N major fixed), pass 2 (N fatal, N major)
   ```

7. Print:
   ```
   ---
   Answer file:    <working_dir>/rlm_answer_<collection-slug>.md
   PDF:            <working_dir>/rlm_answer_<collection-slug>.pdf  (or "skipped — weasyprint not available")
   Provenance:     <working_dir>/rlm_provenance_<collection-slug>.md
   All run files:  <working_dir>
   ```
