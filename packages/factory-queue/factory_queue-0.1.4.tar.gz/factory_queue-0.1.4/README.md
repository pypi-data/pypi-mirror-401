# Factory Queue

[![PyPI version](https://badge.fury.io/py/factory-queue.svg)](https://badge.fury.io/py/factory-queue)
[![Python](https://img.shields.io/pypi/pyversions/factory-queue.svg)](https://pypi.org/project/factory-queue/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

流水线工厂模块，支持多节点、多工位、资源控制、磁盘溢出。

## 功能特性

- ✅ **流水线设计** - 链式创建节点，自动管理依赖
- ✅ **多工位并行** - 每个节点支持多线程同时处理
- ✅ **多分支流水线** - 节点可输出多种数据给不同下游节点
- ✅ **自动通知** - 上游节点完成后自动通知下游
- ✅ **资源控制** - 可设置内存上限、队列大小
- ✅ **磁盘溢出** - 内存不足时自动写入磁盘，防止OOM
- ✅ **优雅退出** - 完整的节点同步机制
- ✅ **实时监控** - 定时输出队列和节点状态
- ✅ **彩色日志** - 不同级别日志使用不同颜色显示

## 安装

```bash
pip install factory-queue
```

## 快速开始

### 流水线模式（推荐）

```python
from factory_queue import Factory, Node, ResourceConfig
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# 定义处理函数
def fetch_data(data_id):
    """头节点：获取数据"""
    raw_data = {"id": data_id, "value": data_id * 10}
    
    # 返回多种产物
    if data_id % 2 == 0:
        return {0: raw_data}  # feed 0: 偶数数据
    else:
        return {1: raw_data}  # feed 1: 奇数数据

def process_even(data):
    """处理偶数数据"""
    data["processed"] = data["value"] * 2
    return data

def process_odd(data):
    """处理奇数数据"""
    data["processed"] = data["value"] * 3
    return data

def save_result(data):
    """叶子节点：保存结果（不需要返回值）"""
    print(f"保存数据: {data}")

# 创建流水线
config = ResourceConfig(max_memory_mb=512, max_queue_size=10000)

with Factory(resource_config=config, enable_monitor=True) as factory:
    # 创建头节点（2个工位并行）
    head = factory.head(func=fetch_data, node_num=2, name="数据获取")
    
    # 创建分支1：处理偶数（使用 feed=0）
    node_even = head.create_node(func=process_even, node_num=2, feed=0, name="偶数处理")
    node_even_save = node_even.create_node(func=save_result, node_num=1, feed=0, name="偶数保存")
    
    # 创建分支2：处理奇数（使用 feed=1）
    node_odd = head.create_node(func=process_odd, node_num=1, feed=1, name="奇数处理")
    node_odd_save = node_odd.create_node(func=save_result, node_num=1, feed=0, name="奇数保存")
    
    # 启动流水线
    factory.start()
    
    # 投放数据
    for i in range(100):
        factory.feed(i)
    
    # 通知结束投喂
    factory.end_feed()
    
    # 等待完成
    factory.wait_complete()
```

## 主要类说明

### Factory

流水线工厂主类，管理整个流水线流程。

**主要方法：**
- `head(func, node_num, name)` - 创建头节点
- `feed(data)` - 投放数据
- `end_feed()` - 通知结束投喂
- `start()` - 启动流水线
- `wait_complete(timeout)` - 等待完成
- `stop()` - 停止流水线
- `close()` - 关闭并清理资源

### Node

流水线节点，支持链式创建下游节点。

**主要方法：**
- `create_node(func, node_num, feed, name)` - 创建下游节点

### ResourceConfig

资源配置类。

**参数：**
- `max_memory_mb` - 最大内存使用量(MB)，默认1024
- `max_queue_size` - 队列最大长度，默认10000
- `disk_overflow_threshold` - 磁盘溢出阈值，默认0.8
- `temp_dir` - 临时目录，默认系统临时目录

## 流水线架构

### 线性流水线

```
input -> 头节点 -> 节点1 -> 节点2 -> 叶子节点
```

### 分支流水线

```
              ┌─> 偶数处理 -> 保存数据库
输入 -> 头节点 ┤
              └─> 奇数处理 -> 生成报告
```

### 节点类型

- **头节点**：接收初始数据，可以产生多种产物
- **中间节点**：处理数据并传递给下游
- **叶子节点**：最终处理，不产生输出

## 高级功能

### 多产物输出

```python
def head_process(data):
    # 返回字典，key 为 feed 索引
    return {
        0: data * 2,      # feed 0: 给第一个分支
        1: data * 3,      # feed 1: 给第二个分支
    }

# 创建两个分支

```

### 使用内存比例配置

```python
# 使用系统内存的 10%
```

## 许可证

MIT License

## 作者

stabvale

## 贡献

欢迎提交 Issue 和 Pull Request！
