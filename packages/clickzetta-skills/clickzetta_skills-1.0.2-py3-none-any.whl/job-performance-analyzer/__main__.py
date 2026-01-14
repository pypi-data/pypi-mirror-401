#!/usr/bin/env python3
"""
Clickzetta Job 性能分析工具 - 命令行入口

使用方法:
    cz-analyze-job <plan.json> <job_profile.json> [output_dir]

示例:
    cz-analyze-job plan.json job_profile.json ./output
"""
import sys
import os

def main():
    """命令行入口函数"""
    # Import here to avoid circular imports
    from .analyze_job import analyze_job, print_header

    if len(sys.argv) < 3:
        print("用法: cz-analyze-job <plan.json> <job_profile.json> [output_dir]")
        print("\n示例:")
        print("  cz-analyze-job plan.json job_profile.json ./output")
        print("\n说明:")
        print("  plan.json        - Clickzetta 执行计划文件")
        print("  job_profile.json - Clickzetta Job 运行概况文件")
        print("  output_dir       - 输出目录 (可选，默认为当前目录)")
        sys.exit(1)

    plan_file = sys.argv[1]
    profile_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "."

    if not os.path.exists(plan_file):
        print(f"错误: 文件不存在 - {plan_file}")
        sys.exit(1)
    if not os.path.exists(profile_file):
        print(f"错误: 文件不存在 - {profile_file}")
        sys.exit(1)

    print_header()
    analyze_job(plan_file, profile_file, output_dir)

if __name__ == '__main__':
    main()
