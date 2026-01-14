import sys
import pdb
import time
import torch
import psutil
import inspect
import threading
import traceback
from functools import wraps
from contextlib import contextmanager
from typing import Optional, Dict, List

GB_UNIT = 1024**3  # GB转换系数

# 尝试导入GPU监控库
try:
    import pynvml

    pynvml.nvmlInit()
    GPU_MONITORING_AVAILABLE = True
except (ImportError, Exception):
    GPU_MONITORING_AVAILABLE = False


# ================== 辅助函数 ==================
class ResourceMonitor:
    """后台监控线程，定期采样CPU和GPU使用率"""

    def __init__(self, process: psutil.Process, interval: float = 0.1):
        self.process = process
        self.interval = interval
        self.monitoring = False
        self.thread = None

        # 监控数据
        self.cpu_percents: List[float] = []
        self.gpu_percents: List[float] = []
        self.gpu_handle = None

        # 初始化GPU监控
        if GPU_MONITORING_AVAILABLE and torch.cuda.is_available():
            try:
                gpu_id = torch.cuda.current_device()
                self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
            except Exception:
                self.gpu_handle = None

    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                # 采样CPU使用率（进程级别）
                cpu_percent = self.process.cpu_percent()
                if cpu_percent is not None:
                    self.cpu_percents.append(cpu_percent)

                # 采样GPU使用率
                if self.gpu_handle is not None:
                    try:
                        util = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
                        self.gpu_percents.append(float(util.gpu))
                    except Exception:
                        pass
            except Exception:
                pass

            time.sleep(self.interval)

    def start(self):
        """启动监控"""
        if self.monitoring:
            return
        self.monitoring = True
        self.cpu_percents.clear()
        self.gpu_percents.clear()
        # 初始化cpu_percent（第一次调用返回0，需要先调用一次）
        self.process.cpu_percent()
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """停止监控并返回统计信息"""
        self.monitoring = False
        if self.thread is not None:
            self.thread.join(timeout=1.0)

        cpu_stats = {
            "max": max(self.cpu_percents) if self.cpu_percents else 0.0,
            "avg": (
                sum(self.cpu_percents) / len(self.cpu_percents)
                if self.cpu_percents
                else 0.0
            ),
        }

        gpu_stats = {
            "max": max(self.gpu_percents) if self.gpu_percents else 0.0,
            "avg": (
                sum(self.gpu_percents) / len(self.gpu_percents)
                if self.gpu_percents
                else 0.0
            ),
        }

        return cpu_stats, gpu_stats


def _init_tracking(
    track_time: bool = True,
    track_memory: bool = True,
    track_usage: bool = True,
):
    """初始化跟踪所需的变量和事件

    Args:
        track_time: 是否统计时间
        track_memory: 是否统计内存
        track_usage: 是否统计CPU/GPU使用率
    """
    tracking_info = {}
    process = None

    # 时间追踪
    if track_time:
        tracking_info["start_time"] = time.perf_counter()
        if torch.cuda.is_available():
            torch.cuda.synchronize()
            tracking_info["start_event"] = torch.cuda.Event(enable_timing=True)
            tracking_info["end_event"] = torch.cuda.Event(enable_timing=True)
        else:
            tracking_info["start_event"] = None
            tracking_info["end_event"] = None

    # 内存追踪
    if track_memory:
        process = psutil.Process()
        tracking_info["process"] = process
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.synchronize()
            tracking_info["gpu_mem_start"] = torch.cuda.memory_allocated() / GB_UNIT
        else:
            tracking_info["gpu_mem_start"] = 0.0
        tracking_info["ram_mem_start"] = process.memory_info().rss / GB_UNIT

    # 使用率监控
    if track_usage:
        if process is None:
            process = psutil.Process()
            tracking_info["process"] = process
        tracking_info["monitor"] = ResourceMonitor(process)
    else:
        tracking_info["monitor"] = None

    return tracking_info


