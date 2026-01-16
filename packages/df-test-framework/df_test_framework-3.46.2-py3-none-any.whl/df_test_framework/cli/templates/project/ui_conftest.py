"""UI项目pytest配置模板

v3.37.0: 更新为 pytest11 Entry Points 自动加载
v3.35.7: 新增视频录制和 EventBus 集成
v3.45.0: 支持 @actions_class 装饰器 + load_actions_fixtures 自动发现
"""

UI_CONFTEST_TEMPLATE = '''"""Pytest全局配置 - UI测试 (v3.42.0)

UI测试专用的pytest配置和fixtures。

v3.42.0 重要变更:
- 支持 @actions_class 装饰器自动注册 Actions 为 fixture
- 使用 load_actions_fixtures() 自动发现并加载所有 Actions
- 与 HTTP 的 @api_class + load_api_fixtures 保持一致
- 配置驱动模式：所有浏览器配置通过 WebConfig 统一管理
- 移除冗余的配置型 fixtures（browser_type/headless/timeout 等）

v3.37.0 重要变更:
- pytest11 Entry Points: pip install df-test-framework 后插件自动加载
- 无需手动声明 pytest_plugins（框架自动注册）

配置方式（推荐 YAML 配置）:
    # config/base.yaml
    web:
      browser_type: chromium
      headless: true
      timeout: 30000
      base_url: https://example.com
      viewport:
        width: 1920
        height: 1080
    test:
      actions_package: {project_name}.actions

或环境变量:
    WEB__BROWSER_TYPE=chromium
    WEB__HEADLESS=true
    TEST__ACTIONS_PACKAGE={project_name}.actions
"""

import pytest
from pathlib import Path

from df_test_framework.infrastructure.logging import get_logger
from df_test_framework.testing.decorators import load_actions_fixtures

logger = get_logger(__name__)


# ============================================================
# v3.37.0: 插件通过 pytest11 Entry Points 自动加载
# ============================================================
# pip install df-test-framework 后，核心插件自动可用，无需手动声明。
#
# UI 测试专用 fixtures（browser_manager/browser/context/page 等）：
pytest_plugins = ["df_test_framework.testing.fixtures.ui"]


# ============================================================
# v3.42.0: @actions_class 装饰器自动注册 Actions fixtures
# ============================================================
# 支持配置驱动的 Actions 自动发现
# 优先使用配置文件中的 test.actions_package，否则使用默认值
#
# 配置方式(config/base.yaml):
#   test:
#     actions_package: {project_name}.actions
#
# 或环境变量: TEST__ACTIONS_PACKAGE={project_name}.actions


def _get_actions_package() -> str:
    """获取 Actions 包路径（优先配置，否则默认值）"""
    default_package = "{project_name}.actions"
    try:
        from df_test_framework.infrastructure.config import get_config
        config = get_config()
        return config.get("test", {{}}).get("actions_package") or default_package
    except Exception:
        return default_package


load_actions_fixtures(globals(), actions_package=_get_actions_package())


# ============================================================
# 浏览器配置说明（v3.42.0 配置驱动模式）
# ============================================================
# 所有浏览器配置通过 WebConfig 统一管理，无需定义配置型 fixtures。
# 框架的 browser_manager fixture 会自动从 RuntimeContext 读取配置。
#
# 命令行选项（由 pytest-playwright 提供）：
#   --headed: 显示浏览器窗口
#   --browser: 指定浏览器类型
#   注意：pytest-playwright 已提供这些选项，无需在 conftest.py 中重复定义


# ========== 测试钩子 ==========

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图和保存视频"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]

            # 失败截图
            screenshots_dir = Path("reports/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshots_dir / f"{item.name}_failure.png"

            try:
                page.screenshot(path=str(screenshot_path))
                print(f"\\n📸 失败截图: {screenshot_path}")

                # 尝试附加到 Allure
                try:
                    import allure
                    allure.attach.file(
                        str(screenshot_path),
                        name="失败截图",
                        attachment_type=allure.attachment_type.PNG
                    )
                except ImportError:
                    pass

            except Exception as e:
                print(f"\\n⚠️  截图失败: {e}")

            # 获取视频路径（如果录制了视频）
            try:
                video = page.video
                if video:
                    video_path = video.path()
                    print(f"\\n🎬 测试视频: {video_path}")

                    # 尝试附加到 Allure
                    try:
                        import allure
                        allure.attach.file(
                            str(video_path),
                            name="测试视频",
                            attachment_type=allure.attachment_type.WEBM
                        )
                    except ImportError:
                        pass
            except Exception:
                pass


# 注意: 标记已在 pyproject.toml 的 [tool.pytest] markers 中定义，无需在此重复注册。
# 框架已自动注册 keep_data 和 debug 标记。
# def pytest_configure(config):
#     """Pytest配置钩子"""
#     config.addinivalue_line("markers", "ui: mark test as ui test")
#     config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_sessionstart(session: pytest.Session) -> None:
    """Session 开始时执行 - 配置 Allure 环境信息"""
    try:
        from df_test_framework.testing.reporting.allure import AllureHelper

        # 通过 env_plugin 获取配置
        if hasattr(session.config, "_df_settings"):
            settings = session.config._df_settings
            current_env = getattr(session.config, "_df_current_env", settings.env)

            AllureHelper.add_environment_info({
                "环境": current_env,
                "应用地址": settings.web.base_url if settings.web else "N/A",
                "浏览器": settings.web.browser_type if settings.web else "chromium",
                "Python版本": "3.12+",
                "框架版本": "df-test-framework v3.45.0",
                "项目版本": "{project_name} v1.0.0",
                "测试类型": "UI自动化测试",
            })
    except Exception as e:
        logger.warning(f"无法加载 Allure 环境信息: {e}")
'''

__all__ = ["UI_CONFTEST_TEMPLATE"]
