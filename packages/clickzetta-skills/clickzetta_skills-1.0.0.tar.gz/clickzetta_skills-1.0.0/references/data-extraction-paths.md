# JSON 数据提取路径快速参考

本文档提供常用的 JSON 路径和计算模式。

## plan.json 关键路径

### 基本信息
```python
# SQL 文本
sql_text = plan['settings']['cz.sql.text']

# 版本信息
version = plan['build_info']['GitBranch']

# VC 模式
is_ap = plan['settings']['cz.inner.is.ap.vc'] == '1'

# 所有已配置参数
settings = plan['settings']
```

### Stage 信息
```python
# 所有 Stage
stages = plan['dml']['stages']

for stage in stages:
    stage_id = stage.get('id', stage.get('stageId'))
    operators = stage.get('operators', [])
```

### Operator 详细信息
```python
# 遍历 Operator
for op in stage['operators']:
    # TableSink
    if 'tableSink' in op:
        sink = op['tableSink']
        mode = sink.get('mode')  # OVERWRITE, APPEND
        sink_type = sink.get('type')  # PhysicalTableSink_DELTA
    
    # TableScan
    if 'tableScan' in op:
        scan = op['tableScan']
        schema = scan['schema']
        fields = [f['name'] for f in schema['fields']]
        # 检查 __incremental_delete 列
        is_append_only = '__incremental_delete' not in fields
    
    # HashAggregate
    if 'hashAgg' in op:
        agg = op['hashAgg']['aggregate']
        stage = agg.get('stage')  # P1, P2, FINAL, COMPLETE
        agg_calls = agg.get('aggregateCalls', [])
        
        for call in agg_calls:
            func = call['function']['function']
            func_name = func['name']  # SUM, COUNT, MIN, MAX, _DF_BF_COLLECT
            
            # BF bits
            if '_DF_BF_COLLECT' in func_name:
                props = func.get('properties', {}).get('properties', [])
                for prop in props:
                    if prop['key'] == 'bits':
                        bits = int(prop['value'])
    
    # Join
    if 'join' in op:
        join = op['join']
        join_type = join.get('joinType')  # BroadcastHashJoin, ShuffleHashJoin
    
    # Calc
    if 'calc' in op:
        calc = op['calc']
        expressions = calc.get('expressions', [])
        # 检查 UDF 或复杂函数
```

## job_profile.json 关键路径

### Stage 统计
```python
profile = profile_data['data']['jobSummary']

for stage_id, stage_data in profile['stageSummary'].items():
    # 时间
    start = int(stage_data['startTime'])
    end = int(stage_data['endTime'])
    elapsed_ms = end - start
    
    # DOP
    dop = 0
    for count in stage_data['taskCountDetail'].values():
        dop += int(float(count))
    
    # IO 统计
    io = stage_data['inputOutputStats']
    input_bytes = int(io['inputBytes'])
    output_bytes = int(io['outputBytes'])
    spill_bytes = int(io['spillingBytes'])
```

### Operator 统计
```python
# Operator 性能
for op_id, op_data in stage_data['operatorSummary'].items():
    # 耗时
    wall_time = op_data['wallTimeNs']
    max_ns = int(wall_time['max'])
    avg_ns = int(wall_time['avg'])
    
    max_ms = max_ns / 1_000_000
    avg_ms = avg_ns / 1_000_000
    
    # 倾斜比率
    skew = max_ms / avg_ms if avg_ms > 0 else 1.0
    
    # Spilling
    if 'spillStats' in op_data:
        spill = op_data['spillStats']
        # 详细的 spill 信息
```

## 常用计算模式

### 计算占比
```python
# Stage 占总体百分比
stage_pct = (stage_elapsed_ms / total_job_time) * 100

# Operator 占 Stage 百分比
op_pct = (op_max_ms / stage_elapsed_ms) * 100
```

### 判断触发条件
```python
# 耗时阈值
is_slow = elapsed_ms > 12000 or (elapsed_ms / total_time * 100) > 15

# DOP 差异
dop_ratio = current_dop / upstream_dop
is_dop_diff = dop_ratio < 0.5

# 数据量阈值
data_gb = bytes / (1024**3)
is_large = data_gb > 10
```

### 搜索 Pattern
```python
# 使用 JSON 字符串搜索
plan_str = json.dumps(stage)

# Join 算法
is_broadcast = 'BroadcastHashJoin' in plan_str or 'Broadcast' in plan_str
is_shuffle = 'ShuffleHashJoin' in plan_str

# Aggregate 阶段
has_p1 = 'P1' in plan_str or 'PARTIAL1' in plan_str
is_complete = 'COMPLETE' in plan_str

# 高成本函数
has_expensive = any(f in plan_str for f in 
    ['MULTI_RANGE_COLLECT', '_DF_BF_COLLECT', 'BF_COLLECT'])

# TableSink
has_tablesink = 'TableSink' in plan_str
is_overwrite = 'OVERWRITE' in plan_str
is_delta = 'PhysicalTableSink_DELTA' in plan_str
```

## 典型分析示例

### 找瓶颈 Operator
```python
# 按耗时排序
sorted_ops = sorted(operator_analysis, 
                   key=lambda x: x['max_time_ms'], 
                   reverse=True)

bottleneck = sorted_ops[0]
```

### 计算上游 DOP
```python
upstream_dops = [
    stage_metrics[sid]['dop'] 
    for sid in stage_metrics 
    if sid != current_stage_id
]
max_upstream_dop = max(upstream_dops) if upstream_dops else 0
```

### 检查参数是否已存在
```python
def should_recommend(param, value):
    if param not in settings:
        return True
    if settings[param] != value:
        return True
    return False
```

## 常见陷阱

### ❌ 错误做法
```python
# 仅从 profile 判断 Join 类型
# profile 中没有算法信息！
join_type = ???  # 无法获取

# 忽略参数检查
optimizations.append(...)  # 可能重复推荐
```

### ✅ 正确做法
```python
# 从 plan 获取算法
plan_str = json.dumps(stage['operators'])
is_broadcast = 'BroadcastHashJoin' in plan_str

# 从 profile 获取性能
elapsed = stage_data['endTime'] - stage_data['startTime']

# 检查参数
if 'cz.optimizer.enable.broadcast.hash.join' not in settings:
    recommend(...)
```
