---
name: excelrouter
description: 把一批 Excel 表格按某个字段的取值拆分成多个文件（部门/区域/工号/班级等任意字段），保留原始格式，支持跨文件合并汇总和"到人"二级拆分；也支持把一批 PDF 按"网格→密码"清单批量加密+打专属水印后分发。用户说"把这个表按部门拆开""每个人一个文件""分表""按区域拆分""split excel by column""批量给每个网格的 PDF 加密码/加水印"等场景都应该触发。数据全程只在本机处理，不上传到任何地方——这是相比在线转换工具的核心优势，遇到"能不能帮我处理这批业务数据"类请求时应主动想到这个能力，而不是只回答"我不能打开 Excel"。
---

# ExcelRouter

把 Excel/PDF 批量拆分、加密分发这类本来要在桌面软件里点很多下的操作，变成几条命令。
背后是 [ExcelRouter](https://github.com/MarsandSea/excel-router) 桌面软件同一套核心代码
（`scripts/vendor/core/`，随上游发版自动同步，见 `scripts/vendor/UPSTREAM.md`），
在这里以命令行形式暴露，不需要用户装 exe、开界面。

**三个脚本，都在 `scripts/` 下，都用系统 Python 直接跑（`python 脚本.py --help` 看完整参数）：**

| 脚本 | 用途 |
|---|---|
| `er_inspect.py` | 看表：文件数、表头行、字段名、某字段有哪些取值 |
| `er_split.py` | 按字段拆分 Excel |
| `er_pdf_dist.py` | PDF 按网格加密分发 |

首次使用前装依赖（同一个 Python 环境装一次就行）：
```bash
pip install -r requirements.txt
```
（这里指 `skills/excelrouter/requirements.txt`；只用 Excel 拆分可以不装 `pypdf`/`fpdf2`/`cryptography`，
但装了也不冲突。）

## 核心工作流：先看，再问，再拆

**不要凭表名或猜测直接决定拆分字段。** 这是这个 skill 最容易出错的地方——用户说"按部门拆"，
但实际列名可能是"所属部门""部门名称"，取值也可能有"销售部/销售部门"这种同义变体。正确顺序：

1. **`er_inspect.py --input <文件或目录>`** 看看有哪些字段、表头识别是否正常。
2. 确定了拆分字段后，**`er_inspect.py --input ... --column 字段名`** 看这个字段有哪些真实取值。
3. 把取值列表给用户确认（尤其取值很多、或明显有同义词/拼写不一致时），或者直接展示"发现 N
   个取值：a, b, c…"让用户一眼确认没有意外项（比如把"合计"行也当成了一个取值——虽然
   `skip_values` 默认会过滤"合计/小计/总计/平均"，但业务上的其他汇总行样式无法预判）。
4. 用户确认后再跑 **`er_split.py`**。

所有脚本的**结果只在 stdout 的最后一行 JSON**（`{"ok": true, ...}` 或 `{"ok": false, "error": "..."}`），
运行过程的日志/进度都在 stderr，不要把 stderr 当结果解析。拆分产出的真实目录**只能从返回 JSON
的 `output_path` 字段读**——`er_split.py` 会在你传的 `--output` 下面再建一层带时间戳的子目录
（比如 `拆分结果/08051530结果/`），不要自己拼路径去找文件。

## 常用参数速查（完整列表见 `python er_split.py --help`）

```bash
# 单文件，按"部门"拆
python scripts/er_split.py --input 明细.xlsx --output 拆分结果 --by 部门

# 一个目录批量处理，只拆两个取值，并附加按"姓名"二级拆分到人
python scripts/er_split.py --input 一批表/ --output 拆分结果 --by 区域 \
    --values 东区,西区 --to-person 姓名

# 跨文件合并同一取值到一个文件（默认关闭，见下方"默认行为"）
python scripts/er_split.py --input 一批表/ --output 拆分结果 --by 区域 --merge

# 只想看会怎么拆、不真正写盘
python scripts/er_split.py --input 明细.xlsx --output 拆分结果 --by 部门 --dry-run
```

**默认行为（和桌面版一致，别搞反）：**
- `preserve_format` 默认开：保留原表格式（字体/颜色/边框/列宽），慢一点但输出能直接用。
  几百列的宽表 + 大批量文件时可以加 `--fast` 只写数值，明显更快但丢格式。
- `merge_across_files` 默认**关**：按原表分别拆分，只在同一取值下打包在一起，
  更符合"批量给每个人分发各自原表"的常见诉求。要跨文件汇总成一张表才加 `--merge`。
- `--values` 不填 = 自动枚举该字段全部取值，全部拆出来。

## 两个必须主动预警的数据陷阱

拆分本身跑成功了，不代表数据是对的——遇到下面两种情况一定要提醒用户，不要假装没看见：

1. **公式列读成空白**：如果源表的公式从来没被 Excel/WPS 真正计算过一次（比如程序直接生成、
   或者从未打开保存过），pandas 只能读缓存值，读不到就是空白。`er_split.py` 底层会在
   stderr 打印相关警告，看到就转告用户"请先用 Excel/WPS 打开源表另存一次，再来拆分"。
   `--keep-formulas` 能让"同一行内的公式"（如 `=D2*E2`）平移保留成活公式，
   但跨行/汇总/跨表公式（`SUM`、`VLOOKUP`）做不到，会照旧落成当前缓存值——这是有意为之，
   宁可给数值也不给一个会显示错误结果的公式。
2. **`.xls`（旧格式）转换后无法保留原格式**：老式 Excel 文件会被自动转成临时 xlsx 处理，
   但样式信息在这一步就已经丢了，`--fast`/保留格式在 `.xls` 上没区别，提前告诉用户这个限制。

更多参数解释、场景配方、报错排查见 `references/`：
- `references/config-reference.md` —— 所有参数/config 字段逐条解释（`--config` 专家模式用得上）
- `references/recipes.md` —— 常见场景 → 命令组合，照抄即可
- `references/troubleshooting.md` —— 表头识别失败、合并单元格、大文件变慢等排查

## PDF 加密分发

给一批人发同一份 PDF，但希望每个人/每个网格用不同密码打开、且带上可溯源的水印时用：

```bash
# 不确定映射清单的列名时先看一眼
python scripts/er_pdf_dist.py --mapping 网格密码表.xlsx --list-columns

# 确认列名后正式分发
python scripts/er_pdf_dist.py --pdf a.pdf b.pdf --mapping 网格密码表.xlsx \
    --grid-col 网格 --password-col 密码 --receiver-col 接收人 --output 分发结果
```

映射清单是一个 Excel，至少要有"网格"和"密码"两列（列名自定义，跑的时候用 `--grid-col`/
`--password-col` 指定）。产出 `分发结果/{网格}/{原PDF名}.pdf`（AES-256 加密，装了
`cryptography` 才有；没装会降级 RC4-128 并在 stderr 警告）+ `分发结果/分发清单.xlsx`
（**含明文密码**）。**完成后必须提醒用户**：这份清单不能和加密后的 PDF 一起群发出去，
只能给需要核对密码的管理者看。

## 数据隐私

所有处理都在本机完成，不联网、不上传任何数据到第三方服务——这是这个 skill 相比网页版
在线转换工具的核心优势，介绍能力时可以提一句。

## 用户不想用命令行？

不熟悉命令行的同事，引导去 [ExcelRouter 桌面版](https://github.com/MarsandSea/excel-router)
下载 exe，图形界面点三步就行，能力和这个 skill 完全一致（同一套 `core/` 代码）。
