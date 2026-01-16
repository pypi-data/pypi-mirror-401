# -*- coding: utf-8 -*-
"""
Factory Queue - 生产者-消费者工厂模块
支持多生产者、多消费者、多队列、资源控制、磁盘溢出

模块结构：
- core.py: 核心底层实现（BaseFactory, DiskBackedQueue, Producer, Consumer 等）
- factory.py: 高层用户接口（Factory, Node）

推荐使用：
    from factory_queue import Factory, Node, ResourceConfig
"""

from .core import (
    # 配置类
    ResourceConfig,
    SharedConfig,
    
    # 核心类
    DiskBackedQueue,
    Producer,
    Consumer,
    ProducerGroup,
    ConsumerGroup,
    BaseFactory,
    
    # 工具类
    ColoredFormatter,
)

# 高层接口（推荐使用）
from .factory import Factory, Node

__version__ = '0.1.3'
__author__ = 'Your Name'
__all__ = [
    # 配置类
    'ResourceConfig',
    'SharedConfig',
    
    # 底层核心类
    'DiskBackedQueue',
    'Producer',
    'Consumer',
    'ProducerGroup',
    'ConsumerGroup',
    'BaseFactory',
    
    # 高层接口（推荐）
    'Factory',
    'Node',
    
    # 工具类
    'ColoredFormatter',
]
