"""测试 UI fixtures - 视频录制配置

测试覆盖:
- browser_record_video fixture 默认值
- browser_video_dir fixture 默认值
- 视频录制配置传递到 context

v3.35.7 新增
"""

from unittest.mock import MagicMock, patch


class TestBrowserManagerVideoConfig:
    """测试 BrowserManager 视频录制配置"""

    def test_init_with_video_config(self):
        """初始化时可以配置视频录制"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web.playwright.browser import (
                BrowserManager,
                BrowserType,
            )

            manager = BrowserManager(
                browser_type=BrowserType.CHROMIUM,
                headless=True,
                record_video=True,
                video_dir="custom/videos",
                video_size={"width": 1920, "height": 1080},
            )

            assert manager.record_video is True
            assert manager.video_dir == "custom/videos"
            assert manager.video_size == {"width": 1920, "height": 1080}

    def test_init_default_video_config(self):
        """默认视频配置"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web.playwright.browser import (
                BrowserManager,
            )

            manager = BrowserManager()

            assert manager.record_video is False
            assert manager.video_dir == "reports/videos"
            assert manager.video_size is None

    def test_video_config_types(self):
        """视频配置类型正确"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web.playwright.browser import (
                BrowserManager,
            )

            manager = BrowserManager(
                record_video=True,
                video_dir="reports/videos",
            )

            assert isinstance(manager.record_video, bool)
            assert isinstance(manager.video_dir, str)


class TestUIFixturesExports:
    """测试 UI fixtures 导出"""

    def test_core_fixtures_are_exported(self):
        """核心 fixtures 在 __all__ 中"""
        from df_test_framework.testing.fixtures import ui

        assert "browser_manager" in ui.__all__
        assert "browser" in ui.__all__
        assert "context" in ui.__all__
        assert "page" in ui.__all__


class TestBrowserManagerStart:
    """测试 BrowserManager.start() 视频录制"""

    @patch("df_test_framework.capabilities.drivers.web.playwright.browser.sync_playwright")
    @patch(
        "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
        True,
    )
    def test_start_creates_video_dir_when_recording(self, mock_sync_playwright):
        """启动时录制视频会创建视频目录"""
        from df_test_framework.capabilities.drivers.web.playwright.browser import (
            BrowserManager,
        )

        # 设置 mock
        mock_playwright = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_sync_playwright.return_value.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        manager = BrowserManager(
            record_video=True,
            video_dir="test_videos",
        )

        with patch("pathlib.Path.mkdir") as mock_mkdir:
            try:
                manager.start()
            finally:
                manager.stop()

            # 验证创建了视频目录
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch("df_test_framework.capabilities.drivers.web.playwright.browser.sync_playwright")
    @patch(
        "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
        True,
    )
    def test_start_passes_video_options_to_context(self, mock_sync_playwright):
        """启动时视频选项传递给 context"""
        from df_test_framework.capabilities.drivers.web.playwright.browser import (
            BrowserManager,
        )

        # 设置 mock
        mock_playwright = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_sync_playwright.return_value.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        manager = BrowserManager(
            record_video=True,
            video_dir="test_videos",
            video_size={"width": 1280, "height": 720},
        )

        with patch("pathlib.Path.mkdir"):
            try:
                manager.start()
            finally:
                manager.stop()

            # 验证 new_context 被调用时包含视频选项
            call_kwargs = mock_browser.new_context.call_args[1]
            assert call_kwargs["record_video_dir"] == "test_videos"
            assert call_kwargs["record_video_size"] == {"width": 1280, "height": 720}

    @patch("df_test_framework.capabilities.drivers.web.playwright.browser.sync_playwright")
    @patch(
        "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
        True,
    )
    def test_start_without_video_no_video_options(self, mock_sync_playwright):
        """不录制视频时，context 不包含视频选项"""
        from df_test_framework.capabilities.drivers.web.playwright.browser import (
            BrowserManager,
        )

        # 设置 mock
        mock_playwright = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_sync_playwright.return_value.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        manager = BrowserManager(record_video=False)

        try:
            manager.start()
        finally:
            manager.stop()

        # 验证 new_context 被调用时不包含视频选项
        call_kwargs = mock_browser.new_context.call_args[1]
        assert "record_video_dir" not in call_kwargs
        assert "record_video_size" not in call_kwargs


class TestWebConfig:
    """测试 WebConfig 配置类（v3.42.0）"""

    def test_web_config_default_values(self):
        """测试 WebConfig 默认值"""
        from df_test_framework.infrastructure.config import WebConfig

        config = WebConfig()

        assert config.base_url is None
        assert config.browser_type == "chromium"
        assert config.headless is True
        assert config.slow_mo == 0
        assert config.timeout == 30000
        assert config.viewport == {"width": 1280, "height": 720}
        assert config.record_video is False
        assert config.video_dir == "reports/videos"
        assert config.video_size is None
        assert config.browser_options == {}

    def test_web_config_custom_values(self):
        """测试 WebConfig 自定义值"""
        from df_test_framework.infrastructure.config import WebConfig

        config = WebConfig(
            base_url="https://example.com",
            browser_type="firefox",
            headless=False,
            slow_mo=100,
            timeout=60000,
            viewport={"width": 1920, "height": 1080},
            record_video=True,
            video_dir="custom/videos",
            video_size={"width": 1920, "height": 1080},
            browser_options={"args": ["--start-maximized"]},
        )

        assert config.base_url == "https://example.com"
        assert config.browser_type == "firefox"
        assert config.headless is False
        assert config.slow_mo == 100
        assert config.timeout == 60000
        assert config.viewport == {"width": 1920, "height": 1080}
        assert config.record_video is True
        assert config.video_dir == "custom/videos"
        assert config.video_size == {"width": 1920, "height": 1080}
        assert config.browser_options == {"args": ["--start-maximized"]}

    def test_web_config_validation_timeout(self):
        """测试 WebConfig 超时验证"""
        import pytest
        from pydantic import ValidationError

        from df_test_framework.infrastructure.config import WebConfig

        # 超时不能低于 1000 毫秒
        with pytest.raises(ValidationError, match="greater than or equal to 1000"):
            WebConfig(timeout=500)

    def test_web_config_in_framework_settings(self):
        """测试 WebConfig 在 FrameworkSettings 中"""
        from df_test_framework.infrastructure.config import FrameworkSettings, WebConfig

        settings = FrameworkSettings(
            web=WebConfig(
                browser_type="firefox",
                headless=False,
            )
        )

        assert settings.web is not None
        assert settings.web.browser_type == "firefox"
        assert settings.web.headless is False


class TestBrowserManagerWithConfig:
    """测试 BrowserManager 配置驱动模式（v3.42.0）"""

    def test_browser_manager_with_web_config(self):
        """测试使用 WebConfig 创建 BrowserManager"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web.playwright.browser import (
                BrowserManager,
                BrowserType,
            )
            from df_test_framework.infrastructure.config import WebConfig

            config = WebConfig(
                base_url="https://example.com",
                browser_type="firefox",
                headless=False,
                timeout=60000,
                viewport={"width": 1920, "height": 1080},
                record_video=True,
                video_dir="custom/videos",
            )

            manager = BrowserManager(config=config)

            assert manager.base_url == "https://example.com"
            assert manager.browser_type == BrowserType.FIREFOX
            assert manager.headless is False
            assert manager.timeout == 60000
            assert manager.viewport == {"width": 1920, "height": 1080}
            assert manager.record_video is True
            assert manager.video_dir == "custom/videos"

    def test_browser_manager_config_priority(self):
        """测试参数优先级：直接参数 > config > 默认值"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web.playwright.browser import (
                BrowserManager,
                BrowserType,
            )
            from df_test_framework.infrastructure.config import WebConfig

            config = WebConfig(
                base_url="https://config.example.com",
                browser_type="firefox",
                headless=False,
            )

            # 直接传入的参数应该优先
            manager = BrowserManager(
                base_url="https://direct.example.com",  # 覆盖 config
                browser_type=BrowserType.CHROMIUM,  # 覆盖 config
                config=config,
            )

            assert manager.base_url == "https://direct.example.com"  # 使用直接参数
            assert manager.browser_type == BrowserType.CHROMIUM
            assert manager.headless is False  # 从 config 读取

    def test_browser_manager_default_values(self):
        """测试使用默认配置"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web.playwright.browser import (
                BrowserManager,
                BrowserType,
            )

            manager = BrowserManager()

            assert manager.browser_type == BrowserType.CHROMIUM
            assert manager.headless is True
            assert manager.timeout == 30000
            assert manager.viewport == {"width": 1280, "height": 720}


