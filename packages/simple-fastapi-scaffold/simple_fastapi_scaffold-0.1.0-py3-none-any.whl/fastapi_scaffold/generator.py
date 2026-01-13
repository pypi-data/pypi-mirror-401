"""模块代码生成器"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def generate_module(project_path, module_name, class_name=None, table_name=None):
    """生成新模块（Model + Schema + Router）"""
    if class_name is None:
        class_name = "".join(word.capitalize() for word in module_name.split("_"))
    if table_name is None:
        table_name = f"{module_name}s"

    # 检查是否在正确的目录（通过检查 main.py）
    if not (project_path / "main.py").exists():
        raise ValueError("未找到 main.py，请确保在项目根目录运行")

    # 获取模板目录
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))

    # 1. 生成 Model
    model_template = env.get_template("module_model.py.jinja2")
    model_content = model_template.render(
        module_name=module_name,
        class_name=class_name,
        table_name=table_name,
    )
    (project_path / "models" / f"{module_name}.py").write_text(model_content, encoding="utf-8")

    # 2. 生成 Schema
    schema_template = env.get_template("module_schema.py.jinja2")
    schema_content = schema_template.render(
        module_name=module_name,
        class_name=class_name,
    )
    schema_dir = project_path / "common" / "entity" / "schemas"
    schema_dir.mkdir(parents=True, exist_ok=True)
    (schema_dir / f"{module_name}.py").write_text(schema_content, encoding="utf-8")

    # 3. 生成 Router
    router_template = env.get_template("module_router.py.jinja2")
    router_content = router_template.render(
        module_name=module_name,
        class_name=class_name,
    )
    (project_path / "router" / f"{module_name}.py").write_text(router_content, encoding="utf-8")

    # 4. 更新 __init__.py 文件
    _update_models_init(project_path / "models" / "__init__.py", module_name, class_name)
    _update_schemas_init(project_path / "common" / "entity" / "schemas" / "__init__.py", module_name, class_name)
    _update_router_init(project_path / "router" / "__init__.py", module_name)


def _update_models_init(init_file, module_name, class_name):
    """更新 models/__init__.py"""
    if not init_file.exists():
        return

    content = init_file.read_text(encoding="utf-8")
    import_line = f"from models.{module_name} import {class_name}"

    if import_line not in content:
        content = content.rstrip() + f"\n{import_line}\n"
        init_file.write_text(content, encoding="utf-8")


def _update_schemas_init(init_file, module_name, class_name):
    """更新 schemas/__init__.py"""
    if not init_file.exists():
        return

    content = init_file.read_text(encoding="utf-8")
    imports = f"""from common.entity.schemas.{module_name} import (
    {class_name}CreateRequest,
    {class_name}UpdateRequest,
    {class_name}Response,
    {class_name}ListResponse,
)"""

    if imports not in content:
        content = content.rstrip() + f"\n{imports}\n"
        init_file.write_text(content, encoding="utf-8")


def _update_router_init(init_file, module_name):
    """更新 router/__init__.py"""
    if not init_file.exists():
        return

    content = init_file.read_text(encoding="utf-8")

    # 添加导入
    import_line = f"from .{module_name} import router as {module_name}_router"
    if import_line not in content:
        lines = content.split("\n")

        # 找到最后一个 from . 导入的位置
        last_import_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("from ."):
                last_import_idx = i

        if last_import_idx >= 0:
            lines.insert(last_import_idx + 1, import_line)
        else:
            lines.insert(0, import_line)

        content = "\n".join(lines)

    # 更新 __all__
    if "__all__" in content:
        lines = content.split("\n")
        all_found = False
        for i, line in enumerate(lines):
            if "__all__" in line:
                all_found = True
            elif all_found and line.strip() == "]":
                # 在 ] 之前添加新项
                lines.insert(i, f'    "{module_name}_router",')
                break

        content = "\n".join(lines)

    init_file.write_text(content, encoding="utf-8")
