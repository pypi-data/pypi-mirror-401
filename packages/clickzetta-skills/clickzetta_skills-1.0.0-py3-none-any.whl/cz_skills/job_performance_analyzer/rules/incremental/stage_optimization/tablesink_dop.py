#!/usr/bin/env python3
"""TableSink DOP 优化规则"""
import json
from typing import Dict, List
from rules.base_rule import BaseRule

class TableSinkDop(BaseRule):
    name = "tablesink_dop"
    category = "incremental/stage_optimization"
    description = "检测 TableSink Stage 的 DOP 是否被自动调小"
    TIME_THRESHOLD_MS = 10000
    DOP_RATIO_THRESHOLD = 0.5
    
    def check(self, stage_data: Dict, context: Dict) -> bool:
        metrics = stage_data.get('metrics', {})
        plan = stage_data.get('plan', {})
        if 'TableSink' not in json.dumps(plan):
            return False
        return metrics.get('elapsed_ms', 0) >= self.TIME_THRESHOLD_MS
    
    def analyze(self, stage_data: Dict, context: Dict) -> Dict:
        stage_id = stage_data.get('stage_id', 'unknown')
        metrics = stage_data.get('metrics', {})
        all_stages = context.get('all_stage_metrics', {})
        settings = context.get('settings', {})
        current_dop = metrics.get('dop', 0)
        
        findings, recommendations, insights = [], [], []
        upstream_dops = [m.get('dop', 0) for sid, m in all_stages.items() if sid != stage_id and m.get('dop', 0) > 0]
        max_upstream = max(upstream_dops) if upstream_dops else 0
        
        if max_upstream > 0:
            dop_ratio = current_dop / max_upstream
            if dop_ratio >= self.DOP_RATIO_THRESHOLD or current_dop > max_upstream:
                insights.append(self.create_insight(f"Stage {stage_id}: DOP={current_dop} 与上游接近，无需调整", stage_id))
            else:
                findings.append(self.create_finding('TABLESINK_DOP', stage_id, 'MEDIUM',
                    f"TableSink DOP={current_dop} 远小于上游 (max={max_upstream})",
                    {'current_dop': current_dop, 'max_upstream_dop': max_upstream}))
                param = 'cz.sql.enable.dag.auto.adaptive.split.size'
                if param not in settings or settings.get(param) != 'false':
                    recommendations.append(self.create_recommendation(param, 'false', 2,
                        f"Stage {stage_id}: TableSink DOP={current_dop} 可能被自动调小", 'MEDIUM',
                        settings.get(param), warning="该参数影响全局"))
        return {'findings': findings, 'recommendations': recommendations, 'insights': insights}
