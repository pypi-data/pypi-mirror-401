# Clickzetta Skills

Clickzetta 系统技能工具集 - 包含性能分析、诊断等专业工具的 Python 包。

## 包含的技能

### 1. Job Performance Analyzer (作业性能分析器)

自动诊断 Clickzetta Job 性能问题的工具，分析执行计划(plan.json)和运行概况(job_profile.json)，识别瓶颈并给出参数优化建议。

**命令**: `cz-analyze-job`

**支持场景**:
- 增量计算(REFRESH)
- AP模式
- GP模式
- Compaction
- 各类SQL场景

**已实现规则**:
- Stage/Operator 级别优化 (7条规则)
- 状态表优化 (6条规则)

## 安装

### 使用 Makefile（推荐）

```bash
# 进入项目目录
cd job-performance-analyzer

# 安装
make install

# 开发模式安装（可编辑）
make install-dev

# 卸载
make uninstall
```

### 手动安装

```bash
# 构建
python3 -m build

# 安装
pip3 install dist/clickzetta_skills-*.whl
```

## 使用

### Job Performance Analyzer

```bash
# 分析性能问题
cz-analyze-job plan.json job_profile.json ./output

# 查看帮助
cz-analyze-job
```

## 开发

### 添加新技能

1. 在 `cz_skills/` 下创建新的技能目录
2. 实现技能逻辑
3. 在 `pyproject.toml` 的 `[project.scripts]` 中添加命令入口
4. 在 `cz_skills/__init__.py` 的 `AVAILABLE_SKILLS` 中注册

示例结构：
```
cz_skills/
├── __init__.py
├── job_performance_analyzer/
│   ├── __init__.py
│   ├── __main__.py
│   └── ...
└── your_new_skill/
    ├── __init__.py
    ├── __main__.py
    └── ...
```

### 运行测试

```bash
make test
```

### 构建发布

```bash
# 构建
make build

# 上传到 PyPI（需要配置 twine）
make upload
```

## 许可证

Apache-2.0

## 作者

Clickzetta Team
