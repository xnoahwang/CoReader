# CoReader Progress

## Active Book

**TheEMythRevisited** — *The E-Myth Revisited* (Gerber)

详见 `books/TheEMythRevisited/_meta/progress.md`

## 项目结构

```
CoReader/
├── .coreader.json          # activeBook = books/ 下的文件夹名
├── progress.md             # 本文件：workspace 总览
├── scripts/
│   └── extract_section.py
└── books/                  # ← 所有书放这里
    └── <BookFolder>/
        ├── *.pdf
        ├── 01.Foreword.md   # 分章笔记（CoReader）
        ├── Summary.md       # 全书大总结（按需）
        ├── KeyPoints.md     # 个人高光（用户整理）
        └── _meta/
            ├── sections.json
            ├── progress.md
            ├── _seeds.md
            ├── _cases.md
            └── _raw/
```

## Books

| 文件夹 (`activeBook`) | 书名 | 状态 |
|------------------------|------|------|
| `TheEMythRevisited` | The E-Myth Revisited | **已读完** |
| `12 rules for life an antidote to chaos` | 12 Rules for Life | pdf-only |
| `Beyond order 12 more rules for life` | Beyond Order | pdf-only |
| `MAPS OF MEANING THE ARCHITECTURE OF BELIEF` | Maps of Meaning | pdf-only |
| `We Who Wrestle with God Perceptions of the Divine` | We Who Wrestle with God | pdf-only |

路径均为 `books/<文件夹>/`。

列出书目：`python scripts/extract_section.py --list-books`

## 阅读产出（每本书）

| 文件 | 用途 |
|------|------|
| `01.*.md` … | CoReader 分章笔记（`r chapter N`） |
| `Summary.md` | 全书大总结（读完或用户要求时由 CoReader 写） |
| `KeyPoints.md` | 个人眼前一亮摘录（**用户自行整理**） |
| `_meta/` | 进度、种子、案例、原文 |

## Handoff

- **加新书**：PDF 放进 `books/<新文件夹>/`，建好 `_meta/sections.json` 后再 `r`
- **切换当前书**：改 `.coreader.json` 的 `activeBook` 为 `books/` 下文件夹名
- **读章节**：`r chapter N`（针对 activeBook）
- **The E-Myth Revisited**：全书读完（2026-06-13）；有 `Summary.md`、`KeyPoints.md`
