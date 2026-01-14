# 增量计算优化完整指南

本文档包含 ClickZetta 增量计算（REFRESH SQL）的完整优化规则。

---

## 4. 增量计算 REFRESH SQL 优化

增量 job 任务优化分两大块：
1. **从运行的 stage/operator 算子级别优化（4.1）**
2. **优化状态表（4.2）**

---

## 4.1 增量 Stage/Operator 级别优化

### 4.1.1 增量 refresh vs 全量 refresh

**目的**：判断 REFRESH 是增量还是全量

**判断方法**：
1. 从 `plan.json` 找到 REFRESH 的目标表
2. 定位对应的 TableSink 算子，获取 `table.path`
3. 判断规则（基于 `path` 和 `overwrite`）：
   - **如果** `path` 是 4 元组且最后一个元素是 `__delta__` → **增量 REFRESH**（写入 delta 文件）
   - **如果** `path` 是 3 元组且 `overwrite=false` → **增量 REFRESH**
   - **其他情况**（3 元组且 `overwrite=true`）→ **全量 REFRESH**

**path 格式说明**：
- **3元组**：`[workspace, namespace, table_name]` - 例如 `['gic_prod', 'kscdm', 'dim_ks_live_daily']`
- **4元组**：`[workspace, namespace, table_name, '__delta__']` - 例如 `['gic_prod', 'kscdm', 'dim_ks_live_daily', '__delta__']`

**注意**：忽略中间表（table_name 包含 `__incr__`、`__state__`、`__temp__` 等 pattern），这些是中间状态表。

**代码示例**：
```python
# 从 TableSink 中获取 path 和 overwrite 标志
table_sink = stage['operators'][i]['tableSink']
path = table_sink['table']['path']  # 列表格式
overwrite = table_sink.get('overwrite', True)

# 判断逻辑
if len(path) == 4 and path[-1] == '__delta__':
    refresh_type = "增量"  # 写入 delta 文件
elif len(path) == 3 and not overwrite:
    refresh_type = "增量"  # overwrite=false
else:
    refresh_type = "全量"  # 3元组且 overwrite=true

# 提取表名（在 path[2]）
table_name = path[2]
```

---

### 4.1.2 单 DOP Aggregate Stage 优化

**触发条件**（必须**全部**满足）：
1. Stage 的 `dop = 1`
2. Stage 耗时 **> 12秒** 或 占总耗时 **> 15%**
3. Stage 包含 **HashAggregate** 算子
4. 聚合函数包含昂贵函数：`MULTI_RANGE_COLLECT`, `_DF_BF_COLLECT`, `BF_COLLECT`, `DF_BF_COLLECT`
5. **聚合状态是 Final 或 Complete**（表示最后一个聚合阶段）
6. **上游 stage 没有 P2 状态**（说明当前只有 2 阶段聚合，没有开启 3 阶段）

**判断逻辑**：
- 如果当前 stage 的 aggregate 是 **Final** 或 **Complete** 状态
- 且上游 stage **没有 P2/PARTIAL2** 状态
- 说明当前只有 **2 阶段聚合**（P1 → Final），需要优化为 **3 阶段**（P1 → P2 → Final）

**优化建议**：

1. **开启三阶段聚合**（如果未开启）：
   ```sql
   set cz.optimizer.incremental.df.three.phase.agg.enable = true;
   ```
   注意：如果已有 `cz.optimizer.df.enable.three.phase.agg=true`，则不需要重复设置

2. **禁用 one-pass 聚合**（如果聚合退化为 Complete）：
   ```sql
   set cz.optimizer.enable.one.pass.agg = false;
   ```

3. **调整 BF bits 阈值**（如果 bits 在 512M-1G 范围内）：
   ```sql
   set cz.optimizer.df.three.phase.agg.bf.width.threshold = <bits值>;
   ```
   - 如果 `bits >= 536870912` 且 `bits < 1073741824`，需要设置此参数
   - 默认阈值是 1073741824，小于此值不会生成 3 阶段
   - 如果 `bits < 536870912`，不建议修改此参数