def _print_start_info(
    tag: str,
    track_time: bool = True,
    track_memory: bool = True,
    gpu_mem_start: Optional[float] = None,
    ram_mem_start: Optional[float] = None,
):
    """打印开始监控信息"""
    # 确定监控类型标签
    monitor_types = []
    if track_time:
        monitor_types.append("时间")
    if track_memory:
        monitor_types.append("内存")
    monitor_label = "、".join(monitor_types) if monitor_types else "性能"

    print(f"\n>>>>>>>>>>>>{monitor_label}监控开始 [{tag}]<<<<<<<<<<<<")
    if track_memory:
        if gpu_mem_start is not None:
            print(f"[GPU] Begin: {gpu_mem_start:.2f} GB")
        if ram_mem_start is not None:
            print(f"[RAM] Begin: {ram_mem_start:.2f} GB")
    print(f"------------------------------------------------")


def _print_end_info(
    tag: str,
    track_time: bool = True,
    track_memory: bool = True,
    track_usage: bool = True,
    elapsed_time_wall: Optional[float] = None,
    elapsed_time_gpu: Optional[float] = None,
    gpu_mem_start: Optional[float] = None,
    gpu_mem_end: Optional[float] = None,
    gpu_mem_peak: Optional[float] = None,
    ram_mem_start: Optional[float] = None,
    ram_mem_end: Optional[float] = None,
    cpu_stats: Optional[Dict[str, float]] = None,
    gpu_stats: Optional[Dict[str, float]] = None,
):
    """打印结束监控信息"""
    # 确定监控类型标签
    monitor_types = []
    if track_time:
        monitor_types.append("时间")
    if track_memory:
        monitor_types.append("内存")
    monitor_label = "、".join(monitor_types) if monitor_types else "性能"

    # 打印时间信息
    if track_time:
        if elapsed_time_wall is not None:
            print(f"\n[Time] Wall Time (端到端): {elapsed_time_wall:.4f} s")
        if elapsed_time_gpu is not None:
            print(f"[Time] GPU Time (GPU执行): {elapsed_time_gpu:.4f} s")

    # 打印内存信息
    if track_memory:
        if gpu_mem_end is not None and gpu_mem_start is not None:
            print(
                f"[GPU] Finish: {gpu_mem_end:.2f} GB (+{gpu_mem_end - gpu_mem_start:.2f} GB)"
            )
        if gpu_mem_peak is not None and gpu_mem_start is not None:
            print(
                f"[GPU] Peak:   {gpu_mem_peak:.2f} GB (+{gpu_mem_peak - gpu_mem_start:.2f} GB)"
            )
        if ram_mem_end is not None and ram_mem_start is not None:
            print(
                f"[RAM] Finish: {ram_mem_end:.2f} GB (+{ram_mem_end - ram_mem_start:.2f} GB)"
            )

    # 打印CPU和GPU使用率
    if track_usage:
        if cpu_stats:
            print(
                f"[CPU] Usage: 峰值 {cpu_stats['max']:.1f}% | 平均 {cpu_stats['avg']:.1f}%"
            )
        if gpu_stats:
            print(
                f"[GPU] Usage: 峰值 {gpu_stats['max']:.1f}% | 平均 {gpu_stats['avg']:.1f}%"
            )

    print(f"<<<<<<<<<<<<{monitor_label}监控结束 [{tag}]>>>>>>>>>>>>\n")


def _calculate_metrics(
    tracking_info,
    track_time: bool = True,
    track_memory: bool = True,
    track_usage: bool = True,
):
    """计算监控指标"""
    metrics = {}

    # 计算时间
    if track_time:
        start_time = tracking_info.get("start_time")
        start_event = tracking_info.get("start_event")
        end_event = tracking_info.get("end_event")

        if start_time is not None:
            metrics["elapsed_time_wall"] = time.perf_counter() - start_time

        if (
            start_event is not None
            and end_event is not None
            and torch.cuda.is_available()
        ):
            torch.cuda.synchronize()
            metrics["elapsed_time_gpu"] = start_event.elapsed_time(end_event) / 1000.0
        elif start_event is not None and torch.cuda.is_available():
            # 如果没有预先创建 end_event，则创建一个
            end_event = torch.cuda.Event(enable_timing=True)
            end_event.record()
            torch.cuda.synchronize()
            metrics["elapsed_time_gpu"] = start_event.elapsed_time(end_event) / 1000.0

    # 计算内存
    if track_memory:
        process = tracking_info.get("process")
        if process is not None:
            metrics["ram_mem_end"] = process.memory_info().rss / GB_UNIT
            metrics["ram_mem_start"] = tracking_info.get("ram_mem_start", 0.0)

        if torch.cuda.is_available():
            metrics["gpu_mem_end"] = torch.cuda.memory_allocated() / GB_UNIT
            metrics["gpu_mem_peak"] = torch.cuda.max_memory_allocated() / GB_UNIT
            metrics["gpu_mem_start"] = tracking_info.get("gpu_mem_start", 0.0)

    # 获取使用率统计
    if track_usage:
        monitor = tracking_info.get("monitor")
        if monitor:
            cpu_stats, gpu_stats = monitor.stop()
            metrics["cpu_stats"] = cpu_stats
            metrics["gpu_stats"] = gpu_stats

    return metrics


