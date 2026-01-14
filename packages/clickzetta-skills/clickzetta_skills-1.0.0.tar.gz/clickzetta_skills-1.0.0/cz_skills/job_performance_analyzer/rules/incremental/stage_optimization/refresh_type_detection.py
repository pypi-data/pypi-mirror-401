#!/usr/bin/env python3
"""增量/全量 REFRESH 判断规则"""
import json
from typing import Dict
from rules.base_rule import BaseRule

class RefreshTypeDetection(BaseRule):
    name = "refresh_type_detection"
    category = "incremental/stage_optimization"
    description = "判断 REFRESH SQL 是增量还是全量刷新"
    INTERMEDIATE_PATTERNS = ['__incr__', '__state__', '__incr_state__', '__temp__']
    
    def check(self, stage_data: Dict, context: Dict) -> bool:
        plan = stage_data.get('plan', {})
        return 'TableSink' in json.dumps(plan)
    
    def analyze(self, stage_data: Dict, context: Dict) -> Dict:
        stage_id = stage_data.get('stage_id', 'unknown')
        plan = stage_data.get('plan', {})
        plan_str = json.dumps(plan)
        findings, recommendations, insights = [], [], []
        
        if any(p in plan_str for p in self.INTERMEDIATE_PATTERNS):
            return {'findings': findings, 'recommendations': recommendations, 
                   'insights': insights, 'refresh_type': None}
        
        is_delta = 'PhysicalTableSink_DELTA' in plan_str
        is_overwrite = 'OVERWRITE' in plan_str
        
        if is_overwrite and not is_delta:
            refresh_type = 'FULL'
            findings.append(self.create_finding('FULL_REFRESH', stage_id, 'WARNING',
                'OVERWRITE 且非 DELTA sink，判定为全量刷新'))
            recommendations.append(self.create_recommendation(
                'cz.optimizer.explain.incremental.plan', 'true', 1,
                f'Stage {stage_id}: 全量刷新，需诊断原因', 'HIGH',
                warning='请执行 EXPLAIN REFRESH 查看退化原因'))
        elif is_delta:
            refresh_type = 'INCREMENTAL'
            insights.append(self.create_insight(f"Stage {stage_id}: 检测到增量刷新 (DELTA sink)", stage_id))
        else:
            refresh_type = 'UNKNOWN'
        
        return {'findings': findings, 'recommendations': recommendations,
               'insights': insights, 'refresh_type': refresh_type}
