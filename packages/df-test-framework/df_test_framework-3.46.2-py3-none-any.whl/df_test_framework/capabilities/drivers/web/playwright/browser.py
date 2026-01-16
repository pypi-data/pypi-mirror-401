"""浏览器管理器

提供浏览器实例的创建、配置和管理
基于 Playwright 实现，支持多种浏览器
"""

from enum import Enum
from typing import Any

try:
    from playwright.sync_api import (
        Browser,
        BrowserContext,
        Page,
        Playwright,
        sync_playwright,
    )

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = Any
    BrowserContext = Any
    Page = Any
    Playwright = Any

    # 为测试 mock 提供占位符
    def sync_playwright():
        raise ImportError("Playwright未安装")


class BrowserType(str, Enum):
    """浏览器类型枚举"""

    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class BrowserManager:
    """
    浏览器管理器

    基于 Playwright 实现，提供浏览器启动、配置和页面管理。

    使用示例:
        >>> # 配置驱动模式（推荐）
        >>> manager = BrowserManager(config=web_config, runtime=runtime)
        >>> manager.start()
        >>> manager.page.goto("https://example.com")
        >>> manager.stop()
        >>>
        >>> # 上下文管理器
        >>> with BrowserManager(config=web_config) as (browser, context, page):
        ...     page.goto("https://example.com")
    """

    def __init__(
        self,
        config: Any | None = None,
        runtime: Any | None = None,
        **overrides: Any,
    ):
        """
        初始化浏览器管理器

        Args:
            config: WebConfig 配置对象
            runtime: RuntimeContext 实例 - 用于事件发布
            **overrides: 配置覆盖（browser_type, headless, timeout 等）

        Raises:
            ImportError: 如果未安装 Playwright
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright未安装。请运行: pip install playwright && playwright install"
            )

        # 从 config 读取配置，overrides 优先
        def get_config(key: str, default: Any) -> Any:
            if key in overrides and overrides[key] is not None:
                return overrides[key]
            if config and hasattr(config, key):
                return getattr(config, key)
            return default

        # 浏览器类型需要特殊处理（字符串转枚举）
        browser_type_value = get_config("browser_type", "chromium")
        if isinstance(browser_type_value, str):
            browser_type_value = BrowserType(browser_type_value)

        self.base_url = get_config("base_url", None)
        self.browser_type = browser_type_value
        self.headless = get_config("headless", True)
        self.slow_mo = get_config("slow_mo", 0)
        self.timeout = get_config("timeout", 30000)
        self.viewport = get_config("viewport", {"width": 1280, "height": 720})
        self.record_video = get_config("record_video", False)
        self.video_dir = get_config("video_dir", "reports/videos")
        self.video_size = get_config("video_size", None)

        # 合并 browser_options
        config_options = getattr(config, "browser_options", {}) if config else {}
        override_options = overrides.get("browser_options", {})
        self.browser_options = {**config_options, **override_options}

        # v3.44.0: 保存 runtime 引用，用于获取 event_bus
        self.runtime = runtime

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    def start(self) -> tuple[Browser, BrowserContext, Page]:
        """
        启动浏览器并创建页面

        Returns:
            tuple: (browser, context, page) 三元组

        Raises:
            RuntimeError: 如果浏览器已经启动
        """
        if self._browser is not None:
            raise RuntimeError("浏览器已经启动，请先调用 stop() 关闭")

        # 启动Playwright
        self._playwright = sync_playwright().start()

        # 获取浏览器启动器
        if self.browser_type == BrowserType.CHROMIUM:
            launcher = self._playwright.chromium
        elif self.browser_type == BrowserType.FIREFOX:
            launcher = self._playwright.firefox
        elif self.browser_type == BrowserType.WEBKIT:
            launcher = self._playwright.webkit
        else:
            raise ValueError(f"不支持的浏览器类型: {self.browser_type}")

        # 启动浏览器
        self._browser = launcher.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            **self.browser_options,
        )

        # 创建浏览器上下文（v3.35.7: 支持视频录制）
        context_options: dict[str, Any] = {"viewport": self.viewport}

        if self.record_video:
            from pathlib import Path

            Path(self.video_dir).mkdir(parents=True, exist_ok=True)
            context_options["record_video_dir"] = self.video_dir
            if self.video_size:
                context_options["record_video_size"] = self.video_size

        self._context = self._browser.new_context(**context_options)

        # 设置默认超时
        self._context.set_default_timeout(self.timeout)

        # 创建页面
        self._page = self._context.new_page()

        # v3.44.0: 事件监听器注册移到 page fixture 中
        # 这里不再自动注册，确保与测试隔离的 EventBus 配合

        return self._browser, self._context, self._page

    def stop(self) -> None:
        """
        关闭浏览器并清理资源
        """
        if self._page:
            self._page.close()
            self._page = None

        if self._context:
            self._context.close()
            self._context = None

        if self._browser:
            self._browser.close()
            self._browser = None

        if self._playwright:
            self._playwright.stop()
            self._playwright = None

    def new_page(self) -> Page:
        """
        在当前上下文中创建新页面

        Returns:
            Page: 新创建的页面

        Raises:
            RuntimeError: 如果浏览器未启动
        """
        if not self._context:
            raise RuntimeError("浏览器未启动，请先调用 start()")

        return self._context.new_page()

    def new_context(self, **context_options: Any) -> BrowserContext:
        """
        创建新的浏览器上下文

        Args:
            context_options: 上下文选项

        Returns:
            BrowserContext: 新的浏览器上下文

        Raises:
            RuntimeError: 如果浏览器未启动
        """
        if not self._browser:
            raise RuntimeError("浏览器未启动，请先调用 start()")

        return self._browser.new_context(**context_options)

    @property
    def browser(self) -> Browser:
        """获取浏览器实例"""
        if not self._browser:
            raise RuntimeError("浏览器未启动，请先调用 start()")
        return self._browser

    @property
    def context(self) -> BrowserContext:
        """获取浏览器上下文"""
        if not self._context:
            raise RuntimeError("浏览器上下文不存在，请先调用 start()")
        return self._context

    @property
    def page(self) -> Page:
        """获取当前页面"""
        if not self._page:
            raise RuntimeError("页面不存在，请先调用 start()")
        return self._page

    def __enter__(self):
        """上下文管理器入口"""
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.stop()
        return False

    # ========== v3.44.0: 事件监听器注册和处理 ==========

    def _setup_event_listeners(self, page: Page) -> None:
        """注册 Playwright 原生事件监听器

        利用 Playwright 自带的事件系统，自动发布 UI 事件到 EventBus。
        这种方式无需包装 Playwright API，维护成本为零。

        v3.44.0 修复: 使用 get_event_bus() 动态获取，支持测试隔离。
        v3.46.1 重构: 移除低价值的底层事件（page.load、network.*），
                      只保留对调试有价值的事件。

        注册的事件（仅保留对调试有价值的）：
        - "console": Console 输出（仅 error/warning 级别）
        - "dialog": 弹窗（alert/confirm/prompt）
        - "pageerror": 页面错误（JS 异常）
        - "crash": 页面崩溃

        Args:
            page: Playwright Page 实例
        """
        from df_test_framework.infrastructure.logging import get_logger

        logger = get_logger(__name__)
        logger.debug("注册 Playwright 事件监听器")

        # Console 事件（仅 error/warning 对调试有价值）
        page.on("console", self._on_console)

        # Dialog 事件（需要知道有意外对话框弹出）
        page.on("dialog", self._on_dialog)

        # 错误事件（对调试非常重要）
        page.on("pageerror", self._on_page_error)
        page.on("crash", self._on_crash)

    def _publish_event(self, event: Any) -> None:
        """发布事件（v3.46.1: 使用 runtime.publish_event）

        v3.46.1: 使用 runtime.publish_event()，自动注入 scope
        """
        if self.runtime:
            try:
                self.runtime.publish_event(event)
            except Exception:
                pass  # 静默失败，不影响主流程

    def _on_console(self, msg: Any) -> None:
        """Console 输出事件处理器

        v3.46.1 重构: 只处理 error 和 warning 级别的消息，
        忽略 log/info/debug 等低价值消息，减少噪音。
        """
        # 只关注 error 和 warning 级别，忽略 log/info/debug 等
        if msg.type not in ("error", "warning"):
            return

        if not self.runtime:
            return

        from df_test_framework.core.events import WebBrowserEvent

        try:
            # 发布 Console 事件（不再记录日志，避免重复输出）
            # ConsoleDebugObserver 会处理事件并输出到控制台
            event = WebBrowserEvent.create(
                event_name="console",
                data={
                    "type": msg.type,
                    "text": msg.text,
                    "location": str(msg.location) if msg.location else "",
                },
            )
            self._publish_event(event)
        except Exception as e:
            from df_test_framework.infrastructure.logging import get_logger

            logger = get_logger(__name__)
            logger.warning(f"处理 Console 事件失败: {e}")

    def _on_dialog(self, dialog: Any) -> None:
        """Dialog 事件处理器"""
        if not self.runtime:
            return

        from df_test_framework.core.events import WebBrowserEvent

        try:
            # 发布 Dialog 事件（不再记录日志，避免重复输出）
            # ConsoleDebugObserver 会处理事件并输出到控制台
            event = WebBrowserEvent.create(
                event_name="dialog",
                data={
                    "type": dialog.type,
                    "message": dialog.message,
                    "default_value": dialog.default_value,
                },
            )
            self._publish_event(event)
        except Exception as e:
            from df_test_framework.infrastructure.logging import get_logger

            logger = get_logger(__name__)
            logger.warning(f"处理 Dialog 事件失败: {e}")

    def _on_page_error(self, error: Exception) -> None:
        """页面错误事件处理器"""
        if not self.runtime:
            return

        from df_test_framework.core.events import UIErrorEvent
        from df_test_framework.infrastructure.logging import get_logger

        logger = get_logger(__name__)

        try:
            # v3.46.0: 输出到 pytest 日志系统
            logger.error(f"❌ Page Error: {error}")

            # 发布页面错误事件
            event = UIErrorEvent.create(
                page_name="Page",
                operation="page_error",
                selector="",
                error=error,
            )
            self._publish_event(event)
        except Exception as e:
            logger.warning(f"处理页面错误事件失败: {e}")

    def _on_crash(self, page: Page) -> None:
        """页面崩溃事件处理器"""
        if not self.runtime:
            return

        from df_test_framework.core.events import UIErrorEvent
        from df_test_framework.infrastructure.logging import get_logger

        logger = get_logger(__name__)

        try:
            # v3.46.0: 输出到 pytest 日志系统
            logger.critical(f"💥 Page Crash: {page.url}")

            # 发布崩溃事件
            crash_error = RuntimeError(f"页面崩溃: {page.url}")
            event = UIErrorEvent.create(
                page_name="Page",
                operation="page_crash",
                selector="",
                error=crash_error,
            )
            self._publish_event(event)
        except Exception as e:
            logger.warning(f"处理页面崩溃事件失败: {e}")


__all__ = ["BrowserManager", "BrowserType"]
