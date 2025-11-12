#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能心理咨询系统架构图生成器（大字体优化版）
生成高质量的学术论文配图（支持PNG和PDF格式）
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.font_manager as fm
import numpy as np
import sys

def find_chinese_font():
    """自动查找系统中可用的中文字体"""
    print("🔍 正在检测系统中文字体...")
    
    preferred_fonts = [
        'WenQuanYi Micro Hei',
        'WenQuanYi Zen Hei',
        'Noto Sans CJK SC',
        'Noto Sans CJK TC',
        'Source Han Sans CN',
        'Droid Sans Fallback',
        'SimHei',
        'Microsoft YaHei',
        'PingFang SC',
        'Heiti SC',
        'STHeiti',
    ]
    
    available_fonts = set([f.name for f in fm.fontManager.ttflist])
    
    for font in preferred_fonts:
        if font in available_fonts:
            print(f"✅ 找到中文字体: {font}")
            return font
    
    print("⚠️  未找到优先字体，尝试搜索其他中文字体...")
    chinese_keywords = ['zh', 'chinese', 'cjk', 'han', 'wqy', 'noto', 'simhei', 'simsun']
    
    for font in available_fonts:
        if any(keyword in font.lower() for keyword in chinese_keywords):
            print(f"✅ 找到备选字体: {font}")
            return font
    
    print("❌ 未找到任何中文字体！")
    return None

def setup_chinese_font():
    """配置matplotlib中文字体"""
    chinese_font = find_chinese_font()
    
    if chinese_font:
        plt.rcParams['font.sans-serif'] = [chinese_font, 'DejaVu Sans', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        print(f"✅ 字体配置成功: {chinese_font}")
        return True
    else:
        print("❌ 错误: 系统中没有找到可用的中文字体")
        return False

# 配色方案
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'bg_light': '#F7F9FC',
    'bg_module': '#E8F0F7',
    'text': '#2C3E50',
    'border': '#34495E',
    'arrow': '#5D6D7E',
    'highlight': '#E74C3C',
    'memory': '#27AE60',
}

def create_architecture_diagram(output_file='architecture_diagram.png', dpi=300):
    """创建系统架构图（大字体版）"""
    # 创建更大的画布以容纳放大的文字
    fig, ax = plt.subplots(1, 1, figsize=(18, 22))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 22)
    ax.axis('off')
    
    # 顶部用户
    draw_user_section(ax, x=9, y=21)
    
    # 对话管理层
    draw_dialogue_manager(ax, x=9, y=19.2)
    
    # 双知识库RAG模块（左侧）
    draw_rag_module(ax, x=4.5, y=14.5)
    
    # 三层记忆模块（右侧）
    draw_memory_module(ax, x=13.5, y=14.5)
    
    # 并行检索箭头
    draw_parallel_arrows(ax)
    
    # 上下文构建模块
    draw_context_builder(ax, x=9, y=9.5)
    
    # LLM层
    draw_llm_layer(ax, x=9, y=6.8)
    
    # 记忆更新模块
    draw_memory_update(ax, x=9, y=4.5)
    
    # 系统回复
    draw_system_response(ax, x=9, y=2.3)
    
    # 底部用户
    draw_user_bottom(ax, x=9, y=0.6)
    
    # 右侧创新点说明
    draw_innovation_box(ax)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"✅ 架构图已生成: {output_file}")
    print(f"   分辨率: {dpi} DPI")
    plt.close()


def draw_user_section(ax, x, y):
    """绘制顶部用户输入部分"""
    user_circle = plt.Circle((x, y), 0.35, color=COLORS['primary'], zorder=10)
    ax.add_patch(user_circle)
    ax.text(x, y, '👤', fontsize=24, ha='center', va='center', zorder=11)
    
    ax.text(x, y-0.7, '用户输入问题', fontsize=15, ha='center', 
            weight='bold', color=COLORS['text'])
    ax.text(x, y-1.2, '"我最近工作压力很大，经常失眠..."', fontsize=13, 
            ha='center', style='italic', color=COLORS['text'])
    
    arrow = FancyArrowPatch((x, y-1.5), (x, y-2.0),
                           arrowstyle='->', mutation_scale=25, 
                           linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow)


