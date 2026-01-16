"""Export Flow command for converting Group project to platform flow format."""

import ast
import json
import random
import string
import uuid
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel

from sdwk.core.project_config import ProjectConfig

console = Console()


@click.command()
@click.option("--project-dir", default=".", help="项目目录路径")
@click.option("--output", "-o", default=None, help="输出文件路径 (默认: flow.json)")
@click.option("--layout", type=click.Choice(["vertical", "horizontal", "grid"]), default="horizontal", help="节点布局方式")
@click.option("--spacing", default=400, help="节点间距")
@click.option("--auto-connect", type=click.Choice(["none", "chain", "type-match", "config"]), default="config", help="自动连接模式：none=不连接, chain=链式连接, type-match=类型匹配, config=从sdw.json读取")
def export_flow(project_dir: str, output: str | None, layout: str, spacing: int, auto_connect: str):
    """将 Group 项目导出为平台可识别的 Flow JSON 格式."""
    project_path = Path(project_dir).resolve()

    console.print(Panel.fit("[bold cyan]SDW Flow Exporter[/bold cyan]\n项目路径: " + str(project_path), border_style="cyan"))

    # 加载项目配置
    try:
        config = ProjectConfig.from_file(project_path / "sdw.json")
        console.print(f"[dim]项目名称:[/dim] {config.name}")
        console.print(f"[dim]项目类型:[/dim] {config.type}")
    except Exception as e:
        console.print(f"[red]✗[/red] 加载项目配置失败: {e}")
        raise click.ClickException("配置文件错误")

    # 检查项目类型
    if config.type != "group":
        console.print("[yellow]警告:[/yellow] 此命令主要用于 Group 类型项目")
        console.print("[dim]对于单节点项目，Flow 只包含一个组件[/dim]")

    # 检查是否已构建
    context = config.get_template_context()
    package_name = context["project_name_snake"]

    if config.type == "group":
        component_dir = project_path / "src" / package_name / "component"
        if not component_dir.exists():
            console.print("[red]✗[/red] 未找到 component 目录，请先执行 sdwk build")
            raise click.ClickException("请先执行 sdwk build")

    # 生成 Flow JSON
    try:
        flow_data = _generate_flow_data(project_path, config, layout, spacing, auto_connect)

        # 确定输出路径
        if output:
            output_path = Path(output)
            if not output_path.is_absolute():
                output_path = project_path / output_path
        else:
            output_path = project_path / "flow.json"

        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(flow_data, f, ensure_ascii=False, indent=2)

        console.print(f"\n[green]✓[/green] Flow 导出成功!")
        console.print(f"[dim]输出文件:[/dim] {output_path}")
        console.print(f"[dim]节点数量:[/dim] {len(flow_data['data']['nodes'])}")
        console.print(f"[dim]边数量:[/dim] {len(flow_data['data']['edges'])}")

    except Exception as e:
        console.print(f"[red]✗[/red] 导出失败: {e}")
        raise click.ClickException(str(e))


