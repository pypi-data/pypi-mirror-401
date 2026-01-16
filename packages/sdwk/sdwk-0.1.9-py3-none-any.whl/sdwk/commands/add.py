"""Add command for adding nodes/edges to existing Group projects."""

import ast
import json
from pathlib import Path
from typing import Any

import click
import questionary
from rich.console import Console
from rich.panel import Panel

from sdwk.core.exceptions import safe_questionary_ask
from sdwk.core.project_config import ProjectConfig
from sdwk.core.template_manager import TemplateManager

console = Console()


@click.group()
def add():
    """向现有 Group 项目添加节点或边."""
    pass


@add.command("node")
@click.option("--project-dir", default=".", help="项目目录路径")
@click.option("--name", help="节点名称")
@click.option("--display-name", help="节点显示名称")
@click.option("--description", help="节点描述")
def add_node(project_dir: str, name: str, display_name: str, description: str):
    """向 Group 项目添加新节点."""
    project_path = Path(project_dir).resolve()

    console.print(Panel.fit(
        "[bold cyan]SDW Add Node[/bold cyan]\n"
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
        console.print(f"[red]✗[/red] 当前项目类型为 '{config.type}'，add node 仅支持 group 类型项目")
        raise click.ClickException("Only group projects are supported")

    # 获取现有节点名称
    existing_nodes = []
    if config.nodes:
        for node in config.nodes:
            node_name = node["name"] if isinstance(node, dict) else node.name
            existing_nodes.append(node_name)

    console.print(f"\n[dim]现有节点: {', '.join(existing_nodes) if existing_nodes else '无'}[/dim]")

    # 交互式收集节点信息
    try:
        node_info = _collect_node_info(name, display_name, description, existing_nodes)
        if not node_info:
            console.print("\n[yellow]操作已取消[/yellow]")
            return
    except KeyboardInterrupt:
        console.print("\n\n[yellow]操作已取消[/yellow]")
        return

    # 生成节点文件（复用 TemplateManager）
    try:
        template_manager = TemplateManager()
        template_context = config.get_template_context()
        package_name = template_context["project_name_snake"]
        package_dir = project_path / "src" / package_name

        # 检查文件是否已存在
        target_file = package_dir / node_info["entry"]
        if target_file.exists():
            console.print(f"[red]✗[/red] 节点文件已存在: {target_file.relative_to(project_path)}")
            raise click.ClickException("Node file already exists")

        # 生成节点文件
        generated_file = template_manager.generate_node(
            package_dir=package_dir,
            node_info=node_info,
            template_context=template_context
        )
        console.print(f"[green]✓[/green] 已创建节点文件: {generated_file.relative_to(project_path)}")

    except Exception as e:
        console.print(f"[red]✗[/red] 生成节点文件失败: {e}")
        raise click.ClickException(str(e))

    # 更新 sdw.json
    try:
        _update_sdw_json(sdw_json_path, node_info)
    except Exception as e:
        console.print(f"[red]✗[/red] 更新 sdw.json 失败: {e}")
        raise click.ClickException(str(e))

    console.print(f"\n[green]✓[/green] 节点 '{node_info['name']}' 添加成功!")
    console.print(f"[dim]节点文件:[/dim] src/{package_name}/{node_info['entry']}")
    console.print("\n[yellow]下一步:[/yellow]")
    console.print("  1. 编辑节点文件，实现业务逻辑")
    console.print("  2. 运行 sdwk build 构建项目")


def _collect_node_info(
    name: str | None,
    display_name: str | None,
    description: str | None,
    existing_nodes: list[str]
) -> dict[str, Any] | None:
    """交互式收集节点信息."""

    # 节点名称
    if not name:
        def validate_name(x: str) -> bool | str:
            x = x.strip()
            if not x:
                return "节点名称不能为空"
            if not x.replace("_", "").replace("-", "").isalnum():
                return "节点名称只能包含字母、数字、下划线和连字符"
            if x in existing_nodes:
                return f"节点 '{x}' 已存在"
            return True

        name = safe_questionary_ask(
            questionary.text(
                "节点名称 (如 data_cleaner):",
                validate=validate_name
            )
        )
        if name is None:
            return None
    else:
        # 验证命令行传入的名称
        if name in existing_nodes:
            console.print(f"[red]✗[/red] 节点 '{name}' 已存在")
            return None

    name = name.strip()

    # 显示名称
    if not display_name:
        default_display = name.replace("_", " ").replace("-", " ").title()
        display_name = safe_questionary_ask(
            questionary.text("显示名称:", default=default_display)
        )
        if display_name is None:
            return None

    # 描述
    if not description:
        description = safe_questionary_ask(
            questionary.text("节点描述:", default=f"{name} functionality")
        )
        if description is None:
            return None

    return {
        "name": name,
        "display_name": display_name.strip(),
        "description": description.strip(),
        "entry": f"{name}.py"
    }


def _update_sdw_json(sdw_json_path: Path, node_info: dict[str, Any]):
    """更新 sdw.json，添加新节点."""
    with open(sdw_json_path, encoding="utf-8") as f:
        sdw_data = json.load(f)

    # 确保 nodes 字段存在
    if "nodes" not in sdw_data:
        sdw_data["nodes"] = []

    # 添加新节点
    new_node = {
        "name": node_info["name"],
        "display_name": node_info["display_name"],
        "entry": node_info["entry"],
        "description": node_info["description"]
    }
    sdw_data["nodes"].append(new_node)

    # 写回文件
    with open(sdw_json_path, "w", encoding="utf-8") as f:
        json.dump(sdw_data, f, ensure_ascii=False, indent=2)

    console.print("[green]✓[/green] 已更新 sdw.json")


@add.command("edge")
@click.option("--project-dir", default=".", help="项目目录路径")
@click.option("--source", help="源节点名称")
@click.option("--target", help="目标节点名称")
@click.option("--source-output", help="源节点输出端口名称")
@click.option("--target-input", help="目标节点输入端口名称")
def add_edge(project_dir: str, source: str, target: str, source_output: str, target_input: str):
    """向 Group 项目添加节点连接 (边)."""
    project_path = Path(project_dir).resolve()

    console.print(Panel.fit(
        "[bold cyan]SDW Add Edge[/bold cyan]\n"
        f"项目路径: {project_path}",
        border_style="cyan"
    ))

    # 检查 sdw.json
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

    # 检查类型
    if config.type != "group":
        console.print(f"[red]✗[/red] 当前项目类型为 '{config.type}'，add edge 仅支持 group 类型项目")
        raise click.ClickException("Only group projects are supported")

    # 获取项目信息
    template_context = config.get_template_context()
    package_name = template_context["project_name_snake"]
    package_dir = project_path / "src" / package_name

    # 构建节点信息映射（包含输入输出）
    nodes_info = _build_nodes_info(config, package_dir)

    if len(nodes_info) < 2:
        console.print("[red]✗[/red] 项目至少需要 2 个节点才能添加连接")
        raise click.ClickException("Need at least 2 nodes")

    # 显示节点信息
    console.print("\n[dim]现有节点:[/dim]")
    for name, info in nodes_info.items():
        inputs_str = ", ".join(info["inputs"]) if info["inputs"] else "无"
        outputs_str = ", ".join(info["outputs"]) if info["outputs"] else "无"
        # 使用 \\[ 转义方括号，避免 Rich 将其解释为格式标签
        console.print(f"  • {name}: Inputs=\\[{inputs_str}] Outputs=\\[{outputs_str}]")

    # 获取现有边
    with open(sdw_json_path, encoding="utf-8") as f:
        sdw_data = json.load(f)
    existing_edges = sdw_data.get("edges") or []  # 处理 null 和缺失的情况

    # 显示现有边
    if existing_edges:
        console.print(f"\n[dim]现有连接 ({len(existing_edges)} 条):[/dim]")
        for idx, edge in enumerate(existing_edges, 1):
            src = edge.get("source", "?")
            tgt = edge.get("target", "?")
            src_out = edge.get("source_output", "output")
            tgt_in = edge.get("target_input", "input_value")
            console.print(f"  {idx}. {src}.{src_out} → {tgt}.{tgt_in}")
    else:
        console.print("\n[dim]现有连接: 无[/dim]")

    # 交互式获取连接信息
    try:
        edge_info = _collect_edge_info(
            source, target, source_output, target_input,
            nodes_info, existing_edges
        )
        if not edge_info:
            console.print("\n[yellow]操作已取消[/yellow]")
            return
    except KeyboardInterrupt:
        console.print("\n\n[yellow]操作已取消[/yellow]")
        return

    # 更新 sdw.json
    if not sdw_data.get("edges"):
        sdw_data["edges"] = []

    sdw_data["edges"].append(edge_info)

    with open(sdw_json_path, "w", encoding="utf-8") as f:
        json.dump(sdw_data, f, ensure_ascii=False, indent=2)

    console.print(f"\n[green]✓[/green] 连接添加成功!")
    console.print(f"[dim]{edge_info['source']}.{edge_info['source_output']} → {edge_info['target']}.{edge_info['target_input']}[/dim]")


def _build_nodes_info(config: ProjectConfig, package_dir: Path) -> dict[str, dict]:
    """构建节点信息映射，包含输入输出列表."""
    nodes_info = {}

    for node in config.nodes or []:
        node_name = node["name"] if isinstance(node, dict) else node.name
        entry_file = node["entry"] if isinstance(node, dict) else node.entry

        # 解析节点文件获取输入输出
        node_file = package_dir / entry_file
        io_info = _parse_node_io(node_file)

        nodes_info[node_name] = {
            "entry": entry_file,
            "inputs": io_info["inputs"],
            "outputs": io_info["outputs"]
        }

    return nodes_info


def _parse_node_io(file_path: Path) -> dict[str, list[str]]:
    """解析节点文件，提取输入输出端口名称."""
    result = {
        "inputs": [],
        "outputs": []
    }

    if not file_path.exists():
        # 文件不存在，返回默认值
        result["inputs"] = ["input_value"]
        result["outputs"] = ["output"]
        return result

    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        # 查找 Component 类
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # 检查是否继承自 Component
                for base in node.bases:
                    if isinstance(base, ast.Name) and "Component" in base.id:
                        # 提取 inputs 和 outputs
                        for item in node.body:
                            if isinstance(item, ast.Assign) and len(item.targets) == 1:
                                if isinstance(item.targets[0], ast.Name):
                                    attr_name = item.targets[0].id
                                    if attr_name == "inputs" and isinstance(item.value, ast.List):
                                        result["inputs"] = _extract_io_names(item.value)
                                    elif attr_name == "outputs" and isinstance(item.value, ast.List):
                                        result["outputs"] = _extract_io_names(item.value)
                        break

        # 如果没有解析到，使用默认值
        if not result["inputs"]:
            result["inputs"] = ["input_value"]
        if not result["outputs"]:
            result["outputs"] = ["output"]

    except Exception as e:
        console.print(f"[yellow]警告: 解析文件 {file_path.name} 失败: {e}[/yellow]")
        result["inputs"] = ["input_value"]
        result["outputs"] = ["output"]

    return result


def _extract_io_names(list_node: ast.List) -> list[str]:
    """从 AST 列表节点中提取输入/输出的 name 属性."""
    names = []

    for element in list_node.elts:
        if isinstance(element, ast.Call):
            # 查找 name= 关键字参数
            for keyword in element.keywords:
                if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
                    names.append(keyword.value.value)
                    break

    return names


def _collect_edge_info(
    source: str | None,
    target: str | None,
    source_output: str | None,
    target_input: str | None,
    nodes_info: dict[str, dict],
    existing_edges: list[dict]
) -> dict[str, str] | None:
    """交互式收集连接信息."""

    node_names = list(nodes_info.keys())

    # 选择源节点
    if not source:
        source = safe_questionary_ask(
            questionary.select("选择源节点:", choices=node_names)
        )
        if source is None:
            return None
    else:
        if source not in nodes_info:
            console.print(f"[red]✗[/red] 源节点 '{source}' 不存在")
            return None

    # 选择源节点的输出端口
    source_outputs = nodes_info[source]["outputs"]
    if not source_output:
        if len(source_outputs) == 1:
            source_output = source_outputs[0]
            console.print(f"[dim]自动选择输出端口: {source_output}[/dim]")
        else:
            source_output = safe_questionary_ask(
                questionary.select(
                    f"选择 {source} 的输出端口:",
                    choices=source_outputs
                )
            )
            if source_output is None:
                return None
    else:
        if source_output not in source_outputs:
            console.print(f"[yellow]警告: 输出端口 '{source_output}' 不在已解析的列表中，将继续使用[/yellow]")

    # 选择目标节点
    available_targets = [n for n in node_names if n != source]
    if not available_targets:
        console.print("[red]✗[/red] 没有可用的目标节点")
        return None

    if not target:
        target = safe_questionary_ask(
            questionary.select("选择目标节点:", choices=available_targets)
        )
        if target is None:
            return None
    else:
        if target not in nodes_info:
            console.print(f"[red]✗[/red] 目标节点 '{target}' 不存在")
            return None
        if target == source:
            console.print("[red]✗[/red] 源节点和目标节点不能相同")
            return None

    # 选择目标节点的输入端口
    target_inputs = nodes_info[target]["inputs"]
    if not target_input:
        if len(target_inputs) == 1:
            target_input = target_inputs[0]
            console.print(f"[dim]自动选择输入端口: {target_input}[/dim]")
        else:
            target_input = safe_questionary_ask(
                questionary.select(
                    f"选择 {target} 的输入端口:",
                    choices=target_inputs
                )
            )
            if target_input is None:
                return None
    else:
        if target_input not in target_inputs:
            console.print(f"[yellow]警告: 输入端口 '{target_input}' 不在已解析的列表中，将继续使用[/yellow]")

    # 检查重复连接
    for edge in existing_edges:
        if (edge.get("source") == source and
            edge.get("target") == target and
            edge.get("source_output") == source_output and
            edge.get("target_input") == target_input):
            console.print(f"[yellow]警告: 完全相同的连接已存在[/yellow]")
            override = safe_questionary_ask(
                questionary.confirm("是否继续添加?", default=False)
            )
            if not override:
                return None
            break

    return {
        "source": source,
        "target": target,
        "source_output": source_output,
        "target_input": target_input
    }

