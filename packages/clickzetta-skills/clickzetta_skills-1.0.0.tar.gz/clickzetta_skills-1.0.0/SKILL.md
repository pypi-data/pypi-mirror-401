---
name: job-performance-analyzer
description: Clickzetta Job 性能自动诊断工具。分析 plan.json 和 job_profile.json，自动识别性能瓶颈并给出参数优化建议。支持增量计算(REFRESH)、AP模式、GP模式、Compaction等各类SQL场景。当用户上传 plan.json 和 job_profile.json 并要求分析性能问题时使用此skill。此 skill 现已打包为 clickzetta-skills Python 包的一部分。
---

# Clickzetta Skills - Job Performance Analyzer

## 概述

这是 **clickzetta-skills** 包中的 Job Performance Analyzer 技能。

自动诊断 Clickzetta Job 性能问题的工具，分析执行计划(plan.json)和运行概况(job_profile.json)，识别瓶颈并给出参数优化建议。

## 包信息

- **包名**: `clickzetta-skills`
- **版本**: 1.0.0
- **命令**: `cz-analyze-job`
- **包含技能**: Job Performance Analyzer (更多技能持续添加中)

## 已实现规则

**Stage/Operator 级别优化** (7条规则):
- `refresh_type_detection` - 增量/全量刷新判断
- `single_dop_aggregate` - 单并行度聚合优化（三阶段聚合）
- `hash_join_optimization` - Broadcast Hash Join 优化
- `tablesink_dop` - TableSink DOP 自动调整检测
- `max_dop_check` - 最大 DOP 限制提示
- `spilling_analysis` - 内存溢出分析
- `active_problem_finding` - 主动瓶颈分析

**状态表优化** (6条规则):
- `non_incremental_diagnosis` - 全量刷新原因诊断
- `row_number_check` - ROW_NUMBER=1 pattern 检查
- `append_only_scan` - Append-Only 表识别
- `state_table_enable` - 状态表启用建议
- `aggregate_reuse` - 聚合结果复用检查
- `heavy_calc_state` - 高耗时 Calc 状态优化

## 使用方式

### 方式1: Claude Skill（推荐）
1. 上传此 .skill 文件
2. 上传 `plan.json` 和 `job_profile.json`
3. 对 Claude 说："分析这两个文件的性能问题"

### 方式2: Python 包安装（推荐用于命令行）

这个 skill 已经打包为 **clickzetta-skills** Python 包，可以独立安装使用。

#### 安装
```bash
# 进入 skill 目录
cd job-performance-analyzer

# 使用 Makefile 安装（推荐）
make install

# 或手动安装
python3 -m build
pip3 install dist/clickzetta_skills-*.whl
```

#### 使用
```bash
# 安装后可直接使用命令
cz-analyze-job plan.json job_profile.json ./output

# 查看帮助
cz-analyze-job
```

#### 开发模式安装
```bash
# 可编辑模式安装，修改代码立即生效
make install-dev
```

#### 其他命令
```bash
make list-skills  # 列出所有可用技能
make verify       # 验证包结构
make dev-check    # 检查安装状态
make uninstall    # 卸载包
```

### 方式3: 直接运行脚本（不推荐，已废弃）
```bash
# 旧方式，不推荐使用
cd job-performance-analyzer/cz_skills/job_performance_analyzer
python3 analyze_job.py plan.json job_profile.json ./output
```

## 架构设计

### 包结构
```
clickzetta-skills/
├── pyproject.toml          # 包配置
├── Makefile                # 构建工具
├── README.md               # 包文档
├── SKILL.md                # Skill 描述（本文件）
├── cz_skills/              # 主包
│   ├── __init__.py         # 包初始化，技能注册表
│   └── job_performance_analyzer/  # Job 性能分析器
│       ├── __init__.py
│       ├── __main__.py     # 命令行入口
│       ├── analyze_job.py  # 主分析逻辑
│       ├── core/           # 核心模块
│       │   ├── parser.py   # JSON 解析
│       │   ├── aligner.py  # Stage 对齐
│       │   └── reporter.py # 报告生成
│       ├── analyzers/      # 分析器
│       │   ├── base_analyzer.py
│       │   └── incremental_analyzer.py
│       ├── rules/          # 规则库
│       │   ├── base_rule.py
│       │   └── incremental/
│       │       ├── stage_optimization/  # 7条 Stage 规则
│       │       └── state_table/         # 6条状态表规则
│       └── utils/          # 工具函数
└── references/             # 参考文档
```

### 添加新技能

要向 clickzetta-skills 包添加新技能：

1. 在 `cz_skills/` 下创建新技能目录：
```bash
mkdir -p cz_skills/your_new_skill
```

2. 创建必要文件：
```python
# cz_skills/your_new_skill/__init__.py
__version__ = "1.0.0"

# cz_skills/your_new_skill/__main__.py
def main():
    print("Your skill logic here")

if __name__ == '__main__':
    main()
```

3. 在 `pyproject.toml` 中注册命令：
```toml
[project.scripts]
cz-your-skill = "cz_skills.your_new_skill.__main__:main"
```

4. 在 `cz_skills/__init__.py` 中注册技能：
```python
AVAILABLE_SKILLS = {
    "your_new_skill": {
        "name": "Your New Skill",
        "description": "技能描述",
        "command": "cz-your-skill",
    },
}
```

5. 重新构建安装：
```bash
make install
```

## 参考文档
- `references/data-extraction-paths.md` - JSON 路径参考
- `references/core-specification.md` - 核心数据提取规范

-- 以下是为了迭代/重新创建skill时使用，正常使用skill时不需要关注以下references
- `references/original_prompt.md` - 原始需求，使用skill时不需要
- `references/incremental-optimization.md` - 增量计算优化规范 ，使用skill时不需要
- `references/skill_architecture.md` - skill架构设计，使用skill时不需要
- `references/recreate-skill-rule.md` - 重新创建skill规则，使用skill时不需要
