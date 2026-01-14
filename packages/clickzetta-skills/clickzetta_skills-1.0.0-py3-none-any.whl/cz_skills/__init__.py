"""
Clickzetta Skills Package

A collection of specialized tools and analyzers for Clickzetta system.

Available Skills:
- job_performance_analyzer: Job 性能自动诊断工具
"""

__version__ = "1.0.0"
__author__ = "Clickzetta Team"

# Skill registry for future expansion
AVAILABLE_SKILLS = {
    "job_performance_analyzer": {
        "name": "Job Performance Analyzer",
        "description": "分析 plan.json 和 job_profile.json，识别性能瓶颈并给出优化建议",
        "command": "cz-analyze-job",
    },
    # Future skills can be added here
    # "table_stats_expert": {...},
    # "sql_history_expert": {...},
}

__all__ = ["AVAILABLE_SKILLS", "__version__"]
