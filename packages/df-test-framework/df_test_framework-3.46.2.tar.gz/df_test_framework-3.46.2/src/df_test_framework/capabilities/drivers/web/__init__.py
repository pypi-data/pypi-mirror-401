"""Web浏览器驱动

支持多种Web驱动实现（Playwright、Selenium等）
通过Factory模式提供统一接口

v3.43.0: 新增现代UI测试模式
- BaseComponent: 可复用组件
- AppActions: 应用业务操作
- 重构 BasePage: 移除过度封装，直接使用 Playwright API
"""

# 协议定义
# 业务操作（v3.43.0）
from .app_actions import AppActions

# 工厂类
from .factory import WebDriverFactory

# 默认实现（Playwright）
from .playwright.browser import BrowserManager, BrowserType
from .playwright.component import BaseComponent
from .playwright.locator import ElementLocator, LocatorType, WaitHelper
from .playwright.page import BasePage
from .protocols import PageProtocol, WebDriverProtocol

__all__ = [
    # 协议
    "WebDriverProtocol",
    "PageProtocol",
    # 工厂
    "WebDriverFactory",
    # Playwright 实现
    "BrowserManager",
    "BrowserType",
    "ElementLocator",
    "LocatorType",
    "WaitHelper",
    # 页面对象模式（v3.43.0 重构）
    "BasePage",
    "BaseComponent",
    "AppActions",
]
