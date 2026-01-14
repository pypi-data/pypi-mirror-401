#!/usr/bin/env python3
"""Aggregate 复用检查规则"""
import json
from typing import Dict
from rules.base_rule import BaseRule

class AggregateReuse(BaseRule):
    name = "aggregate_reuse"
    category = "incremental/state_table"
    description = "检查聚合计算是否利用了之前的结果"
    ALWAYS_INCREMENTAL = ['SUM', 'COUNT', 'sum', 'count']
    APPEND_ONLY_INCREMENTAL = ['MIN', 'MAX', 'min', 'max']
    INCREMENTAL_DELETE_COL = '__incremental_delete'
    
    def check(self, stage_data: Dict, context: Dict) -> bool:
        plan_str = json.dumps(stage_data.get('plan', {}))
        return 'HashAggregate' in plan_str or 'Aggregate' in plan_str
    
    def analyze(self, stage_data: Dict, context: Dict) -> Dict:
        stage_id = stage_data.get('stage_id', 'unknown')
        plan = stage_data.get('plan', {})
        settings = context.get('settings', {})
        findings, recommendations, insights = [], [], []
        
        agg_funcs = self._analyze_aggregates(plan)
        if not agg_funcs:
            return {'findings': findings, 'recommendations': recommendations, 'insights': insights}
        
        is_append_only = self._check_append_only_inputs(plan)
        has_incremental_marker = self._check_incremental_markers(plan)
        
        for func_name in agg_funcs:
            upper_name = func_name.upper()
            if any(f in upper_name for f in self.ALWAYS_INCREMENTAL):
                if not has_incremental_marker:
                    findings.append(self.create_finding('AGG_NOT_REUSING', stage_id, 'WARNING',
                        f"{func_name} 未复用之前的计算结果"))
            elif any(f in upper_name for f in self.APPEND_ONLY_INCREMENTAL):
                if is_append_only and not has_incremental_marker:
                    findings.append(self.create_finding('AGG_NOT_REUSING', stage_id, 'INFO',
                        f"{func_name} 在 append-only 场景下未复用之前的计算结果"))
                    if not settings.get('cz.optimizer.incremental.append.only.tables'):
                        insights.append(self.create_insight(
                            f"Stage {stage_id}: 建议为 append-only 表添加 hint", stage_id))
        
        if has_incremental_marker:
            insights.append(self.create_insight(f"Stage {stage_id}: 聚合计算已利用增量特性", stage_id))
        
        return {'findings': findings, 'recommendations': recommendations, 'insights': insights}
    
    def _analyze_aggregates(self, plan: Dict) -> list:
        funcs = []
        try:
            for op in plan.get('operators', []):
                if 'hashAgg' in op:
                    for call in op['hashAgg'].get('aggregate', {}).get('aggregateCalls', []):
                        name = call.get('function', {}).get('function', {}).get('name', '')
                        if name:
                            funcs.append(name)
        except:
            pass
        return funcs
    
    def _check_append_only_inputs(self, plan: Dict) -> bool:
        try:
            for op in plan.get('operators', []):
                if 'tableScan' in op:
                    cols = [f.get('name', '') for f in op['tableScan'].get('schema', {}).get('fields', [])]
                    if self.INCREMENTAL_DELETE_COL in cols:
                        return False
            return True
        except:
            return False
    
    def _check_incremental_markers(self, plan: Dict) -> bool:
        plan_str = json.dumps(plan).lower()
        return any(m in plan_str for m in ['incremental', 'delta', 'state', 'partial_result'])
