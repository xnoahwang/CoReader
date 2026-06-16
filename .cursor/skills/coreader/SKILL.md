---
name: coreader
description: >-
  Incremental Chinese reading companion for English books in the CoReader
  project. All books live under books/<BookFolder>/ with numbered notes at
  the book root and metadata in _meta/. Optional Summary.md on completion;
  KeyPoints.md is user-curated. English notes via r en (suffix -en.md, never
  overwrites Chinese). Use when the user says r, r en, coreader, 读, 阅读,
  or asks to read/summarize a book section.
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
        ├── 01.Foreword.md      # 编号章节笔记（CoReader 产出，中文）
        ├── 01.Foreword-en.md   # 同上，英文（r en；不覆盖中文）
        ├── 02.Introduction.md
        ├── Summary.md          # 全书大总结（读完或用户要求时）
        ├── Summary-en.md       # 英文全书总结（r en summary）
        ├── KeyPoints.md        # 个人高光摘录（用户自行整理，CoReader 不自动写）
        └── _meta/
            ├── sections.json   # 章节映射（必读，否则 pdf-only）
            ├── progress.md     # 本书阅读进度
            ├── _seeds.md
            ├── _seeds-en.md    # 英文种子（r en 时追加）
            ├── _cases.md
            ├── _cases-en.md    # 英文案例索引（r en 时追加）
            └── _raw/           # 提取原文
```

## 触发命令

| 命令 | 行为 |
|------|------|
| `r <section>` | 读取并总结 **activeBook** 的指定章节（**中文**笔记） |
| `r en <section>` | 同上，写 **英文**笔记；文件名 `<note>-en.md`，**不覆盖**中文 |
| `r en summary` | 基于已读分章笔记写 `Summary-en.md`（英文） |
| `r status` | 显示当前书的已读/未读进度 |
| `r en status` | 显示 **英文**笔记的已读/未读进度 |
| `r list` | 列出当前书可读章节 |
| `r books` | 列出 `books/` 下所有书（ready / pdf-only） |
| `r ask <问题>` | 基于已读笔记 + 原文用 **中文** 回答 |
| `r en ask <question>` | 同上，用 **英文** 回答 |

**读完一本书（三层产出，分工不同）：**

| 层 | 中文 | 英文（`r en`） | 谁写 | 何时 |
|----|------|----------------|------|------|
| 分章笔记 | `01.*.md` … | `01.*-en.md` … | CoReader | 每次 `r` / `r en` |
| 大总结 | `Summary.md` | `Summary-en.md` | CoReader | 用户要求全书总结时 |
| 个人高光 | `KeyPoints.md` | — | **用户** | 用户自行整理 |

示例：`r foreword`、`r chapter 3`、`r en ch7`、`r en summary`

## 硬性规则

1. **只读用户指定的部分**
2. **默认输出语言为中文**；仅当用户命令以 `r en` 开头（或明确要求英文笔记）时，笔记与 `r en ask` 回复用 **英文**
3. **未读不编造**
4. **中文笔记路径** `books/<BookFolder>/<note>.md`
5. **英文笔记路径** `books/<BookFolder>/<note>-en.md`（`<note>` 来自 `sections.json` 的 `note` 字段；**禁止覆盖**同名无 `-en` 文件）
6. **辅助文件路径** `books/<BookFolder>/_meta/`；英文索引用 `_seeds-en.md`、`_cases-en.md`
7. **新书只放 `books/`**，不放在 CoReader 根目录

### 英文笔记文件名

| `sections.json` | 中文 | 英文 |
|-----------------|------|------|
| `"note": "03.Chapter-1"` | `03.Chapter-1.md` | `03.Chapter-1-en.md` |
| `"note": "01.Preface"` | `01.Preface.md` | `01.Preface-en.md` |
| 全书总结 | `Summary.md` | `Summary-en.md` |

Part：`r en part 1` → `Part-1-en.md`（若该书有 Part 笔记）

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

**中文（`r <section>`）：**

1. `books/<BookFolder>/<note>.md` — 正式笔记
2. `books/<BookFolder>/_meta/_seeds.md` — 种子（**追加/更新，禁止覆盖全书历史**）
3. `books/<BookFolder>/_meta/_cases.md` — 案例（追加）
4. `books/<BookFolder>/_meta/progress.md` — 本书进度（`## Completed` 下列中文笔记）
5. 根目录 [progress.md](../../../progress.md) — 若为新书，更新书目表