def _generate_flow_data(project_path: Path, config: ProjectConfig, layout: str, spacing: int, auto_connect: str) -> dict[str, Any]:
    """生成平台格式的 Flow 数据."""
    context = config.get_template_context()
    package_name = context["project_name_snake"]

    nodes = []
    node_infos = []  # 保存节点信息用于生成边

    if config.type == "group" and config.nodes:
        # Group 类型：为每个节点生成 node
        component_dir = project_path / "src" / package_name / "component"

        for idx, node_config in enumerate(config.nodes):
            node_name = node_config["name"] if isinstance(node_config, dict) else node_config.name
            entry_file = node_config["entry"] if isinstance(node_config, dict) else node_config.entry
            display_name = node_config.get("display_name", node_name) if isinstance(node_config, dict) else getattr(node_config, "display_name", node_name)
            description = node_config.get("description", "") if isinstance(node_config, dict) else getattr(node_config, "description", "")

            # 读取 _comp.py 文件获取组件信息和代码
            comp_file = component_dir / f"{Path(entry_file).stem}_comp.py"
            comp_code = ""
            if comp_file.exists():
                component_info = _parse_component_file(comp_file)
                # 读取完整的组件代码
                comp_code = comp_file.read_text(encoding="utf-8")
            else:
                # 如果没有 _comp.py，从源文件解析
                source_file = project_path / "src" / package_name / entry_file
                component_info = _parse_component_file(source_file) if source_file.exists() else {}
                if source_file.exists():
                    comp_code = source_file.read_text(encoding="utf-8")

            # 计算节点位置
            position = _calculate_position(idx, len(config.nodes), layout, spacing)

            # 生成节点 ID（平台格式：{project}-{version}-{node_name}-{random}）
            random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            node_id = f"{config.name}-{config.version}-{node_name}-{random_suffix}"

            # 节点的 data.type 就是 node_name
            data_type = node_name

            # 生成节点
            node_data = _create_node(
                node_id=node_id,
                node_name=node_name,
                display_name=display_name,
                description=description,
                component_info=component_info,
                position=position,
                config=config,
                comp_code=comp_code  # 传入组件代码
            )
            nodes.append(node_data)

            # 保存节点信息
            node_infos.append({
                "id": node_id,
                "name": node_name,
                "data_type": data_type,  # 用于边的 dataType
                "inputs": component_info.get("inputs", []),
                "outputs": component_info.get("outputs", []),
                "class_name": component_info.get("class_name", "")
            })
    else:
        # 单节点项目
        source_file = project_path / "src" / package_name / "run.py"
        comp_code = ""
        if source_file.exists():
            component_info = _parse_component_file(source_file)
            comp_code = source_file.read_text(encoding="utf-8")
        else:
            component_info = {}

        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        node_id = f"{config.name}-{config.version}-{random_suffix}"
        data_type = config.name

        node_data = _create_node(
            node_id=node_id,
            node_name=config.name,
            display_name=config.name,
            description=config.description or "",
            component_info=component_info,
            position={"x": 100, "y": 100},
            config=config,
            comp_code=comp_code
        )
        nodes.append(node_data)

        node_infos.append({
            "id": node_id,
            "name": config.name,
            "data_type": data_type,
            "inputs": component_info.get("inputs", []),
            "outputs": component_info.get("outputs", []),
            "class_name": component_info.get("class_name", "")
        })

    # 生成边（自动连接）
    edges = _generate_edges(nodes, node_infos, auto_connect, config)

    # 构建完整的 Flow 结构
    flow_data = {
        "name": config.name,
        "display_name": config.name.replace("-", " ").replace("_", " ").title(),
        "description": config.description or f"Flow exported from {config.name}",
        "is_component": False,
        "data": {
            "nodes": nodes,
            "edges": edges,
            "viewport": {
                "x": 0,
                "y": 0,
                "zoom": 1
            }
        }
    }

    return flow_data


