"""
SDWK I18n Module - 国际化模块

提供完整的国际化支持，包括：
- I18nManager: 国际化管理器（单例）
- LocaleDetector: 语言检测器
- t() / _(): 翻译函数
- I18nText: 多语言文本包装类（可选工具）
- i18n_component: 组件国际化装饰器（可选工具）

基本使用：
    from sdwk.core.i18n import t, _, get_i18n_manager

    # 使用翻译函数
    message = t("cli.create.success", name="my-project")
    error = _("errors.file_not_found", path="/path/to/file")

    # 设置语言
    manager = get_i18n_manager()
    manager.set_locale("zh-CN")

可选工具（用于组件国际化）：
    from sdwk.core.i18n import I18nText, i18n_component

    @i18n_component
    class MyComponent(Component):
        display_name = I18nText({
            "en": "My Component",
            "zh-CN": "我的组件"
        })
"""

from .manager import I18nManager, get_i18n_manager
from .detector import LocaleDetector, get_locale_detector
from .functions import t, _
from .text import I18nText
from .decorators import i18n_component

__all__ = [
    # Core classes
    'I18nManager',
    'LocaleDetector',

    # Factory functions
    'get_i18n_manager',
    'get_locale_detector',

    # Translation functions
    't',
    '_',

    # Optional tools for component i18n
    'I18nText',
    'i18n_component',
]
