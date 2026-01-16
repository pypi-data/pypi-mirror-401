# -*- coding: utf-8 -*-
"""
Factory Queue - 高层接口 (High-Level API)
流水线工厂模块 - 基于 core.py 的简化封装
提供链式配置接口，自动管理节点依赖和队列
支持多节点、多工位、多类型产物的流水线处理
"""
import inspect
import json
import logging
import pickle
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Callable, Optional, Union

import psutil

from .core import (
    BaseFactory,  # 底层工厂
    ResourceConfig,
    Producer,
    Consumer,
    logger
)


# 自定义日志过滤器：替换技术词汇为业务名称
class _NodeLogFilter(logging.Filter):
    """将底层技术词汇替换为流水线节点名称"""

    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            # 替换技术词汇
            msg = record.msg
            msg = msg.replace('生产者组', '节点组')
            msg = msg.replace('消费者组', '节点组')
            msg = msg.replace('生产者', '节点')
            msg = msg.replace('消费者', '节点')
            msg = msg.replace('_producer_', '_')
            msg = msg.replace('_consumer_', '_')
            msg = msg.replace('producer', '')
            msg = msg.replace('consumer', '')
            record.msg = msg
        return True


# 全局日志过滤器实例
_log_filter_instance = None


class Node:
    """
    流水线节点 - 封装节点配置和处理逻辑
    支持链式创建下游节点
    """

    def __init__(self, factory: 'Factory', name: str,
                 func: Callable, args: Dict[str, Any] = None,
                 node_num: int = 1, is_head: bool = False,
                 save_result: bool = False, print_processing: bool = True,
                 batch_size: int = 1,
                 setup_func: Callable[[Consumer], None] = None,
                 teardown_func: Callable[[Consumer], None] = None):
        """
        初始化节点
        
        Args:
            factory: 流水线工厂实例
            name: 节点名称
            func: 处理函数，签名为 func(data, **kwargs) 或 func(batch, **kwargs)
            args: 传递给处理函数的额外参数
            node_num: 工位数量（并行线程数）
            is_head: 是否为头节点
            save_result: 是否保存处理结果到文件
            print_processing: 是否打印处理日志（默认True）
            batch_size: 每次从上游队列拿取多少个值（默认1，仅叶子节点有效）
            setup_func: 初始化函数，每个线程启动时调用一次（仅叶子节点有效）
            teardown_func: 清理函数，每个线程结束时调用一次（仅叶子节点有效）
        """
        self.factory = factory
        self.name = name
        self.func = func
        self.args = args or {}
        self.node_num = node_num
        self.is_head = is_head
        self.save_result = save_result
        self.print_processing = print_processing
        self.batch_size = batch_size
        self.setup_func = setup_func
        self.teardown_func = teardown_func

        # 节点输出类型：每个feed索引对应一个队列名
        self._output_feeds: Dict[int, str] = {}
        # 下游节点列表
        self._downstream_nodes: List['Node'] = []
        # 上游节点
        self._upstream_node: Optional['Node'] = None
        # 输入队列名称（由上游节点设置）
        self._input_queue_name: Optional[str] = None
        # 内部组名称（用于底层调度）
        self._group_name: Optional[str] = None
        # 缓存节点路径（性能优化）
        self._cached_path: Optional[str] = None

        # 在工厂中注册节点
        self.factory.register_node(self)

    def _get_node_path(self) -> List[str]:
        """获取从头节点到当前节点的路径"""
        path = []
        current = self
        while current is not None:
            path.insert(0, current.name)
            current = current._upstream_node
        return path

    def _get_save_filename(self) -> str:
        """
        生成保存文件名（根据节点路径）
        使用缓存以提高性能
        """
        if self._cached_path is None:
            path = self._get_node_path()
            self._cached_path = "_".join(path)
        return self._cached_path

    @property
    def input_queue_name(self) -> Optional[str]:
        """获取输入队列名称"""
        return self._input_queue_name

    @property
    def output_feeds(self) -> Dict[int, str]:
        """获取输出队列映射"""
        return self._output_feeds

    @property
    def downstream_nodes(self) -> List['Node']:
        """获取下游节点列表"""
        return self._downstream_nodes

    @property
    def upstream_node(self) -> Optional['Node']:
        """获取上游节点"""
        return self._upstream_node

    @property
    def group_name(self) -> Optional[str]:
        """获取内部组名称"""
        return self._group_name

    def set_input_queue_name(self, queue_name: str) -> None:
        """设置输入队列名称"""
        self._input_queue_name = queue_name

    def set_group_name(self, group_name: str) -> None:
        """设置内部组名称"""
        self._group_name = group_name

    def set_upstream_node(self, upstream: 'Node') -> None:
        """设置上游节点"""
        self._upstream_node = upstream

    def add_downstream_node(self, downstream: 'Node') -> None:
        """添加下游节点"""
        self._downstream_nodes.append(downstream)

    def has_downstream(self) -> bool:
        """判断是否有下游节点"""
        return len(self._downstream_nodes) > 0

    def create_node(self, func: Callable, args: Dict[str, Any] = None,
                    node_num: int = 1, feed: Union[int, str] = 0,
                    name: str = None, save_result: bool = False,
                    print_processing: bool = True, batch_size: int = 1,
                    setup_func: Callable[[Consumer], None] = None,
                    teardown_func: Callable[[Consumer], None] = None) -> 'Node':
        """
        从当前节点创建下游节点，支持链式调用
        
        Args:
            func: 处理函数，签名为 func(data, **kwargs) 或 func(batch, **kwargs)
            args: 传递给处理函数的额外参数（字典）
            node_num: 工位数量（并行线程数）
            feed: 使用上游的哪个产物（索引或名称），默认0表示第一个产物
            name: 节点名称（可选，不指定则自动生成）
            save_result: 是否保存处理结果到文件（默认False）
            print_processing: 是否打印处理日志（默认True）
            batch_size: 每次从上游队列拿取多少个值（默认1，仅叶子节点有效）
            setup_func: 初始化函数，每个线程启动时调用一次（仅叶子节点有效）
            teardown_func: 清理函数，每个线程结束时调用一次（仅叶子节点有效）
        
        Returns:
            新创建的节点对象，可继续链式调用
        """
        # 生成下游节点名称
        if name is None:
            node_name = f"{self.name}_node_{len(self._downstream_nodes)}"
        else:
            node_name = name

        # 创建新节点
        new_node = Node(
            factory=self.factory,
            name=node_name,
            func=func,
            args=args,
            node_num=node_num,
            is_head=False,
            save_result=save_result,
            print_processing=print_processing,
            batch_size=batch_size,
            setup_func=setup_func,
            teardown_func=teardown_func
        )

        # 建立上下游关系
        new_node.set_upstream_node(self)
        self.add_downstream_node(new_node)

        # 确定使用哪个feed（队列）
        feed_key = feed if isinstance(feed, int) else feed

        # 确保上游节点有对应的输出feed
        if feed_key not in self._output_feeds:
            feed_queue_name = f"{self.name}_feed_{feed_key}"
            self._output_feeds[feed_key] = feed_queue_name

        # 新节点的输入队列就是上游的输出队列
        new_node.set_input_queue_name(self._output_feeds[feed_key])

        return new_node

    def build_process_func(self) -> Callable:
        """构建节点处理函数（公共接口）"""
        return self._build_process_func()

    def build_consume_func(self) -> Callable:
        """构建叶子节点处理函数（公共接口）"""
        return self._build_consume_func()

    def _build_process_func(self) -> Callable:
        """
        构建节点处理函数，将用户函数包装为内部格式
        
        返回值处理规则：
        1. None: 不输出任何数据
        2. 字典: 按键匹配feed（向后兼容）
        3. 元组(tuple): 按位置分发到不同feed（位置0→feed=0, 位置1→feed=1...）
           - 每个位置的值如果是列表，底层会逐个元素放入队列
           - 每个位置的值如果是单个元素，直接放入队列
        4. 列表(list): 整个列表放入feed=0，底层会逐个元素放入队列
        5. 单个值: 放入feed=0
        
        示例：
        - return [1,2,3] → 1、2、3依次进入feed=0的队列
        - return (val1, val2) → val1进feed=0, val2进feed=1
        - return ([1,2], 'aa') → [1,2]的元素进feed=0, 'aa'进feed=1
        - return 'single' → 'single'进feed=0
        """
        # 提前捕获变量，避免闭包引用self
        node_name = self.name
        save_result_flag = self.save_result
        print_log = self.print_processing  # 是否打印处理日志
        node_args = self.args
        user_func = self.func
        output_feeds = self._output_feeds
        # 预先计算feed键集合（性能优化）
        output_feed_keys = frozenset(output_feeds.keys())
        has_args = bool(node_args)
        
        # 检查用户函数是否接受 worker 参数
        sig = inspect.signature(user_func)
        params = list(sig.parameters.keys())
        # 判断是否有第二个参数（worker）或使用了 **kwargs
        accepts_worker = (
            len(params) >= 2 or 
            any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        )

        # 如果需要保存结果，预先捕获保存方法（绑定self）
        if save_result_flag:
            # 使用lambda捕获self，保持实例方法的绑定
            save_func = lambda result, worker_num: self._save_result_to_file(result, worker_num)
        else:
            save_func = None

        def wrapper(data: Any, producer: Producer) -> Dict[str, Any]:
            try:
                # 提取worker编号用于显示
                worker_id = producer.worker_id
                # 优化：使用rsplit代替split，只分割一次
                worker_num = worker_id.rsplit('_', 1)[-1] if '_' in worker_id else '0'
                display_name = f"{node_name}_{worker_num}"

                # 根据函数签名智能调用
                if accepts_worker:
                    # 函数接受 worker 参数
                    result = user_func(data, producer, **node_args) if has_args else user_func(data, producer)
                else:
                    # 函数不接受 worker 参数
                    result = user_func(data, **node_args) if has_args else user_func(data)

                # 打印处理日志（如果启用）
                if print_log:
                    logger.info(f"[{display_name}] 处理: {data}")

                # 保存处理结果（如果启用）
                if save_func and result is not None:
                    save_func(result, worker_num)

                # 将结果转换为队列分发格式
                if result is None:
                    return {}

                output_dict = {}

                # 情况1：字典返回值（按键匹配feed） - 仅当字典键包含整数feed索引时
                # 优化：使用交集代替any()，性能更好
                if isinstance(result, dict):
                    # 检查是否为feed分发字典
                    if output_feed_keys & result.keys():
                        # 这是一个feed分发字典
                        for feed_key, queue_name in output_feeds.items():
                            if feed_key in result and result[feed_key] is not None:
                                output_dict[queue_name] = result[feed_key]
                        return output_dict
                    # 继续往下执行单一返回值的逻辑

                # 情况2：元组返回值（按位置分发到不同feed）
                if isinstance(result, tuple):
                    for idx, item in enumerate(result):
                        if item is None:
                            continue
                        if idx in output_feeds:
                            # 该位置的值放入对应的feed队列
                            # 如果是列表，底层会逐个元素放入；如果是单值，直接放入
                            output_dict[output_feeds[idx]] = item
                    return output_dict

                # 情况3：列表返回值（整个列表放入feed=0）
                if isinstance(result, list):
                    # 列表作为一组数据，整体放入feed=0
                    if 0 in output_feeds:
                        output_dict[output_feeds[0]] = result
                    return output_dict

                # 情况4：单一返回值（包括普通字典对象），放入feed=0
                if 0 in output_feeds:
                    output_dict[output_feeds[0]] = result

                return output_dict

            except Exception as e:
                logger.error(f"节点 [{node_name}] 处理函数执行失败: {e}", exc_info=True)
                return {}

        return wrapper

    def _build_consume_func(self) -> Callable:
        """
        构建叶子节点处理函数
        叶子节点不产生输出，仅处理数据
        """
        node_name = self.name
        save_result_flag = self.save_result
        print_log = self.print_processing  # 是否打印处理日志
        node_args = self.args
        user_func = self.func
        
        # 检查用户函数是否接受 worker 参数
        sig = inspect.signature(user_func)
        params = list(sig.parameters.keys())
        # 判断是否有第二个参数（worker）或使用了 **kwargs
        accepts_worker = (
            len(params) >= 2 or 
            any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        )

        def wrapper(data: Any, consumer: Consumer):
            try:
                # 提取worker编号用于显示
                worker_id = consumer.worker_id
                worker_num = worker_id.split('_')[-1] if '_' in worker_id else '0'
                display_name = f"{node_name}_{worker_num}"

                # 打印处理日志（如果启用）
                if print_log:
                    logger.info(f"[{display_name}] 处理: {data}")

                # 根据函数签名智能调用
                if accepts_worker:
                    # 函数接受 worker 参数
                    result = user_func(data, consumer, **node_args) if node_args else user_func(data, consumer)
                else:
                    # 函数不接受 worker 参数
                    result = user_func(data, **node_args) if node_args else user_func(data)

                # 保存处理结果（如果启用）
                if save_result_flag and result is not None:
                    self._save_result_to_file(result, worker_num)

            except Exception as e:
                logger.error(f"节点 [{node_name}] 消费函数执行失败: {e}", exc_info=True)

        return wrapper

    def _save_result_to_file(self, result: Any, worker_num: str) -> None:
        """
        保存处理结果到文件
        
        Args:
            result: 要保存的结果数据
            worker_num: 工位编号
        """
        try:
            # 获取并创建temp_dir
            temp_dir = Path(self.factory.get_temp_dir())
            temp_dir.mkdir(parents=True, exist_ok=True)

            # 生成唯一文件名
            base_filename = self._get_save_filename()
            timestamp = int(time.time() * 1000)

            # 根据数据类型选择保存格式
            if isinstance(result, (dict, list)):
                # JSON格式（可读性好）
                filename = f"{base_filename}_w{worker_num}_{timestamp}.json"
                filepath = temp_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                # Pickle格式（支持任意Python对象）
                filename = f"{base_filename}_w{worker_num}_{timestamp}.pkl"
                filepath = temp_dir / filename
                with open(filepath, 'wb') as f:
                    pickle.dump(result, f)

            logger.debug(f"节点 [{self.name}] 保存结果到: {filepath}")
        except Exception as e:
            logger.error(f"节点 [{self.name}] 保存结果失败: {e}", exc_info=True)