# ================== 性能追踪器（同时支持上下文管理器和装饰器）==================
class PerformanceTracker:
    """Track GPU memory, system RAM, and execution time.

    同时支持作为上下文管理器和装饰器使用，类似 torch.no_grad 的设计。

    Args:
        name (str, optional): Optional label for distinguishing tracked code blocks.
            When used as decorator, defaults to function name if not provided.
        track_time (bool, optional): 是否统计时间（Wall Time 和 GPU Time）。默认为 True。
        track_memory (bool, optional): 是否统计内存（GPU 内存和 RAM）。默认为 True。
        track_usage (bool, optional): 是否统计 CPU/GPU 使用率。默认为 True。

    Examples:
        # 作为上下文管理器使用（完整监控）
        with PerformanceTracker("Image Generation"):
            run_model()

        # 只统计时间
        with PerformanceTracker("Image Generation", track_memory=False, track_usage=False):
            run_model()

        # 只统计时间和内存，不统计使用率
        with PerformanceTracker("Image Generation", track_usage=False):
            run_model()

        # 作为装饰器使用（同步函数）
        @PerformanceTracker()
        def run_task():
            pass

        @PerformanceTracker("Custom Task", track_memory=False)
        def run_custom_task():
            pass

        # 作为装饰器使用（异步函数）
        @PerformanceTracker("Async Task")
        async def async_task():
            pass
    """

    def __init__(
        self,
        name: str = "",
        track_time: bool = True,
        track_memory: bool = True,
        track_usage: bool = True,
    ):
        self.name = name
        self.track_time = track_time
        self.track_memory = track_memory
        self.track_usage = track_usage
        self.tracking_info = None

    def __enter__(self):
        """上下文管理器入口"""
        tag = self.name or ""
        self.tracking_info = _init_tracking(
            track_time=self.track_time,
            track_memory=self.track_memory,
            track_usage=self.track_usage,
        )

        # 打印开始信息
        _print_start_info(
            tag,
            track_time=self.track_time,
            track_memory=self.track_memory,
            gpu_mem_start=self.tracking_info.get("gpu_mem_start"),
            ram_mem_start=self.tracking_info.get("ram_mem_start"),
        )

        # 启动资源监控（如果启用）
        if self.track_usage and self.tracking_info.get("monitor"):
            self.tracking_info["monitor"].start()

        # 记录时间事件（如果启用）
        if self.track_time and self.tracking_info.get("start_event") is not None:
            torch.cuda.synchronize()
            self.tracking_info["start_event"].record()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        tag = self.name or ""

        # 记录结束事件（如果启用时间追踪）
        if self.track_time and self.tracking_info.get("end_event") is not None:
            self.tracking_info["end_event"].record()

        # 计算指标
        metrics = _calculate_metrics(
            self.tracking_info,
            track_time=self.track_time,
            track_memory=self.track_memory,
            track_usage=self.track_usage,
        )

        # 打印结束信息
        _print_end_info(
            tag,
            track_time=self.track_time,
            track_memory=self.track_memory,
            track_usage=self.track_usage,
            elapsed_time_wall=metrics.get("elapsed_time_wall"),
            elapsed_time_gpu=metrics.get("elapsed_time_gpu"),
            gpu_mem_start=metrics.get("gpu_mem_start"),
            gpu_mem_end=metrics.get("gpu_mem_end"),
            gpu_mem_peak=metrics.get("gpu_mem_peak"),
            ram_mem_start=metrics.get("ram_mem_start"),
            ram_mem_end=metrics.get("ram_mem_end"),
            cpu_stats=metrics.get("cpu_stats"),
            gpu_stats=metrics.get("gpu_stats"),
        )

        return False  # 不抑制异常

    def __call__(self, func):
        """装饰器支持：当作为装饰器使用时调用"""
        if inspect.iscoroutinefunction(func):
            # 异步函数
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                tag = self.name or func.__name__
                tracking_info = _init_tracking(
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    track_usage=self.track_usage,
                )

                # 打印开始信息
                _print_start_info(
                    tag,
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    gpu_mem_start=tracking_info.get("gpu_mem_start"),
                    ram_mem_start=tracking_info.get("ram_mem_start"),
                )

                # 启动资源监控（如果启用）
                if self.track_usage and tracking_info.get("monitor"):
                    tracking_info["monitor"].start()

                # 记录时间事件（如果启用）
                if self.track_time and tracking_info.get("start_event") is not None:
                    torch.cuda.synchronize()
                    tracking_info["start_event"].record()

                result = await func(*args, **kwargs)

                # 记录结束事件（如果启用时间追踪）
                if self.track_time and tracking_info.get("end_event") is not None:
                    tracking_info["end_event"].record()

                # 计算指标
                metrics = _calculate_metrics(
                    tracking_info,
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    track_usage=self.track_usage,
                )

                # 打印结束信息
                _print_end_info(
                    tag,
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    track_usage=self.track_usage,
                    elapsed_time_wall=metrics.get("elapsed_time_wall"),
                    elapsed_time_gpu=metrics.get("elapsed_time_gpu"),
                    gpu_mem_start=metrics.get("gpu_mem_start"),
                    gpu_mem_end=metrics.get("gpu_mem_end"),
                    gpu_mem_peak=metrics.get("gpu_mem_peak"),
                    ram_mem_start=metrics.get("ram_mem_start"),
                    ram_mem_end=metrics.get("ram_mem_end"),
                    cpu_stats=metrics.get("cpu_stats"),
                    gpu_stats=metrics.get("gpu_stats"),
                )

                return result

            return async_wrapper
        else:
            # 同步函数
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                tag = self.name or func.__name__
                tracking_info = _init_tracking(
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    track_usage=self.track_usage,
                )

                # 打印开始信息
                _print_start_info(
                    tag,
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    gpu_mem_start=tracking_info.get("gpu_mem_start"),
                    ram_mem_start=tracking_info.get("ram_mem_start"),
                )

                # 启动资源监控（如果启用）
                if self.track_usage and tracking_info.get("monitor"):
                    tracking_info["monitor"].start()

                # 记录时间事件（如果启用）
                if self.track_time and tracking_info.get("start_event") is not None:
                    torch.cuda.synchronize()
                    tracking_info["start_event"].record()

                result = func(*args, **kwargs)

                # 记录结束事件（如果启用时间追踪）
                if self.track_time and tracking_info.get("end_event") is not None:
                    tracking_info["end_event"].record()

                # 计算指标
                metrics = _calculate_metrics(
                    tracking_info,
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    track_usage=self.track_usage,
                )

                # 打印结束信息
                _print_end_info(
                    tag,
                    track_time=self.track_time,
                    track_memory=self.track_memory,
                    track_usage=self.track_usage,
                    elapsed_time_wall=metrics.get("elapsed_time_wall"),
                    elapsed_time_gpu=metrics.get("elapsed_time_gpu"),
                    gpu_mem_start=metrics.get("gpu_mem_start"),
                    gpu_mem_end=metrics.get("gpu_mem_end"),
                    gpu_mem_peak=metrics.get("gpu_mem_peak"),
                    ram_mem_start=metrics.get("ram_mem_start"),
                    ram_mem_end=metrics.get("ram_mem_end"),
                    cpu_stats=metrics.get("cpu_stats"),
                    gpu_stats=metrics.get("gpu_stats"),
                )

                return result

            return sync_wrapper


