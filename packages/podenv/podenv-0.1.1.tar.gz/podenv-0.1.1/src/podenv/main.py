#!/usr/bin/env python3
"""podenv 命令行入口点"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """运行 podenv bash 脚本"""
    script_path = Path(__file__).parent / "podenv.sh"

    if not script_path.exists():
        print(f"错误: 找不到脚本 {script_path}", file=sys.stderr)
        sys.exit(1)

    # 传递所有命令行参数给 bash 脚本
    args = ["bash", str(script_path)] + sys.argv[1:]

    try:
        result = subprocess.run(args)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
