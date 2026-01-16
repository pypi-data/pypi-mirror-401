"""SDW Platform SDK CLI."""

from importlib.metadata import PackageNotFoundError, version

import click
from rich.console import Console

from .commands.add import add
from .commands.build import build
from .commands.check import check
from .commands.create import create
from .commands.dev import dev
from .commands.export_flow import export_flow
from .commands.publish import publish
from .commands.remove import remove
from .core.i18n import get_i18n_manager, get_locale_detector

console = Console()


def get_version():
    """获取包版本号."""
    try:
        return version("sdwk")
    except PackageNotFoundError:
        return "0.1.0"  # 开发环境回退版本


@click.group()
@click.version_option(version=get_version(), prog_name="sdwk")
@click.option('--locale', help='Set language (en, zh-CN, etc.)')
@click.pass_context
def main(ctx, locale):
    """SDW Platform SDK - 用于创建、开发和发布SDW平台应用的工具."""
    # 初始化国际化
    detector = get_locale_detector()
    detected_locale = detector.detect(cli_locale=locale)

    manager = get_i18n_manager()
    manager.set_locale(detected_locale)

    # 将 locale 存储到 context 中，供子命令使用
    ctx.ensure_object(dict)
    ctx.obj['locale'] = detected_locale


# 注册子命令
main.add_command(create)
main.add_command(dev)
main.add_command(check)
main.add_command(build)
main.add_command(publish)
main.add_command(add)
main.add_command(remove)
main.add_command(export_flow, name="export-flow")

if __name__ == "__main__":
    main()
