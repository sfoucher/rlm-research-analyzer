# RLM Research Analyzer

A Claude Code skill that synthesizes a Zotero paper collection into a structured literature review — per-paper summaries, cross-paper themes, contradictions, gaps, and a research questions status table — delivered as Markdown, PDF, and Zotero notes.

## What it does

Given a Zotero collection name (and an optional focus question), the skill:

1. **Indexes** the collection — fetches metadata, runs semantic filtering if a focus question is provided
2. **Plans** — derives research questions, groups papers into batches, waits for your approval
3. **Delegates** — spawns parallel Haiku workers to read full text and produce structured per-paper summaries
4. **Aggregates** — consolidates findings into a synthesis with themes, agreements, contradictions, and gaps
5. **Verifies** — runs two adversarial reviewer passes; fixes all FATAL/MAJOR issues before delivery
6. **Delivers** — writes a final Markdown answer, a styled PDF, a provenance file, and creates a Zotero note on each paper with its summary

## Prerequisites

| Requirement | Role | Required? |
|-------------|------|-----------|
| [Claude Code](https://claude.ai/code) | Runs the skill | **Required** |
| [Zotero](https://www.zotero.org/) desktop app (running locally) | Source library | **Required** |
| [zotero-mcp](https://github.com/ussoftwareassociation/zotero-mcp) MCP server | Provides all `zotero_*` tools | **Required** |
| `GEMINI_API_KEY` env var (or OpenAI equivalent) | Semantic search filtering when a focus question is provided | Optional |
| Python packages: `weasyprint`, `markdown` | PDF generation | Optional |

Install optional PDF dependencies:

```bash
pip install weasyprint markdown
```

## How it works

RLM runs in six sequential stages, each building on the last.

### Stage 1 — Initialize

Claude fetches all item metadata (title, abstract, authors, year) from the Zotero collection via zotero-mcp — no full text at this point. If a focus question was provided, it runs a semantic search and intersects the results with the collection to narrow the working set. The full index is written to `rlm_index_<slug>.md`.

### Stage 2 — Plan

Claude reads the index, infers 2–5 specific research questions from the abstracts, and presents a research scope for your approval. You can adjust the questions, include/exclude items, or tweak the anticipated sections. Once approved, items are grouped into batches of ~5 and the plan is written to `rlm_plan_<slug>.md`.

### Stage 3 — Delegate

One Haiku subagent per batch is spawned **in parallel**. Each worker calls `zotero_get_item_fulltext` for every paper in its batch, falls back to the abstract if full text is unavailable, and writes a structured per-paper summary with:
- Key findings tagged with a confidence level (`high` = read in full text, `medium` = abstract only, `low` = inferred)
- Methods, conclusions, and coverage notes
- A verdict per research question (answered / partially answered / unresolved / superseded)

Results land in `slice_N.md` files.

### Stage 4 — Aggregate

Claude reads all slice files, consolidates research question verdicts across papers using a priority rule (Superseded > Answered > Partially answered > Unresolved), and writes the final synthesis to `rlm_answer_<slug>.md`. The synthesis includes:
- All per-paper summaries sorted by first author surname
- Cross-paper themes (each supported by ≥2 papers)
- Agreements, contradictions, and gaps
- Research questions status table
- A Table of Contents and a formatted reference list

### Stage 5 — Verify

An adversarial reviewer subagent reads the synthesis and checks for six issue types: unsupported statements, single-source dependencies, logical breaks, obsolete claims, overstated conclusions, and vague praise. Issues are graded FATAL / MAJOR / MINOR.

All FATAL and MAJOR issues are fixed inline before a second reviewer pass. Minor issues are appended to Gaps & Open Questions. The review log is saved to `rlm_review_<slug>.md`.

### Stage 6 — Deliver

Claude produces the final deliverables:
- Adds a Table of Contents and a formatted Sources section to the answer file
- Generates a styled PDF via `scripts/make_pdf.py` (requires `weasyprint`)
- Writes `rlm_provenance_<slug>.md` with item counts, reviewer pass tallies, and file inventory
- Creates a Zotero note on each processed paper containing its per-paper summary

## Structure

```
rlm-research-analyzer/
├── .claude-plugin/
│   └── plugin.json                          # Plugin metadata
├── skills/
│   └── rlm-research-analyzer/
│       ├── SKILL.md                         # Skill definition (6 stages)
│       ├── scripts/
│       │   └── make_pdf.py                  # PDF generation helper
│       └── references/
│           ├── worker-prompt.md             # Haiku worker subagent prompt template
│           └── reviewer-prompt.md           # Adversarial reviewer subagent prompt template
├── examples/
│   └── image-to-image-transfer/
│       ├── rlm_answer_image-to-image-transfer.md
│       └── rlm_provenance_image-to-image-transfer.md
├── README.md
└── LICENSE
```

## MCP Configuration

Add the `zotero` server to your Claude Code `settings.json` (typically `~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "zotero": {
      "type": "stdio",
      "command": "/path/to/zotero-mcp",
      "args": [],
      "env": {
        "ZOTERO_LOCAL": "true"
      }
    }
  }
}
```

**With Gemini semantic search** (enables focus-question filtering):

```json
{
  "mcpServers": {
    "zotero": {
      "type": "stdio",
      "command": "/path/to/zotero-mcp",
      "args": [],
      "env": {
        "ZOTERO_LOCAL": "true",
        "ZOTERO_EMBEDDING_MODEL": "gemini",
        "GEMINI_API_KEY": "your-gemini-api-key",
        "GEMINI_EMBEDDING_MODEL": "gemini-embedding-001"
      }
    }
  }
}
```

**With OpenAI semantic search:**

```json
{
  "mcpServers": {
    "zotero": {
      "type": "stdio",
      "command": "/path/to/zotero-mcp",
      "args": [],
      "env": {
        "ZOTERO_LOCAL": "true",
        "ZOTERO_EMBEDDING_MODEL": "openai",
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    }
  }
}
```

Replace `/path/to/zotero-mcp` with the actual binary path after installing via `pip install zotero-mcp` or from the [zotero-mcp releases](https://github.com/ussoftwareassociation/zotero-mcp/releases). On Windows the binary is typically at `%USERPROFILE%\.local\bin\zotero-mcp.exe`. On macOS/Linux: `~/.local/bin/zotero-mcp`.

Zotero desktop must be running when Claude Code is active — zotero-mcp reads the local SQLite database directly.

## Installation

In Claude Code, run these two commands:

```
/plugin marketplace add https://github.com/sfoucher/rlm-research-analyzer
```
```
/plugin install rlm-research-analyzer@rlm-research-analyzer
```

Then activate:

```
/reload-plugins
```

## Usage

In Claude Code, invoke the skill with:

```
/rlm-research-analyzer "Collection Name"
```

Or with a focus question:

```
/rlm-research-analyzer "Collection Name" what methods are used for domain adaptation in remote sensing?
```

The collection name must be quoted when a focus question follows it. Without quotes and no focus question, the entire argument is treated as the collection name.

## Output files

All outputs are written to `<project_root>/rlm-runs/<collection-slug>/`:

| File | Description |
|------|-------------|
| `rlm_index_<slug>.md` | Indexed items with abstracts |
| `rlm_plan_<slug>.md` | Research questions, batches, research scope |
| `slice_N.md` | Per-batch worker outputs (intermediate) |
| `rlm_review_<slug>.md` | Reviewer pass output (intermediate) |
| `rlm_answer_<slug>.md` | Final synthesis |
| `rlm_answer_<slug>.pdf` | Styled PDF (requires weasyprint) |
| `rlm_provenance_<slug>.md` | Run metadata: item counts, reviewer passes, files consulted |

In addition, a Zotero note is created on each processed paper with its per-paper summary.

## PDF generation

The `skills/rlm-research-analyzer/scripts/make_pdf.py` script converts the final Markdown answer to a styled PDF:

```bash
python skills/rlm-research-analyzer/scripts/make_pdf.py \
  --collection "Image-to-Image Transfer" \
  --date "2026-04-20" \
  --input rlm-runs/image-to-image-transfer/rlm_answer_image-to-image-transfer.md \
  --output rlm-runs/image-to-image-transfer/rlm_answer_image-to-image-transfer.pdf
```

The skill invokes this automatically in Stage 6 if `weasyprint` and `markdown` are installed.

## Example output

See [`examples/image-to-image-transfer/`](examples/image-to-image-transfer/) for a complete run on a 13-paper collection about image-to-image transfer in remote sensing (SAR-to-optical, domain adaptation, super-resolution).

## Collection size guidance

| Collection size | Recommendation |
|----------------|----------------|
| ≤ 20 papers | Run directly |
| 20–50 papers | Use a focus question to filter |
| > 50 papers | The skill will prompt you before proceeding |

## License

MIT — see [LICENSE](LICENSE).
