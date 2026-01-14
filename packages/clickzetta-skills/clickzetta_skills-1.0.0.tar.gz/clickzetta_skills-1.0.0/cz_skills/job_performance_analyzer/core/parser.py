#!/usr/bin/env python3
"""核心解析器 - 解析 plan.json 和 job_profile.json"""
import json
from typing import Dict, Any

class PlanProfileParser:
    def __init__(self, plan_file: str, profile_file: str):
        with open(plan_file, 'r', encoding='utf-8') as f:
            self.plan = json.load(f)
        with open(profile_file, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
            if 'data' in profile_data:
                self.profile = profile_data.get('data', {}).get('jobSummary', {})
            else:
                self.profile = profile_data.get('jobSummary', profile_data)
        self._parsed_data = None
    
    def parse(self) -> Dict[str, Any]:
        if self._parsed_data:
            return self._parsed_data
        settings = dict(self.plan.get('settings', {}))
        sql_text = settings.get('cz.sql.text', '')
        self._parsed_data = {
            'sql_info': {
                'text': sql_text,
                'is_refresh': 'REFRESH' in sql_text.upper(),
                'is_compaction': 'COMPACTION' in sql_text.upper() or 'OPTIMIZE' in sql_text.upper(),
            },
            'version_info': {
                'git_branch': self.plan.get('build_info', {}).get('GitBranch', 'Unknown'),
            },
            'vc_mode': {
                'is_ap': settings.get('cz.inner.is.ap.vc', '0') == '1',
                'mode': 'AP' if settings.get('cz.inner.is.ap.vc', '0') == '1' else 'GP',
            },
            'settings': settings,
            'plan_stages': self._parse_plan_stages(),
            'profile_stages': self._parse_profile_stages(),
        }
        return self._parsed_data
    
    def _parse_plan_stages(self) -> Dict[str, Dict]:
        stages = {}
        if 'dml' in self.plan and 'stages' in self.plan['dml']:
            for stage in self.plan['dml']['stages']:
                stage_id = stage.get('id', stage.get('stageId'))
                if stage_id:
                    stages[stage_id] = stage
        return stages
    
    def _parse_profile_stages(self) -> Dict[str, Dict]:
        stages = {}
        if 'stageSummary' in self.profile:
            for stage_id, stage_data in self.profile['stageSummary'].items():
                stages[stage_id] = stage_data
        return stages
    
    def is_refresh_sql(self) -> bool:
        return 'REFRESH' in self.plan.get('settings', {}).get('cz.sql.text', '').upper()
    
    def is_ap_mode(self) -> bool:
        return self.plan.get('settings', {}).get('cz.inner.is.ap.vc', '0') == '1'
