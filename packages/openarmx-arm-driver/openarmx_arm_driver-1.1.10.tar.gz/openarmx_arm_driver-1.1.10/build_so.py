#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   build_so.py
@Time    :   2025/12/21
@Author  :   Wei Lindong
@Version :   1.0
@Desc    :   将 _lib 目录中的 Python 文件编译为 .so 文件
             使用 Cython 进行编译，提高性能并保护源代码
'''

import os
import sys
import shutil
import glob
import argparse
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

# 项目路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'src', 'openarmx_arm_driver', '_lib')

# 需要编译的 Python 文件（排除 __init__.py）
PYTHON_FILES = [
    'can_comm.py',
    'can_utils.py',
    'log_utils.py',
    'motor_config_loader.py',
    'motor_control.py',
    'motor_manager.py',
]

def clean_build_files():
    """清理编译过程中产生的临时文件"""
    print("正在清理临时文件...")

    patterns = [
        os.path.join(LIB_DIR, '*.c'),
        os.path.join(LIB_DIR, '*.html'),
        os.path.join(LIB_DIR, '*.o'),
        os.path.join(SCRIPT_DIR, 'build'),
    ]

    for pattern in patterns:
        if os.path.isdir(pattern):
            shutil.rmtree(pattern, ignore_errors=True)
            print(f"  删除目录: {pattern}")
        else:
            for file in glob.glob(pattern):
                try:
                    os.remove(file)
                    print(f"  删除文件: {file}")
                except Exception as e:
                    print(f"  删除失败 {file}: {e}")

def backup_original_files():
    """备份原始 Python 文件"""
    backup_dir = os.path.join(LIB_DIR, '_backup_py')

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"创建备份目录: {backup_dir}")

    for py_file in PYTHON_FILES:
        src = os.path.join(LIB_DIR, py_file)
        dst = os.path.join(backup_dir, py_file)

        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"备份: {py_file} -> _backup_py/{py_file}")

def build_so_files():
    """编译 Python 文件为 .so 文件"""
    print("\n开始编译 .so 文件...")
    print("=" * 60)

    # 构建扩展模块列表
    extensions = []

    for py_file in PYTHON_FILES:
        py_path = os.path.join(LIB_DIR, py_file)

        if not os.path.exists(py_path):
            print(f"警告: 文件不存在 {py_path}")
            continue

        # 模块名称
        module_name = f"openarmx_arm_driver._lib.{py_file[:-3]}"

        # 创建扩展
        ext = Extension(
            module_name,
            [py_path],
            extra_compile_args=['-O3'],  # 优化级别
        )
        extensions.append(ext)
        print(f"添加编译目标: {module_name}")

    if not extensions:
        print("错误: 没有找到需要编译的文件")
        return False

    print("\n正在编译...")
    print("-" * 60)

    # 执行编译
    setup(
        name='openarmx_lib',
        ext_modules=cythonize(
            extensions,
            compiler_directives={
                'language_level': "3",      # Python 3
                'embedsignature': True,     # 保留函数签名
                'boundscheck': False,       # 关闭边界检查（提高性能）
                'wraparound': False,        # 关闭负索引（提高性能）
            },
            annotate=False,  # 不生成 HTML 注释文件
        ),
        script_args=['build_ext', '--inplace'],
    )

    print("-" * 60)
    print("编译完成!\n")
    return True

def verify_so_files():
    """验证 .so 文件是否生成成功"""
    print("验证 .so 文件...")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for py_file in PYTHON_FILES:
        module_name = py_file[:-3]  # 移除 .py
        so_pattern = os.path.join(LIB_DIR, f"{module_name}.*.so")
        so_files = glob.glob(so_pattern)

        if so_files:
            print(f"✓ {module_name}: {os.path.basename(so_files[0])}")
            success_count += 1
        else:
            print(f"✗ {module_name}: 未找到 .so 文件")
            fail_count += 1

    print("=" * 60)
    print(f"成功: {success_count} | 失败: {fail_count}")

    return fail_count == 0

def remove_original_py_files(auto_mode=False):
    """删除原始 .py 文件（已备份）"""
    if auto_mode:
        print("\n自动模式: 跳过删除原始 .py 文件")
        print("提示: 原始文件已备份到 _backup_py 目录")
        return

    print("\n是否删除原始 .py 文件? (已备份到 _backup_py 目录)")
    response = input("输入 'yes' 确认删除，其他任意键跳过: ").strip().lower()

    if response == 'yes':
        print("正在删除原始 .py 文件...")
        for py_file in PYTHON_FILES:
            py_path = os.path.join(LIB_DIR, py_file)
            if os.path.exists(py_path):
                os.remove(py_path)
                print(f"  删除: {py_file}")
        print("原始文件已删除")
    else:
        print("保留原始 .py 文件")

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='将 _lib 目录中的 Python 文件编译为 .so 文件'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='自动模式：跳过交互式提示（用于构建流程）'
    )
    args = parser.parse_args()

    print("=" * 60)
    print("OpenArmX _lib 目录编译脚本")
    print("将 Python 文件编译为 .so 格式")
    if args.auto:
        print("模式: 自动构建（非交互式）")
    print("=" * 60)
    print()

    # 检查 Cython 是否安装
    try:
        import Cython
        print(f"Cython 版本: {Cython.__version__}")
    except ImportError:
        print("错误: 未安装 Cython")
        print("请运行: pip install Cython")
        sys.exit(1)

    # 检查目录是否存在
    if not os.path.exists(LIB_DIR):
        print(f"错误: 目录不存在 {LIB_DIR}")
        sys.exit(1)

    print(f"源目录: {LIB_DIR}")
    print(f"编译文件数: {len(PYTHON_FILES)}\n")

    # 1. 备份原始文件
    backup_original_files()

    # 2. 编译 .so 文件
    if not build_so_files():
        print("\n编译失败!")
        sys.exit(1)

    # 3. 清理临时文件
    clean_build_files()

    # 4. 验证 .so 文件
    if not verify_so_files():
        print("\n警告: 部分文件编译失败")

    # 5. 可选：删除原始 .py 文件
    remove_original_py_files(auto_mode=args.auto)

    print("\n" + "=" * 60)
    print("脚本执行完成!")
    print("=" * 60)
    print("\n提示:")
    print("  1. 原始文件已备份到: _lib/_backup_py/")
    print("  2. 如需恢复，从备份目录复制回来即可")
    print("  3. 记得更新 pyproject.toml 中的 package-data 配置")

if __name__ == '__main__':
    main()
