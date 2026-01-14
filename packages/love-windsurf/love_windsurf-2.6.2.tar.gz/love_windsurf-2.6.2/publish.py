#!/usr/bin/env python3
"""
PyPI 发布脚本
============

用于构建并发布 love_windsurf 包到 PyPI。

使用方法:
    python publish.py                    # 交互式输入 token
    python publish.py --token <TOKEN>    # 命令行指定 token
    python publish.py --bump patch       # 自动升级补丁版本并发布
    python publish.py --bump minor       # 自动升级次版本并发布
    python publish.py --bump major       # 自动升级主版本并发布
    python publish.py --build-only       # 仅构建不发布
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Windows 编码修复
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    # 禁用 rich 进度条以避免 GBK 编码问题
    os.environ["FORCE_COLOR"] = "0"


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent


def get_current_version() -> str:
    """从 pyproject.toml 获取当前版本号"""
    pyproject_path = get_project_root() / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if match:
        return match.group(1)
    raise ValueError("无法从 pyproject.toml 中找到版本号")


def bump_version(bump_type: str) -> str:
    """升级版本号
    
    Args:
        bump_type: 'major', 'minor', 或 'patch'
    
    Returns:
        新版本号
    """
    current = get_current_version()
    parts = current.split(".")
    
    if len(parts) != 3:
        raise ValueError(f"版本号格式不正确: {current}")
    
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"无效的升级类型: {bump_type}")
    
    new_version = f"{major}.{minor}.{patch}"
    
    # 更新 pyproject.toml
    pyproject_path = get_project_root() / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")
    new_content = re.sub(
        r'version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content
    )
    pyproject_path.write_text(new_content, encoding="utf-8")
    
    print(f"[OK] 版本号已从 {current} 升级到 {new_version}")
    return new_version


def clean_build_dirs():
    """清理构建目录"""
    project_root = get_project_root()
    dirs_to_clean = ["dist", "build"]
    
    for dir_name in dirs_to_clean:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"[CLEAN] 已清理: {dir_name}/")
    
    # 清理 egg-info
    for egg_info in project_root.glob("*.egg-info"):
        shutil.rmtree(egg_info)
        print(f"[CLEAN] 已清理: {egg_info.name}/")


def build_package():
    """构建包"""
    print("[BUILD] 开始构建...")
    project_root = get_project_root()
    
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        cwd=project_root,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"[ERROR] 构建失败:\n{result.stderr}")
        sys.exit(1)
    
    print("[OK] 构建成功!")
    
    # 显示构建产物
    dist_dir = project_root / "dist"
    if dist_dir.exists():
        for f in dist_dir.iterdir():
            print(f"   - {f.name}")


def upload_to_pypi(token: str):
    """上传到 PyPI
    
    Args:
        token: PyPI API token
    """
    print("[INFO] 上传到 PyPI...")
    project_root = get_project_root()
    dist_dir = project_root / "dist"
    
    # 获取 dist 目录下的所有文件
    dist_files = list(dist_dir.glob("*"))
    if not dist_files:
        print("[ERROR] dist 目录为空，请先构建")
        sys.exit(1)
    
    # 设置环境变量以避免 Windows 编码问题
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    
    # 构建命令，明确列出文件而不是使用通配符
    cmd = [
        sys.executable, "-m", "twine", "upload",
        "--non-interactive",
        "-u", "__token__",
        "-p", token
    ] + [str(f) for f in dist_files]
    
    result = subprocess.run(
        cmd,
        cwd=project_root,
        capture_output=True,
        text=True,
        env=env
    )
    
    if result.returncode != 0:
        # 检查是否是版本已存在的错误
        if "File already exists" in result.stderr or "File already exists" in result.stdout:
            print("[ERROR] 发布失败: 该版本已存在于 PyPI")
            print("[TIP] 使用 --bump patch 自动升级版本号")
        else:
            print(f"[ERROR] 发布失败:\n{result.stderr}\n{result.stdout}")
        sys.exit(1)
    
    print("[SUCCESS] 发布成功!")
    version = get_current_version()
    print(f"[URL] https://pypi.org/project/love-windsurf/{version}/")


def main():
    parser = argparse.ArgumentParser(
        description="构建并发布 love_windsurf 到 PyPI"
    )
    parser.add_argument(
        "--token",
        help="PyPI API token (也可通过 PYPI_TOKEN 环境变量设置)"
    )
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        help="自动升级版本号"
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="仅构建，不发布"
    )
    parser.add_argument(
        "--skip-clean",
        action="store_true",
        help="跳过清理步骤"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("love_windsurf PyPI 发布工具")
    print("=" * 50)
    
    # 显示当前版本
    current_version = get_current_version()
    print(f"[VERSION] 当前版本: {current_version}")
    
    # 升级版本号
    if args.bump:
        bump_version(args.bump)
    
    # 清理
    if not args.skip_clean:
        clean_build_dirs()
    
    # 构建
    build_package()
    
    # 发布
    if not args.build_only:
        # 获取 token
        token = args.token or os.environ.get("PYPI_TOKEN")
        
        if not token:
            print("\n[INPUT] 请输入 PyPI API token:")
            token = input().strip()
        
        if not token:
            print("[ERROR] 未提供 token，取消发布")
            sys.exit(1)
        
        upload_to_pypi(token)
    
    print("\n" + "=" * 50)
    print("[DONE] 完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