**代码示例**：
```python
# 检查当前 stage 的聚合状态
has_final = 'FINAL' in aggregate_mode
has_complete = 'Complete' in aggregate_mode

# 检查上游 stage 是否有 P2
upstream_has_p2 = False
for upstream_stage in upstream_stages:
    if 'P2' in upstream_aggregate_mode or 'PARTIAL2' in upstream_aggregate_mode:
        upstream_has_p2 = True
        break

# 判断是否需要优化
if (has_final or has_complete) and not upstream_has_p2:
    # 当前只有 2 阶段，需要开启 3 阶段优化
    recommend_three_phase_agg = True
```

---

### 4.1.3 Hash Join 优化

**目的**：优化 Hash Join 算法选择

**触发条件**：
**IF** 参数不存在 **OR** 当前值 < bits：
```sql
-- 推荐
set cz.optimizer.df.three.phase.agg.bf.width.threshold = <bits值>;
```

**ELSE IF** `bits < 536870912`（< 512M）：
- **不推荐**修改此参数（bits 太小）

#### 步骤 4: 检查上游 Aggregate P2

**IF** Final Aggregate 仍然很慢：
- 检查上游 Stage 是否缺失 **Aggregate P2**（PARTIAL2）
- 如果缺失，回到步骤 1-3 检查上游 Stage

---

### 4.1.3 Hash Join 优化

**触发条件**：
1. Stage 耗时 **> 10秒** 或 占总耗时 **> 8%**
2. Stage 包含 Join operator
3. Join 耗时 **> 30%** 的 Stage 时间

**分析方法**：
- Join 算法：从 `plan.json` 获取
- 数据量/Shuffle 量：从 `job_profile.json` 获取

**优化建议**：

**IF** Join 算法 = `Broadcast Hash Join`  
**AND** Broadcast/Shuffle 数据量异常大：

搜索 settings 中 `cz.optimizer.enable.broadcast.hash.join`：

**IF** 参数不存在 **OR** 值 = `true`：
```sql
-- 推荐
set cz.optimizer.enable.broadcast.hash.join = false;
```

**代码示例**：
```python
plan_str = json.dumps(stage['operators'])
is_broadcast = 'BroadcastHashJoin' in plan_str or 'Broadcast' in plan_str
```

---

### 4.1.4 包含 TableSink 的 Stage DOP 优化

**触发条件**（必须**全部**满足）：
1. Stage 包含 **TableSink** 算子
2. Stage 耗时 **> 10秒**
3. Stage DOP **与上游 DOP 差异较大**

**不应推荐的情况**：
- Stage **不包含** TableSink 算子
- Stage DOP 与上游 DOP 接近（≥ 上游max * 0.5）
- Stage DOP **已大于**上游 DOP

**原因推断**：
系统可能根据**目标表文件大小**自动调整了 DOP。

**优化建议**：

计算上游最大 DOP：
```python
upstream_dops = [metrics['dop'] for sid, metrics in stages if sid != current_stage]
max_upstream = max(upstream_dops)
```

**IF** `current_dop < max_upstream * 0.5` **AND** `current_dop <= max_upstream`：

搜索 settings 中 `cz.sql.enable.dag.auto.adaptive.split.size`：

**IF** 参数不存在 **OR** 值 = `true`：
```sql
-- 推荐
set cz.sql.enable.dag.auto.adaptive.split.size = false;
```

⚠️ **警告**：此参数影响全局，请谨慎使用。

---

### 4.1.5 最大 DOP 提示

**DAG 限制**：
- Map 最大 DOP = `4096`
- Reduce 最大 DOP = `2048`

**原则**：
- 达到这些限制通常**不是问题**
- **除非**用户显式调整过这些参数：
  - `cz.optimizer.mapper.stage.max.dop`
  - `cz.optimizer.reducer.stage.max.dop`

