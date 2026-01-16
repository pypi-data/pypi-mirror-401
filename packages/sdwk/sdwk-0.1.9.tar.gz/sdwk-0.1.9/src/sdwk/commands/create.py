"""Create command for generating new SDW projects."""

from typing import Any

import click
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from sdwk.core.exceptions import safe_questionary_ask
from sdwk.core.template_manager import TemplateManager
from sdwk.core.i18n import t

console = Console()


@click.command()
@click.option("--name", help="Project name / 项目名称")
@click.option("--type", "project_type", type=click.Choice(["node", "graph", "group"]), help="Project type / 项目类型")
@click.option("--description", help="Project description / 项目描述")
@click.option("--platform-url", help="Platform URL / 平台地址")
@click.option("--output-dir", help="Output directory / 输出目录", default=".")
@click.option("--dev", is_flag=True, help="Development mode / 开发环境模式")
def create(name: str, project_type: str, description: str, platform_url: str, output_dir: str, dev: bool):
    """Create a new SDW project / 创建新的SDW项目."""
    # 显示标题
    title = f"[bold blue]{t('cli.create.title')}[/bold blue]\n{t('cli.create.subtitle')}"
    console.print(Panel.fit(title, border_style="blue"))

    try:
        # 交互式收集项目信息
        project_info = _collect_project_info(name, project_type, description, platform_url)

        if not project_info:
            # 用户取消了操作
            console.print(f"\n[yellow]{t('cli.create.cancelled')}[/yellow]")
            return

        # 添加 dev 环境标志
        project_info["dev_mode"] = dev

    except KeyboardInterrupt:
        console.print(f"\n\n[yellow]{t('cli.create.cancelled')}[/yellow]")
        return

    # 创建项目
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(t('cli.create.creating'), total=None)

            template_manager = TemplateManager()
            project_path = template_manager.create_project(project_info=project_info, output_dir=output_dir)

            progress.update(task, description=t('cli.create.completed'))

        console.print(f"\n[green]✓[/green] {t('cli.create.success')}")
        console.print(f"[dim]{t('cli.create.project_path')}[/dim] {project_path}")
        console.print(f"\n[yellow]{t('cli.create.next_steps')}[/yellow]")
        console.print(f"  cd {project_info['name']}")
        console.print("  sdwk dev")

    except Exception as e:
        console.print(f"[red]✗[/red] {t('cli.create.error', error=str(e))}")
        raise click.ClickException(str(e))


def _collect_project_info(name: str, project_type: str, description: str, platform_url: str) -> dict[str, Any] | None:
    """交互式收集项目信息."""
    # 项目名称
    if not name:
        name = safe_questionary_ask(
            questionary.text(
                t('cli.create.prompt_name'),
                validate=lambda x: len(x.strip()) > 0 or t('cli.create.name_empty_error')
            )
        )
        if name is None:
            return None

    # 项目类型
    if not project_type:
        project_type = safe_questionary_ask(
            questionary.select(
                t('cli.create.prompt_type'),
                choices=[
                    questionary.Choice(t('cli.create.type_node'), "node"),
                    questionary.Choice(t('cli.create.type_graph'), "graph"),
                    questionary.Choice(t('cli.create.type_group'), "group"),
                ],
            )
        )
        if project_type is None:
            return None

    # 项目描述
    if not description:
        description = safe_questionary_ask(
            questionary.text(
                t('cli.create.prompt_description'),
                default=t('cli.create.default_description')
            )
        )
        if description is None:
            return None

    # 平台地址
    if not platform_url:
        platform_url = safe_questionary_ask(
            questionary.text(
                t('cli.create.prompt_platform_url'),
                default=t('cli.create.default_platform_url')
            )
        )
        if platform_url is None:
            return None

    nodes = []
    category = None
    if project_type == "group":
        # Group项目特有配置
        category = safe_questionary_ask(questionary.text("平台组件分组 (Category):", default="MyGroup"))
        if category is None:
            return None

        node_names_str = safe_questionary_ask(questionary.text("初始节点名称 (逗号分隔):", default="node1,node2"))
        if node_names_str is None:
            return None

        for node_name_input in node_names_str.split(","):
            clean_name = node_name_input.strip()
            if clean_name:
                nodes.append({
                    "name": clean_name,
                    "display_name": clean_name.replace("_", " ").title(),
                    "entry": f"{clean_name}.py",
                    "description": f"{clean_name} functionality"
                })

        if not nodes:
            # 默认至少一个
            nodes.append({
                "name": "example_node",
                "display_name": "Example Node",
                "entry": "example_node.py",
                "description": "Example node functionality"
            })

    return {
        "name": name.strip(),
        "type": project_type,
        "description": description.strip(),
        "platform_url": platform_url.strip(),
        "category": category,
        "nodes": nodes,
    }

