"""
I18nText - 多语言文本包装类

这是一个可选工具类，供开发者在需要组件国际化时使用。
支持：
- 存储多语言文本
- 根据当前语言自动选择合适的文本
- 回退机制
- 序列化和反序列化
"""

from typing import Dict, Optional, Any, Union
from .manager import get_i18n_manager


class I18nText:
    """多语言文本包装类"""

    def __init__(self, translations: Union[str, Dict[str, str]], default_locale: str = 'en'):
        """
        初始化多语言文本

        Args:
            translations: 翻译字典或单一文本
                - 如果是字符串，将作为默认语言的文本
                - 如果是字典，键为语言代码，值为对应文本
            default_locale: 默认语言

        Examples:
            >>> # 方式1：传入字典
            >>> text = I18nText({
            ...     "en": "Hello",
            ...     "zh-CN": "你好",
            ...     "ja": "こんにちは"
            ... })

            >>> # 方式2：传入单一文本（作为默认语言）
            >>> text = I18nText("Hello")
        """
        if isinstance(translations, str):
            # 如果传入的是字符串，作为默认语言的文本
            self._translations = {default_locale: translations}
        else:
            self._translations = translations.copy()

        self._default_locale = default_locale

    def get(self, locale: Optional[str] = None) -> str:
        """
        获取指定语言的文本

        Args:
            locale: 语言代码，如果为 None 则使用当前语言

        Returns:
            对应语言的文本，如果找不到则使用回退机制
        """
        # 如果没有指定语言，使用当前语言
        if locale is None:
            manager = get_i18n_manager()
            locale = manager.get_locale()

        # 尝试获取指定语言的文本
        if locale in self._translations:
            return self._translations[locale]

        # 回退到默认语言
        if self._default_locale in self._translations:
            return self._translations[self._default_locale]

        # 如果默认语言也没有，返回第一个可用的文本
        if self._translations:
            return next(iter(self._translations.values()))

        # 如果完全没有翻译，返回空字符串
        return ""

    def __str__(self) -> str:
        """字符串表示，返回当前语言的文本"""
        return self.get()

    def __repr__(self) -> str:
        """对象表示"""
        return f"I18nText({self._translations})"

    def add_translation(self, locale: str, text: str):
        """添加或更新指定语言的翻译"""
        self._translations[locale] = text

    def has_locale(self, locale: str) -> bool:
        """检查是否有指定语言的翻译"""
        return locale in self._translations

    def get_available_locales(self) -> list[str]:
        """获取所有可用的语言列表"""
        return list(self._translations.keys())

    def to_dict(self) -> Dict[str, str]:
        """转换为字典（用于序列化）"""
        return self._translations.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, str], default_locale: str = 'en') -> 'I18nText':
        """从字典创建实例（用于反序列化）"""
        return cls(data, default_locale)