def _generate_edges(nodes: list[dict], node_infos: list[dict], auto_connect: str, config: ProjectConfig) -> list[dict[str, Any]]:
    """生成节点之间的边."""
    edges = []

    if auto_connect == "none" or len(nodes) < 2:
        return edges

    # 构建节点名称到ID的映射
    name_to_id = {info["name"]: info["id"] for info in node_infos}
    name_to_info = {info["name"]: info for info in node_infos}

    if auto_connect == "config":
        # 从 sdw.json 的 edges 配置读取连接关系
        if not config.edges:
            console.print("[yellow]警告: sdw.json 中未定义 edges，无法自动连接[/yellow]")
            return edges

        for edge_config in config.edges:
            source_name = edge_config.get("source")
            target_name = edge_config.get("target")
            source_output = edge_config.get("source_output", "output")
            target_input = edge_config.get("target_input", "input_value")

            if source_name not in name_to_id:
                console.print(f"[yellow]警告: 未找到源节点 '{source_name}'[/yellow]")
                continue
            if target_name not in name_to_id:
                console.print(f"[yellow]警告: 未找到目标节点 '{target_name}'[/yellow]")
                continue

            source_id = name_to_id[source_name]
            target_id = name_to_id[target_name]
            source_info = name_to_info[source_name]
            target_info = name_to_info[target_name]

            edge = _create_edge(
                source_id=source_id,
                target_id=target_id,
                source_output=source_output,
                target_input=target_input,
                source_data_type=source_info.get("data_type", source_name),
                target_data_type=target_info.get("data_type", target_name)
            )
            edges.append(edge)

        console.print(f"[dim]从配置文件读取了 {len(edges)} 条连接[/dim]")
        return edges

    elif auto_connect == "chain":
        # 链式连接：节点1 -> 节点2 -> 节点3 -> ...
        for i in range(len(nodes) - 1):
            source_node = nodes[i]
            target_node = nodes[i + 1]
            source_info = node_infos[i]
            target_info = node_infos[i + 1]

            # 获取源节点的第一个输出
            source_outputs = source_info.get("outputs", [])
            if not source_outputs:
                source_output_name = "output"
            else:
                source_output_name = source_outputs[0].get("name", "output")

            # 获取目标节点的第一个输入
            target_inputs = target_info.get("inputs", [])
            if not target_inputs:
                target_input_name = "input_value"
            else:
                target_input_name = target_inputs[0].get("name", "input_value")

            edge = _create_edge(
                source_id=source_node["id"],
                target_id=target_node["id"],
                source_output=source_output_name,
                target_input=target_input_name,
                source_data_type=source_info.get("data_type", source_info["name"]),
                target_data_type=target_info.get("data_type", target_info["name"])
            )
            edges.append(edge)

    elif auto_connect == "type-match":
        # 类型匹配：根据输入输出类型匹配连接
        for i, source_node in enumerate(nodes):
            source_info = node_infos[i]
            source_outputs = source_info.get("outputs", [])

            for j, target_node in enumerate(nodes):
                if i >= j:  # 不连接自己和前面的节点
                    continue

                target_info = node_infos[j]
                target_inputs = target_info.get("inputs", [])

                # 尝试匹配输出和输入
                for output_def in source_outputs or [{"name": "output", "type": "Data"}]:
                    output_type = output_def.get("type", "Data")
                    output_name = output_def.get("name", "output")

                    for input_def in target_inputs or [{"name": "input_value", "type": "Data"}]:
                        input_type = input_def.get("type", "Data")
                        input_name = input_def.get("name", "input_value")

                        # 类型匹配（简单匹配，都是 Data 类型或类型相同）
                        if output_type == input_type or output_type in ["Data", "str", "any"] or input_type in ["Data", "str", "any"]:
                            edge = _create_edge(
                                source_id=source_node["id"],
                                target_id=target_node["id"],
                                source_output=output_name,
                                target_input=input_name,
                                source_data_type=source_info.get("data_type", source_info["name"]),
                                target_data_type=target_info.get("data_type", target_info["name"])
                            )
                            edges.append(edge)
                            break  # 每对节点只连接一次
                    else:
                        continue
                    break

    return edges


