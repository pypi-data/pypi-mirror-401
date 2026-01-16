"""Remove command for removing nodes/edges from existing Group projects."""

import json
import os
from pathlib import Path

import click
import questionary
from rich.console import Console
from rich.panel import Panel

from sdwk.core.exceptions import safe_questionary_ask
from sdwk.core.project_config import ProjectConfig

console = Console()


@click.group()
def remove():
    """从现有 Group 项目删除节点或边."""
    pass


@remove.command("node")
@click.option("--project-dir", default=".", help="项目目录路径")
@click.option("--name", help="要删除的节点名称")
@click.option("--keep-file", is_flag=True, default=False, help="保留节点源文件，仅从配置中移除")
@click.option("--force", "-f", is_flag=True, default=False, help="跳过确认直接删除")
def remove_node(project_dir: str, name: str, keep_file: bool, force: bool):
    """从 Group 项目删除节点."""
    project_path = Path(project_dir).resolve()

    console.print(Panel.fit(
        "[bold cyan]SDW Remove Node[/bold cyan]\n"
        f"项目路径: {project_path}",
        border_style="cyan"
    ))

    # 检查 sdw.json 是否存在
    sdw_json_path = project_path / "sdw.json"
    if not sdw_json_path.exists():
        console.print("[red]✗[/red] 未找到 sdw.json，请在 Group 项目根目录下执行此命令")
        raise click.ClickException("sdw.json not found")

    # 加载配置
    try:
        config = ProjectConfig.from_file(sdw_json_path)
    except Exception as e:
        console.print(f"[red]✗[/red] 加载配置失败: {e}")
        raise click.ClickException(str(e))

    # 检查是否为 group 类型
    if config.type != "group":
        console.print(f"[red]✗[/red] 当前项目类型为 '{config.type}'，remove node 仅支持 group 类型项目")
        raise click.ClickException("Only group projects are supported")

    # 获取现有节点
    with open(sdw_json_path, encoding="utf-8") as f:
        sdw_data = json.load(f)

    existing_nodes = sdw_data.get("nodes") or []
    if not existing_nodes:
        console.print("[yellow]项目中没有节点可以删除[/yellow]")
        return

    node_names = [n["name"] if isinstance(n, dict) else n.name for n in existing_nodes]
    console.print(f"\n[dim]现有节点: {', '.join(node_names)}[/dim]")

    # 选择要删除的节点
    if not name:
        name = safe_questionary_ask(
            questionary.select("选择要删除的节点:", choices=node_names)
        )
        if name is None:
            console.print("\n[yellow]操作已取消[/yellow]")
            return
    else:
        if name not in node_names:
            console.print(f"[red]✗[/red] 节点 '{name}' 不存在")
            raise click.ClickException("Node not found")

    # 获取节点信息
    node_to_remove = None
    for node in existing_nodes:
        node_name = node["name"] if isinstance(node, dict) else node.name
        if node_name == name:
            node_to_remove = node
            break

    entry_file = node_to_remove["entry"] if isinstance(node_to_remove, dict) else node_to_remove.entry

    # 检查是否有边引用此节点
    existing_edges = sdw_data.get("edges") or []
    affected_edges = []
    for idx, edge in enumerate(existing_edges):
        if edge.get("source") == name or edge.get("target") == name:
            affected_edges.append((idx, edge))

    if affected_edges:
        console.print(f"\n[yellow]警告: 以下连接将被同时删除:[/yellow]")
        for idx, edge in affected_edges:
            console.print(f"  • {edge.get('source')}.{edge.get('source_output', 'output')} → {edge.get('target')}.{edge.get('target_input', 'input_value')}")

    # 确认删除
    if not force:
        confirm_msg = f"确定删除节点 '{name}'?"
        if not keep_file:
            confirm_msg += f" (源文件 {entry_file} 也将被删除)"
        confirm = safe_questionary_ask(
            questionary.confirm(confirm_msg, default=False)
        )
        if not confirm:
            console.print("\n[yellow]操作已取消[/yellow]")
            return

    # 从 nodes 中移除
    new_nodes = [n for n in existing_nodes if (n["name"] if isinstance(n, dict) else n.name) != name]
    sdw_data["nodes"] = new_nodes

    # 从 edges 中移除相关边
    if affected_edges:
        new_edges = [e for e in existing_edges if e.get("source") != name and e.get("target") != name]
        sdw_data["edges"] = new_edges
        console.print(f"[green]✓[/green] 已删除 {len(affected_edges)} 条相关连接")

    # 保存配置
    with open(sdw_json_path, "w", encoding="utf-8") as f:
        json.dump(sdw_data, f, ensure_ascii=False, indent=2)
    console.print("[green]✓[/green] 已更新 sdw.json")

    # 删除源文件
    if not keep_file:
        template_context = config.get_template_context()
        package_name = template_context["project_name_snake"]
        source_file = project_path / "src" / package_name / entry_file
        if source_file.exists():
            os.remove(source_file)
            console.print(f"[green]✓[/green] 已删除源文件: {source_file.relative_to(project_path)}")
        else:
            console.print(f"[dim]源文件不存在: {entry_file}[/dim]")

        # 删除构建产物
        comp_file = project_path / "src" / package_name / "component" / f"{Path(entry_file).stem}_comp.py"
        if comp_file.exists():
            os.remove(comp_file)
            console.print(f"[green]✓[/green] 已删除构建产物: {comp_file.relative_to(project_path)}")

    console.print(f"\n[green]✓[/green] 节点 '{name}' 删除成功!")


