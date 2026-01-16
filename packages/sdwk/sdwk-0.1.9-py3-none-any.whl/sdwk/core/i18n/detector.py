"""
Locale Detector - 语言检测器

从多个来源检测语言设置，按优先级顺序：
1. 命令行参数
2. 环境变量
3. 配置文件
4. 系统语言
5. 默认语言
"""

import os
import locale
from pathlib import Path
from typing import Optional, Dict, Any
import json


class LocaleDetector:
    """语言检测器"""

    def __init__(self, default_locale: str = 'en'):
        """
        初始化语言检测器

        Args:
            default_locale: 默认语言
        """
        self.default_locale = default_locale
        self._config_file: Optional[Path] = None

    def set_config_file(self, config_file: str | Path):
        """设置配置文件路径"""
        self._config_file = Path(config_file)

    def detect(
        self,
        cli_locale: Optional[str] = None,
        env_var: str = 'SDWK_LOCALE',
        config_key: str = 'locale'
    ) -> str:
        """
        检测语言设置

        Args:
            cli_locale: 命令行参数指定的语言
            env_var: 环境变量名称
            config_key: 配置文件中的键名

        Returns:
            检测到的语言代码
        """
        # 1. 命令行参数（最高优先级）
        if cli_locale:
            return self._normalize_locale(cli_locale)

        # 2. 环境变量
        env_locale = os.environ.get(env_var)
        if env_locale:
            return self._normalize_locale(env_locale)

        # 3. 配置文件
        config_locale = self._read_from_config(config_key)
        if config_locale:
            return self._normalize_locale(config_locale)

        # 4. 系统语言
        system_locale = self._detect_system_locale()
        if system_locale:
            return self._normalize_locale(system_locale)

        # 5. 默认语言
        return self.default_locale

    def _read_from_config(self, config_key: str) -> Optional[str]:
        """从配置文件读取语言设置"""
        if not self._config_file or not self._config_file.exists():
            return None

        try:
            with open(self._config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get(config_key)
        except (json.JSONDecodeError, IOError):
            return None

    def _detect_system_locale(self) -> Optional[str]:
        """检测系统语言"""
        try:
            # 尝试获取系统默认语言
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                return system_locale
        except Exception:
            pass

        # 尝试从环境变量获取
        for env_var in ['LANG', 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES']:
            lang = os.environ.get(env_var)
            if lang:
                # 提取语言代码（如 en_US.UTF-8 -> en_US）
                return lang.split('.')[0]

        return None

    def _normalize_locale(self, locale_str: str) -> str:
        """
        规范化语言代码

        将各种格式的语言代码转换为标准格式：
        - en_US -> en
        - zh_CN -> zh-CN
        - zh_TW -> zh-TW
        - ja_JP -> ja
        """
        if not locale_str:
            return self.default_locale

        # 移除编码部分（如 .UTF-8）
        locale_str = locale_str.split('.')[0]

        # 处理下划线和连字符
        if '_' in locale_str:
            parts = locale_str.split('_')
            lang = parts[0].lower()

            # 对于中文，保留地区代码
            if lang == 'zh' and len(parts) > 1:
                region = parts[1].upper()
                return f"{lang}-{region}"

            # 其他语言只返回语言代码
            return lang

        # 已经是标准格式
        return locale_str.lower()


# 全局检测器实例
_locale_detector = LocaleDetector()


def get_locale_detector() -> LocaleDetector:
    """获取全局 LocaleDetector 实例"""
    return _locale_detector
