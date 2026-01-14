#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终端进度显示模块
使用 Rich 库实现分屏界面：上方显示任务进度，下方显示滚动日志
"""

import logging
import os
import threading
import sys
from collections import deque
from datetime import datetime
from typing import Optional

from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text


class TerminalUI:
    """终端UI管理器，提供分屏进度显示"""

    # 进度面板固定高度
    PROGRESS_PANEL_HEIGHT = 10

    def __init__(self, max_log_lines: int = 500):
        # 使用独立的 Console，强制输出到 stderr 避免与 uvicorn 冲突
        self.console = Console(stderr=True, force_terminal=True)
        # 日志缓冲区容量（存储更多历史日志）
        self.log_buffer = deque(maxlen=max_log_lines)
        # 日志显示行数（从环境变量读取，默认4行）
        self.log_display_lines = int(os.getenv("TERMINAL_LOG_LINES", "4"))
        # 日志滚动位置（0表示最新，正数表示向上滚动的行数）
        self.scroll_offset = 0
        self._lock = threading.Lock()

        # 任务统计
        self.stats = {
            'total': 0,
            'current': 0,
            'success': 0,
            'out_of_stock': 0,
            'cart_missing': 0,
            'failed': 0,
            'captcha': 0,
            'current_url': '',
            'start_time': None,
            'data_source': ''
        }

        # Rich 组件
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
            console=self.console,
            expand=True
        )
        self.task_id = None
        self.live: Optional[Live] = None
        self._running = False

    def _create_stats_table(self) -> Table:
        """创建统计信息表格"""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Label", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Label2", style="cyan")
        table.add_column("Value2", style="green")

        # 计算进度百分比
        progress_pct = (self.stats['current'] / max(self.stats['total'], 1)) * 100
        success_rate = (self.stats['success'] / max(self.stats['current'], 1)) * 100

        table.add_row(
            "总数:", str(self.stats['total']),
            "已检测:", f"{self.stats['current']} ({progress_pct:.1f}%)"
        )
        table.add_row(
            "正常:", f"[green]{self.stats['success']}[/green]",
            "正常率:", f"[green]{success_rate:.1f}%[/green]"
        )
        table.add_row(
            "无库存:", f"[yellow]{self.stats['out_of_stock']}[/yellow]",
            "购物车丢失:", f"[red]{self.stats['cart_missing']}[/red]"
        )
        table.add_row(
            "其他异常:", f"[red]{self.stats['failed']}[/red]",
            "验证码:", f"[yellow]{self.stats['captcha']}[/yellow]"
        )

        return table

    def _get_terminal_height(self) -> int:
        """获取实时终端高度"""
        try:
            return os.get_terminal_size().lines
        except OSError:
            return self.console.size.height

    def _get_visible_log_lines(self) -> int:
        """计算可见的日志行数（基于终端实际高度）"""
        terminal_height = self._get_terminal_height()
        # 终端高度 - 进度面板高度 - 日志面板边框(2) - 边距(1)
        visible = terminal_height - self.PROGRESS_PANEL_HEIGHT - 2 - 1
        return max(visible, 3)  # 最小3行

    def _create_scrollbar(self, total_lines: int, visible_lines: int, scroll_pos: int) -> str:
        """创建滚动条指示器"""
        if total_lines <= visible_lines:
            return ""

        # 计算滚动条位置
        scrollbar_height = visible_lines - 2  # 减去上下箭头
        if scrollbar_height < 1:
            return ""

        # 计算滑块位置和大小
        thumb_size = max(1, int(scrollbar_height * visible_lines / total_lines))
        thumb_pos = int((scrollbar_height - thumb_size) * scroll_pos / max(total_lines - visible_lines, 1))

        # 构建滚动条
        scrollbar = "▲\n"
        for i in range(scrollbar_height):
            if thumb_pos <= i < thumb_pos + thumb_size:
                scrollbar += "█\n"
            else:
                scrollbar += "░\n"
        scrollbar += "▼"

        return scrollbar

    def _create_renderable(self):
        """创建可渲染的内容"""
        # 创建整体布局
        layout = Layout()

        # 分割为上下两部分：进度区域（固定高度）和日志区域（填充剩余）
        layout.split_column(
            Layout(name="progress", size=self.PROGRESS_PANEL_HEIGHT),
            Layout(name="log")
        )

        # 上方：进度信息
        stats_table = self._create_stats_table()

        # 当前URL显示
        current_url = self.stats['current_url']
        if len(current_url) > 70:
            current_url = current_url[:67] + "..."
        url_text = Text(f"当前: {current_url}", style="dim")

        # 数据来源
        source_text = Text(f"数据来源: {self.stats['data_source']}", style="italic cyan")

        progress_content = Group(
            source_text,
            self.progress,
            Text(""),
            stats_table,
            url_text
        )

        progress_panel = Panel(
            progress_content,
            title="[bold]任务进度[/bold]",
            border_style="blue"
        )

        layout["progress"].update(progress_panel)

        # 下方：日志区域（自动填充剩余高度）
        visible_lines = self._get_visible_log_lines()

        log_lines = list(self.log_buffer)
        total_lines = len(log_lines)

        # 计算显示范围
        if total_lines <= visible_lines:
            # 日志未填满，从顶部开始显示
            display_lines = log_lines
            scroll_pos = 0
        else:
            # 日志已填满，显示最新的日志（底部）
            start_idx = total_lines - visible_lines
            display_lines = log_lines[start_idx:]
            scroll_pos = total_lines - visible_lines

        # 构建日志文本
        log_text = Text()

        for i, line in enumerate(display_lines):
            # 根据日志级别着色
            newline = "\n"
            if "ERROR" in line or "错误" in line:
                log_text.append(line + newline, style="red")
            elif "WARNING" in line or "警告" in line:
                log_text.append(line + newline, style="yellow")
            elif "成功" in line or "SUCCESS" in line:
                log_text.append(line + newline, style="green")
            else:
                log_text.append(line + newline, style="dim")

        # 如果日志行数少于可见行数，在底部添加空行填充，使内容从顶部开始
        if len(display_lines) < visible_lines:
            padding_lines = visible_lines - len(display_lines)
            for _ in range(padding_lines):
                log_text.append("\n")

        # 创建滚动条
        scrollbar = self._create_scrollbar(total_lines, visible_lines, scroll_pos)

        # 构建标题（包含滚动信息）
        if total_lines > visible_lines:
            title = f"[bold]实时日志[/bold] [dim]({total_lines} 行, 显示最新 {visible_lines} 行)[/dim]"
        else:
            title = "[bold]实时日志[/bold]"

        # 使用 Table 来并排显示日志和滚动条
        if scrollbar:
            log_table = Table(show_header=False, box=None, padding=0, expand=True)
            log_table.add_column("log", ratio=1)
            log_table.add_column("scrollbar", width=1)
            log_table.add_row(log_text, Text(scrollbar, style="dim cyan"))

            log_panel = Panel(
                log_table,
                title=title,
                border_style="green"
            )
        else:
            log_panel = Panel(
                log_text,
                title=title,
                border_style="green"
            )

        layout["log"].update(log_panel)

        return layout

    def start(self, total: int, data_source: str = ""):
        """启动终端UI"""
        self.stats['total'] = total
        self.stats['current'] = 0
        self.stats['success'] = 0
        self.stats['out_of_stock'] = 0
        self.stats['cart_missing'] = 0
        self.stats['failed'] = 0
        self.stats['captcha'] = 0
        self.stats['start_time'] = datetime.now()
        self.stats['data_source'] = data_source

        self.task_id = self.progress.add_task("检测进度", total=total)

        # 使用全屏模式避免与其他输出混合
        # screen=True: 占据整个终端，避免闪烁和追加问题
        self.live = Live(
            self._create_renderable(),
            console=self.console,
            refresh_per_second=4,
            screen=True,  # 全屏模式，避免与其他输出混合
            transient=False
        )
        self._running = True
        self.live.start()

    def stop(self):
        """停止终端UI"""
        self._running = False
        if self.live:
            self.live.stop()
            self.live = None
        # 打印最终统计
        self.console.print(self._create_renderable())

    def update(self, url: str = "", status: str = "success"):
        """更新进度"""
        if not self._running:
            return

        with self._lock:
            self.stats['current'] += 1
            self.stats['current_url'] = url

            if status == "success":
                self.stats['success'] += 1
            elif status == "out_of_stock":
                self.stats['out_of_stock'] += 1
            elif status == "cart_button_missing":
                self.stats['cart_missing'] += 1
            else:
                self.stats['failed'] += 1

            if self.task_id is not None:
                self.progress.update(self.task_id, completed=self.stats['current'])

            if self.live:
                self.live.update(self._create_renderable())

    def increment_captcha(self):
        """增加验证码计数"""
        with self._lock:
            self.stats['captcha'] += 1
            # 不手动触发更新，等待下次自动刷新

    def correct_stats(self, original_status: str):
        """重试成功后修正统计：将原状态计数减1，成功计数加1

        Args:
            original_status: 原始状态 (out_of_stock, cart_button_missing, failed)
        """
        with self._lock:
            # 减少原状态计数
            if original_status == "out_of_stock":
                self.stats['out_of_stock'] = max(0, self.stats['out_of_stock'] - 1)
            elif original_status == "cart_button_missing":
                self.stats['cart_missing'] = max(0, self.stats['cart_missing'] - 1)
            else:
                self.stats['failed'] = max(0, self.stats['failed'] - 1)

            # 增加成功计数
            self.stats['success'] += 1

            if self.live:
                self.live.update(self._create_renderable())

    def add_log(self, message: str):
        """添加日志消息"""
        with self._lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_buffer.append(f"[{timestamp}] {message}")
            # 立即触发更新，确保日志实时显示
            if self.live and self._running:
                self.live.update(self._create_renderable())

    def get_stats(self) -> dict:
        """获取当前统计信息"""
        return self.stats.copy()


class TerminalLogHandler(logging.Handler):
    """自定义日志处理器，将日志输出到终端UI"""

    def __init__(self, terminal_ui: TerminalUI):
        super().__init__()
        self.terminal_ui = terminal_ui

    def emit(self, record):
        try:
            msg = self.format(record)
            # 简化日志消息，只保留关键信息
            if " - " in msg:
                parts = msg.split(" - ", 2)
                if len(parts) >= 3:
                    msg = parts[2]  # 只保留消息部分
            self.terminal_ui.add_log(msg)
        except Exception:
            pass


# 全局实例（可选使用）
_terminal_ui: Optional[TerminalUI] = None


def get_terminal_ui() -> Optional[TerminalUI]:
    """获取全局终端UI实例"""
    return _terminal_ui


def create_terminal_ui(max_log_lines: int = 12) -> TerminalUI:
    """创建并返回终端UI实例"""
    global _terminal_ui
    _terminal_ui = TerminalUI(max_log_lines=max_log_lines)
    return _terminal_ui
