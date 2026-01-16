"""
评估框架模块

提供场景评估的基础框架和通用功能，包括：
- 评估器基类：定义标准评估接口
- 评估管道：管理评估流程和结果
- 评估报告：生成标准化评估报告
- 结果处理：评估结果的存储和分析
- 配置管理：评估参数和配置管理
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union, Protocol
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import json
import time
from datetime import datetime
import logging

class EvaluationType(Enum):
    """评估类型"""
    ECONOMIC = "economic"
    RELIABILITY = "reliability"
    ENVIRONMENTAL = "environmental"
    RISK = "risk"
    SOCIAL = "social"
    COMPREHENSIVE = "comprehensive"

class EvaluationStatus(Enum):
    """评估状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class EvaluationContext:
    """评估上下文"""
    scenario_id: str
    scenario_data: Dict[str, Any]
    evaluation_type: EvaluationType
    config: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EvaluationResult:
    """评估结果基类"""
    context: EvaluationContext
    status: EvaluationStatus
    metrics: Dict[str, float]
    indicators: Dict[str, Any]
    execution_time: float
    created_at: datetime = field(default_factory=datetime.now)
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'context': {
                'scenario_id': self.context.scenario_id,
                'evaluation_type': self.context.evaluation_type.value,
                'timestamp': self.context.timestamp.isoformat(),
                'metadata': self.context.metadata
            },
            'status': self.status.value,
            'metrics': self.metrics,
            'indicators': self.indicators,
            'execution_time': self.execution_time,
            'created_at': self.created_at.isoformat(),
            'error_message': self.error_message
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvaluationResult':
        """从字典创建结果"""
        context_data = data['context']
        context = EvaluationContext(
            scenario_id=context_data['scenario_id'],
            scenario_data={},  # 需要从其他地方恢复
            evaluation_type=EvaluationType(context_data['evaluation_type']),
            config={},  # 需要从其他地方恢复
            timestamp=datetime.fromisoformat(context_data['timestamp']),
            metadata=context_data['metadata']
        )
        
        result = cls(
            context=context,
            status=EvaluationStatus(data['status']),
            metrics=data['metrics'],
            indicators=data['indicators'],
            execution_time=data['execution_time'],
            created_at=datetime.fromisoformat(data['created_at']),
            error_message=data.get('error_message')
        )
        
        return result

class Evaluator(ABC):
    """评估器抽象基类"""
    
    def __init__(self, name: str, evaluation_type: EvaluationType):
        self.name = name
        self.evaluation_type = evaluation_type
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    @abstractmethod
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行评估"""
        pass
    
    @abstractmethod
    def validate_input(self, context: EvaluationContext) -> bool:
        """验证输入"""
        pass
    
    @abstractmethod
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        pass
    
    def preprocess(self, context: EvaluationContext) -> EvaluationContext:
        """预处理"""
        return context
    
    def postprocess(self, result: EvaluationResult) -> EvaluationResult:
        """后处理"""
        return result

class EvaluationPipeline:
    """评估管道"""
    
    def __init__(self, name: str):
        self.name = name
        self.evaluators: Dict[EvaluationType, Evaluator] = {}
        self.execution_order: List[EvaluationType] = []
        self.conditional_evaluators: List[tuple[Callable[[EvaluationContext], bool], Evaluator]] = []
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    def add_evaluator(self, evaluator: Evaluator, condition: Optional[Callable[[EvaluationContext], bool]] = None):
        """添加评估器"""
        if condition:
            self.conditional_evaluators.append((condition, evaluator))
        else:
            self.evaluators[evaluator.evaluation_type] = evaluator
            if evaluator.evaluation_type not in self.execution_order:
                self.execution_order.append(evaluator.evaluation_type)
    
    def remove_evaluator(self, evaluation_type: EvaluationType):
        """移除评估器"""
        if evaluation_type in self.evaluators:
            del self.evaluators[evaluation_type]
            self.execution_order.remove(evaluation_type)
    
    def execute(self, context: EvaluationContext) -> Dict[EvaluationType, EvaluationResult]:
        """执行评估管道"""
        results = {}
        start_time = time.time()
        
        self.logger.info(f"开始执行评估管道: {self.name}")
        self.logger.info(f"场景ID: {context.scenario_id}")
        self.logger.info(f"评估类型: {context.evaluation_type.value}")
        
        try:
            # 执行无条件评估器
            for eval_type in self.execution_order:
                if eval_type == context.evaluation_type:
                    evaluator = self.evaluators[eval_type]
                    self.logger.info(f"执行评估器: {evaluator.name}")
                    
                    if not evaluator.validate_input(context):
                        raise ValueError(f"评估器 {evaluator.name} 输入验证失败")
                    
                    # 预处理
                    processed_context = evaluator.preprocess(context)
                    
                    # 执行评估
                    result = evaluator.evaluate(processed_context)
                    
                    # 后处理
                    result = evaluator.postprocess(result)
                    
                    results[eval_type] = result
                    break
            
            # 执行条件评估器
            for condition, evaluator in self.conditional_evaluators:
                if condition(context):
                    self.logger.info(f"执行条件评估器: {evaluator.name}")
                    
                    if not evaluator.validate_input(context):
                        self.logger.warning(f"条件评估器 {evaluator.name} 输入验证失败，跳过")
                        continue
                    
                    processed_context = evaluator.preprocess(context)
                    result = evaluator.evaluate(processed_context)
                    result = evaluator.postprocess(result)
                    results[evaluator.evaluation_type] = result
            
            total_time = time.time() - start_time
            self.logger.info(f"评估管道执行完成，耗时: {total_time:.2f}秒")
            
        except Exception as e:
            self.logger.error(f"评估管道执行失败: {str(e)}")
            raise
        
        return results
    
    def get_evaluator(self, evaluation_type: EvaluationType) -> Optional[Evaluator]:
        """获取评估器"""
        return self.evaluators.get(evaluation_type)

class ReportFormatter(Protocol):
    """报告格式化协议"""
    def format(self, results: Dict[EvaluationType, EvaluationResult]) -> str:
        """格式化结果为报告"""
        pass

class JSONReportFormatter:
    """JSON报告格式化器"""
    
    def format(self, results: Dict[EvaluationType, EvaluationResult]) -> str:
        """格式化为JSON"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'scenario_count': 1,  # 单场景评估
            'evaluations': {}
        }
        
        for eval_type, result in results.items():
            report_data['evaluations'][eval_type.value] = result.to_dict()
        
        return json.dumps(report_data, indent=2, ensure_ascii=False)

