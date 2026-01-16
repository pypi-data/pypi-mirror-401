"""
I18n Decorators - 国际化装饰器

提供装饰器来简化组件的国际化处理：
- i18n_component: 自动处理组件类中的 I18nText 属性
"""

from typing import Type, Any
from functools import wraps
from .text import I18nText


def i18n_component(cls: Type) -> Type:
    """
    组件国际化装饰器

    自动处理组件类中的 I18nText 属性，使其在访问时自动返回当前语言的文本。

    使用方法：
        @i18n_component
        class MyComponent(Component):
            display_name = I18nText({
                "en": "My Component",
                "zh-CN": "我的组件"
            })

    Args:
        cls: 要装饰的组件类

    Returns:
        装饰后的组件类
    """
    # 保存原始的 __init__ 方法
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        # 调用原始的 __init__
        original_init(self, *args, **kwargs)

        # 处理类属性中的 I18nText 对象
        for attr_name in dir(cls):
            if attr_name.startswith('_'):
                continue

            attr_value = getattr(cls, attr_name, None)
            if isinstance(attr_value, I18nText):
                # 为实例创建一个属性，返回当前语言的文本
                setattr(self, f'_{attr_name}_i18n', attr_value)

    # 替换 __init__ 方法
    cls.__init__ = new_init

    # 为每个 I18nText 属性创建 property
    for attr_name in dir(cls):
        if attr_name.startswith('_'):
            continue

        attr_value = getattr(cls, attr_name, None)
        if isinstance(attr_value, I18nText):
            # 创建 property 来动态获取当前语言的文本
            def make_property(name):
                def getter(self):
                    i18n_obj = getattr(self, f'_{name}_i18n', None)
                    if i18n_obj:
                        return i18n_obj.get()
                    return getattr(cls, name).get()
                return property(getter)

            setattr(cls, attr_name, make_property(attr_name))

    return cls