**处理方式**：
```python
if stage_dop >= 4096 or stage_dop >= 2048:
    # 检查是否用户主动设置了 max dop 参数
    if 'cz.optimizer.mapper.stage.max.dop' in settings or \
       'cz.optimizer.reducer.stage.max.dop' in settings:
        # 可能需要分析
        pass
    else:
        # 达到系统限制，这是正常的
        print(f"Stage {stage_id} DOP达到系统限制，这是正常的")
```

---

### 4.1.6 SpillingBytes 分析

**分析级别**：
1. **Stage 级别** - 总 Spill 大小
2. **Operator 级别** - 可以看到 `opId` 的 spill stats

**数据提取**：
```python
# Stage 级别
spill_bytes = stage_data['inputOutputStats']['spillingBytes']

# Operator 级别
for op_id, op_data in stage_data['operatorSummary'].items():
    if 'spillStats' in op_data:
        op_spill = op_data['spillStats']
        # 分析具体算子的 spilling
```

**注意**：
- **Shuffle Write 的 Spill 可能可以忽略**
- 重点关注其他算子的 Spilling

**分析输出**：
```python
if spill_bytes > 1024**3:  # > 1GB
    print(f"Stage {stage_id} Spilling: {spill_bytes/(1024**3):.2f} GB")
    # 分析哪个 operator 导致
    for op_id, op_data in operators:
        if has_spill(op_data):
            print(f"  Operator {op_id}: {op_spill} bytes")
```

---

### 4.1.7 主动问题发现（**必须执行**）

**要求**：
- **不允许**"没有发现问题"的结论
- 必须遍历**所有 Stage**
- 对耗时较长的 Stage 主动分析原因

**分析步骤**：

1. **找出 Top 耗时 Stage**（至少 Top 5）

2. **对每个 Stage 分析**：
   ```python
   # a. 找瓶颈 Operator
   bottleneck_op = max(operators, key=lambda op: op['max_time_ms'])
   
   # b. 判断原因
   if bottleneck_op['skew_ratio'] > 5.0:
       reason = "数据倾斜严重"
       suggestion = "SQL 改写或数据预处理"
   
   elif bottleneck_op['stage_pct'] > 80:
       reason = "单个 Operator 占主导"
       suggestion = "检查算子逻辑或数据分布"
   
   elif stage_dop <= 10:
       reason = "DOP 较低"
       suggestion = "检查是否需要提高并行度"
   
   elif stage_spill > 1GB:
       reason = f"Spilling 较大: {spill_gb:.2f} GB"
       suggestion = "检查内存配置或数据倾斜"
   ```

3. **输出分析结果**：
   ```
   [分析] Stage stg11: 212.7s (77.6%)
     瓶颈 Operator: Calc97
       耗时: 207.9s (97.7% of Stage)
       倾斜: 57.6x
     → 原因: 数据倾斜严重
     → 建议: SQL 改写或数据预处理
   ```

---

## 4.2 状态表优化

### 4.2.1 判断是否增量刷新

**目的**：确认当前 job 是否为增量刷新

使用 **4.1.1** 的方法判断。

---

### 4.2.2 非增量原因诊断

**触发条件**：
- Job **非增量刷新**（根据 4.2.1 判断）

**推荐操作**：

**IF** job 非增量刷新：
```sql
-- 推荐设置以下 flag 后重新执行 EXPLAIN REFRESH
set cz.optimizer.explain.incremental.plan = true;
set cz.optimizer.print.non.incremental.reason = true;
set cz.optimizer.print.non.incremental.reason_msg_max_length = 100000;
set cz.optimizer.incremental.force.incremental = true;
```

**THEN** 执行：
```sql
EXPLAIN REFRESH <表名>;
```

查看输出以了解为什么退化为全量刷新。

---

### 4.2.3 Row number=1 Pattern 检查

**触发条件**：
- 当前任务执行速度**不符合预期**

**检查步骤**：

#### 步骤 1: 搜索 `row number = 1` pattern

