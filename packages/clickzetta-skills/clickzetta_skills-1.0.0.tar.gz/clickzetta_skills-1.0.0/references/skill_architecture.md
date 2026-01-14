# Job Performance Analyzer Skill - 模块化架构设计

## 当前问题
- 单一脚本 30KB+，所有逻辑混在一起
- REFRESH SQL、Regular SQL、AP/GP 模式代码耦合
- 后续新增规则（如 4.2 状态表优化）难以扩展
- 规则迭代时需要修改大量代码

## 新架构设计

### 关键理解
1. **第 3 章是完整的增量计算分析**，包含两个部分：
   - 3.0-3.6: Stage/Operator 级别优化（对应原来的 4.1）
   - （未来）状态表级别优化（对应原来的 4.2）
2. **第 4 章是 AP 模式**（独立的）
3. **规则命名不带数字**，避免后续调整困难

```
job-performance-analyzer-zh.skill/
├── SKILL.md                          # 主文档（使用说明）
│
├── scripts/
│   ├── analyze_job.py                # 主入口脚本（轻量级）
│   │
│   ├── core/                         # 核心模块
│   │   ├── __init__.py
│   │   ├── parser.py                 # JSON 解析与数据提取
│   │   ├── aligner.py                # Stage/Operator 对齐
│   │   └── reporter.py               # 报告生成
│   │
│   ├── analyzers/                    # 分析器模块（按 SQL 类型分类）
│   │   ├── __init__.py
│   │   ├── base_analyzer.py          # 基类分析器
│   │   ├── incremental_analyzer.py   # 增量计算分析器 (第3章)
│   │   ├── regular_analyzer.py       # 普通 SQL 分析器
│   │   └── ap_analyzer.py            # AP 模式分析器 (第4章)
│   │
│   ├── rules/                        # 规则库（每个规则独立文件）
│   │   ├── __init__.py
│   │   │
│   │   ├── incremental/              # 增量计算规则 (第3章)
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── stage_optimization/   # 3.0-3.6 Stage/Operator 优化
│   │   │   │   ├── __init__.py
│   │   │   │   ├── refresh_type_detection.py    # 3.0 增量/全量判断
│   │   │   │   ├── single_dop_aggregate.py      # 3.1 单 DOP 聚合
│   │   │   │   ├── hash_join_optimization.py    # 3.2 Hash Join
│   │   │   │   ├── tablesink_dop.py             # 3.3 TableSink DOP
│   │   │   │   ├── max_dop_check.py             # 3.4 最大 DOP
│   │   │   │   ├── spilling_analysis.py         # 3.5 Spilling
│   │   │   │   └── active_problem_finding.py    # 3.6 主动问题发现
│   │   │   │
│   │   │   └── state_table/          # （未来）状态表优化
│   │   │       ├── __init__.py
│   │   │       ├── non_incremental_detection.py # 非增量诊断
│   │   │       ├── row_number_check.py          # 行号检查
│   │   │       ├── append_only_scan.py          # 仅追加扫描
│   │   │       └── ...
│   │   │
│   │   ├── ap_mode/                  # AP 模式规则 (第4章)
│   │   │   ├── __init__.py
│   │   │   └── ... (TODO)
│   │   │
│   │   └── common/                   # 通用规则（跨类型）
│   │       ├── __init__.py
│   │       ├── data_skew.py          # 数据倾斜检测
│   │       └── operator_bottleneck.py # 算子瓶颈分析
│   │
│   └── utils/                        # 工具函数
│       ├── __init__.py
│       ├── json_path.py              # JSON 路径提取
│       ├── settings_checker.py       # 参数检查
│       └── formatters.py             # 输出格式化
│
└── references/                       # 参考文档
    ├── core-specification.md         # 核心规范（第2章）
    ├── incremental-optimization.md   # 增量计算优化规范（第3章）
    └── data-extraction-paths.md      # 数据提取路径
```

