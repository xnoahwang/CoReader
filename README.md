# CoReader

An incremental **Chinese reading companion** for English books, built to work with [Cursor](https://cursor.com) and an AI agent. You choose which section to read; the agent extracts the PDF text, writes structured notes in Chinese, and tracks progress—without pre-reading the whole book or inventing content from unread chapters.

## What it does

| Principle | Meaning |
|-----------|---------|
| **On demand** | Only the section you ask for (`r chapter 3`, `r preface`, …) is read and summarized |
| **Chinese notes** | Chapter notes are written in Chinese, with English terms introduced once then explained |
| **No fabrication** | Unread sections are not summarized or guessed |
| **Persistent artifacts** | Notes, progress, seeds, and extracted raw text live in the repo as Markdown |

CoReader is not a generic ebook reader. It is a **workflow + folder layout + extraction script + Cursor skill** for turning serious English reading into durable, searchable Chinese study notes.

## Repository layout

```
CoReader/
├── .coreader.json              # { "activeBook": "<BookFolder>" }
├── progress.md                 # Workspace overview
├── requirements.txt            # pymupdf for PDF extraction
├── scripts/
│   └── extract_section.py      # CLI: list sections, extract text
├── .cursor/skills/coreader/    # Agent skill (commands, rules, templates)
└── books/
    └── <BookFolder>/
        ├── *.pdf               # Source PDF (local; see .gitignore)
        ├── 01.Foreword.md      # Numbered chapter notes (agent output)
        ├── Summary.md          # Full-book summary (on request)
        ├── KeyPoints.md        # Personal highlights (user-owned)
        └── _meta/
            ├── sections.json   # Section → PDF page mapping (required)
            ├── progress.md     # Per-book reading progress
            ├── _seeds.md       # Running themes / open threads
            ├── _cases.md       # Story & example index
            └── _raw/           # Extracted section text
```

## Three layers of output

| Layer | File | Who writes it | When |
|-------|------|---------------|------|
| Chapter notes | `01.*.md`, `02.*.md`, … | CoReader (agent) | Each `r <section>` |
| Book summary | `Summary.md` | CoReader (agent) | When you ask for a full summary after finishing |
| Highlights | `KeyPoints.md` | **You** | Your own “aha” excerpts; agent does not edit by default |

## Commands (in Cursor chat)

Use these with the CoReader skill enabled (or say `r`, `读`, `阅读`):

| Command | Action |
|---------|--------|
| `r <section>` | Read and summarize the **active** book’s section |
| `r status` | Show read / unread progress for the active book |
| `r list` | List sections for the active book |
| `r books` | List all folders under `books/` (`ready` vs `pdf-only`) |
| `r ask <question>` | Answer from read notes + source text (Chinese) |

Examples: `r foreword`, `r chapter 3`, `r ch7`, `r preface`

Set the active book in `.coreader.json`:

```json
{
  "activeBook": "TheMomTest"
}
```

The value is the **folder name** under `books/`, not a path.

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Requires **Python 3.10+** and [PyMuPDF](https://pypi.org/project/PyMuPDF/) (`pymupdf`).

### 2. Add a book (or use an existing one)

1. Create `books/<BookFolder>/` and place the PDF inside.
2. Create `books/<BookFolder>/_meta/` and `_meta/_raw/`.
3. Add `_meta/sections.json` (see `books/TheEMythRevisited/_meta/sections.json` for a full example).
4. Set `activeBook` in `.coreader.json`.
5. In Cursor, run `r list` then `r chapter 1` (or the first section id).

A folder with only a PDF and no `sections.json` is **pdf-only**—extraction and `r` commands will not work until setup is done.

### 3. Extract text manually (optional)

```bash
python scripts/extract_section.py --list
python scripts/extract_section.py --list-books
python scripts/extract_section.py chapter-1 -o books/TheMomTest/_meta/_raw/chapter-1.txt
python scripts/extract_section.py --book "TheMomTest" foreword
```

`sections.json` maps each section to `start_page` / `end_page` (1-based PDF page indices) and optional aliases.

### Example `sections.json` entry

```json
{
  "id": "chapter-1",
  "note": "02.Chapter-1",
  "aliases": ["chapter-1", "chapter 1", "ch1", "第1章"],
  "title": "Chapter 1: The Mom Test",
  "start_page": 7,
  "end_page": 22
}
```

- `note` → output filename stem (`02.Chapter-1.md`)
- `aliases` → what you can type after `r`

## Books in this repo

These folders are tracked in git (notes + metadata; PDFs included where present):

| Folder | Title | Status |
|--------|-------|--------|
| [`books/TheEMythRevisited/`](books/TheEMythRevisited/) | *The E-Myth Revisited* (Michael E. Gerber) | Complete · [Summary](books/TheEMythRevisited/Summary.md) |
| [`books/TheMomTest/`](books/TheMomTest/) | *The Mom Test* (Rob Fitzpatrick) | Complete · [Summary](books/TheMomTest/Summary.md) |

Other books may exist locally under `books/` but are **ignored by git** (see `.gitignore`). Add your own PDFs locally; only promote folders to the repo when you want to share notes.

## Cursor agent skill

Agent behavior is defined in:

- [`.cursor/skills/coreader/SKILL.md`](.cursor/skills/coreader/SKILL.md) — workflow and rules  
- [`.cursor/skills/coreader/output-template.md`](.cursor/skills/coreader/output-template.md) — note structure and style  

Style reference for chapter notes: `books/TheEMythRevisited/15.Chapter-13.md`.

## Note style (short)

- Chinese-first prose; avoid mixed English fragments in Chinese sentences  
- First mention: `中文（English）`; later use Chinese  
- Use `###` sections, tables, and blockquotes for contrasts and logic chains  
- `_seeds.md` and `_cases.md` are append-only indexes across the whole book  

## License & PDFs

This project shares **reading notes and tooling**, not publishing rights to the underlying books. PDFs in `books/` are for personal study; if you fork or publish the repo, respect copyright and do not redistribute books you do not have the right to share.

## Contributing

This is primarily a personal reading workspace. If you use the layout or skill elsewhere, copying `scripts/extract_section.py`, the `books/<BookFolder>/_meta/` pattern, and the Cursor skill is enough to get started on your own titles.