def _create_edge(source_id: str, target_id: str, source_output: str, target_input: str, source_data_type: str, target_data_type: str) -> dict[str, Any]:
    """创建平台格式的边数据.

    平台使用特殊的 handle 格式：JSON 字符串中使用 œ 代替 "
    """
    # 构建 sourceHandle JSON 对象
    # dataType 是节点的 data.type（即 node_name）
    source_handle_obj = {
        "dataType": source_data_type,
        "id": source_id,
        "name": source_output,
        "output_types": ["Data"]
    }

    # 构建 targetHandle JSON 对象
    target_handle_obj = {
        "fieldName": target_input,
        "id": target_id,
        "inputTypes": ["Data"],
        "type": "other"
    }

    # 将 JSON 对象转换为使用 œ 代替 " 的字符串格式
    def to_handle_string(obj: dict) -> str:
        # 先转为 JSON 字符串，然后替换引号为 œ
        json_str = json.dumps(obj, separators=(',', ':'))
        return json_str.replace('"', 'œ')

    source_handle_str = to_handle_string(source_handle_obj)
    target_handle_str = to_handle_string(target_handle_obj)

    # 构建边 ID
    edge_id = f"xy-edge__{source_id}{source_handle_str}-{target_id}{target_handle_str}"

    return {
        "id": edge_id,
        "source": source_id,
        "target": target_id,
        "sourceHandle": source_handle_str,
        "targetHandle": target_handle_str,
        "data": {
            "sourceHandle": source_handle_obj,
            "targetHandle": target_handle_obj
        },
        "animated": False,
        "className": "",
        "selected": False
    }


def _parse_component_file(file_path: Path) -> dict[str, Any]:
    """解析组件文件，提取输入输出定义."""
    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        info = {
            "class_name": None,
            "inputs": [],
            "outputs": [],
            "display_name": None,
            "description": None,
            "icon": "code"
        }

        # 查找 Component 类
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # 检查是否继承自 Component
                for base in node.bases:
                    if isinstance(base, ast.Name) and "Component" in base.id:
                        info["class_name"] = node.name

                        # 提取类属性
                        for item in node.body:
                            if isinstance(item, (ast.Assign, ast.AnnAssign)):
                                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                                    attr_name = item.target.id
                                elif isinstance(item, ast.Assign) and len(item.targets) == 1:
                                    if isinstance(item.targets[0], ast.Name):
                                        attr_name = item.targets[0].id
                                    else:
                                        continue
                                else:
                                    continue

                                value = item.value

                                if attr_name == "display_name" and isinstance(value, ast.Constant):
                                    info["display_name"] = value.value
                                elif attr_name == "description" and isinstance(value, ast.Constant):
                                    info["description"] = value.value
                                elif attr_name == "icon" and isinstance(value, ast.Constant):
                                    info["icon"] = value.value
                                elif attr_name == "inputs" and isinstance(value, ast.List):
                                    info["inputs"] = _parse_io_list(value, source_code)
                                elif attr_name == "outputs" and isinstance(value, ast.List):
                                    info["outputs"] = _parse_io_list(value, source_code)
                        break

        return info
    except Exception as e:
        console.print(f"[yellow]警告: 解析文件 {file_path.name} 失败: {e}[/yellow]")
        return {}


def _parse_io_list(list_node: ast.List, source_code: str) -> list[dict[str, Any]]:
    """解析输入/输出列表."""
    io_list = []

    for element in list_node.elts:
        if isinstance(element, ast.Call):
            io_def = {"type": "str"}

            # 获取类型名称
            if isinstance(element.func, ast.Name):
                io_def["input_type"] = element.func.id

            # 获取关键字参数
            for keyword in element.keywords:
                arg_name = keyword.arg
                if isinstance(keyword.value, ast.Constant):
                    io_def[arg_name] = keyword.value.value
                elif isinstance(keyword.value, ast.Name):
                    io_def[arg_name] = keyword.value.id

            io_list.append(io_def)

    return io_list


def _calculate_position(index: int, total: int, layout: str, spacing: int) -> dict[str, float]:
    """计算节点位置."""
    base_x = 100
    base_y = 100

    if layout == "vertical":
        return {
            "x": base_x,
            "y": base_y + index * spacing
        }
    elif layout == "horizontal":
        return {
            "x": base_x + index * spacing,
            "y": base_y
        }
    else:  # grid
        cols = max(1, int(total ** 0.5))
        row = index // cols
        col = index % cols
        return {
            "x": base_x + col * spacing,
            "y": base_y + row * spacing
        }


