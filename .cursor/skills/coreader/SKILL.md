---
name: coreader
description: >-
  Incremental Chinese reading companion for English books in the CoReader
  project. All books live under books/<BookFolder>/ with numbered notes at
  the book root and metadata in _meta/. Use when the user says r, coreader,
  读, 阅读, or asks to read/summarize a book section.
---

# CoReader

按需阅读英文书的中文读书伴侣。用户指哪读哪，不预读全书。

**所有书放在 `books/` 下。** 新建书 = 在 `books/` 里建文件夹，不要放在项目根目录。

## 项目结构

```
CoReader/
├── .coreader.json              # { "activeBook": "<BookFolder>" }  folder name only
├── progress.md                 # workspace 总览与书目表
├── scripts/extract_section.py
└── books/
    └── <BookFolder>/           # 文件夹名 = activeBook 的值
        ├── *.pdf               # 原书 PDF
        ├── 01.Foreword.md      # 编号笔记（与 PDF 同级，方便阅读）
        ├── 02.Introduction.md
        └── _meta/
            ├── sections.json   # 章节映射（必读，否则 pdf-only）
            ├── progress.md     # 本书阅读进度
            ├── _seeds.md
            ├── _cases.md
            └── _raw/           # 提取原文
```

## 触发命令

| 命令 | 行为 |
|------|------|
| `r <section>` | 读取并总结 **activeBook** 的指定章节 |
| `r status` | 显示当前书的已读/未读进度 |
| `r list` | 列出当前书可读章节 |
| `r books` | 列出 `books/` 下所有书（ready / pdf-only） |
| `r ask <问题>` | 基于已读笔记 + 原文回答；笔记不清时可更新对应笔记 |

示例：`r foreword`、`r chapter 3`、`r ch7`、`r books`

## 硬性规则

1. **只读用户指定的部分**
2. **输出语言为中文**
3. **未读不编造**
4. **笔记路径** `books/<BookFolder>/<note>.md`
5. **辅助文件路径** `books/<BookFolder>/_meta/`
6. **新书只放 `books/`**，不放在 CoReader 根目录

## 工作流程

### Step 0: 确定当前书

读取 [.coreader.json](../../../.coreader.json) 的 `activeBook`（**仅文件夹名**，不含 `books/` 前缀）。

书目录 = `books/<activeBook>/`

### Step 1: 解析 section

```bash
python scripts/extract_section.py --list
python scripts/extract_section.py --list-books   # 所有书
```

章节映射：`books/<BookFolder>/_meta/sections.json`

### Step 2: 提取原文

```bash
python scripts/extract_section.py <section-id> -o books/<BookFolder>/_meta/_raw/<section-id>.txt
```

其他书：`python scripts/extract_section.py --book "<BookFolder>" --list`

### Step 3–4: 生成笔记并持久化

1. `books/<BookFolder>/<note>.md` — 正式笔记
2. `books/<BookFolder>/_meta/_seeds.md` — 种子（**追加/更新，禁止覆盖全书历史**）
3. `books/<BookFolder>/_meta/_cases.md` — 案例（追加）
4. `books/<BookFolder>/_meta/progress.md` — 本书进度
5. 根目录 [progress.md](../../../progress.md) — 若为新书，更新书目表

笔记格式见 [output-template.md](output-template.md)。

**笔记清晰度（硬性）：**

- **中文优先**：复杂逻辑用完整中文句子，不要为省字写出歧义缩写。
- **逻辑链写全**：「矛盾 → 解法」逐步列出，不要压缩成一行。
- **英文术语**：首次出现附中文或括号释义。
- **易混点**：因果、否定、指代易混时，用 **易混点** 小标题或阅读提示单独说明。
- **跨章概念**：注明与已读章节的呼应。
- **用户追问后**：更新对应 `<note>.md` 并检查同章其他易混表述。

Part 标题页不占序号；`r part 1` → `books/<BookFolder>/Part-1.md`

### Step 5: 回复用户

简短确认即可，路径带 `books/` 前缀，如 `books/TheEMythRevisited/03.Chapter-1.md`。不要重复笔记正文。

## 新增一本书

1. 在 **`books/`** 下新建 `<BookFolder>/`（文件夹名建议与 PDF 主题一致、无特殊字符冲突）
2. 放入 PDF
3. 新建 `books/<BookFolder>/_meta/`、`_meta/_raw/`
4. 编写 `_meta/sections.json`（见已有书 `books/TheEMythRevisited/_meta/sections.json`）
5. 新建空 `_meta/_seeds.md`、`_cases.md`、`_meta/progress.md`
6. 更新 `.coreader.json` 的 `activeBook` 为 `<BookFolder>`
7. 更新根目录 `progress.md` 书目表

仅放 PDF、尚未建 `sections.json` 的书为 **pdf-only**，不能 `r` 读章节，直到完成 setup。

## 附加资源

- [output-template.md](output-template.md)
- [progress.md](../../../progress.md)
