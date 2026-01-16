"""
Translation Functions - 翻译函数

提供便捷的全局翻译函数：
- t(): 标准翻译函数
- _(): 简短别名（遵循 gettext 惯例）
"""

from typing import Optional
from .manager import get_i18n_manager


def t(key: str, locale: Optional[str] = None, **kwargs) -> str:
    """
    翻译函数

    Args:
        key: 翻译键，支持点号分隔的嵌套键（如 "cli.create.success"）
        locale: 指定语言，如果为 None 则使用当前语言
        **kwargs: 用于变量插值的参数

    Returns:
        翻译后的文本

    Examples:
        >>> t("cli.create.success")
        "Project created successfully"

        >>> t("cli.create.success", name="my-project")
        "Project 'my-project' created successfully"

        >>> t("cli.create.success", locale="zh-CN")
        "项目创建成功"
    """
    manager = get_i18n_manager()
    return manager.translate(key, locale, **kwargs)


def _(key: str, **kwargs) -> str:
    """
    翻译函数的简短别名

    这是 t() 函数的简短版本，遵循 gettext 的 _() 惯例。
    不支持指定 locale 参数，始终使用当前语言。

    Args:
        key: 翻译键
        **kwargs: 用于变量插值的参数

    Returns:
        翻译后的文本

    Examples:
        >>> _("cli.error.not_found")
        "File not found"

        >>> _("cli.error.invalid", field="name")
        "Invalid field: name"
    """
    return t(key, **kwargs)
