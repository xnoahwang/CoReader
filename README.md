# CoReader

An incremental **Chinese reading companion** for English books, built to work with [Cursor](https://cursor.com) and an AI agent. You choose which section to read; the agent extracts the PDF text, writes structured notes in Chinese, and tracks progress—without pre-reading the whole book or inventing content from unread chapters.

## What it does

| Principle | Meaning |
|-----------|---------|
| **On demand** | Only the section you ask for (`r chapter 3`, `r preface`, …) is read and summarized |
| **Chinese notes (default)** | `r <section>` → `03.Chapter-1.md` — Chinese study notes |
| **English notes (optional)** | `r en <section>` → `03.Chapter-1-en.md` — parallel English notes, never overwrites Chinese |
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
        ├── 01.Foreword.md      # Chapter notes, Chinese (default)
        ├── 01.Foreword-en.md   # Chapter notes, English (r en)
        ├── Summary.md          # Full-book summary (Chinese)
        ├── Summary-en.md       # Full-book summary (r en summary)
        ├── KeyPoints.md        # Personal highlights (user-owned)
        └── _meta/
            ├── sections.json   # Section → PDF page mapping (required)
            ├── progress.md     # Per-book reading progress
            ├── _seeds.md       # Running themes / open threads
            ├── _cases.md       # Story & example index
            └── _raw/           # Extracted section text
```

## Three layers of output

| Layer | Chinese | English (`r en`) | Who writes | When |
|-------|---------|------------------|------------|--------|
| Chapter notes | `01.*.md` | `01.*-en.md` | CoReader | Each `r` / `r en <section>` |
| Book summary | `Summary.md` | `Summary-en.md` | CoReader | On request after finishing |
| Highlights | `KeyPoints.md` | — | **You** | Your own excerpts |

## Commands (in Cursor chat)

Use these with the CoReader skill enabled (or say `r`, `读`, `阅读`):

| Command | Action |
|---------|--------|
| `r <section>` | Read and summarize section → **Chinese** note (`<note>.md`) |
| `r en <section>` | Same → **English** note (`<note>-en.md`; does not overwrite Chinese) |
| `r en summary` | Write `Summary-en.md` from read English (or Chinese) chapter notes |
| `r status` | Read / unread progress (Chinese notes) |
| `r en status` | Read / unread progress (English `-en` notes) |
| `r list` | List sections for the active book |
| `r books` | List all folders under `books/` (`ready` vs `pdf-only`) |
| `r ask <question>` | Answer from notes + source text (**Chinese**) |
| `r en ask <question>` | Same, in **English** |

Examples: `r foreword`, `r chapter 3`, `r en ch7`, `r en summary`

**Naming:** if `sections.json` has `"note": "03.Chapter-1"`, English output is `03.Chapter-1-en.md`.

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

**Chinese (`r`):** Chinese-first prose; first mention `中文（English）`; `###` sections and tables.

**English (`r en`):** Full English sentences; same structure as Chinese notes; indexes in `_seeds-en.md` / `_cases-en.md`.

See `.cursor/skills/coreader/output-template.md` for both.

## License & PDFs

This project shares **reading notes and tooling**, not publishing rights to the underlying books. PDFs in `books/` are for personal study; if you fork or publish the repo, respect copyright and do not redistribute books you do not have the right to share.

## Contributing

This is primarily a personal reading workspace. If you use the layout or skill elsewhere, copying `scripts/extract_section.py`, the `books/<BookFolder>/_meta/` pattern, and the Cursor skill is enough to get started on your own titles.
