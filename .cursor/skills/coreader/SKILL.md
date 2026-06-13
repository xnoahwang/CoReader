---
name: coreader
description: >-
  Incremental Chinese reading companion for English books in the CoReader
  project. Each book lives in its own folder with numbered notes at the book
  root and metadata in _meta/. Use when the user says r, coreader, 读,
  阅读, or asks to read/summarize a book section.
---

# CoReader

按需阅读英文书的中文读书伴侣。用户指哪读哪，不预读全书。

## 项目结构

```
CoReader/
├── .coreader.json              # { "activeBook": "TheEMythRevisited" }
├── progress.md                 # workspace 总览
├── scripts/extract_section.py
└── <BookFolder>/
    ├── *.pdf                   # 原书
    ├── 01.Foreword.md          # 编号笔记（书文件夹根目录，方便阅读）
    ├── 02.Introduction.md
    └── _meta/                  # 配置与辅助，不影响阅读浏览
        ├── sections.json
        ├── progress.md
        ├── _seeds.md
        ├── _cases.md
        └── _raw/
```

## 触发命令

| 命令 | 行为 |
|------|------|
| `r <section>` | 读取并总结指定章节 |
| `r status` | 显示当前书的已读/未读进度 |
| `r ask <问题>` | 仅基于已读笔记回答 |
| `r list` | 列出当前书可读章节 |

示例：`r foreword`、`r chapter 3`、`r ch7`

## 硬性规则

1. **只读用户指定的部分**
2. **输出语言为中文**
3. **未读不编造**
4. **笔记写入** `<BookFolder>/<note>.md`（根目录，如 `01.Foreword.md`）
5. **辅助文件写入** `<BookFolder>/_meta/`（种子、案例、原文、进度、sections.json）

## 工作流程

### Step 0: 确定当前书

读取 [.coreader.json](../../../.coreader.json) 的 `activeBook`。

### Step 1: 解析 section

```bash
python scripts/extract_section.py --list
```

章节映射：`<BookFolder>/_meta/sections.json`

### Step 2: 提取原文

```bash
python scripts/extract_section.py <section-id> -o <BookFolder>/_meta/_raw/<section-id>.txt
```

### Step 3–4: 生成笔记并持久化

1. `<BookFolder>/<note>.md` — 正式笔记
2. `<BookFolder>/_meta/_seeds.md` — 种子
3. `<BookFolder>/_meta/_cases.md` — 案例
4. `<BookFolder>/_meta/progress.md` — 进度

Part 标题页不占序号；`r part 1` → `<BookFolder>/Part-1.md`

### Step 5: 回复用户

简短确认即可，注明路径如 `TheEMythRevisited/03.Chapter-1.md`。不要重复笔记正文。

## 新增一本书

1. 新建 `<BookFolder>/` 和 `<BookFolder>/_meta/`、`_meta/_raw/`
2. 放入 PDF、`_meta/sections.json`、空 `_seeds.md` / `_cases.md`
3. 更新 `.coreader.json`

## 附加资源

- [output-template.md](output-template.md)