在 plan 中搜索是否包含 ROW_NUMBER 相关的 pattern（可能在 Filter 或 Calc 中）。

#### 步骤 2: 判断输入表是否 Append-only

**方法**：检查 TableScan operator 中是否包含 `__incremental_delete` 列

**IF** 不包含此列 → 表是 **Append-only**

```python
for op in stage['operators']:
    if 'tableScan' in op:
        schema = op['tableScan']['schema']
        cols = [field['name'] for field in schema['fields']]
        
        if '__incremental_delete' not in cols:
            is_append_only = True
```

#### 步骤 3: 检查 Window 算法

**IF** 输入表是 Append-only  
**BUT** Window 没有基于 `rn=1` 的结果继续计算：

搜索 settings 中 `cz.optimizer.incremental.window.sd.to.sd.rule.enable`：

**IF** 参数不存在 **OR** 值 = `true`：
```sql
-- 推荐
set cz.optimizer.incremental.window.sd.to.sd.rule.enable = false;
```

**THEN** 重新运行

**IF** 任务仍退化为全量刷新：
- 回到 **4.2.2** 继续分析原因

#### 步骤 4: 检查表 Property

**IF** 输入表是 Append-only：

检查表是否具备以下 property：
```sql
-- 方法 1: 表 property
SHOW CREATE TABLE <表名>;
-- 查找: 'incr.append.only.table' = 'true'

-- 方法 2: Job parameter
-- 查找 settings: cz.optimizer.incremental.append.only.tables = 'xxx'
```

**IF** 没有设置：
```
⚠️ 提醒用户添加：
ALTER TABLE <表名> SET TBLPROPERTIES ('incr.append.only.table' = 'true');
-- 或
set cz.optimizer.incremental.append.only.tables = '<表名>';
```

---

### 4.2.4 Append-only Scan 检查

**目的**：检查当前 query 是否还包含 Append-only 的 scan，并预判算法是否最优

**检查方法**：

使用 **4.2.3 步骤 2** 的方法检查所有 TableScan。

**预判**：
- **IF** 有 Append-only scan **AND** 使用了复杂的 Join/Aggregate
- → 可能算法不是最优的
- → 考虑是否可以利用 Append-only 特性简化计算

**示例输出**：
```
发现 Append-only scan: table_a (无 __incremental_delete 列)
当前使用算法: Hash Join + Full Aggregate
建议: 考虑是否可以利用 Append-only 特性进行增量计算
```

---

### 4.2.5 状态表启用建议

**检查步骤**：

#### 步骤 1: 检查是否包含增量临时状态表

在 plan 中搜索表名包含状态表 pattern 的表（如 `__state__`, `__incr_state__` 等）。

#### 步骤 2: 判断是否值得存储中间状态

**考虑因素**：

1. **是否需要状态**（参考流计算的带状态计算定义）：
   - 有聚合计算（SUM, COUNT, MIN, MAX）
   - 有 Window 函数
   - 有 JOIN（需要保存 Join 状态）

2. **状态表是否会过大**：
   - 根据每一步的 stats 信息（inputBytes, outputBytes）
   - 根据输入表的增量数据大小
   - 判断状态表大小是否可接受

**决策逻辑**：
```python
# 计算中间结果大小
intermediate_size = stage_output_bytes

# 计算增量数据大小
delta_size = input_table_delta_bytes

# 判断
if intermediate_size < delta_size * 10:  # 状态表不会太大
    if has_aggregate or has_window or has_join:
        recommend_state_table = True
```

#### 步骤 3: 推荐参数

**IF** 不包含状态表 **AND** 值得存储中间状态：

搜索 settings 中 `cz.optimizer.incremental.enable.state.table`：

**IF** 参数不存在 **OR** 值 = `false`：
```sql
-- 推荐
set cz.optimizer.incremental.enable.state.table = true;
```

**附加说明**：
```
状态表大小预估: <size> GB
增量数据大小: <delta_size> GB
建议: 开启状态表可以避免重复计算
```

