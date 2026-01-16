"""Full项目pytest配置模板

v3.45.0: 合并 API 和 UI 配置，支持完整项目
"""

FULL_CONFTEST_TEMPLATE = """\"\"\"Pytest 全局配置和 Fixtures - Full 项目 (v3.45.0)

基于 df-test-framework v3.45.0 提供测试运行时环境和公共 fixtures。

v3.45.0 重要变更:
- 合并 API 和 UI 配置，支持完整项目（API + UI）
- 同时支持 @api_class 和 @actions_class 装饰器
- 使用 load_api_fixtures() 和 load_actions_fixtures() 自动发现

v3.38.7 重要变更:
- structlog 25.5.0 最佳实践升级
- pytest 日志集成修复: 无重复输出，统一格式

v3.38.0 重要变更:
- pytest11 Entry Points: pip install df-test-framework 后插件自动加载
- 无需手动声明 pytest_plugins(框架自动注册)
- pytest 9.0 原生 TOML 配置(使用 [tool.pytest])

配置系统:
- YAML 分层配置(推荐): config/base.yaml + config/environments/{env}.yaml
- 支持 _extends 继承机制(如 local.yaml extends test.yaml)
- --env 参数切换环境(如 --env=local)
- 现代化配置 API: get_settings(), get_config(), get_settings_for_class()

框架自动提供的核心 fixtures(通过 Entry Points 自动加载):
- settings: 框架配置(通过 env_plugin 自动加载)
- current_env: 当前环境名称
- runtime: 运行时上下文(Session级别)
- http_client: HTTP客户端(Session级别，支持中间件系统)
- database: 数据库连接(Session级别)
- redis_client: Redis客户端(Session级别)
- uow: Unit of Work(事务管理 + Repository)
- cleanup: 配置驱动的数据清理
- prepare_data / data_preparer: 数据准备工具
- http_mock: HTTP请求Mock(隔离测试)
- time_mock: 时间Mock(时间敏感测试)
- local_file_client / s3_client / oss_client: 存储客户端
- metrics_manager / metrics_observer: Prometheus 指标收集
- console_debugger / debug_mode: 彩色控制台调试输出
- allure_observer: Allure 事件自动记录
- browser_manager / browser / context / page: UI 测试 fixtures
- app_actions: 基础业务操作 fixture
\"\"\"

import pytest
from pathlib import Path

from df_test_framework.infrastructure.logging import get_logger
from df_test_framework.testing.decorators import load_api_fixtures, load_actions_fixtures

logger = get_logger(__name__)

# ============================================================
# v3.37.0: 插件通过 pytest11 Entry Points 自动加载
# ============================================================
# pip install df-test-framework 后，以下插件自动可用，无需手动声明：
#   - df_test_framework.testing.fixtures.core - 核心 fixtures
#   - df_test_framework.testing.plugins.env_plugin - 环境管理
#   - df_test_framework.testing.plugins.logging_plugin - 日志配置(structlog)
#   - df_test_framework.testing.fixtures.allure - Allure 自动记录
#
# Full 项目需要手动添加 UI 测试 fixtures：
pytest_plugins = ["df_test_framework.testing.fixtures.ui"]


# ============================================================
# v3.45.0: 自动加载 API 和 UI Actions fixtures
# ============================================================
# 支持配置驱动的自动发现
#
# 配置方式(config/base.yaml):
#   test:
#     apis_package: {project_name}.apis
#     actions_package: {project_name}.actions
#
# 或环境变量:
#   TEST__APIS_PACKAGE={project_name}.apis
#   TEST__ACTIONS_PACKAGE={project_name}.actions


def _get_apis_package() -> str:
    \"\"\"获取 API 包路径(优先配置, 否则默认值)\"\"\"
    default_package = "{project_name}.apis"
    try:
        from df_test_framework.infrastructure.config import get_config
        config = get_config()
        return config.get("test", {{}}).get("apis_package") or default_package
    except Exception:
        return default_package


def _get_actions_package() -> str:
    \"\"\"获取 Actions 包路径（优先配置，否则默认值）\"\"\"
    default_package = "{project_name}.actions"
    try:
        from df_test_framework.infrastructure.config import get_config
        config = get_config()
        return config.get("test", {{}}).get("actions_package") or default_package
    except Exception:
        return default_package


# 自动加载所有 @api_class 和 @actions_class 装饰的类
load_api_fixtures(globals(), apis_package=_get_apis_package())
load_actions_fixtures(globals(), actions_package=_get_actions_package())


# ============================================================
# 浏览器配置说明（v3.42.0 配置驱动模式）
# ============================================================
# 所有浏览器配置通过 WebConfig 统一管理，无需定义配置型 fixtures。
# 框架的 browser_manager fixture 会自动从 RuntimeContext 读取配置。
#
# 配置方式（推荐 YAML 配置）:
#     # config/base.yaml
#     web:
#       browser_type: chromium
#       headless: true
#       timeout: 30000
#       base_url: https://example.com
#       viewport:
#         width: 1920
#         height: 1080
#
# 命令行选项（由 pytest-playwright 提供）：
#   --headed: 显示浏览器窗口
#   --browser: 指定浏览器类型
#   注意：pytest-playwright 已提供这些选项，无需在 conftest.py 中重复定义


# ========== 测试钩子 ==========

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    \"\"\"测试失败时自动截图和保存视频\"\"\"
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
#     \"\"\"Pytest配置钩子\"\"\"
#     config.addinivalue_line("markers", "ui: mark test as ui test")
#     config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_sessionstart(session: pytest.Session) -> None:
    \"\"\"Session 开始时执行 - 配置 Allure 环境信息\"\"\"
    try:
        from df_test_framework.testing.reporting.allure import AllureHelper

        # 通过 env_plugin 获取配置(存储在 session.config 中)
        if hasattr(session.config, "_df_settings"):
            settings = session.config._df_settings
            current_env = getattr(session.config, "_df_current_env", settings.env)

            # 根据配置判断是否有 UI 测试
            has_ui = settings.web is not None
            has_api = settings.http is not None

            env_info = {
                "环境": current_env,
                "Python版本": "3.12+",
                "框架版本": "df-test-framework v3.45.0",
                "项目版本": "{project_name} v1.0.0",
            }

            if has_api:
                env_info["API地址"] = settings.http.base_url

            if has_ui:
                env_info["应用地址"] = settings.web.base_url
                env_info["浏览器"] = settings.web.browser_type

            if has_api and has_ui:
                env_info["测试类型"] = "API + UI 自动化测试"
            elif has_api:
                env_info["测试类型"] = "API 自动化测试"
            elif has_ui:
                env_info["测试类型"] = "UI 自动化测试"

            AllureHelper.add_environment_info(env_info)
    except Exception as e:
        logger.warning(f"无法加载 Allure 环境信息: {e}")


# ============================================================
# API 测试数据清理示例
# ============================================================
# v3.18.0+: 推荐使用配置驱动的清理(CLEANUP__MAPPINGS__*)
# 框架自动提供 cleanup fixture，只需在 .env 中配置映射即可
#
# .env 示例:
#   CLEANUP__ENABLED=true
#   CLEANUP__MAPPINGS__orders__table=order_table
#   CLEANUP__MAPPINGS__orders__field=order_no
#
# 使用方式:
#   def test_create_order(http_client, cleanup):
#       order_no = DataGenerator.test_id("TEST_ORD")
#       response = http_client.post("/orders", json={{"order_no": order_no}})
#       cleanup.add("orders", order_no)  # 自动清理

"""

__all__ = ["FULL_CONFTEST_TEMPLATE"]
