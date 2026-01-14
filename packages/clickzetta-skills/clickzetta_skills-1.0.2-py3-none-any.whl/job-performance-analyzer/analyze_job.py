#!/usr/bin/env python3
"""
Clickzetta Job 性能分析工具
使用方法: python analyze_job.py <plan.json> <job_profile.json> [output_dir]
"""
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from core.parser import PlanProfileParser
from core.aligner import StageAligner
from analyzers import get_analyzer

def print_header():
    print("=" * 80)
    print("Clickzetta Job 性能分析工具 v2.0")
    print("=" * 80)
    print("\n已实现规则:")
    print("  ✅ Stage/Operator 级别优化 (7条):")
    print("     增量/全量判断、单DOP聚合、Hash Join、TableSink DOP、最大DOP、Spilling、主动问题发现")
    print("  ✅ 状态表优化 (6条):")
    print("     非增量诊断、Row Number检查、Append-Only Scan、状态表启用、Aggregate复用、Calc状态优化")

def analyze_job(plan_file: str, profile_file: str, output_dir: str = "."):
    print("\n" + "=" * 80)
    print("步骤1: 解析输入文件")
    print("=" * 80)
    
    parser = PlanProfileParser(plan_file, profile_file)
    parsed_data = parser.parse()
    sql_info = parsed_data['sql_info']
    vc_mode = parsed_data['vc_mode']
    settings = parsed_data['settings']
    version_info = parsed_data['version_info']

    print(f"\n[SQL 类型] {'REFRESH SQL' if sql_info['is_refresh'] else 'Regular SQL'}")
    print(f"[VC 模式] {vc_mode['mode']} Mode")
    print(f"[版本信息] {version_info['git_branch']}")
    print(f"[已有参数] Total: {len(settings)}")
    
    print("\n" + "=" * 80)
    print("步骤2: Stage 对齐与统计")
    print("=" * 80)
    
    aligner = StageAligner(parsed_data)
    aligned_data = aligner.align()
    total_time = aligned_data['total_job_time']
    
    print(f"\n[统计] Aligned Stages: {len(aligned_data['aligned_stages'])}, 总耗时: {total_time/1000:.2f}s")
    
    top_stages = aligner.get_top_stages(10)
    print(f"\n[Top 10 Stage]")
    print(f"{'#':<4}{'Stage':<12}{'Time(s)':>10}{'%':>8}{'DOP':>8}")
    print("-" * 45)
    for i, (sid, m) in enumerate(top_stages, 1):
        pct = m['elapsed_ms'] / total_time * 100 if total_time else 0
        print(f"{i:<4}{sid:<12}{m['elapsed_ms']/1000:>10.2f}{pct:>8.1f}{m['dop']:>8}")
    
    top_ops = aligner.get_top_operators(10)
    print(f"\n[Top 10 Operator]")
    print(f"{'#':<4}{'Stage':<12}{'Operator':<25}{'Max(s)':>10}{'Stage%':>8}{'Skew':>8}")
    print("-" * 70)
    for i, op in enumerate(top_ops, 1):
        print(f"{i:<4}{op['stage_id']:<12}{op['operator_id']:<25}"
              f"{op['max_time_ms']/1000:>10.2f}{op['stage_pct']:>8.1f}{op['skew_ratio']:>8.1f}")
    
    sql_type = 'REFRESH' if sql_info['is_refresh'] else 'REGULAR'
    analyzer = get_analyzer(sql_type=sql_type, vc_mode=vc_mode['mode'],
                           enable_state_table_rules=sql_info['is_refresh'])
    analyzer.context['settings'] = settings
    analyzer.context['vc_mode'] = vc_mode['mode']
    analyzer.context['version_info'] = version_info
    
    print("\n" + "=" * 80)
    print("步骤3: 执行规则分析")
    print("=" * 80)
    
    analyzer.analyze(aligned_data)
    reporter = analyzer.get_report()
    reporter.set_metadata('vc_mode', vc_mode['mode'])
    
    print("\n" + reporter.generate_console_report(analyzer.context))
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "analysis_results.json")
    reporter.save_json_report(output_path)
    print(f"\n结果已保存: {output_path}")
    
    return reporter.generate_json_report()

def main():
    if len(sys.argv) < 3:
        print("用法: python analyze_job.py <plan.json> <job_profile.json> [output_dir]")
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
