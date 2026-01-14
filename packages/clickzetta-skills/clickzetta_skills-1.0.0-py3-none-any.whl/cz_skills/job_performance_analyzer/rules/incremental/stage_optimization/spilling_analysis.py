#!/usr/bin/env python3
"""Spilling 分析规则"""
from typing import Dict
from rules.base_rule import BaseRule

class SpillingAnalysis(BaseRule):
    name = "spilling_analysis"
    category = "incremental/stage_optimization"
    description = "检测内存溢出到磁盘的情况"
    STAGE_SPILL_THRESHOLD_GB = 1.0
    IGNORABLE_SPILL_PATTERNS = ['ShuffleWrite', 'ShuffleExchange']
    
    def check(self, stage_data: Dict, context: Dict) -> bool:
        spill_bytes = stage_data.get('metrics', {}).get('spill_bytes', 0)
        return spill_bytes / (1024**3) > self.STAGE_SPILL_THRESHOLD_GB
    
    def analyze(self, stage_data: Dict, context: Dict) -> Dict:
        stage_id = stage_data.get('stage_id', 'unknown')
        metrics = stage_data.get('metrics', {})
        profile = stage_data.get('profile', {})
        spill_gb = metrics.get('spill_bytes', 0) / (1024**3)
        
        findings = [self.create_finding('SPILLING', stage_id, 'MEDIUM',
            f"Stage Spilling: {spill_gb:.2f} GB", {'spill_gb': spill_gb})]
        insights = []
        
        if 'operatorSummary' in profile:
            for op_id, op_data in profile['operatorSummary'].items():
                if 'spillStats' in op_data or 'inputOutputStats' in op_data:
                    is_ignorable = any(p in op_id for p in self.IGNORABLE_SPILL_PATTERNS)
                    msg = f"Stage {stage_id}: {op_id} 有 Spill" + (" (可忽略)" if is_ignorable else "，需关注")
                    insights.append(self.create_insight(msg, stage_id))
        
        if spill_gb > self.STAGE_SPILL_THRESHOLD_GB * 2:
            insights.append(self.create_insight(
                f"Stage {stage_id}: Spilling 较大 ({spill_gb:.2f} GB)，建议检查数据倾斜或内存配置", stage_id))
        
        return {'findings': findings, 'recommendations': [], 'insights': insights}
