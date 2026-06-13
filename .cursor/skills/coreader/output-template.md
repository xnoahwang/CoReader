# 笔记输出模板

所有书在 **`books/<BookFolder>/`**。笔记写入 `books/<BookFolder>/<note>.md`（与 PDF 同级）。

`<BookFolder>` = `.coreader.json` 里 `activeBook` 的值（不含 `books/` 前缀）。

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

## 核心总结：写法要求

1. **先结构后缩写**：小节标题 + 完整句；I-Q-O、六条规则等可用列表/表格。
2. **论证链不压缩**：例如 Orchestration 段应写清「人本性 unpredictable → 企业要 predictable → 系统提供 predictability」，而非单行混写。
3. **否定与归属写清**：「不能每次都复制就不拥有」→ 改为「若不能每次都同样复制，就不算拥有」。
4. **案例与概念分离**：案例放「案例卡片」；核心总结只保留论点，避免一句多义。

### 易混点（按需插入）

当章节有 paradox、因果链、术语多义时，在核心总结内用 **易混点** 小标题展开，并在「阅读提示」中再点一次。

## 案例卡片格式

```markdown
### <案例名>
- **人物/场景**：
- **发生了什么**：
- **说明什么**：
- **关联概念**：
```

## 阅读提示

至少包含：本章记忆点、与前后章关系、易混概念一句澄清（若有）。

## 文件位置

| 用途 | 路径 |
|------|------|
| 编号笔记 | `books/<BookFolder>/01.Foreword.md` … |
| 章节映射 | `books/<BookFolder>/_meta/sections.json` |
| 本书进度 | `books/<BookFolder>/_meta/progress.md` |
| 种子清单 | `books/<BookFolder>/_meta/_seeds.md` |
| 案例索引 | `books/<BookFolder>/_meta/_cases.md` |
| 提取原文 | `books/<BookFolder>/_meta/_raw/<section-id>.txt` |
| 书目总览 | 根目录 `progress.md` |

## _seeds.md / _cases.md 追加格式

**禁止用 Write 覆盖整个 _seeds.md**；只追加新章条目或更新单条状态。

```markdown
- [<section-id>] **<概念>** — <说明>（状态：…）
- [<section-id>] **<案例>** — <人物>：<事件> → <观点>
```

## 新书 checklist

1. `books/<BookFolder>/` + PDF
2. `books/<BookFolder>/_meta/sections.json`
3. 空 `_seeds.md`、`_cases.md`、`progress.md`
4. 更新 `.coreader.json` → `activeBook`
5. 更新根目录 `progress.md` 书目表
