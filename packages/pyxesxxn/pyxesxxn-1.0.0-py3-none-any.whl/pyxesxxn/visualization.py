"""可视化与结果展示模块 (Visualization & Result Presentation Module)

该模块构建动态拓扑图（包括Web界面与Matplotlib/Plotly可视化），
展示故障定位结果、自愈策略执行过程及供电恢复状态。

核心功能：
- 实时展示故障区段、类型及开关操作序列
- 可视化非故障区域供电恢复的时序过程
"""

from __future__ import annotations
from typing import Dict, List, Optional, Union, Any, Tuple
from enum import Enum
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Polygon, FancyBboxPatch
from matplotlib.collections import PatchCollection
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import warnings
import tempfile
import os
from pathlib import Path
import json
import base64
from io import BytesIO


class VisualizationType(Enum):
    """可视化类型枚举"""
    TOPOLOGY = "topology"  # 拓扑图
    TIME_SERIES = "time_series"  # 时序图
    HEATMAP = "heatmap"  # 热力图
    ANIMATION = "animation"  # 动画
    DASHBOARD = "dashboard"  # 仪表盘


class ColorScheme(Enum):
    """颜色方案枚举"""
    DEFAULT = "default"  # 默认配色
    DARK = "dark"  # 深色主题
    PASTEL = "pastel"  # 柔和配色
    CONTRAST = "contrast"  # 高对比度


@dataclass
class VisualizationConfig:
    """可视化配置类"""
    type: VisualizationType
    color_scheme: ColorScheme = ColorScheme.DEFAULT
    width: int = 800
    height: int = 600
    title: str = ""
    interactive: bool = True
    animation_duration: int = 1000  # 动画时长（毫秒）
    auto_play: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type.value,
            'color_scheme': self.color_scheme.value,
            'width': self.width,
            'height': self.height,
            'title': self.title,
            'interactive': self.interactive,
            'animation_duration': self.animation_duration,
            'auto_play': self.auto_play
        }


@dataclass
class VisualizationResult:
    """可视化结果类"""
    success: bool
    figure: Optional[Any] = None
    html_content: Optional[str] = None
    image_data: Optional[bytes] = None
    animation_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def save_to_file(self, filepath: str) -> None:
        """保存到文件"""
        if self.figure is not None:
            if hasattr(self.figure, 'savefig'):  # matplotlib figure
                self.figure.savefig(filepath, dpi=300, bbox_inches='tight')
            elif hasattr(self.figure, 'write_image'):  # plotly figure
                self.figure.write_image(filepath)
        
        if self.html_content:
            with open(filepath + '.html', 'w', encoding='utf-8') as f:
                f.write(self.html_content)


