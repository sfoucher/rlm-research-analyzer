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
