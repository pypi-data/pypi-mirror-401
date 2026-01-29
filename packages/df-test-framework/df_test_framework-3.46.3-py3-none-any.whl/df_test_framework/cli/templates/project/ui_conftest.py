"""UI项目pytest配置模板

v3.46.3: 失败诊断由框架统一实现，无需手动添加 hook
v3.45.0: 支持 @actions_class 装饰器 + load_actions_fixtures 自动发现
v3.37.0: 更新为 pytest11 Entry Points 自动加载
"""

UI_CONFTEST_TEMPLATE = '''"""Pytest全局配置 - UI测试 (v3.46.3)

UI测试专用的pytest配置和fixtures。

v3.46.3 重要变更: ⭐
- 失败截图和视频处理由框架统一实现（通过 pytest11 自动加载）
- 无需在 conftest.py 中手动添加 pytest_runtest_makereport hook
- 通过 YAML 配置控制失败诊断行为

v3.42.0 重要变更:
- 支持 @actions_class 装饰器自动注册 Actions 为 fixture
- 使用 load_actions_fixtures() 自动发现并加载所有 Actions
- 与 HTTP 的 @api_class + load_api_fixtures 保持一致
- 配置驱动模式：所有浏览器配置通过 WebConfig 统一管理

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

      # 视频录制
      record_video: retain-on-failure  # off/on/retain-on-failure/on-first-retry
      video_dir: reports/videos

      # 失败诊断（v3.46.3）⭐
      screenshot_on_failure: true      # 默认 true
      screenshot_dir: reports/screenshots
      attach_to_allure: true          # 默认 true

    test:
      actions_package: {project_name}.actions

或环境变量:
    WEB__BROWSER_TYPE=chromium
    WEB__HEADLESS=true
    WEB__RECORD_VIDEO=retain-on-failure
    WEB__SCREENSHOT_ON_FAILURE=true
    TEST__ACTIONS_PACKAGE={project_name}.actions
"""

import pytest

from df_test_framework.infrastructure.logging import get_logger
from df_test_framework.testing.decorators import load_actions_fixtures

logger = get_logger(__name__)


# ============================================================
# v3.46.3: UI 插件通过 pytest11 自动加载 ⭐
# ============================================================
# pip install df-test-framework 后，以下功能自动可用：
#   - df_test_framework.testing.fixtures.ui (浏览器 fixtures)
#   - pytest_runtest_makereport hook (失败诊断)
#
# 无需手动声明 pytest_plugins
# 无需手动添加 pytest_runtest_makereport hook
#
# 失败诊断功能（自动生效）：
#   - 失败时自动截图
#   - 根据配置保留/删除视频
#   - 自动附加到 Allure 报告
#   - 输出诊断信息


# ============================================================
# Actions 自动发现
# ============================================================
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


# ============================================================
# v3.46.3: 失败诊断说明 ⭐
# ============================================================
# 框架已自动实现失败诊断功能，无需手动添加 pytest_runtest_makereport hook。
#
# 功能包括：
#   1. 失败时自动截图（可配置）
#   2. 视频文件处理（根据 record_video 模式）
#   3. Allure 附件自动添加（可配置）
#   4. 诊断信息输出
#
# 配置方式：
#   # config/base.yaml
#   web:
#     screenshot_on_failure: true      # 默认 true
#     screenshot_dir: reports/screenshots
#     record_video: retain-on-failure  # 仅保留失败的视频
#     attach_to_allure: true          # 默认 true
#
# 禁用失败截图（如果需要）：
#   web:
#     screenshot_on_failure: false


# ============================================================
# Session 钩子（保留）
# ============================================================
def pytest_sessionstart(session: pytest.Session) -> None:
    """Session 开始时执行 - 配置 Allure 环境信息"""
    try:
        from df_test_framework.testing.reporting.allure import AllureHelper

        # 通过 env_plugin 获取配置
        if hasattr(session.config, "_df_settings"):
            settings = session.config._df_settings
            current_env = getattr(session.config, "_df_current_env", settings.env)

            AllureHelper.add_environment_info({{
                "环境": current_env,
                "应用地址": settings.web.base_url if settings.web else "N/A",
                "浏览器": settings.web.browser_type if settings.web else "chromium",
                "Python版本": "3.12+",
                "框架版本": "df-test-framework v3.46.3",
                "项目版本": "{project_name} v1.0.0",
                "测试类型": "UI自动化测试",
            }})
    except Exception as e:
        logger.warning(f"无法加载 Allure 环境信息: {{e}}")
'''

__all__ = ["UI_CONFTEST_TEMPLATE"]