@remove.command("edge")
@click.option("--project-dir", default=".", help="项目目录路径")
@click.option("--index", "-i", type=int, help="要删除的边索引（从1开始）")
@click.option("--source", help="源节点名称")
@click.option("--target", help="目标节点名称")
@click.option("--force", "-f", is_flag=True, default=False, help="跳过确认直接删除")
def remove_edge(project_dir: str, index: int, source: str, target: str, force: bool):
    """从 Group 项目删除节点连接."""
    project_path = Path(project_dir).resolve()

    console.print(Panel.fit(
        "[bold cyan]SDW Remove Edge[/bold cyan]\n"
        f"项目路径: {project_path}",
        border_style="cyan"
    ))

    # 检查 sdw.json
    sdw_json_path = project_path / "sdw.json"
    if not sdw_json_path.exists():
        console.print("[red]✗[/red] 未找到 sdw.json，请在 Group 项目根目录下执行此命令")
        raise click.ClickException("sdw.json not found")

    # 加载配置
    with open(sdw_json_path, encoding="utf-8") as f:
        sdw_data = json.load(f)

    # 检查类型
    if sdw_data.get("type") != "group":
        console.print(f"[red]✗[/red] 当前项目类型为 '{sdw_data.get('type')}'，remove edge 仅支持 group 类型项目")
        raise click.ClickException("Only group projects are supported")

    # 获取现有边
    existing_edges = sdw_data.get("edges") or []
    if not existing_edges:
        console.print("[yellow]项目中没有连接可以删除[/yellow]")
        return

    # 显示现有边
    console.print(f"\n[dim]现有连接 ({len(existing_edges)} 条):[/dim]")
    edge_choices = []
    for idx, edge in enumerate(existing_edges, 1):
        src = edge.get("source", "?")
        tgt = edge.get("target", "?")
        src_out = edge.get("source_output", "output")
        tgt_in = edge.get("target_input", "input_value")
        edge_str = f"{src}.{src_out} → {tgt}.{tgt_in}"
        console.print(f"  {idx}. {edge_str}")
        edge_choices.append(f"{idx}. {edge_str}")

    # 确定要删除的边
    edge_to_remove_idx = None

    if index is not None:
        # 通过索引删除
        if index < 1 or index > len(existing_edges):
            console.print(f"[red]✗[/red] 索引 {index} 超出范围 (1-{len(existing_edges)})")
            raise click.ClickException("Invalid index")
        edge_to_remove_idx = index - 1
    elif source and target:
        # 通过源节点和目标节点匹配
        for idx, edge in enumerate(existing_edges):
            if edge.get("source") == source and edge.get("target") == target:
                edge_to_remove_idx = idx
                break
        if edge_to_remove_idx is None:
            console.print(f"[red]✗[/red] 未找到从 '{source}' 到 '{target}' 的连接")
            raise click.ClickException("Edge not found")
    else:
        # 交互式选择
        selected = safe_questionary_ask(
            questionary.select("选择要删除的连接:", choices=edge_choices)
        )
        if selected is None:
            console.print("\n[yellow]操作已取消[/yellow]")
            return
        # 解析选择的索引
        edge_to_remove_idx = int(selected.split(".")[0]) - 1

    edge_to_remove = existing_edges[edge_to_remove_idx]
    edge_desc = f"{edge_to_remove.get('source')}.{edge_to_remove.get('source_output', 'output')} → {edge_to_remove.get('target')}.{edge_to_remove.get('target_input', 'input_value')}"

    # 确认删除
    if not force:
        confirm = safe_questionary_ask(
            questionary.confirm(f"确定删除连接 '{edge_desc}'?", default=False)
        )
        if not confirm:
            console.print("\n[yellow]操作已取消[/yellow]")
            return

    # 删除边
    del existing_edges[edge_to_remove_idx]
    sdw_data["edges"] = existing_edges

    # 保存配置
    with open(sdw_json_path, "w", encoding="utf-8") as f:
        json.dump(sdw_data, f, ensure_ascii=False, indent=2)

    console.print(f"\n[green]✓[/green] 连接删除成功!")
    console.print(f"[dim]已删除: {edge_desc}[/dim]")
    console.print(f"[dim]剩余连接: {len(existing_edges)} 条[/dim]")
