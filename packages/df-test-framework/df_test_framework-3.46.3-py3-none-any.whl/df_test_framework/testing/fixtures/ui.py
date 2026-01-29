"""UI测试fixtures

提供UI自动化测试的pytest fixtures和失败诊断hooks

v3.46.3: 统一失败诊断架构
- 在同一文件中提供 fixtures + hooks（功能内聚）
- context fixture 职责简化：只负责资源管理
- pytest_runtest_makereport hook：统一处理失败诊断
- 通过 pytest11 自动加载，零配置使用

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

# ========== Fixtures ==========


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

    v3.46.3: 职责简化 - 只负责资源管理
    - 启动录屏（如果配置）
    - 不处理失败判断和视频删除（移到 pytest_runtest_makereport hook）

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

    # 配置录屏（如果启用）
    record_mode = browser_manager.record_video
    if record_mode and record_mode != "off":
        from pathlib import Path

        Path(browser_manager.video_dir).mkdir(parents=True, exist_ok=True)
        context_options["record_video_dir"] = browser_manager.video_dir
        if browser_manager.video_size:
            context_options["record_video_size"] = browser_manager.video_size

    ctx = browser.new_context(**context_options)

    # 设置默认超时
    ctx.set_default_timeout(browser_manager.timeout)

    yield ctx

    # 只关闭资源，不处理视频文件（由 pytest_runtest_makereport hook 处理）
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
    # Hooks (pytest 会自动发现)
    "pytest_runtest_makereport",
]


# ========== 失败诊断 Hooks ==========


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行后的钩子 - 统一处理失败诊断

    v3.46.3: 所有失败诊断逻辑统一在此处理
    - 失败时：截图 + 保留视频 + Allure 附件
    - 成功时：根据配置决定是否删除视频

    功能:
    1. 失败自动截图（可配置）
    2. 视频文件处理（根据 record_video 模式）
    3. Allure 附件自动添加（可配置）
    4. 诊断信息输出

    配置:
        # config/base.yaml
        web:
          screenshot_on_failure: true      # 默认 true
          screenshot_dir: reports/screenshots
          record_video: retain-on-failure  # off/on/retain-on-failure/on-first-retry
          attach_to_allure: true           # 默认 true
    """
    outcome = yield
    report = outcome.get_result()

    # 只处理测试执行阶段（call）
    if report.when == "call":
        # 检查是否是 UI 测试（有 page 或 context fixture）
        if "page" in item.funcargs or "context" in item.funcargs:
            _handle_ui_test_result(item, report)


def _handle_ui_test_result(item, report):
    """处理 UI 测试结果（失败或成功）

    Args:
        item: pytest 测试项
        report: pytest 测试报告
    """
    # 获取配置
    config = _get_failure_config(item.config)

    # 获取 page 和 context
    page = item.funcargs.get("page")
    context = item.funcargs.get("context")

    if report.failed:
        # ========== 失败处理 ==========
        if page and config["screenshot_on_failure"]:
            _take_failure_screenshot(page, item, config)

        if page or context:
            _handle_video_on_failure(page, context, config)
    else:
        # ========== 成功处理 ==========
        # 根据录制模式决定是否删除视频
        if config["record_video"] == "retain-on-failure":
            video_path = _get_video_path(page, context)
            if video_path:
                _delete_video_file(video_path)
        elif config["record_video"] == "on-first-retry":
            # 非重试时删除视频
            if not _is_first_retry(item):
                video_path = _get_video_path(page, context)
                if video_path:
                    _delete_video_file(video_path)


def _get_failure_config(pytest_config):
    """获取失败诊断配置

    优先级: WebConfig > 默认值

    Args:
        pytest_config: pytest Config 对象

    Returns:
        dict: 失败诊断配置
    """
    settings = getattr(pytest_config, "_df_settings", None)

    if settings and hasattr(settings, "web") and settings.web:
        web_config = settings.web
        return {
            "screenshot_on_failure": getattr(web_config, "screenshot_on_failure", True),
            "screenshot_dir": getattr(web_config, "screenshot_dir", "reports/screenshots"),
            "record_video": getattr(web_config, "record_video", False),
            "attach_to_allure": getattr(web_config, "attach_to_allure", True),
        }

    # 默认配置
    return {
        "screenshot_on_failure": True,
        "screenshot_dir": "reports/screenshots",
        "record_video": False,
        "attach_to_allure": True,
    }


def _take_failure_screenshot(page, item, config):
    """失败时自动截图

    Args:
        page: Playwright Page 对象
        item: pytest 测试项
        config: 失败诊断配置
    """
    from pathlib import Path

    screenshots_dir = Path(config["screenshot_dir"])
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshots_dir / f"{item.name}_failure.png"

    try:
        page.screenshot(path=str(screenshot_path))
        print(f"\n📸 失败截图: {screenshot_path}")

        # 附加到 Allure
        if config["attach_to_allure"]:
            _attach_to_allure(screenshot_path, "失败截图", "png")
    except Exception as e:
        print(f"\n⚠️  截图失败: {e}")


def _handle_video_on_failure(page, context, config):
    """失败时处理视频（输出路径 + Allure 附件）

    Args:
        page: Playwright Page 对象
        context: Playwright BrowserContext 对象
        config: 失败诊断配置
    """
    video_path = _get_video_path(page, context)
    if video_path:
        print(f"\n🎬 测试视频: {video_path}")

        if config["attach_to_allure"]:
            _attach_to_allure(video_path, "测试视频", "webm")


def _get_video_path(page, context):
    """获取视频路径

    Args:
        page: Playwright Page 对象
        context: Playwright BrowserContext 对象

    Returns:
        str | None: 视频文件路径
    """
    try:
        if page and page.video:
            return page.video.path()
        elif context and context.pages:
            first_page = context.pages[0]
            if first_page.video:
                return first_page.video.path()
    except Exception:
        pass
    return None


def _delete_video_file(video_path: str) -> None:
    """删除视频文件

    Args:
        video_path: 视频文件路径
    """
    try:
        from pathlib import Path

        Path(video_path).unlink(missing_ok=True)
    except Exception:
        pass  # 静默失败，不影响测试


def _is_first_retry(item) -> bool:
    """检查是否是首次重试

    需要 pytest-rerunfailures 插件支持

    Args:
        item: pytest 测试项

    Returns:
        bool: 是否是首次重试
    """
    try:
        # pytest-rerunfailures 会在 node 上添加 execution_count 属性
        execution_count = getattr(item, "execution_count", 0)
        return execution_count == 1  # 0 是首次执行，1 是首次重试
    except Exception:
        return False


def _attach_to_allure(file_path, name, attachment_type):
    """附加到 Allure 报告

    Args:
        file_path: 文件路径
        name: 附件名称
        attachment_type: 附件类型（png/webm）
    """
    try:
        import allure

        # 映射类型
        type_map = {
            "png": allure.attachment_type.PNG,
            "webm": allure.attachment_type.WEBM,
        }

        allure.attach.file(
            str(file_path),
            name=name,
            attachment_type=type_map.get(attachment_type, allure.attachment_type.TEXT),
        )
    except ImportError:
        pass  # 未安装 allure-pytest，跳过