def _create_node(
    node_id: str,
    node_name: str,
    display_name: str,
    description: str,
    component_info: dict[str, Any],
    position: dict[str, float],
    config: ProjectConfig,
    comp_code: str = ""
) -> dict[str, Any]:
    """创建平台格式的节点数据."""
    context = config.get_template_context()
    package_name = context["project_name_snake"]

    # 构建模板数据（输入输出配置）
    template = {
        "_type": component_info.get("class_name", f"{node_name.title().replace('_', '')}Component")
    }

    # 添加 code 字段（组件代码）
    if comp_code:
        template["code"] = {
            "type": "code",
            "required": True,
            "placeholder": "",
            "list": False,
            "show": True,
            "multiline": True,
            "value": comp_code,
            "fileTypes": [],
            "file_path": "",
            "password": False,
            "name": "code",
            "advanced": True,
            "dynamic": True,
            "info": "",
            "load_from_db": False,
            "title_case": False
        }

    # 添加输入字段（完整格式匹配平台）
    for input_def in component_info.get("inputs", []):
        field_name = input_def.get("name", "input_value")
        template[field_name] = {
            "tool_mode": True,
            "trace_as_metadata": True,
            "list": False,
            "list_add_label": "Add More",
            "trace_as_input": True,
            "required": input_def.get("required", False),
            "placeholder": "",
            "show": True,
            "name": field_name,
            "value": input_def.get("value", ""),
            "display_name": input_def.get("display_name", field_name.replace("_", " ").title()),
            "advanced": False,
            "input_types": ["Data"],  # 关键字段：输入类型
            "dynamic": False,
            "info": input_def.get("info", ""),
            "title_case": False,
            "type": "other",  # 关键字段：字段类型
            "_input_type": input_def.get("input_type", "DataInput")
        }

    # 构建输出定义（完整格式匹配平台）
    outputs = []
    for output_def in component_info.get("outputs", []):
        outputs.append({
            "types": ["Data"],
            "selected": "Data",
            "name": output_def.get("name", "output"),
            "hidden": None,
            "display_name": output_def.get("display_name", "Output"),
            "method": output_def.get("method", "build_output"),
            "value": "__UNDEFINED__",
            "cache": True,
            "required_inputs": None,
            "allows_loop": False,
            "group_outputs": False,
            "options": None,
            "tool_mode": True
        })

    if not outputs:
        outputs.append({
            "types": ["Data"],
            "selected": "Data",
            "name": "output",
            "hidden": None,
            "display_name": "Output",
            "method": "build_output",
            "value": "__UNDEFINED__",
            "cache": True,
            "required_inputs": None,
            "allows_loop": False,
            "group_outputs": False,
            "options": None,
            "tool_mode": True
        })

    # 构建节点（完整格式匹配平台）
    node_type = component_info.get("class_name", f"{node_name.title().replace('_', '')}Component")

    # 获取输入字段名称列表
    field_order = [input_def.get("name", "input_value") for input_def in component_info.get("inputs", [])]
    if not field_order:
        field_order = ["input_value"]

    node = {
        "id": node_id,
        "type": "genericNode",
        "position": position,
        "data": {
            "node": {
                "template": template,
                "description": description or component_info.get("description", ""),
                "icon": component_info.get("icon", "code"),
                "base_classes": ["Data"],
                "display_name": display_name or component_info.get("display_name", node_name),
                "documentation": "https://docs.sdwplatform.org/components-custom-components",
                "minimized": False,
                "custom_fields": {},
                "output_types": [],
                "pinned": False,
                "conditional_paths": [],
                "frozen": False,
                "outputs": outputs,
                "field_order": field_order,
                "beta": False,
                "legacy": False,
                "edited": False,
                "metadata": {},
                "tool_mode": False,
                "lf_version": "",
                # SDK 组件特有字段
                "file_name": f"{config.name}-{config.version}",
                "package_name": package_name
            },
            "showNode": True,
            "type": node_name,
            "id": node_id
        },
        "selected": False,
        "measured": {
            "width": 320,
            "height": 167
        }
    }

    return node
