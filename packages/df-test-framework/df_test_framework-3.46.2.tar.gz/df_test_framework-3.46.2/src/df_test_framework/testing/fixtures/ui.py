"""UI测试fixtures

提供UI自动化测试的pytest fixtures

v3.42.0: 配置驱动模式
- browser_manager fixture 从 RuntimeContext 获取配置
- 通过 WebConfig 统一管理浏览器配置

v3.44.0: EventBus 集成到 RuntimeContext
- 使用 test_runtime fixture（包含测试专用 EventBus）
- context fixture 正确应用 WebConfig 配置（viewport/timeout/视频录制）
- page fixture 自动注册事件监听器
- 事件通过 runtime.event_bus 发布
"""

from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from df_test_framework.bootstrap.runtime import RuntimeContext

try:
    from playwright.sync_api import Browser, BrowserContext, Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = None
    BrowserContext = None
    Page = None

from df_test_framework.capabilities.drivers.web import BrowserManager


@pytest.fixture(scope="function")
def browser_manager(test_runtime: RuntimeContext) -> Generator[BrowserManager, None, None]:
    """
    浏览器管理器（函数级）

    v3.44.0: 改为 function 级别，使用 test_runtime（包含测试专用 EventBus）

    配置示例:
        # .env 文件
        WEB__BROWSER_TYPE=chromium
        WEB__HEADLESS=true
        WEB__TIMEOUT=30000
        WEB__VIEWPORT__width=1920
        WEB__VIEWPORT__height=1080

    Yields:
        BrowserManager: 浏览器管理器实例
    """
    if not PLAYWRIGHT_AVAILABLE:
        pytest.skip("Playwright未安装，跳过UI测试")

    # 从 test_runtime 获取配置，创建 BrowserManager
    web_config = test_runtime.settings.web
    manager = BrowserManager(config=web_config, runtime=test_runtime)
    manager.start()

    yield manager

    manager.stop()


@pytest.fixture(scope="function")
def browser(browser_manager: BrowserManager) -> Browser:
    """
    浏览器实例（函数级）

    Args:
        browser_manager: 浏览器管理器

    Returns:
        Browser: Playwright浏览器实例
    """
    return browser_manager.browser


@pytest.fixture(scope="function")
def context(
    browser: Browser, browser_manager: BrowserManager
) -> Generator[BrowserContext, None, None]:
    """
    浏览器上下文（函数级）

    每个测试函数创建独立的浏览器上下文，测试间相互隔离

    v3.44.0: 正确应用 WebConfig 配置
    - viewport: 视口大小
    - timeout: 默认超时时间
    - record_video: 视频录制配置

    Args:
        browser: 浏览器实例
        browser_manager: 浏览器管理器（用于读取配置）

    Yields:
        BrowserContext: Playwright浏览器上下文
    """
    # 从 browser_manager 读取 WebConfig 配置
    context_options: dict[str, Any] = {
        "viewport": browser_manager.viewport,
    }

    # 视频录制配置
    if browser_manager.record_video:
        from pathlib import Path

        Path(browser_manager.video_dir).mkdir(parents=True, exist_ok=True)
        context_options["record_video_dir"] = browser_manager.video_dir
        if browser_manager.video_size:
            context_options["record_video_size"] = browser_manager.video_size

    ctx = browser.new_context(**context_options)

    # 设置默认超时
    ctx.set_default_timeout(browser_manager.timeout)

    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, browser_manager: BrowserManager) -> Generator[Page, None, None]:
    """
    页面实例（函数级）

    每个测试函数获取独立的页面实例

    v3.44.0: 自动注册事件监听器
    - 事件通过 runtime.event_bus 发布
    - 支持测试隔离（每个测试有独立的 EventBus）

    Args:
        context: 浏览器上下文
        browser_manager: 浏览器管理器（用于注册事件监听器）

    Yields:
        Page: Playwright页面实例

    示例:
        >>> def test_example(page):
        ...     page.goto("https://example.com")
        ...     assert page.title() == "Example Domain"
    """
    p = context.new_page()

    # v3.44.0: 自动注册事件监听器
    # 使用 BrowserManager 的方法，确保事件处理逻辑统一
    browser_manager._setup_event_listeners(p)

    yield p
    p.close()


@pytest.fixture(scope="function")
def ui_manager(browser_manager: BrowserManager):
    """
    UI管理器（函数级）

    提供完整的浏览器管理器，包含browser、context、page

    Args:
        browser_manager: 浏览器管理器

    Returns:
        BrowserManager: 浏览器管理器实例

    示例:
        >>> def test_with_manager(ui_manager):
        ...     page = ui_manager.page
        ...     page.goto("https://example.com")
        ...     assert page.title() == "Example Domain"
    """
    return browser_manager


# ========== 便捷 fixtures ==========


@pytest.fixture
def goto(page: Page):
    """
    页面导航助手

    提供简化的页面导航方法

    Args:
        page: 页面实例

    Returns:
        callable: 导航函数

    示例:
        >>> def test_navigation(goto):
        ...     goto("/login")  # 导航到登录页
    """

    def _goto(url: str, **kwargs):
        """导航到指定URL"""
        page.goto(url, **kwargs)
        return page

    return _goto


@pytest.fixture
def screenshot(page: Page):
    """
    截图助手

    提供便捷的截图功能

    Args:
        page: 页面实例

    Returns:
        callable: 截图函数

    示例:
        >>> def test_with_screenshot(page, screenshot):
        ...     page.goto("https://example.com")
        ...     screenshot("example.png")
    """

    def _screenshot(path: str = None, **kwargs):
        """
        页面截图

        Args:
            path: 保存路径
            kwargs: 其他参数
        """
        return page.screenshot(path=path, **kwargs)

    return _screenshot


# ========== App Actions Fixture ==========


@pytest.fixture
def app_actions(page: Page, browser_manager: BrowserManager):
    """
    应用业务操作 fixture（v3.44.0）

    提供 AppActions 基类实例，用于简单场景。
    复杂项目应在 conftest.py 中定义项目专用的 AppActions fixture。

    Args:
        page: 页面实例（已注册事件监听器）
        browser_manager: 浏览器管理器（用于获取配置）

    Returns:
        AppActions: 基础业务操作实例

    示例:
        >>> def test_navigation(app_actions):
        ...     app_actions.goto("/login")
        ...     # 直接使用 page 进行操作
        ...     app_actions.page.get_by_label("Username").fill("admin")

    Note:
        推荐在项目 conftest.py 中定义专用的 AppActions:

        >>> @pytest.fixture
        >>> def app_actions(page, test_runtime):
        ...     from myproject.app_actions import MyAppActions
        ...     return MyAppActions(page, runtime=test_runtime)
    """
    from df_test_framework.capabilities.drivers.web import AppActions

    return AppActions(
        page=page,
        base_url=browser_manager.base_url or "",
        runtime=browser_manager.runtime,
    )


__all__ = [
    # 核心 fixtures
    "browser_manager",
    "browser",
    "context",
    "page",
    "ui_manager",
    # 业务操作 fixture
    "app_actions",
    # 便捷 fixtures
    "goto",
    "screenshot",
]
