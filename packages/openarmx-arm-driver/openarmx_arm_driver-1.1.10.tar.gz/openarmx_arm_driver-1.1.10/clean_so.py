#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   clean_so.py
@Time    :   2025/12/21
@Author  :   Wei Lindong
@Version :   1.0
@Desc    :   清理 _lib 目录中的 .so 文件，恢复原始 .py 文件
'''

import os
import sys
import shutil
import glob

# 项目路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'src', 'openarmx_arm_driver', '_lib')
BACKUP_DIR = os.path.join(LIB_DIR, '_backup_py')

def remove_so_files():
    """删除所有 .so 文件"""
    print("正在删除 .so 文件...")
    print("=" * 60)

    so_pattern = os.path.join(LIB_DIR, '*.so')
    so_files = glob.glob(so_pattern)

    if not so_files:
        print("未找到 .so 文件")
        return 0

    removed_count = 0
    for so_file in so_files:
        try:
            os.remove(so_file)
            print(f"  删除: {os.path.basename(so_file)}")
            removed_count += 1
        except Exception as e:
            print(f"  删除失败 {os.path.basename(so_file)}: {e}")

    print("=" * 60)
    print(f"已删除 {removed_count} 个 .so 文件\n")
    return removed_count

def restore_py_files():
    """从备份恢复原始 .py 文件"""
    print("正在恢复原始 .py 文件...")
    print("=" * 60)

    if not os.path.exists(BACKUP_DIR):
        print("备份目录不存在，无法恢复")
        return 0

    py_files = glob.glob(os.path.join(BACKUP_DIR, '*.py'))

    if not py_files:
        print("备份目录中未找到 .py 文件")
        return 0

    restored_count = 0
    for backup_file in py_files:
        file_name = os.path.basename(backup_file)
        target_file = os.path.join(LIB_DIR, file_name)

        try:
            shutil.copy2(backup_file, target_file)
            print(f"  恢复: {file_name}")
            restored_count += 1
        except Exception as e:
            print(f"  恢复失败 {file_name}: {e}")

    print("=" * 60)
    print(f"已恢复 {restored_count} 个 .py 文件\n")
    return restored_count

def remove_backup_dir():
    """删除备份目录"""
    if os.path.exists(BACKUP_DIR):
        print("是否删除备份目录?")
        response = input("输入 'yes' 确认删除，其他任意键跳过: ").strip().lower()

        if response == 'yes':
            try:
                shutil.rmtree(BACKUP_DIR)
                print(f"已删除备份目录: {BACKUP_DIR}\n")
            except Exception as e:
                print(f"删除备份目录失败: {e}\n")
        else:
            print("保留备份目录\n")

def clean_build_artifacts():
    """清理编译产生的其他文件"""
    print("正在清理编译产物...")
    print("=" * 60)

    patterns = [
        os.path.join(LIB_DIR, '*.c'),
        os.path.join(LIB_DIR, '*.html'),
        os.path.join(LIB_DIR, '*.o'),
        os.path.join(LIB_DIR, '__pycache__'),
        os.path.join(SCRIPT_DIR, 'build'),
    ]

    cleaned_count = 0
    for pattern in patterns:
        if os.path.isdir(pattern):
            try:
                shutil.rmtree(pattern, ignore_errors=True)
                print(f"  删除目录: {os.path.basename(pattern)}")
                cleaned_count += 1
            except Exception as e:
                print(f"  删除失败 {pattern}: {e}")
        else:
            for file in glob.glob(pattern):
                try:
                    os.remove(file)
                    print(f"  删除文件: {os.path.basename(file)}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"  删除失败 {file}: {e}")

    print("=" * 60)
    print(f"已清理 {cleaned_count} 个文件/目录\n")

def main():
    """主函数"""
    print("=" * 60)
    print("OpenArmX _lib 目录清理脚本")
    print("删除 .so 文件并恢复原始 .py 文件")
    print("=" * 60)
    print()

    # 检查目录是否存在
    if not os.path.exists(LIB_DIR):
        print(f"错误: 目录不存在 {LIB_DIR}")
        sys.exit(1)

    print(f"目标目录: {LIB_DIR}\n")

    # 1. 删除 .so 文件
    remove_so_files()

    # 2. 恢复原始 .py 文件
    restore_py_files()

    # 3. 清理编译产物
    clean_build_artifacts()

    # 4. 可选：删除备份目录
    remove_backup_dir()

    print("=" * 60)
    print("清理完成!")
    print("=" * 60)

if __name__ == '__main__':
    main()
