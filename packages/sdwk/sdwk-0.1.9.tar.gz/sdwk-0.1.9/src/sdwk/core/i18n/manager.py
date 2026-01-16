"""
I18n Manager - 国际化管理器

提供单例模式的国际化管理功能，负责：
- 翻译文件的加载和缓存
- 语言切换
- 翻译查询和变量插值
- 回退机制
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from threading import Lock


class I18nManager:
    """国际化管理器（单例模式）"""

    _instance: Optional['I18nManager'] = None
    _lock: Lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 避免重复初始化
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self._current_locale: str = 'en'
        self._default_locale: str = 'en'
        self._translations: Dict[str, Dict[str, Any]] = {}
        self._locale_dir: Optional[Path] = None
        self._fallback_chain: List[str] = ['en']

        # 自动检测并设置 locale 目录
        self._auto_detect_locale_dir()

    def _auto_detect_locale_dir(self):
        """自动检测 locales 目录位置"""
        # 尝试从当前文件位置推断
        current_file = Path(__file__)
        # 从 src/sdwk/core/i18n/manager.py 到 src/sdwk/locales
        possible_dir = current_file.parent.parent.parent / 'locales'

        if possible_dir.exists():
            self._locale_dir = possible_dir
        else:
            # 如果不存在，设置为 None，后续可以手动设置
            self._locale_dir = None

    def set_locale_dir(self, locale_dir: str | Path):
        """设置翻译文件目录"""
        self._locale_dir = Path(locale_dir)
        if not self._locale_dir.exists():
            raise FileNotFoundError(f"Locale directory not found: {locale_dir}")

    def set_locale(self, locale: str):
        """设置当前语言"""
        self._current_locale = locale
        # 如果该语言的翻译还未加载，尝试加载
        if locale not in self._translations:
            self._load_locale(locale)

    def get_locale(self) -> str:
        """获取当前语言"""
        return self._current_locale

    def set_default_locale(self, locale: str):
        """设置默认语言（回退语言）"""
        self._default_locale = locale
        if locale not in self._translations:
            self._load_locale(locale)

    def set_fallback_chain(self, locales: List[str]):
        """设置回退链"""
        self._fallback_chain = locales
        # 预加载所有回退语言
        for locale in locales:
            if locale not in self._translations:
                self._load_locale(locale)

    def _load_locale(self, locale: str):
        """加载指定语言的翻译文件"""
        if self._locale_dir is None:
            # 如果没有设置 locale 目录，使用空字典
            self._translations[locale] = {}
            return

        locale_file = self._locale_dir / f"{locale}.json"
        if not locale_file.exists():
            # 如果文件不存在，使用空字典
            self._translations[locale] = {}
            return

        try:
            with open(locale_file, 'r', encoding='utf-8') as f:
                self._translations[locale] = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # 加载失败时使用空字典
            self._translations[locale] = {}
            print(f"Warning: Failed to load locale file {locale_file}: {e}")

    def _get_nested_value(self, data: Dict[str, Any], key: str) -> Optional[Any]:
        """从嵌套字典中获取值，支持点号分隔的键"""
        keys = key.split('.')
        current = data

        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None

        return current

    def translate(self, key: str, locale: Optional[str] = None, **kwargs) -> str:
        """
        翻译指定的键

        Args:
            key: 翻译键，支持点号分隔的嵌套键（如 "cli.create.success"）
            locale: 指定语言，如果为 None 则使用当前语言
            **kwargs: 用于变量插值的参数

        Returns:
            翻译后的文本，如果找不到则返回键本身
        """
        target_locale = locale or self._current_locale

        # 尝试从目标语言获取翻译
        if target_locale in self._translations:
            value = self._get_nested_value(self._translations[target_locale], key)
            if value is not None:
                return self._interpolate(value, kwargs)

        # 回退到回退链
        for fallback_locale in self._fallback_chain:
            if fallback_locale in self._translations:
                value = self._get_nested_value(self._translations[fallback_locale], key)
                if value is not None:
                    return self._interpolate(value, kwargs)

        # 如果都找不到，返回键本身
        return key

    def _interpolate(self, text: str, params: Dict[str, Any]) -> str:
        """
        变量插值

        支持的格式：
        - {variable}: 简单替换
        - {variable:format}: 带格式的替换（未来扩展）
        """
        if not params:
            return text

        try:
            return text.format(**params)
        except (KeyError, ValueError) as e:
            # 如果插值失败，返回原文本
            print(f"Warning: Interpolation failed for text '{text}': {e}")
            return text

    def has_translation(self, key: str, locale: Optional[str] = None) -> bool:
        """检查是否存在指定键的翻译"""
        target_locale = locale or self._current_locale

        if target_locale in self._translations:
            value = self._get_nested_value(self._translations[target_locale], key)
            if value is not None:
                return True

        return False

    def get_available_locales(self) -> List[str]:
        """获取所有已加载的语言列表"""
        return list(self._translations.keys())

    def reload_locale(self, locale: str):
        """重新加载指定语言的翻译文件"""
        if locale in self._translations:
            del self._translations[locale]
        self._load_locale(locale)

    def clear_cache(self):
        """清除所有翻译缓存"""
        self._translations.clear()


# 全局单例实例
_i18n_manager = I18nManager()


def get_i18n_manager() -> I18nManager:
    """获取全局 I18nManager 实例"""
    return _i18n_manager