def draw_dialogue_manager(ax, x, y):
    """绘制对话管理层"""
    width, height = 11, 1.4
    rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                          boxstyle="round,pad=0.1", 
                          edgecolor=COLORS['border'], 
                          facecolor=COLORS['bg_module'],
                          linewidth=2.5)
    ax.add_patch(rect)
    
    ax.text(x, y+0.25, '对话管理层 (Dialogue Manager)', 
            fontsize=16, ha='center', weight='bold', color=COLORS['text'])
    ax.text(x, y-0.25, '统一协调 · 上下文构建 · 流程控制', 
            fontsize=12, ha='center', color=COLORS['text'])


def draw_rag_module(ax, x, y):
    """绘制双知识库RAG模块"""
    width, height = 6.5, 7.5
    
    outer_rect = FancyBboxPatch((x-width/2-0.15, y-height/2-0.15), 
                               width+0.3, height+0.3,
                               boxstyle="round,pad=0.1",
                               edgecolor=COLORS['highlight'], 
                               facecolor='none',
                               linewidth=3, linestyle='--')
    ax.add_patch(outer_rect)
    
    main_rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                              boxstyle="round,pad=0.1",
                              edgecolor=COLORS['primary'], 
                              facecolor=COLORS['bg_light'],
                              linewidth=2.5)
    ax.add_patch(main_rect)
    
    ax.text(x, y+height/2-0.5, '双知识库RAG模块', 
            fontsize=15, ha='center', weight='bold', color=COLORS['primary'])
    ax.text(x, y+height/2-0.9, '(创新点 ①)', 
            fontsize=11, ha='center', color=COLORS['highlight'], weight='bold')
    
    # 专业心理知识库
    kb1_y = y + 1.5
    kb1_rect = FancyBboxPatch((x-width/2+0.3, kb1_y-1.05), width-0.6, 2.1,
                             boxstyle="round,pad=0.05",
                             edgecolor=COLORS['border'], 
                             facecolor='white',
                             linewidth=1.5)
    ax.add_patch(kb1_rect)
    
    ax.text(x, kb1_y+0.7, '专业心理知识库', fontsize=13, ha='center', weight='bold')
    ax.text(x, kb1_y+0.25, '• SmileChat 16K', fontsize=11, ha='center')
    ax.text(x, kb1_y-0.15, '• CBT/MBSR文献', fontsize=11, ha='center')
    ax.text(x, kb1_y-0.55, '• 治疗指南', fontsize=11, ha='center')
    ax.text(x, kb1_y-0.95, '• 50K知识片段', fontsize=11, ha='center')
    
    ax.text(x, kb1_y-1.5, '↕ 向量检索', fontsize=10, ha='center', style='italic')
    ax.text(x, kb1_y-1.85, '权重: 60%', fontsize=11, ha='center', 
            weight='bold', color=COLORS['accent'])
    
    # 个人信息知识库
    kb2_y = y - 1.7
    kb2_rect = FancyBboxPatch((x-width/2+0.3, kb2_y-1.05), width-0.6, 2.1,
                             boxstyle="round,pad=0.05",
                             edgecolor=COLORS['border'], 
                             facecolor='white',
                             linewidth=1.5)
    ax.add_patch(kb2_rect)
    
    ax.text(x, kb2_y+0.7, '个人信息知识库', fontsize=13, ha='center', weight='bold')
    ax.text(x, kb2_y+0.25, '• 用户基本档案', fontsize=11, ha='center')
    ax.text(x, kb2_y-0.15, '• 历史问题记录', fontsize=11, ha='center')
    ax.text(x, kb2_y-0.55, '• 干预历史追踪', fontsize=11, ha='center')
    ax.text(x, kb2_y-0.95, '• 动态更新', fontsize=11, ha='center')
    
    ax.text(x, kb2_y-1.5, '↕ 向量检索', fontsize=10, ha='center', style='italic')
    ax.text(x, kb2_y-1.85, '权重: 40%', fontsize=11, ha='center', 
            weight='bold', color=COLORS['accent'])
    
    ax.text(x, y-height/2+0.4, '[时间衰减] [重排序]', fontsize=10, 
            ha='center', style='italic', color=COLORS['text'])