@contextmanager
def debug_code(name: str = ""):
    """
    报错时进入pdb，并停留在原始报错位置，可以访问当时的局部变量

    调试提示：
    - 使用 'u' (up) 命令向上移动到调用栈的上一层，查看调用者的变量
    - 使用 'd' (down) 命令向下移动到调用栈的下一层
    - 使用 'w' (where) 命令查看当前调用栈
    - 使用 'l' (list) 命令查看当前代码
    - 使用 'pp <变量名>' 打印变量值
    - 使用 'c' (continue) 继续执行，或 'q' (quit) 退出
    """
    print(f"\n[开始执行] {name}")
    try:
        yield
    except Exception as e:
        print(f"❌ 捕获异常: {repr(e)}")
        # 获取异常信息
        exc_type, exc_value, tb = sys.exc_info()
        traceback.print_exc()  # 打印完整错误堆栈

        # 打印调用栈信息
        print("\n" + "=" * 60)
        print("调用栈信息 (从最外层到报错位置):")
        print("=" * 60)
        frame = tb
        stack_level = 0
        while frame:
            frame_info = frame.tb_frame
            filename = frame_info.f_code.co_filename
            lineno = frame.tb_lineno
            func_name = frame_info.f_code.co_name

            # 获取局部变量（排除内部变量）
            local_vars = {
                k: v for k, v in frame_info.f_locals.items() if not k.startswith("__")
            }

            print(f"\n[{stack_level}] {func_name}() at {filename}:{lineno}")
            if local_vars:
                print(f"    局部变量: {', '.join(local_vars.keys())}")
            else:
                print(f"    局部变量: (无)")

            frame = frame.tb_next
            stack_level += 1

        print("\n" + "=" * 60)
        print("调试提示:")
        print("  u (up)      - 向上移动到调用栈的上一层，查看调用者的变量")
        print("  d (down)    - 向下移动到调用栈的下一层")
        print("  w (where)   - 查看当前调用栈")
        print("  l (list)    - 查看当前代码")
        print("  pp <变量>   - 打印变量值")
        print("  c (continue)- 继续执行")
        print("  q (quit)    - 退出调试")
        print("=" * 60 + "\n")

        pdb.post_mortem(tb)  # 进入出错位置作用域调试
        # 不raise，允许继续执行
    finally:
        print(f"[结束执行] {name}\n")