class Factory:
    """
    流水线工厂 - 基于原有BaseFactory的简化封装
    提供链式配置接口，自动管理节点依赖和队列
    """

    def __init__(self, resource_config: ResourceConfig = None,
                 enable_monitor: bool = True, monitor_interval: float = 10.0,
                 max_memory_percent: float = None,
                 hide_technical_terms: bool = True):
        """
        初始化流水线工厂
        
        Args:
            resource_config: 资源配置
            enable_monitor: 是否启用监控
            monitor_interval: 监控间隔（秒）
            max_memory_percent: 最大内存使用比例（0-1之间），如0.5表示使用50%系统内存
                               如果指定，会覆盖resource_config中的max_memory_mb
            hide_technical_terms: 是否隐藏底层技术词汇（默认True，将底层术语替换为节点）
        """
        global _log_filter_instance
        # 如果启用隐藏技术词汇，添加日志过滤器（只添加一次）
        if hide_technical_terms and _log_filter_instance is None:
            _log_filter_instance = _NodeLogFilter()
            # 将过滤器添加到 core 模块的 logger
            factory_logger = logging.getLogger('factory_queue.core')
            factory_logger.addFilter(_log_filter_instance)

        # 处理内存比例配置
        if max_memory_percent is not None:
            if not (0 < max_memory_percent <= 1):
                raise ValueError(f"max_memory_percent必须在0-1之间，当前值: {max_memory_percent}")

            # 获取系统总内存
            total_memory_mb = psutil.virtual_memory().total / (1024 * 1024)
            calculated_memory_mb = int(total_memory_mb * max_memory_percent)

            logger.info(
                f"系统总内存: {total_memory_mb:.0f}MB, 配置使用比例: {max_memory_percent * 100:.0f}%, 计算得: {calculated_memory_mb}MB")

            # 如果没有提供resource_config，创建一个
            if resource_config is None:
                resource_config = ResourceConfig(max_memory_mb=calculated_memory_mb)
            else:
                # 覆盖max_memory_mb
                resource_config.max_memory_mb = calculated_memory_mb

        # 创建底层工厂
        self._base_factory = BaseFactory(
            resource_config=resource_config,
            enable_monitor=enable_monitor,
            monitor_interval=monitor_interval
        )

        # 头节点
        self._head_node: Optional[Node] = None
        # 所有节点（包括头节点）
        self._all_nodes: List[Node] = []
        # 输入队列名称（固定）
        self._input_queue_name = "pipeline_input"

        # 是否已构建
        self._built = False

    def head(self, func: Callable, args: Dict[str, Any] = None,
             node_num: int = 1, name: str = "head",
             save_result: bool = False, print_processing: bool = True,
             setup_func: Callable[[Consumer], None] = None,
             teardown_func: Callable[[Consumer], None] = None) -> Node:
        """
        创建头节点（流水线起点）
        
        Args:
            func: 处理函数
            args: 函数参数
            node_num: 工位数量
            name: 节点名称（默认"head"）
            save_result: 是否保存处理结果到文件（默认False）
            print_processing: 是否打印处理日志（默认True）
            setup_func: 初始化函数（头节点通常不需要，保留以保持接口一致性）
            teardown_func: 清理函数（头节点通常不需要，保留以保持接口一致性）
        
        Returns:
            头节点对象
        """
        if self._head_node is not None:
            raise ValueError("头节点已存在，不能重复创建")

        self._head_node = Node(
            factory=self,
            name=name,
            func=func,
            args=args,
            node_num=node_num,
            is_head=True,
            save_result=save_result,
            print_processing=print_processing,
            setup_func=setup_func,
            teardown_func=teardown_func
        )

        # 头节点的输入队列是固定的
        self._head_node.set_input_queue_name(self._input_queue_name)

        return self._head_node

    def register_node(self, node: Node) -> None:
        """注册节点到工厂"""
        self._all_nodes.append(node)

    def get_temp_dir(self) -> str:
        """获取临时目录路径"""
        return self._base_factory.resource_config.temp_dir

    def _register_node(self, node: Node):
        """私有方法，已弃用，使用 register_node 代替"""
        self.register_node(node)

    def _build(self):
        """
        构建流水线：创建所有队列和节点组
        在start()时自动调用
        """
        if self._built:
            return

        if self._head_node is None:
            raise ValueError("请先创建头节点")

        logger.info("开始构建流水线...")

        # 创建输入队列
        self._base_factory.create_queue(self._input_queue_name, max_size=5000)

        # 遍历所有节点，创建对应的节点组
        for node in self._all_nodes:
            self._build_node(node)

        self._built = True
        logger.info(f"流水线构建完成，共 {len(self._all_nodes)} 个节点")

    def _build_node(self, node: Node) -> None:
        """
        为单个节点创建内部处理组
        
        - 中间节点：有下游节点，需要传递数据
        - 叶子节点：无下游节点，仅处理数据
        
        Args:
            node: 要构建的节点
        """
        # 获取节点输入队列
        input_queue_name = node.input_queue_name

        # 判断节点类型：是否有下游
        has_downstream = node.has_downstream()

        if has_downstream:
            # 中间节点：创建内部处理组
            output_queue_names = list(node.output_feeds.values())

            # 为每个输出队列创建队列对象
            for queue_name in output_queue_names:
                self._base_factory.create_queue(queue_name, max_size=100000)

            # 创建内部处理组（使用节点名作为组名，这样worker_id就是节点名_工位号）
            producer_group_name = f"{node.name}_producer_group"
            node.set_group_name(producer_group_name)

            self._base_factory.create_producer_group(
                name=node.name,  # 使用节点名，生成简洁的worker_id
                input_queue_name=input_queue_name,
                output_consumer_names=output_queue_names,
                process_func=node.build_process_func(),
                num_workers=node.node_num,
                process_func_args={},
                setup_func=node.setup_func,
                teardown_func=node.teardown_func
            )
            # 更新组名为实际创建的组名（用于内部引用）
            node.set_group_name(node.name)

            logger.info(
                f"节点 [{node.name}] 创建为节点组，"
                f"工位数={node.node_num}, 输出队列={output_queue_names}"
            )
        else:
            # 叶子节点：创建内部处理组（使用节点名作为组名）
            consumer_group_name = f"{node.name}_consumer_group"
            node.set_group_name(consumer_group_name)

            # 绑定上游节点（使用上游节点的group_name）
            bind_names = None
            upstream = node.upstream_node
            if upstream and upstream.group_name:
                bind_names = [upstream.group_name]

            self._base_factory.create_consumer_group(
                name=input_queue_name,  # 队列名
                consume_func=node.build_consume_func(),
                num_workers=node.node_num,
                batch_size=node.batch_size,
                batch_timeout=None,
                bind_producer_names=bind_names,
                consume_func_args={},
                setup_func=node.setup_func,
                teardown_func=node.teardown_func
            )
            # 更新组名为实际的组名（就是input_queue_name）
            node.set_group_name(input_queue_name)

            logger.info(
                f"节点 [{node.name}] 创建为节点组，"
                f"工位数={node.node_num}, 绑定上游={bind_names}, 批量大小={node.batch_size}"
            )

    def feed(self, data: Any) -> bool:
        """
        向流水线投放数据
        
        Args:
            data: 要处理的数据
        
        Returns:
            是否投放成功
        """
        if not self._built:
            raise RuntimeError("请先调用 start() 启动流水线")
        return self._base_factory.feed(self._input_queue_name, data)

    def feed_batch(self, data_list: List[Any]) -> None:
        """
        批量投放数据
        
        Args:
            data_list: 数据列表
        """
        if not self._built:
            raise RuntimeError("请先调用 start() 启动流水线")
        self._base_factory.feed_batch(self._input_queue_name, data_list)

    def end_feed(self) -> None:
        """
        通知头节点：没有更多数据了
        """
        if self._head_node and self._head_node.group_name:
            self._base_factory.end_feed(self._head_node.group_name)
            logger.info(f"已通知头节点 [{self._head_node.name}] 结束投喂")
        else:
            logger.warning("头节点不存在或未构建，无法通知结束投喂")

    def start(self) -> None:
        """启动流水线，自动构建所有节点"""
        self._build()
        self._base_factory.start()
        logger.info("流水线已启动")

    def wait_complete(self, timeout: float = None) -> None:
        """
        等待流水线处理完成
        
        实现逻辑：
        1. 启动监控线程，检测中间节点完成并自动通知下游
        2. 等待所有叶子节点完成
        3. 停止监控线程
        
        Args:
            timeout: 超时时间（秒），默认无限等待
        """
        # 启动自动通知线程
        stop_monitor = threading.Event()

        def auto_notify_downstream():
            """监控中间节点，完成后自动通知下游"""
            notified = set()  # 已通知的节点

            while not stop_monitor.is_set():
                time.sleep(0.5)  # 检查间隔

                # 遍历所有中间节点
                for node in self._all_nodes:
                    if not node.group_name:
                        continue

                    # 跳过已通知的节点
                    if node.group_name in notified:
                        continue

                    # 只处理中间节点
                    if not node.has_downstream():
                        continue

                    # 检查该节点是否完成
                    stats = self._base_factory.stats
                    pg_stats = stats.get("producer_groups", {}).get(node.group_name)

                    if pg_stats and pg_stats.get("finished"):
                        # 该节点已完成，通知所有下游节点
                        for downstream_node in node.downstream_nodes:
                            if downstream_node.group_name and downstream_node.has_downstream():
                                # 下游也是中间节点
                                self._base_factory.end_feed(downstream_node.group_name)
                                logger.info(
                                    f"节点 [{node.name}] 完成，自动通知下游节点 [{downstream_node.name}] 结束投喂"
                                )

                        notified.add(node.group_name)

        # 启动监控线程
        monitor_thread = threading.Thread(target=auto_notify_downstream, daemon=True)
        monitor_thread.start()

        try:
            # 等待底层工厂完成（等待所有节点）
            self._base_factory.wait_complete(timeout=timeout)
        finally:
            # 停止监控线程
            stop_monitor.set()
            monitor_thread.join(timeout=1)

    def stop(self) -> None:
        """停止流水线，中断所有处理线程"""
        self._base_factory.stop()

    def close(self) -> None:
        """关闭流水线，清理资源"""
        self._base_factory.close()

    @property
    def stats(self) -> Dict:
        """
        获取流水线统计信息
        返回简化后的统计数据，包含输入输出信息
        """
        raw_stats = self._base_factory.stats

        def simplify_worker_stats(worker_stats: Dict, worker_type: str) -> Dict:
            """处理单个worker的统计信息"""
            worker_id = worker_stats.get('worker_id', '')

            # 清理worker_id中的内部标识
            simplified_id = worker_id
            simplified_id = simplified_id.replace('_feed_', '_')
            simplified_id = simplified_id.replace('_consumer_', '_')
            simplified_id = simplified_id.replace('_producer_', '_')

            result = {
                'worker_id': simplified_id,
                'running': worker_stats.get('running', False),
                'errors': worker_stats.get('errors', 0)
            }

            # 添加处理数据统计
            if worker_type == 'producer':
                result['input'] = worker_stats.get('processed', 0)
                result['output'] = worker_stats.get('processed', 0)
            else:  # consumer
                result['consumed'] = worker_stats.get('processed', 0)

            return result

        # 处理中间节点统计
        if 'producer_groups' in raw_stats:
            for pg_name, pg_stats in raw_stats['producer_groups'].items():
                if 'producers' in pg_stats:
                    pg_stats['producers'] = [
                        simplify_worker_stats(p, 'producer')
                        for p in pg_stats['producers']
                    ]

        # 处理叶子节点统计
        if 'consumer_groups' in raw_stats:
            for cg_name, cg_stats in raw_stats['consumer_groups'].items():
                if 'consumers' in cg_stats:
                    cg_stats['consumers'] = [
                        simplify_worker_stats(c, 'consumer')
                        for c in cg_stats['consumers']
                    ]

        return raw_stats

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