class HTMLReportFormatter:
    """HTML报告格式化器"""
    
    def __init__(self, template: Optional[str] = None):
        self.template = template or self._get_default_template()
    
    def format(self, results: Dict[EvaluationType, EvaluationResult]) -> str:
        """格式化为HTML"""
        html_parts = [
            "<html>",
            "<head>",
            "<title>PyPSA场景评估报告</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; }",
            ".section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }",
            ".metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }",
            ".metric { padding: 10px; background: #f5f5f5; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>PyPSA场景评估报告</h1>",
            f"<p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        ]
        
        for eval_type, result in results.items():
            html_parts.extend([
                f'<div class="section">',
                f'<h2>{eval_type.value.title()}评估</h2>',
                f'<p>状态: {result.status.value}</p>',
                f'<p>执行时间: {result.execution_time:.2f}秒</p>',
                '<div class="metrics">'
            ])
            
            for metric_name, value in result.metrics.items():
                html_parts.append(f'<div class="metric"><strong>{metric_name}</strong>: {value:.4f}</div>')
            
            html_parts.extend(['</div>', '</div>'])
        
        html_parts.extend(["</body>", "</html>"])
        return '\n'.join(html_parts)
    
    def _get_default_template(self) -> str:
        """获取默认模板"""
        return "default_template"

class EvaluationReport:
    """评估报告"""
    
    def __init__(self, 
                 title: str = "PyPSA场景评估报告",
                 formatter: Optional[ReportFormatter] = None):
        self.title = title
        self.formatter = formatter or JSONReportFormatter()
        self.sections: List[Dict[str, Any]] = []
        self.generated_at = datetime.now()
    
    def add_section(self, title: str, content: str, level: int = 2):
        """添加章节"""
        self.sections.append({
            'title': title,
            'content': content,
            'level': level
        })
    
    def add_evaluation_results(self, results: Dict[EvaluationType, EvaluationResult]):
        """添加评估结果"""
        self.add_section(
            "评估结果",
            self.formatter.format(results),
            level=2
        )
    
    def generate(self) -> str:
        """生成报告"""
        # 根据格式化器类型生成不同的报告格式
        if self.formatter.format_type == "markdown":
            return self._generate_markdown_report()
        elif self.formatter.format_type == "html":
            return self._generate_html_report()
        elif self.formatter.format_type == "json":
            return self._generate_json_report()
        else:
            return self._generate_text_report()
    
    def _generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        report_lines = ["# 评估报告\n"]
        
        for section in self.sections:
            level = section['level']
            title = section['title']
            content = section['content']
            
            # 添加标题
            report_lines.append(f"{'#' * level} {title}\n")
            
            # 添加内容
            if isinstance(content, dict):
                for key, value in content.items():
                    report_lines.append(f"- **{key}**: {value}")
            elif isinstance(content, list):
                for item in content:
                    report_lines.append(f"- {item}")
            else:
                report_lines.append(str(content))
            
            report_lines.append("\n")
        
        return "\n".join(report_lines)
    
    def _generate_html_report(self) -> str:
        """生成HTML格式报告"""
        html_lines = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <title>评估报告</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
            "        h1 { color: #2c3e50; }",
            "        h2 { color: #34495e; }",
            "        h3 { color: #7f8c8d; }",
            "        .section { margin-bottom: 20px; }",
            "    </style>",
            "</head>",
            "<body>",
            "    <h1>评估报告</h1>"
        ]
        
        for section in self.sections:
            level = section['level']
            title = section['title']
            content = section['content']
            
            # 添加标题
            html_lines.append(f"    <h{level}>{title}</h{level}>")
            
            # 添加内容
            html_lines.append("    <div class=\"section\">")
            if isinstance(content, dict):
                html_lines.append("        <ul>")
                for key, value in content.items():
                    html_lines.append(f"            <li><strong>{key}</strong>: {value}</li>")
                html_lines.append("        </ul>")
            elif isinstance(content, list):
                html_lines.append("        <ul>")
                for item in content:
                    html_lines.append(f"            <li>{item}</li>")
                html_lines.append("        </ul>")
            else:
                html_lines.append(f"        <p>{content}</p>")
            html_lines.append("    </div>")
        
        html_lines.extend([
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html_lines)
    
    def _generate_json_report(self) -> str:
        """生成JSON格式报告"""
        import json
        report_data = {
            "title": "评估报告",
            "sections": self.sections
        }
        return json.dumps(report_data, ensure_ascii=False, indent=2)
    
    def _generate_text_report(self) -> str:
        """生成文本格式报告"""
        report_lines = ["评估报告", "=" * 40]
        
        for section in self.sections:
            title = section['title']
            content = section['content']
            
            # 添加标题
            report_lines.append(f"\n{title}")
            report_lines.append("-" * len(title))
            
            # 添加内容
            if isinstance(content, dict):
                for key, value in content.items():
                    report_lines.append(f"  {key}: {value}")
            elif isinstance(content, list):
                for item in content:
                    report_lines.append(f"  - {item}")
            else:
                report_lines.append(f"  {content}")
        
        return "\n".join(report_lines)
    
    def save_to_file(self, file_path: str):
        """保存到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.generate())

class EvaluationManager:
    """评估管理器"""
    
    def __init__(self, 
                 pipelines: Dict[str, EvaluationPipeline],
                 default_config: Optional[Dict[str, Any]] = None):
        self.pipelines = pipelines
        self.default_config = default_config or {}
        self.results_cache: Dict[str, EvaluationResult] = {}
        self.logger = logging.getLogger(__name__)
    
    def evaluate_scenario(self, 
                        scenario_id: str,
                        scenario_data: Dict[str, Any],
                        pipeline_name: str = "default") -> Dict[EvaluationType, EvaluationResult]:
        """评估场景"""
        if pipeline_name not in self.pipelines:
            raise ValueError(f"评估管道不存在: {pipeline_name}")
        
        pipeline = self.pipelines[pipeline_name]
        
        # 创建评估上下文
        context = EvaluationContext(
            scenario_id=scenario_id,
            scenario_data=scenario_data,
            evaluation_type=EvaluationType.COMPREHENSIVE,  # 默认为综合评估
            config=self.default_config.copy()
        )
        
        # 执行评估
        results = pipeline.execute(context)
        
        # 缓存结果
        for eval_type, result in results.items():
            cache_key = f"{scenario_id}_{eval_type.value}"
            self.results_cache[cache_key] = result
        
        return results
    
    def get_evaluation_history(self, scenario_id: str) -> List[EvaluationResult]:
        """获取评估历史"""
        history = []
        for key, result in self.results_cache.items():
            if key.startswith(f"{scenario_id}_"):
                history.append(result)
        return sorted(history, key=lambda x: x.created_at)
    
    def compare_scenarios(self, 
                        scenario_ids: List[str],
                        evaluation_type: EvaluationType) -> pd.DataFrame:
        """比较场景"""
        comparison_data = []
        
        for scenario_id in scenario_ids:
            cache_key = f"{scenario_id}_{evaluation_type.value}"
            if cache_key in self.results_cache:
                result = self.results_cache[cache_key]
                row = {'scenario_id': scenario_id}
                row.update(result.metrics)
                comparison_data.append(row)
        
        if not comparison_data:
            return pd.DataFrame()
        
        return pd.DataFrame(comparison_data)

def create_default_pipeline() -> EvaluationPipeline:
    """创建默认评估管道"""
    pipeline = EvaluationPipeline("default")
    
    # 这里可以添加默认的评估器
    # 实际使用时会从各个具体评估模块导入
    
    return pipeline