class TestWebConfigExports:
    """测试 WebConfig 导出"""

    def test_web_config_is_exported(self):
        """WebConfig 可以从主模块导入"""
        from df_test_framework.infrastructure.config import WebConfig

        assert WebConfig is not None

    def test_web_config_in_all(self):
        """WebConfig 在 __all__ 中"""
        from df_test_framework.infrastructure import config

        assert "WebConfig" in config.__all__


class TestBrowserManagerEventListeners:
    """测试 BrowserManager 事件监听器（v3.44.0）

    v3.44.0 架构变更：
    - 事件监听器不再在 BrowserManager.start() 中自动注册
    - 改为在 page fixture 中调用 _setup_event_listeners() 注册
    - 使用 get_global_event_bus() 动态获取 EventBus（支持测试隔离）
    """

    @patch("df_test_framework.capabilities.drivers.web.playwright.browser.sync_playwright")
    @patch(
        "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
        True,
    )
    def test_setup_event_listeners_registers_all_events(self, mock_sync_playwright):
        """_setup_event_listeners() 注册所有事件监听器"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.drivers.web.playwright.browser import (
            BrowserManager,
        )

        # 设置 mock
        mock_playwright = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_sync_playwright.return_value.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        manager = BrowserManager()

        try:
            manager.start()

            # v3.44.0: start() 不再自动注册事件监听器
            assert not mock_page.on.called

            # 手动调用 _setup_event_listeners()（模拟 page fixture 的行为）
            manager._setup_event_listeners(mock_page)

            # 验证 page.on() 被调用（注册事件监听器）
            assert mock_page.on.called
            # 验证注册了多个事件（v3.46.1: 只注册关键事件）
            call_args_list = [call[0][0] for call in mock_page.on.call_args_list]
            assert "console" in call_args_list
            assert "dialog" in call_args_list
            assert "pageerror" in call_args_list
            assert "crash" in call_args_list
        finally:
            manager.stop()

    @patch("df_test_framework.capabilities.drivers.web.playwright.browser.sync_playwright")
    @patch(
        "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
        True,
    )
    def test_browser_manager_start_does_not_register_event_listeners(self, mock_sync_playwright):
        """BrowserManager.start() 不再自动注册事件监听器（v3.44.0 架构变更）"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.drivers.web.playwright.browser import (
            BrowserManager,
        )

        # 设置 mock
        mock_playwright = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_sync_playwright.return_value.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        manager = BrowserManager()

        try:
            manager.start()

            # v3.44.0: start() 不再自动注册事件监听器
            # 事件监听器改为在 page fixture 中注册
            mock_page.on.assert_not_called()
        finally:
            manager.stop()

    @patch("df_test_framework.capabilities.drivers.web.playwright.browser.sync_playwright")
    @patch(
        "df_test_framework.capabilities.drivers.web.playwright.browser.PLAYWRIGHT_AVAILABLE",
        True,
    )
    def test_page_load_event_publishes_to_event_bus(self, mock_sync_playwright):
        """页面加载完成时发布事件到 EventBus"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.drivers.web.playwright.browser import (
            BrowserManager,
        )

        # 设置 mock
        mock_playwright = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_page.url = "https://example.com/login"
        mock_page.title.return_value = "Login Page"

        mock_sync_playwright.return_value.start.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # v3.46.1: 创建带 runtime 的 BrowserManager
        from df_test_framework.bootstrap import ProviderRegistry, RuntimeContext
        from df_test_framework.infrastructure.config import FrameworkSettings
        from df_test_framework.infrastructure.logging import logger

        # 创建 mock EventBus
        mock_event_bus = MagicMock()

        # 创建 RuntimeContext
        runtime = RuntimeContext(
            settings=FrameworkSettings(app_name="test"),
            logger=logger,
            providers=ProviderRegistry(providers={}),
            event_bus=mock_event_bus,
        )

        manager = BrowserManager(runtime=runtime)

        try:
            manager.start()
            # 手动调用 _setup_event_listeners()（模拟 page fixture 的行为）
            manager._setup_event_listeners(mock_page)

            # v3.46.1: 找到 "console" 事件的处理器（不再有 load 事件）
            console_handler = None
            for call in mock_page.on.call_args_list:
                if call[0][0] == "console":
                    console_handler = call[0][1]
                    break

            assert console_handler is not None, "未找到 console 事件处理器"

            # 创建 mock console message（v3.46.1: 使用 error 类型）
            mock_console_msg = MagicMock()
            mock_console_msg.type = "error"  # v3.46.1: 只处理 error/warning
            mock_console_msg.text = "test error message"

            # 触发处理器
            console_handler(mock_console_msg)

            # 验证发布了事件到 EventBus
            assert mock_event_bus.publish_sync.called, "Event should be published"
            # 获取发布的事件
            published_event = mock_event_bus.publish_sync.call_args[0][0]
            # 验证事件类型（WebBrowserEvent 使用 event_name）
            # v3.46.1: 事件名称是 "console"，不是 "page.console"
            assert published_event.event_name == "console"
        finally:
            manager.stop()


class TestBasePageWithRuntime:
    """测试 BasePage 支持 runtime 参数（v3.44.0）"""

    def test_basepage_with_runtime_reads_base_url(self):
        """BasePage 使用 runtime 时自动读取 base_url"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.page.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from unittest.mock import MagicMock

            from df_test_framework.capabilities.drivers.web.playwright.page import (
                BasePage,
            )

            # 创建 mock runtime
            mock_runtime = MagicMock()
            mock_runtime.settings.web.base_url = "https://example.com"

            # 创建 mock page
            mock_page = MagicMock()

            # 创建测试页面类
            class TestPage(BasePage):
                def wait_for_page_load(self):
                    pass

            # 使用 runtime 创建页面对象
            page_obj = TestPage(mock_page, url="/login", runtime=mock_runtime)

            # 验证 base_url 从 runtime 读取
            assert page_obj.base_url == "https://example.com"
            assert page_obj.runtime is mock_runtime

    def test_basepage_explicit_base_url_takes_priority(self):
        """显式传入的 base_url 优先于 runtime 中的配置"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.page.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from unittest.mock import MagicMock

            from df_test_framework.capabilities.drivers.web.playwright.page import (
                BasePage,
            )

            # 创建 mock runtime
            mock_runtime = MagicMock()
            mock_runtime.settings.web.base_url = "https://runtime.example.com"

            # 创建 mock page
            mock_page = MagicMock()

            # 创建测试页面类
            class TestPage(BasePage):
                def wait_for_page_load(self):
                    pass

            # 显式传入 base_url
            page_obj = TestPage(
                mock_page,
                url="/login",
                base_url="https://explicit.example.com",
                runtime=mock_runtime,
            )

            # 验证使用显式传入的 base_url
            assert page_obj.base_url == "https://explicit.example.com"

    def test_basepage_without_runtime_uses_default(self):
        """不提供 runtime 时使用默认值"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.page.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from unittest.mock import MagicMock

            from df_test_framework.capabilities.drivers.web.playwright.page import (
                BasePage,
            )

            # 创建 mock page
            mock_page = MagicMock()

            # 创建测试页面类
            class TestPage(BasePage):
                def wait_for_page_load(self):
                    pass

            # 不提供 runtime
            page_obj = TestPage(mock_page, url="/login")

            # 验证使用默认 base_url
            assert page_obj.base_url == ""
            assert page_obj.runtime is None