---

### 4.2.6 Aggregate 复用检查

**目的**：检查 Aggregate 计算是否利用了之前的计算结果

**期望行为**：
- **SUM, COUNT**: 无论如何都应尽量使用之前的结果
- **MIN, MAX**: 在 Append-only 情况下应尽量使用之前的结果

**检查步骤**：

#### 步骤 1: 找到 Aggregate operator

```python
for op in stage['operators']:
    if 'hashAgg' in op:
        agg_calls = op['hashAgg']['aggregate']['aggregateCalls']
        for call in agg_calls:
            func_name = call['function']['function']['name']
            # 检查是否是 SUM, COUNT, MIN, MAX
```

#### 步骤 2: 检查是否有增量计算标识

在 Aggregate 的 properties 或上游 Scan 中查找增量计算相关标识。

**IF** 发现没有复用之前的结果：

#### 步骤 3: 检查是否存在状态

使用 **4.2.5** 的方法检查状态表。

**IF** 状态存在：

#### 步骤 4: 检查是否有 Append-only 输入

使用 **4.2.3 步骤 2** 的方法。

**IF** 是 Append-only **BUT** 缺少系统 hint：

```
⚠️ 建议补充 hint:
ALTER TABLE <表名> SET TBLPROPERTIES ('incr.append.only.table' = 'true');
```

**示例输出**：
```
发现 Aggregate: SUM(amount)
检查: 没有利用之前的计算结果
原因: 输入表 orders 是 Append-only 但缺少 hint
建议: 添加 'incr.append.only.table' = 'true' property
```

---

### 4.2.7 Calc 状态优化

**触发条件**（必须**全部**满足）：
1. Calc operator 占其所属 Stage 耗时 **> 30%**
2. 该 Stage 占整体耗时 **> 10%**

**检查步骤**：

#### 步骤 1: 识别高耗时 Calc

```python
for op in operator_analysis:
    if 'Calc' in op['operator_id']:
        if op['stage_pct'] > 30 and stage_total_pct > 10:
            # 触发优化检查
```

#### 步骤 2: 分析 Calc 内容

在 plan 中查看 Calc operator 的详细内容：

```python
calc_op = find_operator(plan, 'calc')
expressions = calc_op['calc']['expressions']

# 检查是否有高成本函数
for expr in expressions:
    if is_udf(expr) or is_complex_function(expr):
        has_heavy_calc = True
```

#### 步骤 3: 特别关注 UDF

**IF** Calc 包含**用户自定义函数（UDF）**：
- UDF 通常耗时较长
- 非常适合通过状态表优化

#### 步骤 4: 推荐参数

**IF** 发现高耗时 Calc（特别是包含 UDF）：

搜索 settings 中 `cz.optimizer.incremental.create.rule.based.table.on.heavy.calc`：

**IF** 参数不存在 **OR** 值 = `false`：
```sql
-- 推荐
set cz.optimizer.incremental.create.rule.based.table.on.heavy.calc = true;
```

**示例输出**：
```
发现高耗时 Calc: Calc25
  Stage 占比: 45.2%
  整体占比: 12.3%
  包含 UDF: my_custom_transform()
建议: 开启 Calc 状态优化
  set cz.optimizer.incremental.create.rule.based.table.on.heavy.calc = true;
```

---

## 总结：参数推荐原则

### ❌ 禁止行为

1. **不要给没有依据的参数**
2. **不要凭空给 flag**
3. **不要推荐已存在且正确的参数**

### ✅ 必须做到

1. **仅在发现实际问题时才建议参数**
2. **每个建议必须有明确的触发条件**
3. **每个建议必须引用实际数据作为证据**
4. **必须检查 settings 避免重复建议**

### 📋 其他可能有用的参数

对于那些**可能**有用但没有明确问题证据的参数：
- 单独列出
- **不要给强烈建议**
- 让用户自行决定是否重跑