def debug_on_error_decorator(name: str = None):
    """装饰器版：函数执行报错时进入pdb调试模式

    调试提示：
    - 使用 'u' (up) 命令向上移动到调用栈的上一层，查看调用者的变量
    - 使用 'd' (down) 命令向下移动到调用栈的下一层
    - 使用 'w' (where) 命令查看当前调用栈
    """

    def _print_debug_info(exc_type, exc_value, tb):
        """打印调试信息"""
        print(f"❌ 捕获异常: {repr(exc_value)}")
        traceback.print_exc()

        print("\n" + "=" * 60)
        print("调用栈信息 (从最外层到报错位置):")
        print("=" * 60)
        frame = tb
        stack_level = 0
        while frame:
            frame_info = frame.tb_frame
            filename = frame_info.f_code.co_filename
            lineno = frame.tb_lineno
            func_name = frame_info.f_code.co_name

            # 获取局部变量（排除内部变量）
            local_vars = {
                k: v for k, v in frame_info.f_locals.items() if not k.startswith("__")
            }

            print(f"\n[{stack_level}] {func_name}() at {filename}:{lineno}")
            if local_vars:
                print(f"    局部变量: {', '.join(local_vars.keys())}")
            else:
                print(f"    局部变量: (无)")

            frame = frame.tb_next
            stack_level += 1

        print("\n" + "=" * 60)
        print("调试提示:")
        print("  u (up)      - 向上移动到调用栈的上一层，查看调用者的变量")
        print("  d (down)    - 向下移动到调用栈的下一层")
        print("  w (where)   - 查看当前调用栈")
        print("  l (list)    - 查看当前代码")
        print("  pp <变量>   - 打印变量值")
        print("=" * 60 + "\n")

    def decorator(func):
        if inspect.iscoroutinefunction(func):
            # 异步函数支持
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                tag = name or func.__name__
                print(f"\n[开始执行] {tag}")
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    exc_type, exc_value, tb = sys.exc_info()
                    _print_debug_info(exc_type, exc_value, tb)
                    pdb.post_mortem(tb)
                    raise
                finally:
                    print(f"[结束执行] {tag}\n")

            return async_wrapper
        else:
            # 普通同步函数
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                tag = name or func.__name__
                print(f"\n[开始执行] {tag}")
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    exc_type, exc_value, tb = sys.exc_info()
                    _print_debug_info(exc_type, exc_value, tb)
                    pdb.post_mortem(tb)
                    raise
                finally:
                    print(f"[结束执行] {tag}\n")

            return sync_wrapper

    return decorator