## 核心设计原则

### 1. 单一职责
每个规则文件只负责一个检测规则：
```python
# rules/incremental/stage_optimization/single_dop_aggregate.py
class SingleDopAggregate:
    """3.1: 单 DOP 聚合优化"""
    
    name = "single_dop_aggregate"
    category = "incremental/stage_optimization"
    
    def check(self, stage_data, context):
        """检查是否触发该规则
        
        触发条件：
        1. Stage DOP = 1
        2. 包含 HashAggregate P1
        3. 使用高成本聚合函数
        4. 耗时 > 12秒 或 占比 > 15%
        """
        pass
    
    def analyze(self, stage_data, context):
        """分析问题并返回建议
        
        分析步骤：
        1. 检查三阶段聚合参数
        2. 检查是否退化为 one-pass
        3. 检查 Bloom Filter bits
        """
        pass
    
    def get_recommendations(self, analysis_result):
        """生成参数建议"""
        return [
            {
                'setting': 'cz.optimizer.incremental.df.three.phase.agg.enable',
                'value': 'true',
                'priority': 1,
                'reason': '...'
            }
        ]
```

### 2. 分析器组合规则
每个分析器组合对应类型的规则：
```python
# analyzers/incremental_analyzer.py
class IncrementalAnalyzer(BaseAnalyzer):
    """增量计算分析器 (第3章 REFRESH SQL)"""
    
    def __init__(self):
        # Stage/Operator 优化规则 (3.0-3.6)
        from rules.incremental.stage_optimization import (
            RefreshTypeDetection,
            SingleDopAggregate,
            HashJoinOptimization,
            TableSinkDop,
            MaxDopCheck,
            SpillingAnalysis,
            ActiveProblemFinding
        )
        
        self.stage_rules = [
            RefreshTypeDetection(),    # 3.0 增量/全量判断
            SingleDopAggregate(),      # 3.1 单 DOP 聚合
            HashJoinOptimization(),    # 3.2 Hash Join
            TableSinkDop(),            # 3.3 TableSink DOP
            MaxDopCheck(),             # 3.4 最大 DOP
            SpillingAnalysis(),        # 3.5 Spilling
            ActiveProblemFinding(),    # 3.6 主动问题发现
        ]
        
        # 状态表优化规则（未来扩展）
        self.state_table_rules = []
    
    def analyze(self, aligned_data):
        # 先执行 Stage 优化分析
        for rule in self.stage_rules:
            if rule.check(aligned_data, self.context):
                result = rule.analyze(aligned_data, self.context)
                self.add_finding(result)
        
        # 如果需要，执行状态表分析
        if self.state_table_rules:
            for rule in self.state_table_rules:
                if rule.check(aligned_data, self.context):
                    result = rule.analyze(aligned_data, self.context)
                    self.add_finding(result)
```

### 3. 主脚本轻量化
```python
# scripts/analyze_job.py (主入口)
from core.parser import PlanProfileParser
from core.aligner import StageAligner
from core.reporter import Reporter
from analyzers import get_analyzer

def main():
    # 1. 解析输入
    parser = PlanProfileParser(plan_file, profile_file)
    data = parser.parse()
    
    # 2. 对齐 Stage/Operator
    aligner = StageAligner(data)
    aligned = aligner.align()
    
    # 3. 选择分析器
    analyzer = get_analyzer(data.sql_type, data.vc_mode)
    
    # 4. 执行分析
    findings = analyzer.analyze(aligned)
    
    # 5. 生成报告
    reporter = Reporter(findings)
    reporter.generate()
```

## 优势

### 1. 易于维护
- 每个规则独立，修改互不影响
- 新增规则只需添加新文件，无需改动现有代码