class PowerGridVisualizer:
    """电网可视化类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化可视化模块
        
        Parameters
        ----------
        config : Optional[Dict[str, Any]], default=None
            配置参数
        """
        self.config = config or {}
        self.colors = self._initialize_colors()
        
        # 默认配置
        self.default_config = {
            'default_figsize': (12, 8),
            'animation_fps': 10,
            'node_size': 300,
            'font_size': 10,
            'line_width': 2,
            'color_blind_friendly': False,
            'export_formats': ['png', 'html', 'pdf']
        }
        
        # 更新配置
        self.default_config.update(self.config)
    
    def _initialize_colors(self) -> Dict[str, str]:
        """初始化颜色配置"""
        return {
            'normal': '#2E86AB',      # 正常状态 - 蓝色
            'fault': '#A23B72',       # 故障状态 - 紫色
            'restored': '#F18F01',    # 恢复状态 - 橙色
            'isolated': '#C73E1D',    # 隔离状态 - 红色
            'switch_open': '#6A8D73', # 开关断开 - 绿色
            'switch_closed': '#3C1518', # 开关闭合 - 深红
            'background': '#F5F5F5',  # 背景色
            'grid': '#CCCCCC'         # 网格色
        }
    
    def create_topology_plot(self, network_data: Dict[str, Any],
                            fault_data: Optional[Dict[str, Any]] = None,
                            config: Optional[VisualizationConfig] = None) -> VisualizationResult:
        """创建拓扑图可视化
        
        Parameters
        ----------
        network_data : Dict[str, Any]
            网络数据
        fault_data : Optional[Dict[str, Any]], default=None
            故障数据
        config : Optional[VisualizationConfig], default=None
            可视化配置
            
        Returns
        -------
        VisualizationResult
            可视化结果
        """
        if config is None:
            config = VisualizationConfig(type=VisualizationType.TOPOLOGY)
        
        try:
            # 创建图形
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            # 绘制拓扑图
            self._draw_topology(ax, network_data, fault_data)
            
            # 设置图形属性
            ax.set_title(config.title or '配电网拓扑图', fontsize=14, fontweight='bold')
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            
            # 添加图例
            self._add_topology_legend(ax)
            
            plt.tight_layout()
            
            return VisualizationResult(
                success=True,
                figure=fig,
                metadata={'type': 'topology', 'config': config.to_dict()}
            )
            
        except Exception as e:
            warnings.warn(f"创建拓扑图失败: {e}")
            return VisualizationResult(success=False)
    
    def _draw_topology(self, ax: plt.Axes, network_data: Dict[str, Any], 
                      fault_data: Optional[Dict[str, Any]]) -> None:
        """绘制拓扑图"""
        # 提取节点和边数据
        nodes = network_data.get('nodes', [])
        edges = network_data.get('edges', [])
        
        # 绘制节点
        for node in nodes:
            self._draw_node(ax, node, fault_data)
        
        # 绘制边
        for edge in edges:
            self._draw_edge(ax, edge, fault_data)
        
        # 绘制故障位置（如果有）
        if fault_data:
            self._draw_fault_location(ax, fault_data)
    
    def _draw_node(self, ax: plt.Axes, node: Dict[str, Any], 
                  fault_data: Optional[Dict[str, Any]]) -> None:
        """绘制节点"""
        x, y = node.get('x', 0), node.get('y', 0)
        node_type = node.get('type', 'bus')
        node_id = node.get('id', 'unknown')
        
        # 确定节点状态和颜色
        status = self._get_node_status(node, fault_data)
        color = self.colors[status]
        
        # 根据节点类型绘制不同形状
        if node_type == 'bus':
            # 母线 - 圆形
            circle = Circle((x, y), radius=0.1, facecolor=color, 
                          edgecolor='black', linewidth=1)
            ax.add_patch(circle)
        elif node_type == 'generator':
            # 发电机 - 三角形
            triangle = Polygon([(x-0.1, y-0.1), (x+0.1, y-0.1), (x, y+0.1)], 
                             facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(triangle)
        elif node_type == 'load':
            # 负荷 - 矩形
            rect = Rectangle((x-0.08, y-0.08), 0.16, 0.16, 
                           facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(rect)
        
        # 添加节点标签
        ax.text(x, y+0.15, node_id, ha='center', va='bottom', 
               fontsize=self.default_config['font_size'])
    
    def _draw_edge(self, ax: plt.Axes, edge: Dict[str, Any], 
                  fault_data: Optional[Dict[str, Any]]) -> None:
        """绘制边（线路）"""
        from_node = edge.get('from')
        to_node = edge.get('to')
        edge_id = edge.get('id', 'unknown')
        
        # 获取节点坐标（简化处理，实际应用中需要从网络数据中查找）
        x1, y1 = 0, 0  # 起点坐标
        x2, y2 = 1, 1  # 终点坐标
        
        # 确定边状态和颜色
        status = self._get_edge_status(edge, fault_data)
        color = self.colors[status]
        
        # 绘制线路
        line_width = self.default_config['line_width']
        if status == 'fault':
            line_width *= 2  # 故障线路加粗显示
        
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=line_width, 
               alpha=0.8, solid_capstyle='round')
        
        # 添加线路标签（中点）
        mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
        ax.text(mid_x, mid_y, edge_id, ha='center', va='center', 
               fontsize=self.default_config['font_size']-2, 
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7))
    
    def _draw_fault_location(self, ax: plt.Axes, fault_data: Dict[str, Any]) -> None:
        """绘制故障位置"""
        location = fault_data.get('location', {})
        fault_type = fault_data.get('type', 'unknown')
        
        if 'x' in location and 'y' in location:
            x, y = location['x'], location['y']
            
            # 故障标记 - 红色叉号
            ax.scatter(x, y, color='red', marker='x', s=200, 
                      linewidth=3, zorder=10)
            
            # 故障类型标签
            ax.text(x, y+0.2, f"故障: {fault_type}", ha='center', 
                   va='bottom', fontsize=10, color='red', 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                           edgecolor='red', alpha=0.8))
    
    def _get_node_status(self, node: Dict[str, Any], 
                        fault_data: Optional[Dict[str, Any]]) -> str:
        """获取节点状态"""
        node_id = node.get('id', '')
        
        if fault_data:
            # 检查节点是否在故障影响范围内
            affected_nodes = fault_data.get('affected_nodes', [])
            if node_id in affected_nodes:
                return 'fault'
            
            # 检查节点是否已恢复
            restored_nodes = fault_data.get('restored_nodes', [])
            if node_id in restored_nodes:
                return 'restored'
        
        return 'normal'
    
    def _get_edge_status(self, edge: Dict[str, Any], 
                        fault_data: Optional[Dict[str, Any]]) -> str:
        """获取边状态"""
        edge_id = edge.get('id', '')
        
        if fault_data:
            # 检查边是否为故障线路
            fault_location = fault_data.get('location', {})
            if fault_location.get('edge_id') == edge_id:
                return 'fault'
            
            # 检查边是否被隔离
            isolated_edges = fault_data.get('isolated_edges', [])
            if edge_id in isolated_edges:
                return 'isolated'
        
        return 'normal'
    
    def _add_topology_legend(self, ax: plt.Axes) -> None:
        """添加拓扑图图例"""
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['normal'], 
                      markersize=8, label='正常节点'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['fault'], 
                      markersize=8, label='故障节点'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['restored'], 
                      markersize=8, label='恢复节点'),
            plt.Line2D([0], [0], color=self.colors['normal'], linewidth=2, label='正常线路'),
            plt.Line2D([0], [0], color=self.colors['fault'], linewidth=3, label='故障线路'),
            plt.Line2D([0], [0], color=self.colors['isolated'], linewidth=2, 
                      linestyle='--', label='隔离线路')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', 
                 bbox_to_anchor=(1.1, 1), framealpha=0.9)
    
    def create_time_series_plot(self, time_series_data: pd.DataFrame,
                               config: Optional[VisualizationConfig] = None) -> VisualizationResult:
        """创建时序图可视化
        
        Parameters
        ----------
        time_series_data : pd.DataFrame
            时序数据
        config : Optional[VisualizationConfig], default=None
            可视化配置
            
        Returns
        -------
        VisualizationResult
            可视化结果
        """
        if config is None:
            config = VisualizationConfig(type=VisualizationType.TIME_SERIES)
        
        try:
            # 使用Plotly创建交互式时序图
            fig = make_subplots(rows=2, cols=1, 
                               subplot_titles=('电压曲线', '电流曲线'),
                               vertical_spacing=0.1)
            
            # 添加电压曲线
            if 'voltage' in time_series_data.columns:
                fig.add_trace(
                    go.Scatter(x=time_series_data.index, 
                              y=time_series_data['voltage'],
                              name='电压', line=dict(color='blue')),
                    row=1, col=1
                )
            
            # 添加电流曲线
            if 'current' in time_series_data.columns:
                fig.add_trace(
                    go.Scatter(x=time_series_data.index, 
                              y=time_series_data['current'],
                              name='电流', line=dict(color='red')),
                    row=2, col=1
                )
            
            # 更新布局
            fig.update_layout(
                title=config.title or '电网时序数据',
                width=config.width,
                height=config.height,
                showlegend=True,
                template='plotly_white'
            )
            
            # 生成HTML内容
            html_content = fig.to_html(include_plotlyjs='cdn')
            
            return VisualizationResult(
                success=True,
                figure=fig,
                html_content=html_content,
                metadata={'type': 'time_series', 'config': config.to_dict()}
            )
            
        except Exception as e:
            warnings.warn(f"创建时序图失败: {e}")
            return VisualizationResult(success=False)
    
    def create_animation(self, animation_data: Dict[str, Any],
                        config: Optional[VisualizationConfig] = None) -> VisualizationResult:
        """创建动画可视化
        
        Parameters
        ----------
        animation_data : Dict[str, Any]
            动画数据
        config : Optional[VisualizationConfig], default=None
            可视化配置
            
        Returns
        -------
        VisualizationResult
            可视化结果
        """
        if config is None:
            config = VisualizationConfig(type=VisualizationType.ANIMATION)
        
        try:
            # 创建动画
            fig, ax = plt.subplots(figsize=(config.width/100, config.height/100))
            
            # 获取动画帧数据
            frames = animation_data.get('frames', [])
            
            def animate(frame_num):
                ax.clear()
                frame_data = frames[frame_num]
                
                # 绘制当前帧的拓扑图
                self._draw_topology(ax, frame_data.get('network', {}), 
                                  frame_data.get('fault', {}))
                
                # 添加时间戳
                timestamp = frame_data.get('timestamp', frame_num)
                ax.set_title(f'{config.title} - 时间: {timestamp:.2f}s', 
                           fontsize=12, fontweight='bold')
                
                ax.set_aspect('equal')
                ax.grid(True, alpha=0.3)
            
            # 创建动画
            anim = animation.FuncAnimation(
                fig, animate, frames=len(frames),
                interval=config.animation_duration, 
                repeat=config.auto_play
            )
            
            # 保存动画
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as f:
                anim.save(f.name, writer='pillow', fps=self.default_config['animation_fps'])
                animation_path = f.name
            
            return VisualizationResult(
                success=True,
                figure=fig,
                animation_path=animation_path,
                metadata={'type': 'animation', 'config': config.to_dict()}
            )
            
        except Exception as e:
            warnings.warn(f"创建动画失败: {e}")
            return VisualizationResult(success=False)
    
    def create_dashboard(self, dashboard_data: Dict[str, Any],
                        config: Optional[VisualizationConfig] = None) -> VisualizationResult:
        """创建仪表盘可视化
        
        Parameters
        ----------
        dashboard_data : Dict[str, Any]
            仪表盘数据
        config : Optional[VisualizationConfig], default=None
            可视化配置
            
        Returns
        -------
        VisualizationResult
            可视化结果
        """
        if config is None:
            config = VisualizationConfig(type=VisualizationType.DASHBOARD)
        
        try:
            # 创建仪表盘布局
            fig = make_subplots(
                rows=2, cols=2,
                specs=[[{"type": "scatter"}, {"type": "pie"}],
                       [{"type": "bar"}, {"type": "indicator"}]],
                subplot_titles=('实时数据', '状态分布', '性能指标', '系统状态')
            )
            
            # 实时数据曲线
            if 'real_time_data' in dashboard_data:
                real_time_data = dashboard_data['real_time_data']
                fig.add_trace(
                    go.Scatter(x=real_time_data.index, y=real_time_data.values,
                              name='实时数据', line=dict(color='green')),
                    row=1, col=1
                )
            
            # 状态分布饼图
            if 'status_distribution' in dashboard_data:
                status_data = dashboard_data['status_distribution']
                fig.add_trace(
                    go.Pie(labels=list(status_data.keys()), 
                          values=list(status_data.values()),
                          name='状态分布'),
                    row=1, col=2
                )
            
            # 性能指标柱状图
            if 'performance_metrics' in dashboard_data:
                metrics = dashboard_data['performance_metrics']
                fig.add_trace(
                    go.Bar(x=list(metrics.keys()), y=list(metrics.values()),
                          name='性能指标', marker_color='orange'),
                    row=2, col=1
                )
            
            # 系统状态指示器
            if 'system_status' in dashboard_data:
                status = dashboard_data['system_status']
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number+delta",
                        value=status.get('health_score', 0),
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "系统健康度"},
                        gauge={'axis': {'range': [None, 100]}},
                        delta={'reference': 50}
                    ),
                    row=2, col=2
                )
            
            # 更新布局
            fig.update_layout(
                title=config.title or '电网监控仪表盘',
                width=config.width,
                height=config.height,
                template='plotly_dark' if config.color_scheme == ColorScheme.DARK else 'plotly_white'
            )
            
            # 生成HTML内容
            html_content = fig.to_html(include_plotlyjs='cdn')
            
            return VisualizationResult(
                success=True,
                figure=fig,
                html_content=html_content,
                metadata={'type': 'dashboard', 'config': config.to_dict()}
            )
            
        except Exception as e:
            warnings.warn(f"创建仪表盘失败: {e}")
            return VisualizationResult(success=False)
    
    def create_restoration_timeline(self, restoration_data: Dict[str, Any]) -> VisualizationResult:
        """创建供电恢复时间线可视化
        
        Parameters
        ----------
        restoration_data : Dict[str, Any]
            恢复数据
            
        Returns
        -------
        VisualizationResult
            可视化结果
        """
        try:
            # 提取恢复事件
            events = restoration_data.get('events', [])
            
            # 创建时间线图
            fig = go.Figure()
            
            for i, event in enumerate(events):
                start_time = event['start_time']
                end_time = event.get('end_time', start_time + 1)
                description = event['description']
                status = event['status']
                
                # 根据状态选择颜色
                color_map = {
                    'fault': 'red',
                    'isolated': 'orange',
                    'restoring': 'yellow',
                    'restored': 'green'
                }
                color = color_map.get(status, 'gray')
                
                fig.add_trace(go.Scatter(
                    x=[start_time, end_time],
                    y=[i, i],
                    mode='lines+markers',
                    line=dict(color=color, width=10),
                    marker=dict(size=15, color=color),
                    name=description,
                    hoverinfo='text',
                    text=description
                ))
            
            # 更新布局
            fig.update_layout(
                title='供电恢复时间线',
                xaxis_title='时间 (秒)',
                yaxis_title='恢复事件',
                showlegend=True,
                height=400
            )
            
            return VisualizationResult(
                success=True,
                figure=fig,
                metadata={'type': 'restoration_timeline'}
            )
            
        except Exception as e:
            warnings.warn(f"创建恢复时间线失败: {e}")
            return VisualizationResult(success=False)
    
    def export_visualization(self, result: VisualizationResult, 
                            format: str = 'png') -> str:
        """导出可视化结果
        
        Parameters
        ----------
        result : VisualizationResult
            可视化结果
        format : str, default='png'
            导出格式
            
        Returns
        -------
        str
            导出文件路径
        """
        if not result.success:
            raise ValueError("无法导出失败的可视化结果")
        
        with tempfile.NamedTemporaryFile(suffix=f'.{format}', delete=False) as f:
            if result.figure is not None:
                if hasattr(result.figure, 'savefig'):  # matplotlib
                    result.figure.savefig(f.name, format=format, 
                                        dpi=300, bbox_inches='tight')
                elif hasattr(result.figure, 'write_image'):  # plotly
                    result.figure.write_image(f.name, format=format)
            
            return f.name
    
    def generate_report(self, visualization_results: List[VisualizationResult]) -> str:
        """生成综合报告
        
        Parameters
        ----------
        visualization_results : List[VisualizationResult]
            可视化结果列表
            
        Returns
        -------
        str
            HTML报告内容
        """
        # 创建HTML报告
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>电网可视化报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .visualization {{ margin: 20px 0; border: 1px solid #ddd; padding: 15px; }}
                .metadata {{ background: #f5f5f5; padding: 10px; margin: 10px 0; }}
                img, iframe {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            <h1>电网可视化分析报告</h1>
            <p>生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        for i, result in enumerate(visualization_results):
            if result.success:
                html_content += f"""
                <div class="visualization">
                    <h2>可视化 {i+1}</h2>
                    <div class="metadata">
                        <strong>类型:</strong> {result.metadata.get('type', 'unknown')}<br>
                        <strong>配置:</strong> {json.dumps(result.metadata.get('config', {}), indent=2, ensure_ascii=False)}
                    </div>
                """
                
                if result.html_content:
                    # 嵌入Plotly HTML内容
                    html_content += result.html_content
                elif result.figure is not None:
                    # 将matplotlib图形转换为base64图像
                    if hasattr(result.figure, 'savefig'):
                        buf = BytesIO()
                        result.figure.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                        buf.seek(0)
                        img_data = base64.b64encode(buf.read()).decode('utf-8')
                        html_content += f'<img src="data:image/png;base64,{img_data}" alt="可视化图像">'
                
                html_content += "</div>"
        
        html_content += """
            </body>
        </html>
        """
        
        return html_content


# 工具函数
def create_sample_network_data() -> Dict[str, Any]:
    """创建示例网络数据"""
    return {
        'nodes': [
            {'id': 'Bus1', 'type': 'bus', 'x': 0, 'y': 0},
            {'id': 'Gen1', 'type': 'generator', 'x': -1, 'y': 1},
            {'id': 'Load1', 'type': 'load', 'x': 1, 'y': 1},
            {'id': 'Bus2', 'type': 'bus', 'x': 2, 'y': 0},
            {'id': 'Load2', 'type': 'load', 'x': 3, 'y': 1}
        ],
        'edges': [
            {'id': 'Line1', 'from': 'Bus1', 'to': 'Bus2'},
            {'id': 'Line2', 'from': 'Gen1', 'to': 'Bus1'},
            {'id': 'Line3', 'from': 'Bus1', 'to': 'Load1'},
            {'id': 'Line4', 'from': 'Bus2', 'to': 'Load2'}
        ]
    }


def create_sample_fault_data() -> Dict[str, Any]:
    """创建示例故障数据"""
    return {
        'type': 'single_line_ground',
        'location': {'x': 1, 'y': 0, 'edge_id': 'Line1'},
        'affected_nodes': ['Bus1', 'Bus2'],
        'isolated_edges': ['Line1']
    }


def validate_visualization_module(visualizer: PowerGridVisualizer) -> bool:
    """验证可视化模块功能"""
    try:
        # 测试拓扑图功能
        network_data = create_sample_network_data()
        fault_data = create_sample_fault_data()
        
        result = visualizer.create_topology_plot(network_data, fault_data)
        
        return result.success
    except Exception as e:
        warnings.warn(f"可视化模块验证失败: {e}")
        return False