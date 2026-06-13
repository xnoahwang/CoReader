# 笔记输出模板

笔记写入 `<BookFolder>/<note>.md`（书文件夹根目录，与 PDF 同级）。

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

## 文件位置

| 用途 | 路径 |
|------|------|
| 编号笔记 | `<BookFolder>/01.Foreword.md` … |
| 章节映射 | `<BookFolder>/_meta/sections.json` |
| 阅读进度 | `<BookFolder>/_meta/progress.md` |
| 种子清单 | `<BookFolder>/_meta/_seeds.md` |
| 案例索引 | `<BookFolder>/_meta/_cases.md` |
| 提取原文 | `<BookFolder>/_meta/_raw/<section-id>.txt` |

## _seeds.md / _cases.md 追加格式

```markdown
- [<section-id>] **<概念>** — <说明>（状态：…）
- [<section-id>] **<案例>** — <人物>：<事件> → <观点>
```
