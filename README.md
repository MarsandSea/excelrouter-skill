<div align="center">

# excelrouter-skill

**[ExcelRouter](https://github.com/MarsandSea/excel-router) 的 Claude Skill 版**

在 Claude Code / Claude 里直接说"把这个表按部门拆开"，不用装 exe、不用开界面。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

*A Claude Skill that ports [ExcelRouter](https://github.com/MarsandSea/excel-router)'s
Excel-splitting and PDF secure-distribution engine into a command-line skill —
same core code as the desktop app, no GUI required.*

作者 / Author：**AbeLin** · MIT License

</div>

---

## 这是什么

[ExcelRouter](https://github.com/MarsandSea/excel-router) 是一个 Windows 桌面工具：把一批
Excel 按任意字段的取值拆分成多个文件，还能给一批 PDF 按"网格→密码"清单批量加密分发。
它的核心逻辑（`core/`）和桌面界面完全解耦——本仓把这部分核心代码原样搬进一个 **Claude
Skill**，让 Claude 能直接在对话里帮你拆表、分发 PDF，数据全程本机处理，不上传。

- 想要图形界面、给不熟悉命令行的同事用 → 去 [excel-router](https://github.com/MarsandSea/excel-router) 下载 exe。
- 想让 Claude 直接帮你干活、或者想把这个能力接进自己的 Claude Code 工作流 → 用这个仓库。

## 安装

**方式一：作为 Claude Code 插件市场安装**
```
/plugin marketplace add MarsandSea/excelrouter-skill
/plugin install excelrouter
```

**方式二：手动拷贝为本地 skill**
```bash
git clone https://github.com/MarsandSea/excelrouter-skill.git
cp -r excelrouter-skill/skills/excelrouter ~/.claude/skills/
```

安装后装一次 Python 依赖（Excel 拆分只需要前三个；PDF 加密分发要装齐）：
```bash
pip install -r skills/excelrouter/requirements.txt
```

## 用法

装好后正常和 Claude 对话即可，比如：

> 把这批 Excel 按"区域"字段拆开，每个区域一个文件，再按姓名拆到人

Claude 会自动触发 `excelrouter` skill：先看表结构和字段取值、和你确认拆分字段，
再执行拆分。也可以直接手动跑三个命令行脚本，见
[`skills/excelrouter/SKILL.md`](skills/excelrouter/SKILL.md) 和
[`skills/excelrouter/references/`](skills/excelrouter/references/) 下的配方/参数手册。

## 版本如何跟上游同步

`skills/excelrouter/scripts/vendor/core/` 是
[excel-router](https://github.com/MarsandSea/excel-router) 仓库 `core/` 目录的逐字副本，
由 [`.github/workflows/sync-upstream.yml`](.github/workflows/sync-upstream.yml) 自动维护：

- 每天定时检查上游最新的 `v*` 发布 tag，有新版本就拉取、跑测试、测试通过才提交并打同名 tag。
- 也可以去本仓 Actions 页手动点 **Run workflow** 立即同步。
- 只跟发布 tag 走，不跟上游 `main` 分支的半成品——上游还没打 tag 的改动不会被同步过来。

当前对应的上游版本、commit、同步时间见
[`skills/excelrouter/scripts/vendor/UPSTREAM.md`](skills/excelrouter/scripts/vendor/UPSTREAM.md)。
**`vendor/` 目录下的文件不要手改**，下次同步会直接覆盖。

## 目录结构

```
excelrouter-skill/
├── .claude-plugin/           # 插件市场清单（marketplace.json + plugin.json）
├── skills/excelrouter/
│   ├── SKILL.md              # skill 主文件，触发词/工作流/常见陷阱
│   ├── requirements.txt
│   ├── scripts/
│   │   ├── _common.py        # 公共小工具（sys.path 引导、默认配置、JSON 输出约定）
│   │   ├── er_inspect.py     # 看表：字段名/取值/表头行
│   │   ├── er_split.py       # Excel 拆分
│   │   ├── er_pdf_dist.py    # PDF 按网格加密分发
│   │   └── vendor/core/      # ← 上游 core/ 的逐字副本，自动同步，勿手改
│   └── references/           # 参数手册 / 场景配方 / 排查手册
├── tests/test_cli.py         # 三个脚本的冒烟测试
└── .github/workflows/
    ├── sync-upstream.yml     # 拉取式自动同步
    └── ci.yml                # push/PR 跑测试
```

## 开发

```bash
pip install -r skills/excelrouter/requirements.txt
pip install pytest ruff
pytest -q
ruff check .
```

## 协议

MIT License，与上游 [excel-router](https://github.com/MarsandSea/excel-router) 一致。
`scripts/vendor/core/` 下每个文件保留原始版权头，请勿删除。