class TestAppActionsWithRuntime:
    """测试 AppActions 支持 runtime 参数（v3.44.0）"""

    def test_app_actions_with_runtime_reads_base_url(self):
        """AppActions 使用 runtime 时自动读取 base_url"""
        with patch(
            "df_test_framework.capabilities.drivers.web.app_actions.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from unittest.mock import MagicMock

            from df_test_framework.capabilities.drivers.web import AppActions

            # 创建 mock runtime
            mock_runtime = MagicMock()
            mock_runtime.settings.web.base_url = "https://example.com"

            # 创建 mock page
            mock_page = MagicMock()

            # 使用 runtime 创建 AppActions
            app_actions = AppActions(mock_page, runtime=mock_runtime)

            # 验证 base_url 从 runtime 读取
            assert app_actions.base_url == "https://example.com"
            assert app_actions.runtime is mock_runtime

    def test_app_actions_explicit_base_url_takes_priority(self):
        """显式传入的 base_url 优先于 runtime 中的配置"""
        with patch(
            "df_test_framework.capabilities.drivers.web.app_actions.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from unittest.mock import MagicMock

            from df_test_framework.capabilities.drivers.web import AppActions

            # 创建 mock runtime
            mock_runtime = MagicMock()
            mock_runtime.settings.web.base_url = "https://runtime.example.com"

            # 创建 mock page
            mock_page = MagicMock()

            # 显式传入 base_url
            app_actions = AppActions(
                mock_page,
                base_url="https://explicit.example.com",
                runtime=mock_runtime,
            )

            # 验证使用显式传入的 base_url
            assert app_actions.base_url == "https://explicit.example.com"

    def test_app_actions_without_runtime_uses_default(self):
        """不提供 runtime 时使用默认值"""
        with patch(
            "df_test_framework.capabilities.drivers.web.app_actions.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from unittest.mock import MagicMock

            from df_test_framework.capabilities.drivers.web import AppActions

            # 创建 mock page
            mock_page = MagicMock()

            # 不提供 runtime
            app_actions = AppActions(mock_page)

            # 验证使用默认 base_url
            assert app_actions.base_url == ""
            assert app_actions.runtime is None