def draw_memory_module(ax, x, y):
    """绘制三层记忆模块"""
    width, height = 6.5, 7.5
    
    outer_rect = FancyBboxPatch((x-width/2-0.15, y-height/2-0.15), 
                               width+0.3, height+0.3,
                               boxstyle="round,pad=0.1",
                               edgecolor=COLORS['highlight'], 
                               facecolor='none',
                               linewidth=3, linestyle='--')
    ax.add_patch(outer_rect)
    
    main_rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                              boxstyle="round,pad=0.1",
                              edgecolor=COLORS['memory'], 
                              facecolor=COLORS['bg_light'],
                              linewidth=2.5)
    ax.add_patch(main_rect)
    
    ax.text(x, y+height/2-0.5, '三层记忆模块', 
            fontsize=15, ha='center', weight='bold', color=COLORS['memory'])
    ax.text(x, y+height/2-0.9, '(创新点 ②)', 
            fontsize=11, ha='center', color=COLORS['highlight'], weight='bold')
    
    # L3 长期记忆
    l3_y = y + 2.0
    l3_rect = FancyBboxPatch((x-width/2+0.3, l3_y-0.8), width-0.6, 1.6,
                            boxstyle="round,pad=0.05",
                            edgecolor=COLORS['border'], 
                            facecolor='white',
                            linewidth=1.5)
    ax.add_patch(l3_rect)
    
    ax.text(x, l3_y+0.6, '长期记忆 (L3)', fontsize=13, ha='center', weight='bold')
    ax.text(x, l3_y+0.15, '• 用户档案', fontsize=11, ha='center')
    ax.text(x, l3_y-0.25, '• 情绪趋势', fontsize=11, ha='center')
    ax.text(x, l3_y-0.65, '• 历史摘要', fontsize=11, ha='center')
    
    # L2 短期记忆
    l2_y = y + 0.2
    l2_rect = FancyBboxPatch((x-width/2+0.3, l2_y-0.8), width-0.6, 1.6,
                            boxstyle="round,pad=0.05",
                            edgecolor=COLORS['border'], 
                            facecolor='white',
                            linewidth=1.5)
    ax.add_patch(l2_rect)
    
    ax.text(x, l2_y+0.6, '短期记忆 (L2)', fontsize=13, ha='center', weight='bold')
    ax.text(x, l2_y+0.15, '• 会话级摘要', fontsize=11, ha='center')
    ax.text(x, l2_y-0.25, '• 关键信息提取', fontsize=11, ha='center')
    ax.text(x, l2_y-0.65, '• 近期20会话', fontsize=11, ha='center')
    
    # L1 工作记忆
    l1_y = y - 1.6
    l1_rect = FancyBboxPatch((x-width/2+0.3, l1_y-0.8), width-0.6, 1.6,
                            boxstyle="round,pad=0.05",
                            edgecolor=COLORS['border'], 
                            facecolor='white',
                            linewidth=1.5)
    ax.add_patch(l1_rect)
    
    ax.text(x, l1_y+0.6, '工作记忆 (L1)', fontsize=13, ha='center', weight='bold')
    ax.text(x, l1_y+0.15, '• 当前会话上下文', fontsize=11, ha='center')
    ax.text(x, l1_y-0.25, '• 最近10轮对话', fontsize=11, ha='center')
    ax.text(x, l1_y-0.65, '• 实时情绪状态', fontsize=11, ha='center')