**英文（`r en <section>`）：**

1. `books/<BookFolder>/<note>-en.md` — 英文笔记（**不得写入或覆盖** `<note>.md`）
2. `_meta/_seeds-en.md` — 英文种子（追加，禁止覆盖）
3. `_meta/_cases-en.md` — 英文案例（追加）
4. `_meta/progress.md` — 在 `## English completed`（无则新建）下记录 `<note>-en`

笔记格式见 [output-template.md](output-template.md)。**中文风格标杆：** `books/TheEMythRevisited/15.Chapter-13.md`。**英文**见 output-template 的「English notes」节。

**笔记写法（硬性，与 output-template 一致）：**

- **中文为主，禁止散装英语**：正文用完整中文句；禁止「Technician obsession 围栏了 nature」「realistically地」这类中英碎片句。
- **术语**：首次 `中文（English）`，同章后文用中文；金句/人名可保留英文并解释。
- **排版**：长句拆行；`###` 分节；对照用表格；关键区分用引用标题 + 表格局部正文。
- **故事/隐喻**（Sarah、野马等）：独立小节 + 必要时「用中文说清楚就是」引用块。
- **逻辑链**、**易混点**、**跨章呼应**：写全、写清，不压缩成一行。
- **用户追问或微调后**：按用户确认的风格写后续章节；修订时通查同章类似表述。
- **_seeds.md / _cases.md**：追加条目，中文为主，禁止覆盖全书历史。
- **英文笔记（`r en`）**：完整英文句；结构与中文平行；`_seeds-en.md` / `_cases-en.md` 追加、禁止覆盖。

Part 标题页不占序号；`r part 1` → `Part-1.md`；`r en part 1` → `Part-1-en.md`

### Step 5: 回复用户

简短确认即可，路径带 `books/` 前缀，如 `books/TheEMythRevisited/03.Chapter-1.md` 或 `books/TheEMythRevisited/03.Chapter-1-en.md`。**不要重复笔记正文。** 聊天语言跟随命令：`r` → 中文；`r en` → 英文。

### 全书总结（可选，非每章必做）

用户明确要求「全书总结 / 做成 Summary」时：

**中文：** 基于已读分章笔记 + `_seeds.md` 写 `Summary.md`；更新 `_meta/progress.md` 与根目录 `progress.md`。

**英文（`r en summary`）：** 基于已读 **英文** 分章笔记（或尚无英文笔记时，可读中文笔记作参考但 **输出必须英文**）写 `Summary-en.md`；更新 `_meta/progress.md` 的 `## English completed`。**不得覆盖** `Summary.md`。

**不要** 顺带生成或改写 `KeyPoints.md`（用户私人高光本）。仅当用户明确要求时才协助 KeyPoints；英文高光无默认路径，可自定 `KeyPoints-en.md`。

## 新增一本书

1. 在 **`books/`** 下新建 `<BookFolder>/`（文件夹名建议与 PDF 主题一致、无特殊字符冲突）
2. 放入 PDF
3. 新建 `books/<BookFolder>/_meta/`、`_meta/_raw/`
4. 编写 `_meta/sections.json`（见已有书 `books/TheEMythRevisited/_meta/sections.json`）
5. 新建空 `_meta/_seeds.md`、`_cases.md`、`_meta/progress.md`（英文笔记产生时再建 `_seeds-en.md`、`_cases-en.md`）
6. 更新 `.coreader.json` 的 `activeBook` 为 `<BookFolder>`
7. 更新根目录 `progress.md` 书目表

仅放 PDF、尚未建 `sections.json` 的书为 **pdf-only**，不能 `r` 读章节，直到完成 setup。

## 附加资源

- [output-template.md](output-template.md)
- [progress.md](../../../progress.md)
