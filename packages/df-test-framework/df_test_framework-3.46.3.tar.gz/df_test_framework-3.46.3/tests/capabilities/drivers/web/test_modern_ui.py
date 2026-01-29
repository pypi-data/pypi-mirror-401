"""测试现代UI模式

v3.43.0: 测试 BaseComponent、BasePage、AppActions

测试覆盖:
- BaseComponent 组件封装
- 简化的 BasePage
- AppActions 业务操作
"""

from unittest.mock import MagicMock, patch


class TestBaseComponent:
    """测试 BaseComponent 组件基类"""

    def test_component_with_test_id(self):
        """测试使用 test-id 创建组件"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.component.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import BaseComponent

            # 创建 mock page
            mock_page = MagicMock()
            mock_locator = MagicMock()
            mock_page.get_by_test_id.return_value = mock_locator

            # 创建组件
            component = BaseComponent(mock_page, test_id="login-form")

            assert component.page == mock_page
            assert component.test_id == "login-form"
            assert component.root == mock_locator
            mock_page.get_by_test_id.assert_called_once_with("login-form")

    def test_component_without_test_id(self):
        """测试不使用 test-id 创建组件（整个页面）"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.component.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import BaseComponent

            mock_page = MagicMock()

            component = BaseComponent(mock_page)

            assert component.page == mock_page
            assert component.test_id is None
            assert component.root == mock_page

    def test_component_get_by_role(self):
        """测试组件的 get_by_role 方法"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.component.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import BaseComponent

            mock_page = MagicMock()
            mock_root = MagicMock()
            mock_page.get_by_test_id.return_value = mock_root

            component = BaseComponent(mock_page, test_id="form")

            # 调用 get_by_role
            component.get_by_role("button", name="Submit")

            # 应该在 root 上调用
            mock_root.get_by_role.assert_called_once_with("button", name="Submit")

    def test_component_locator_methods(self):
        """测试组件的各种定位方法"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.component.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import BaseComponent

            mock_page = MagicMock()
            mock_root = MagicMock()
            mock_page.get_by_test_id.return_value = mock_root

            component = BaseComponent(mock_page, test_id="form")

            # 测试各种定位方法
            component.get_by_test_id("submit-btn")
            component.get_by_label("Username")
            component.get_by_placeholder("Enter email")
            component.get_by_text("Welcome")
            component.locator("#username")

            # 验证都在 root 上调用
            mock_root.get_by_test_id.assert_called_once()
            mock_root.get_by_label.assert_called_once()
            mock_root.get_by_placeholder.assert_called_once()
            mock_root.get_by_text.assert_called_once()
            mock_root.locator.assert_called_once()


class TestBasePage:
    """测试简化的 BasePage"""

    def test_base_page_goto(self):
        """测试页面导航"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.page.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import BasePage

            # 创建具体页面类
            class LoginPage(BasePage):
                def wait_for_page_load(self):
                    pass

            mock_page = MagicMock()

            page = LoginPage(mock_page, url="/login", base_url="https://example.com")
            page.goto()

            # 验证调用了 page.goto
            mock_page.goto.assert_called_once_with("https://example.com/login")

    def test_base_page_title_property(self):
        """测试 title 属性"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.page.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import BasePage

            class LoginPage(BasePage):
                def wait_for_page_load(self):
                    pass

            mock_page = MagicMock()
            mock_page.title.return_value = "Login Page"

            page = LoginPage(mock_page)

            assert page.title == "Login Page"
            mock_page.title.assert_called_once()

    def test_base_page_screenshot(self):
        """测试截图方法"""
        with patch(
            "df_test_framework.capabilities.drivers.web.playwright.page.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import BasePage

            class LoginPage(BasePage):
                def wait_for_page_load(self):
                    pass

            mock_page = MagicMock()
            mock_page.screenshot.return_value = b"screenshot_data"

            page = LoginPage(mock_page)
            result = page.screenshot("test.png")

            assert result == b"screenshot_data"
            mock_page.screenshot.assert_called_once_with(path="test.png")


class TestAppActions:
    """测试 AppActions 业务操作基类"""

    def test_app_actions_init(self):
        """测试 AppActions 初始化"""
        with patch(
            "df_test_framework.capabilities.drivers.web.app_actions.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import AppActions

            mock_page = MagicMock()
            actions = AppActions(mock_page, base_url="https://example.com")

            assert actions.page == mock_page
            assert actions.base_url == "https://example.com"

    def test_app_actions_goto(self):
        """测试 AppActions 的 goto 方法"""
        with patch(
            "df_test_framework.capabilities.drivers.web.app_actions.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import AppActions

            mock_page = MagicMock()
            actions = AppActions(mock_page, base_url="https://example.com")

            # 测试带路径
            actions.goto("/login")
            mock_page.goto.assert_called_with("https://example.com/login")

            # 测试不带路径
            actions.goto()
            mock_page.goto.assert_called_with("https://example.com")

    def test_app_actions_custom_implementation(self):
        """测试自定义 AppActions 实现"""
        with patch(
            "df_test_framework.capabilities.drivers.web.app_actions.PLAYWRIGHT_AVAILABLE",
            True,
        ):
            from df_test_framework.capabilities.drivers.web import AppActions

            class MyAppActions(AppActions):
                def login_as_admin(self):
                    self.page.get_by_label("Username").fill("admin")
                    self.page.get_by_label("Password").fill("admin123")
                    self.page.get_by_role("button", name="Sign in").click()

            mock_page = MagicMock()
            actions = MyAppActions(mock_page, base_url="https://example.com")

            actions.login_as_admin()

            # 验证调用了正确的方法
            mock_page.get_by_label.assert_any_call("Username")
            mock_page.get_by_label.assert_any_call("Password")


class TestModernUIExports:
    """测试现代UI模式的导出"""

    def test_base_component_is_exported(self):
        """BaseComponent 可以导入"""
        from df_test_framework.capabilities.drivers.web import BaseComponent

        assert BaseComponent is not None

    def test_app_actions_is_exported(self):
        """AppActions 可以导入"""
        from df_test_framework.capabilities.drivers.web import AppActions

        assert AppActions is not None

    def test_all_exports_available(self):
        """所有导出都可用"""
        import df_test_framework.capabilities.drivers.web as web

        assert "BaseComponent" in web.__all__
        assert "AppActions" in web.__all__
        assert "BasePage" in web.__all__