def draw_parallel_arrows(ax):
    """绘制并行检索箭头"""
    arrow1 = FancyArrowPatch((7.5, 18), (5.2, 17.5),
                            arrowstyle='->', mutation_scale=18, 
                            linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((10.5, 18), (12.8, 17.5),
                            arrowstyle='->', mutation_scale=18, 
                            linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow2)
    
    ax.text(9, 17.7, '并行检索', fontsize=11, ha='center', 
            weight='bold', color=COLORS['arrow'],
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white', 
                     edgecolor=COLORS['arrow'], linewidth=1.5))


def draw_context_builder(ax, x, y):
    """绘制上下文构建模块"""
    width, height = 9, 2.6
    
    arrow1 = FancyArrowPatch((5.2, 11), (x, y+height/2+0.4),
                            arrowstyle='->', mutation_scale=18, 
                            linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((12.8, 11), (x, y+height/2+0.4),
                            arrowstyle='->', mutation_scale=18, 
                            linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow2)
    
    ax.text(x, y+height/2+0.95, '检索结果融合', fontsize=11, ha='center', 
            weight='bold', color=COLORS['arrow'])
    
    rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                         boxstyle="round,pad=0.1",
                         edgecolor=COLORS['border'], 
                         facecolor=COLORS['bg_module'],
                         linewidth=2.5)
    ax.add_patch(rect)
    
    ax.text(x, y+0.9, '上下文构建模块', fontsize=14, ha='center', 
            weight='bold', color=COLORS['text'])
    
    context_items = [
        '系统提示词 +',
        '专业知识检索结果 (3-5文档) +',
        '个人信息检索结果 (2-3文档) +',
        '长期记忆 (档案+趋势) +',
        '短期记忆 (近期摘要) +',
        '工作记忆 (当前对话10轮)'
    ]
    
    start_y = y + 0.4
    for i, item in enumerate(context_items):
        ax.text(x, start_y - i*0.32, item, fontsize=10, ha='center')
    
    arrow_down = FancyArrowPatch((x, y-height/2-0.1), (x, y-height/2-0.7),
                                arrowstyle='->', mutation_scale=25, 
                                linewidth=2.5, color=COLORS['accent'])
    ax.add_patch(arrow_down)
    
    ax.text(x+1.8, y-height/2-0.4, '增强型上下文', fontsize=11, 
            weight='bold', color=COLORS['accent'],
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white', 
                     edgecolor=COLORS['accent'], linewidth=1.5))


def draw_llm_layer(ax, x, y):
    """绘制LLM层"""
    width, height = 8, 2.0
    
    rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                         boxstyle="round,pad=0.15",
                         edgecolor=COLORS['secondary'], 
                         facecolor='#F0E6F6',
                         linewidth=2.5)
    ax.add_patch(rect)
    
    ax.text(x, y+0.6, '大语言模型层 (LLM)', fontsize=15, ha='center', 
            weight='bold', color=COLORS['secondary'])
    ax.text(x, y+0.15, '🤖 Qwen2-7B-Instruct 或 OpenAI GPT-4', 
            fontsize=11, ha='center')
    ax.text(x, y-0.3, '基于增强上下文生成专业且个性化回复', 
            fontsize=10, ha='center', style='italic')
    
    arrow = FancyArrowPatch((x, y-height/2-0.1), (x, y-height/2-0.7),
                           arrowstyle='->', mutation_scale=25, 
                           linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow)


