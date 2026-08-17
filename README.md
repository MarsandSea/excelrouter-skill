<div align="center">

# 📊 ExcelRouter · 表格拆分 & PDF 加密分发

**对 AI 说一句话，拆表 / 加密 PDF 全自动完成** — Claude Code 与 WorkBuddy 双端可用

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![SkillHub](https://img.shields.io/badge/SkillHub-审核中%20%2F%20即将上架-1a73e8)

*"帮我把这张工资表按部门拆开，每个部门一个文件"——剩下的交给 AI。*
*数据全程本机处理，不联网、不上传。*

作者 / Author：**AbeLin** · MIT License · ⭐ 觉得好用请点个 Star 支持作者

</div>

---

## ✨ 为什么用它

| | |
|---|---|
| 🧩 **一句话触发** | 不用装软件、不用开界面、不用写代码，直接对 AI 说需求 |
| 🗂️ **Excel 按字段拆分** | 部门 / 区域 / 工号 / 班级……任意列，保留原始格式 |
| 🔐 **PDF 批量加密分发** | 按"网格→密码"清单批量加密 + 专属水印 + 密码分发清单 |
| 🛡️ **数据全程本机** | 所有处理在本地完成，不联网、不上传，适合敏感数据 |

**典型场景：**
- 一张几百人的工资表 / 考勤表 / 销售明细 → 按部门拆成单文件发给各部门负责人
- 一批 PDF 合同 / 报告 → 按接收人分别加密、打上专属水印后分发
- 同一个人散落在多个文件里 → 跨文件合并成"到人"的个人档案

---

## 📸 效果预览

> TODO：替换为你的真实截图（建议放 `docs/screenshots/` 目录）
>
> 1. 一句话拆分前 → 拆分后按部门生成的文件列表
> 2. 打开拆分结果，展示格式（字体/颜色/列宽）原样保留
> 3. PDF 加密分发前后对比 + 密码分发清单

---

## 🚀 安装

### 方式一：WorkBuddy（推荐，国产办公用户）

上架 SkillHub（skillhub.cn）后可直接在 WorkBuddy 技能市场搜索 **ExcelRouter** 一键安装：

```
WorkBuddy → 左侧「技能 / 专家」→ 搜索 ExcelRouter → 安装
```

> 审核通过前，可用方式二手动安装，效果完全一样。

### 方式二：Claude Code 插件市场安装

```
/plugin marketplace add MarsandSea/excelrouter-skill
/plugin install excelrouter
```

### 方式三：手动拷贝为本地 skill

```bash
git clone https://github.com/MarsandSea/excelrouter-skill.git
cp -r excelrouter-skill/skills/excelrouter ~/.claude/skills/      # Claude Code
# 或
cp -r excelrouter-skill/skills/excelrouter ~/.workbuddy/skills/   # WorkBuddy
```

### 安装 Python 依赖（一次性）

```bash
pip install -r skills/excelrouter/requirements.txt
```

> 只用 Excel 拆分只需 `pandas` / `openpyxl` / `xlrd`；PDF 加密分发再加
> `pypdf` / `fpdf2` / `cryptography`（缺 `cryptography` 会降级为 RC4-128，功能仍可用）。

---

## 💬 快速上手

### 拆 Excel

把文件路径告诉 AI，说清楚按什么字段拆，例如：

```
"帮我把这份工资表按部门拆开，每个部门一个文件"
"这一批月度报表，按区域拆，顺便按姓名也拆到人"
"只要东区和西区的数据，其它区域不用管"
```

AI 会先自动看一眼有哪些字段、每个字段有哪些取值，**跟你确认没有拆错**
（比如"销售部"和"销售部门"算不算同一个），再动手拆分，完成后告诉你文件在哪。

### PDF 加密分发

先准备一张「网格→密码」Excel 清单（一行一个人，至少含"密码"列），然后说：

```
"把这几个 PDF 按这张密码表批量加密，每个人一个专属密码，再加个水印"
```

AI 会确认哪列是密码、哪列是接收人，然后输出：
- ✅ 加密后的 PDF（AES-256）
- ✅ 带专属水印（接收人 / 网格 / 日期）
- ✅ 「分发清单.xlsx」（明文密码）

> ⚠️ **安全提醒**：分发清单含明文密码，只给自己或管理员留底，
> **千万不要和加密后的 PDF 一起发出去**！

---

## 🧰 更多能力（一句话就能触发）

| 你想干嘛 | 就这么说 |
|---|---|
| 跨文件合并再拆 | "这整个文件夹的月度报表，每个区域整理一份" |
| 拆到个人 | "按部门拆，再按工号拆到每个人" |
| 只要部分取值 | "只要东区和西区的数据" |
| 同人跨文件合成总表 | "同一个人在好几个文件里都有数据，希望合成一张总表" |
| 同义取值合并 | "有的写'销售部'有的写'销售部门'，是同一个部门" |
| 表头不在第一行 | "表头在第三行，别认错了" |
| 保留公式 | "接收人要能看到金额是怎么算出来的公式" |
| 先看结果不动文件 | "先看看会拆出哪些文件，不要真的写盘" |
| 自定义水印 | "水印写'内部资料·请勿外传'" |

完整参数说明见
[`skills/excelrouter/SKILL.md`](skills/excelrouter/SKILL.md) 和
[`skills/excelrouter/references/`](skills/excelrouter/references/)（配方 / 参数手册 / 排查手册）。

---

## 🛡️ 数据安全

- ✅ 全程本机处理，无网络调用，不上传任何数据
- ✅ 密码仅用于本地 PDF 加密，不落盘到日志
- ✅ 代码开源（MIT），核心逻辑可逐行审查
- ✅ 依赖均为知名 PyPI 包：openpyxl / pandas / xlrd / pypdf / fpdf2 / cryptography

---

## ❓ FAQ

**Q：要钱吗？**
A：免费，MIT 开源，随便用。

**Q：支持哪些 Excel 格式？**
A：`.xlsx` 完美支持（保留格式）；`.xls` 会自动转换后再处理（旧格式样式会丢失，建议另存为 `.xlsx`）。

**Q：数据区有合并单元格怎么办？**
A：表头区的合并单元格会保留；数据区的合并单元格暂不支持，建议源表数据区避免合并。

**Q：没有中文字体会影响水印吗？**
A：Windows 会自动探测 `simhei.ttf`；其他系统可用 `--font 字体.ttf` 指定（需 `.ttf` 格式）。

**Q：这个 skill 和 ExcelRouter 桌面版什么关系？**
A：本仓是 [excel-router](https://github.com/MarsandSea/excel-router) 桌面工具核心逻辑的
Skill 移植版，同一套引擎、无需 GUI。要图形界面给同事用，去下载桌面版 exe。

---

## 🔄 版本如何跟上游同步

`skills/excelrouter/scripts/vendor/core/` 是
[excel-router](https://github.com/MarsandSea/excel-router) 仓库 `core/` 目录的逐字副本，
由 [`.github/workflows/sync-upstream.yml`](.github/workflows/sync-upstream.yml) 自动维护：

- 每天定时检查上游最新的 `v*` 发布 tag，有新版本就拉取、跑测试、测试通过才提交并打同名 tag。
- 也可以去本仓 Actions 页手动点 **Run workflow** 立即同步。
- 只跟发布 tag 走，不跟上游 `main` 分支的半成品。

当前对应的上游版本、commit、同步时间见
[`skills/excelrouter/scripts/vendor/UPSTREAM.md`](skills/excelrouter/scripts/vendor/UPSTREAM.md)。
**`vendor/` 目录下的文件不要手改**，下次同步会直接覆盖。

---

## 📁 目录结构

```
excelrouter-skill/
├── .claude-plugin/           # 插件市场清单（marketplace.json + plugin.json）
├── skills/excelrouter/
│   ├── SKILL.md              # skill 主文件，触发词/工作流/常见陷阱
│   ├── manifest.yaml         # WorkBuddy SkillHub 市场元信息（slug/版本/触发词/标签）
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

---

## 🧑‍💻 开发

```bash
pip install -r skills/excelrouter/requirements.txt
pip install pytest ruff
pytest -q
ruff check .
```

## 📣 支持作者

觉得有用的话：
- ⭐ 给本仓库点个 Star
- 🐛 遇到问题提 Issue（附上报错信息 + 最小复现文件）
- 🤝 欢迎 PR（先跑通 `pytest -q` 和 `ruff check .`）

## 📄 协议

MIT License，与上游 [excel-router](https://github.com/MarsandSea/excel-router) 一致。
`scripts/vendor/core/` 下每个文件保留原始版权头，请勿删除。