### 2. 易于测试
```python
# 可以单独测试每个规则
def test_single_dop_agg():
    from rules.incremental.stage_optimization import SingleDopAggregate
    
    rule = SingleDopAggregate()
    stage_data = load_test_data("single_dop_case.json")
    
    # 测试触发条件
    assert rule.check(stage_data, context) == True
    
    # 测试分析逻辑
    result = rule.analyze(stage_data, context)
    assert '三阶段聚合' in result['recommendations'][0]['reason']
```

### 3. 易于扩展
- **新增 Stage 优化规则**: 在 `rules/incremental/stage_optimization/` 添加新文件
- **新增状态表规则**: 在 `rules/incremental/state_table/` 添加新文件
- **新增 AP 模式**: 创建 `analyzers/ap_analyzer.py` + `rules/ap_mode/`
- **新增通用规则**: 在 `rules/common/` 添加

示例 - 添加新的 Stage 优化规则：
```python
# rules/incremental/stage_optimization/shuffle_optimization.py
class ShuffleOptimization:
    """新规则：Shuffle 优化"""
    
    name = "shuffle_optimization"
    category = "incremental/stage_optimization"
    
    def check(self, stage_data, context):
        # 检查逻辑
        pass
    
    def analyze(self, stage_data, context):
        # 分析逻辑
        pass

# 在 IncrementalAnalyzer 中注册
self.stage_rules.append(ShuffleOptimization())
```

### 4. 便于版本管理
```python
# 每个规则可以有版本信息和适用条件
class SingleDopAggregate:
    name = "single_dop_aggregate"
    version = "2.0"
    min_engine_version = "1.2"
    
    # 规则的变更历史
    changelog = {
        "2.0": "增加 Bloom Filter bits 检查",
        "1.5": "优化三阶段聚合检测逻辑",
        "1.0": "初始版本"
    }
    
    def is_applicable(self, context):
        """判断规则是否适用于当前环境"""
        engine_version = context.get('engine_version')
        return engine_version >= self.min_engine_version
```

## 迭代路径

### Phase 1: 基础架构 + Stage 优化（当前重点）
- ✅ 核心模块：parser, aligner, reporter
- ✅ IncrementalAnalyzer + 7 个 Stage 优化规则 (3.0-3.6)
  - 3.0 增量/全量判断
  - 3.1 单 DOP 聚合
  - 3.2 Hash Join
  - 3.3 TableSink DOP
  - 3.4 最大 DOP 检查
  - 3.5 Spilling 分析
  - 3.6 主动问题发现
- ✅ 基础报告生成

### Phase 2: 状态表优化（未来扩展）
- 📋 状态表规则模块 `rules/incremental/state_table/`
- 📋 6+ 个状态表优化规则
- 📋 需要 Claude 深度分析的规则框架
- 📋 与 IncrementalAnalyzer 集成

### Phase 3: AP 模式（未来）
- 📋 APAnalyzer 实现
- 📋 `rules/ap_mode/` 规则库
- 📋 AP 模式专属优化

### Phase 4: 通用增强
- 📋 数据倾斜高级检测
- 📋 多 SQL 对比分析
- 📋 历史趋势分析
- 📋 可视化报告

## 配置文件支持

```yaml
# config.yaml（可选）
analyzers:
  refresh:
    enabled: true
    rules:
      - single_dop_agg: 
          threshold_seconds: 12
          threshold_percent: 15
      - hash_join:
          threshold_seconds: 10
          threshold_percent: 8
  
  state_table:
    enabled: false  # 需要手动启用
    
output:
  format: json  # json, markdown, html
  verbose: true
```

## 向后兼容

保留简化版单文件脚本：
```
scripts/
├── analyze_job.py              # 新架构（推荐）
└── analyze_job_standalone.py   # 单文件版本（简单场景）
```

## 实施建议

1. **第一步**: 重构现有代码到新架构（Phase 1）
2. **第二步**: 补充测试用例和文档
3. **第三步**: 实现 Phase 2（状态表优化）
4. **第四步**: 收集反馈，优化 API

是否开始实施？