def draw_memory_update(ax, x, y):
    """绘制记忆更新模块"""
    width, height = 8, 1.8
    
    rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                         boxstyle="round,pad=0.1",
                         edgecolor=COLORS['border'], 
                         facecolor=COLORS['bg_module'],
                         linewidth=2.5)
    ax.add_patch(rect)
    
    ax.text(x, y+0.6, '记忆更新模块', fontsize=14, ha='center', 
            weight='bold', color=COLORS['text'])
    
    update_items = [
        '• 添加新轮次到工作记忆',
        '• 会话结束→生成摘要→短期',
        '• 更新用户档案→长期记忆'
    ]
    
    for i, item in enumerate(update_items):
        ax.text(x, y - 0.05 - i*0.35, item, fontsize=10, ha='center')
    
    arrow = FancyArrowPatch((x, y-height/2-0.1), (x, y-height/2-0.6),
                           arrowstyle='->', mutation_scale=25, 
                           linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow)


def draw_system_response(ax, x, y):
    """绘制系统回复"""
    width, height = 8.5, 2.0
    
    rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                         boxstyle="round,pad=0.1",
                         edgecolor=COLORS['primary'], 
                         facecolor='#E8F4F8',
                         linewidth=2.5)
    ax.add_patch(rect)
    
    ax.text(x, y+0.7, '【系统回复】', fontsize=13, ha='center', 
            weight='bold', color=COLORS['primary'])
    
    response_text = [
        '"理解你的压力。根据你上次提到的',
        '项目deadline问题，建议尝试：',
        '1. 艾森豪威尔矩阵优先级管理',
        '2. 4-7-8呼吸法改善失眠',
        '3. 固定\'担忧时间\'技术..."'
    ]
    
    for i, line in enumerate(response_text):
        ax.text(x, y+0.25 - i*0.27, line, fontsize=9.5, ha='center', 
                style='italic')
    
    arrow = FancyArrowPatch((x, y-height/2-0.1), (x, y-height/2-0.5),
                           arrowstyle='->', mutation_scale=25, 
                           linewidth=2.5, color=COLORS['arrow'])
    ax.add_patch(arrow)


def draw_user_bottom(ax, x, y):
    """绘制底部用户"""
    user_circle = plt.Circle((x, y), 0.35, color=COLORS['primary'], zorder=10)
    ax.add_patch(user_circle)
    ax.text(x, y, '👤', fontsize=24, ha='center', va='center', zorder=11)
    ax.text(x, y-0.6, '用户', fontsize=13, ha='center', weight='bold')


def draw_innovation_box(ax):
    """绘制右下角创新点说明框"""
    x, y = 15.2, 1.8
    width, height = 2.6, 4.0
    
    rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                         boxstyle="round,pad=0.1",
                         edgecolor=COLORS['highlight'], 
                         facecolor='#FFF9F0',
                         linewidth=2.5, linestyle='-')
    ax.add_patch(rect)
    
    ax.text(x, y+1.7, '关键创新', fontsize=11, ha='center', 
            weight='bold', color=COLORS['highlight'])
    
    innovations = [
        '① 双知识库',
        '   RAG架构',
        '',
        '② 三层记忆',
        '   系统',
        '',
        '③ 端到端',
        '   实现',
        '',
        '④ 多维度',
        '   评估'
    ]
    
    start_y = y + 1.3
    for i, text in enumerate(innovations):
        ax.text(x, start_y - i*0.3, text, fontsize=9, ha='center',
               color=COLORS['text'])


if __name__ == '__main__':
    print("=" * 60)
    print("  智能心理咨询系统架构图生成器 v3.0 (大字体版)")
    print("=" * 60)
    print("")
    
    if not setup_chinese_font():
        sys.exit(1)
    
    print("")
    print("🎨 开始生成图片...")
    print("")
    
    try:
        create_architecture_diagram('architecture_diagram.png', dpi=300)
        create_architecture_diagram('architecture_diagram.pdf', dpi=300)
        
        print("")
        print("=" * 60)
        print("  🎉 所有图片生成完成！")
        print("=" * 60)
        print("")
        print("📁 文件列表：")
        print("   ✓ architecture_diagram.png (大字体版)")
        print("   ✓ architecture_diagram.pdf (大字体版)")
        print("")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)