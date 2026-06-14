# 笔记输出模板

所有书在 **`books/<BookFolder>/`**。笔记写入 `books/<BookFolder>/<note>.md`（与 PDF 同级）。

`<BookFolder>` = `.coreader.json` 里 `activeBook` 的值（不含 `books/` 前缀）。

**风格标杆：** `books/TheEMythRevisited/15.Chapter-13.md` — 之后各章笔记均按此风格写。

## 笔记结构

```markdown
# <章节中文标题>

> 原文：<English title> · pp.<start>-<end>
> 阅读日期：<YYYY-MM-DD>

## 核心总结
## 种子 / 伏笔
## 案例卡片
## 与已读部分的呼应
## 阅读提示
```

## 语言与排版（硬性）

### 1. 中文为主，禁止散装英语

正文用 **完整中文句子**。禁止在中文句子里夹杂英文词碎片。

| 反例（禁止） | 正例 |
|--------------|------|
| Technician obsession 围栏了 entrepreneurial nature | 技工式的沉迷会 **压制** 企业家天性 |
| realistically地有机会 | **现实地**有机会 / ** realistically（现实地）** |
| enrich life 而非 drain life | 用来 **丰富** 人生，而不是 **吸干** 人生 |
| walk away / pursue / document | **放弃** / **去追** / **写下来** |

### 2. 英文术语：首次对照，之后用中文

- **首次**：`**中文（English）**` 或 `**中文**（English）`
- **同一文件内再次出现**：优先只用中文
- **原文金句、书名、人名**：可保留英文，附中文解释

示例：

```markdown
商业发展计划七步中的 **第二步：战略目标（Strategic Objective）**。
……下文写「战略目标」即可，不必反复 Strategic Objective。
```

### 3. 段落与层次

- 开篇用 **1～2 句** 说清本章在全书中的位置（承上启下）
- 长 bullet **拆行**：一句一意，子说明缩进或另起一行
- 复杂论证用 **`###` / `####` 小标题**，必要时用 **`---`** 分隔叙事段
- 对照关系用 **表格**（如三人格、商品 vs 产品、技工 vs 企业家）
- 全书级关键区分：引用块 **只放标题句** + 表格局部正文（表格不要每行加 `>`，避免预览不渲染）

```markdown
> **商品 vs 产品（全书关键区分）：**

| 概念 | 中文理解 | 例子 |
|------|----------|------|
| **商品（commodity）** | 顾客手里真正拿走的东西 | … |
| **产品（product）** | 顾客离开时的感受 | … |
```

### 4. 隐喻、故事、易混点

- 作者用故事（如 Sarah、野马、幕布）→ 单独小节，必要时 **「用中文说清楚就是：」** + 引用块总结
- 用户曾追问不懂的句 → 写成 **对照表** 或 **分步逻辑**，不要一行带过
- **易混点** 小标题：因果链、否定、指代不清时使用；**阅读提示** 再点一次

### 5. 论证链

逐步写清，不用箭头串中英混搭：

```markdown
1. 人本性不可预测
2. 企业却必须对客户可预测
3. 解法：靠系统，不靠「把人变可靠」
```

### 6. 案例与概念分离

- **核心总结**：论点、框架、标准
- **案例卡片**：人物、情节、说明什么
- **_seeds.md / _cases.md**：同样中文为主，不用散装英语

## 核心总结：推荐结构

```markdown
## 核心总结

<1～2 句：本章在全书 / 七步中的位置>

### <第一个主题>
- …

### <第二个主题>
…

---

### <叙事人物>的故事（若有）
#### 1. …
#### 2. …
> 用中文说清楚就是：…
```

## 案例卡片格式

标题用 **中文**；「说明什么」用完整中文句。

```markdown
### Revlon「卖希望，不是卖化妆品」
- **人物/场景**：
- **发生了什么**：
- **说明什么**：
- **关联概念**：第六章……；第九章……
```

## 阅读提示

至少包含：

1. 本章记忆点（中文）
2. 与前后章关系
3. 易混概念一句澄清（若有）
4. 下一章预告

## 文件位置

| 用途 | 路径 |
|------|------|
| 编号笔记 | `books/<BookFolder>/01.Foreword.md` … |
| 全书总结 | `books/<BookFolder>/Summary.md` — CoReader 按需；结构总览 |
| 个人高光 | `books/<BookFolder>/KeyPoints.md` — **用户自有**；眼前一亮摘录，与分章笔记、Summary 分开 |
| 章节映射 | `books/<BookFolder>/_meta/sections.json` |
| 本书进度 | `books/<BookFolder>/_meta/progress.md` |
| 种子清单 | `books/<BookFolder>/_meta/_seeds.md` |
| 案例索引 | `books/<BookFolder>/_meta/_cases.md` |
| 提取原文 | `books/<BookFolder>/_meta/_raw/<section-id>.txt` |
| 书目总览 | 根目录 `progress.md` |

## _seeds.md / _cases.md 追加格式

**禁止用 Write 覆盖整个 _seeds.md**；只追加新章条目或更新单条状态。

```markdown
- [<section-id>] **<中文概念>** — <中文说明>（状态：…）
- [<section-id>] **<中文案例名>** — <人物>：<事件> → <观点>
```

## 用户修订

用户微调笔记后，后续新章 **默认采用用户确认过的风格**（以最新章节笔记为准）。用户指出某段不懂时，修订笔记并检查同章类似表述。

## 新书 checklist

1. `books/<BookFolder>/` + PDF
2. `books/<BookFolder>/_meta/sections.json`
3. 空 `_seeds.md`、`_cases.md`、`progress.md`
4. 更新 `.coreader.json` → `activeBook`
5. 更新根目录 `progress.md` 书目表
