# CoReader Progress

## Active Book

**TheEMythRevisited** — *The E-Myth Revisited* (Gerber)

详见 `TheEMythRevisited/_meta/progress.md`

## 项目结构

每本书一个文件夹：

```
<BookFolder>/
├── *.pdf                  # 原书
├── 01.Foreword.md         # 编号笔记（直接放这里，方便阅读）
├── 02.Introduction.md
├── 03.Chapter-1.md
└── _meta/                 # 与阅读无关的配置与辅助文件
    ├── sections.json
    ├── progress.md
    ├── _seeds.md
    ├── _cases.md
    └── _raw/
```

## Books

| 文件夹 | 书名 | 状态 |
|--------|------|------|
| `TheEMythRevisited/` | The E-Myth Revisited | 进行中 |

## Handoff

- 切换当前书：修改 `.coreader.json` 的 `activeBook`
