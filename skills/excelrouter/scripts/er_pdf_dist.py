#!/usr/bin/env python
"""
excelrouter · PDF 按网格加密分发：同一批 PDF，按「网格→密码」映射清单，
为每个网格生成专属打开密码 + 专属水印（可溯源）的副本，并输出含明文密码的分发清单。

Copyright (c) 2026 AbeLin
MIT License

用法：
  # 第一步：不确定映射清单的列名时，先看一眼表头
  python er_pdf_dist.py --mapping 映射.xlsx --list-columns

  # 第二步：确认列名后正式分发
  python er_pdf_dist.py --pdf a.pdf b.pdf --mapping 映射.xlsx \
      --grid-col 网格 --password-col 密码 --receiver-col 接收人 --output 分发结果

输出：stdout 一行 JSON。分发清单「分发清单.xlsx」含明文密码，务必提醒用户
不要把这份清单和加密后的 PDF 一起发给同一批人。
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import bootstrap, build_config, check_deps, emit, emit_error, eprint  # noqa: E402

bootstrap()

import core.pdf_dist as pdf_dist  # noqa: E402
from core.pdf_dist import MANIFEST_NAME, list_mapping_columns, run_pdf_dist  # noqa: E402


def main():
    ap = argparse.ArgumentParser(
        description="PDF 按网格加密分发（专属密码 + 专属水印 + 分发清单）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--pdf", nargs="+", default=[], help="待分发的 PDF 文件，可多个")
    ap.add_argument("--mapping", required=True, help="「网格→密码」映射清单 xlsx 路径")
    ap.add_argument("--list-columns", action="store_true",
                     help="只列出映射清单第 1 行的表头，不做分发（先跑这个确认列名）")
    ap.add_argument("--grid-col", default="", help="映射清单里的网格列名")
    ap.add_argument("--password-col", default="", help="映射清单里的密码列名")
    ap.add_argument("--receiver-col", default="", help="映射清单里的接收人列名（选填）")
    ap.add_argument("--output", default="", help="输出目录；不填则用「第一个PDF所在目录/分发结果」")
    ap.add_argument("--no-watermark", action="store_true", help="不加水印")
    ap.add_argument("--watermark-text", default="{grid} {date}", help="水印模板，支持 {grid} {date} 占位")
    ap.add_argument("--opacity", type=float, default=0.15, help="水印透明度 0~1")
    ap.add_argument("--angle", type=float, default=45, help="水印旋转角度")
    ap.add_argument("--font", default="", help="中文字体 .ttf 路径（非 Windows 环境找不到系统字体时用）")
    args = ap.parse_args()

    if not os.path.exists(args.mapping):
        emit_error(f"找不到映射清单：{args.mapping}")
        return

    if args.list_columns:
        check_deps()
        try:
            cols = list_mapping_columns(args.mapping)
        except Exception as e:
            emit_error(f"读取映射清单表头失败：{e}")
            return
        emit({"ok": True, "columns": cols})
        return

    check_deps(need_pdf=True)

    if not args.pdf:
        emit_error("缺少 --pdf（至少一个待分发的 PDF 文件），或改用 --list-columns 只看映射清单表头")
        return
    for p in args.pdf:
        if not os.path.exists(p):
            emit_error(f"找不到 PDF：{p}")
            return
    if not args.grid_col or not args.password_col:
        emit_error("缺少 --grid-col / --password-col。不确定列名时先跑 --list-columns 看表头。")
        return

    if args.font:
        if not os.path.exists(args.font):
            emit_error(f"找不到字体文件：{args.font}")
            return
        # 上游 _find_cjk_font() 只扫 Windows 系统字体目录，非 Windows 环境（或想指定字体时）
        # 用 monkeypatch 覆盖，不改 vendor 代码——下次同步不会把这个补丁冲掉。
        pdf_dist._find_cjk_font = lambda: args.font

    config = build_config(
        pdf_input_paths=[os.path.abspath(p) for p in args.pdf],
        pdf_mapping_path=os.path.abspath(args.mapping),
        output_path=os.path.abspath(args.output) if args.output else "",
        pdf_grid_column=args.grid_col,
        pdf_password_column=args.password_col,
        pdf_receiver_column=args.receiver_col,
        pdf_watermark=not args.no_watermark,
        pdf_watermark_text=args.watermark_text,
        pdf_watermark_opacity=args.opacity,
        pdf_watermark_angle=args.angle,
    )

    try:
        output_root = run_pdf_dist(config, log_fn=eprint, progress_fn=lambda v: eprint(f"[进度 {int(v * 100)}%]"))
    except Exception as e:
        emit_error(f"分发失败：{e}")
        return

    if not output_root:
        emit_error("分发失败：没有任何网格成功生成（详见上方日志）")
        return

    eprint(f"⚠ {MANIFEST_NAME} 含明文密码，请只发给需要核对密码的管理者，不要和加密 PDF 一起群发出去")
    emit({"ok": True, "output_path": output_root, "manifest": os.path.join(output_root, MANIFEST_NAME)})


if __name__ == "__main__":
    main()
