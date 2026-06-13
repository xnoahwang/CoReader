#!/usr/bin/env python3
"""Extract a single book section from a CoReader book PDF.

All books live under <project>/books/<BookFolder>/.
activeBook in .coreader.json is the folder name only (not a path).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "books"
CONFIG_FILE = ROOT / ".coreader.json"
META_DIR = "_meta"


def normalize_book_name(book: str) -> str:
    return book.replace("\\", "/").strip("/").removeprefix("books/")


def resolve_book_dir(book: str | None) -> Path:
    if book:
        name = normalize_book_name(book)
    else:
        if not CONFIG_FILE.exists():
            raise SystemExit(f"Missing {CONFIG_FILE}. Set activeBook or pass --book.")
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        name = config.get("activeBook")
        if not name:
            raise SystemExit(f"Missing activeBook in {CONFIG_FILE}")
    return BOOKS_DIR / name


def list_book_dirs() -> list[Path]:
    if not BOOKS_DIR.is_dir():
        return []
    return sorted(p for p in BOOKS_DIR.iterdir() if p.is_dir())


def book_ready(book_dir: Path) -> bool:
    return (book_dir / META_DIR / "sections.json").exists()


def format_available_books() -> str:
    books = list_book_dirs()
    if not books:
        return f"No book folders in {BOOKS_DIR}"
    lines = ["Available books:"]
    for book_dir in books:
        status = "ready" if book_ready(book_dir) else "pdf-only"
        lines.append(f"  {book_dir.name}  ({status})")
    return "\n".join(lines)


def load_active_book_dir(book: str | None) -> Path:
    book_dir = resolve_book_dir(book)
    if not book_dir.is_dir():
        hint = format_available_books()
        raise SystemExit(f"Book folder not found: {book_dir}\n{hint}")
    return book_dir


def meta_dir(book_dir: Path) -> Path:
    return book_dir / META_DIR


def load_sections(book_dir: Path) -> dict:
    sections_file = meta_dir(book_dir) / "sections.json"
    if not sections_file.exists():
        raise SystemExit(
            f"Missing {sections_file}\n"
            f"Book {book_dir.name} is not set up yet (pdf-only). "
            f"Add _meta/sections.json before extracting sections."
        )
    with sections_file.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_section(config: dict, query: str) -> dict:
    q = query.strip().lower()
    for section in config["sections"]:
        if section["id"] == q or q in [a.lower() for a in section["aliases"]]:
            return section
    raise SystemExit(f"Unknown section: {query!r}. Run with --list to see options.")


def extract_pages(pdf_path: Path, start_page: int, end_page: int) -> str:
    doc = fitz.open(pdf_path)
    chunks: list[str] = []
    for page_num in range(start_page, end_page + 1):
        if page_num < 1 or page_num > len(doc):
            continue
        text = doc[page_num - 1].get_text().strip()
        if text:
            chunks.append(f"--- page {page_num} ---\n{text}")
    doc.close()
    return "\n\n".join(chunks)


def print_books_list() -> None:
    active = None
    if CONFIG_FILE.exists():
        active = json.loads(CONFIG_FILE.read_text(encoding="utf-8")).get("activeBook")
    print(f"Books directory: {BOOKS_DIR}")
    for book_dir in list_book_dirs():
        status = "ready" if book_ready(book_dir) else "pdf-only"
        marker = " *" if book_dir.name == active else ""
        print(f"{book_dir.name:50}  {status}{marker}")
    if active:
        print(f"\n* activeBook in .coreader.json")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(description="Extract one section from a CoReader book PDF.")
    parser.add_argument("section", nargs="?", help="Section id or alias, e.g. foreword, chapter-1")
    parser.add_argument(
        "--book",
        help="Book folder name under books/ (default: .coreader.json activeBook)",
    )
    parser.add_argument("--list", action="store_true", help="List sections for the selected book")
    parser.add_argument("--list-books", action="store_true", help="List all folders under books/")
    parser.add_argument("--output", "-o", type=Path, help="Write extracted text to file")
    args = parser.parse_args()

    if args.list_books:
        print_books_list()
        return

    book_dir = load_active_book_dir(args.book)
    config = load_sections(book_dir)
    pdf_path = book_dir / config["book"]
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    if args.list:
        print(f"Book: {book_dir.name} — {config.get('title', config['book'])}")
        print(f"Path: books/{book_dir.name}/")
        for section in config["sections"]:
            aliases = ", ".join(section["aliases"])
            note = section.get("note", "—")
            print(f"{section['id']:12}  {note:16}  p{section['start_page']}-{section['end_page']}  {section['title']}")
            print(f"             aliases: {aliases}")
        return

    if not args.section:
        parser.error("section argument required unless --list or --list-books is used")

    section = resolve_section(config, args.section)
    text = extract_pages(pdf_path, section["start_page"], section["end_page"])

    header = (
        f"# {section['title']}\n"
        f"book: {book_dir.name}\n"
        f"pages: {section['start_page']}-{section['end_page']}\n"
        f"section_id: {section['id']}\n\n"
    )
    output = header + text

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
