"""CLI 命令行工具"""
import os
import shutil
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .generator import generate_module

console = Console()


@click.group()
@click.version_option(version="0.1.2", prog_name="simple-fastapi-scaffold")
def main():
    """FastAPI Scaffold - 一键生成企业级后端项目"""
    pass


@main.command()
@click.argument("project_name", type=str)
@click.option("--description", "-d", default="FastAPI Backend Project", help="项目描述")
@click.option("--author", "-a", default="", help="作者名称")
@click.option("--force", "-f", is_flag=True, help="强制覆盖已存在的目录")
def init(project_name, description, author, force):
    """初始化一个新的 FastAPI 后端项目

    示例:
        simple-fastapi-scaffold init my-backend
        simple-fastapi-scaffold init my-backend --description "我的后端项目" --force
    """
    project_path = Path.cwd() / project_name

    # 检查目录是否存在
    if project_path.exists() and not force:
        console.print(
            f"[red]目录 [bold]{project_name}[/bold] 已存在！[/red]\n"
            f"使用 [bold]--force[/bold] 选项覆盖已有目录，或选择其他名称。"
        )
        raise click.Abort()

    # 清理已存在的目录
    if project_path.exists() and force:
        shutil.rmtree(project_path)

    with console.status("[bold green]正在创建项目..."):
        _create_project(project_path, project_name, description, author)

    console.print(
        Panel(
            f"[green]✓[/green] 项目 [bold]{project_name}[/bold] 创建成功！\n\n"
            f"下一步:\n"
            f"  [cyan]cd {project_name}[/cyan]\n"
            f"  [cyan]uv sync[/cyan]\n"
            f"  [cyan]uv run python init_db.py[/cyan]\n"
            f"  [cyan]uv run uvicorn main:app --reload[/cyan]\n\n"
            f"访问 [cyan]http://localhost:8000/docs[/cyan] 查看 API 文档",
            title="[bold green]成功[/bold green]",
            border_style="green",
        )
    )


@main.command()
@click.argument("module_name", type=str)
@click.option("--class-name", "-c", help="类名（默认自动生成）")
@click.option("--table-name", "-t", help="表名（默认自动生成）")
def add(module_name, class_name, table_name):
    """添加新模块（Model + Schema + Router）

    示例:
        simple-fastapi-scaffold add article
        simple-fastapi-scaffold add user --class-name UserProfile
    """
    project_path = Path.cwd()

    # 检查是否在项目根目录
    if not (project_path / "main.py").exists():
        console.print("[red]错误: 请在项目根目录下运行此命令[/red]")
        raise click.Abort()

    with console.status(f"[bold green]正在添加模块 {module_name}..."):
        generate_module(project_path, module_name, class_name, table_name)

    console.print(
        Panel(
            f"[green]✓[/green] 模块 [bold]{module_name}[/bold] 添加成功！\n\n"
            f"生成的文件:\n"
            f"  [cyan]models/{module_name}.py[/cyan]\n"
            f"  [cyan]common/entity/schemas/{module_name}.py[/cyan]\n"
            f"  [cyan]router/{module_name}.py[/cyan]\n\n"
            f"记得在 [cyan]main.py[/cyan] 中注册路由:\n"
            f"  [cyan]from router import {module_name}_router[/cyan]\n"
            f"  [cyan]app.include_router({module_name}_router)[/cyan]",
            title="[bold green]成功[/bold green]",
            border_style="green",
        )
    )


def _create_project(project_path, project_name, description, author):
    """创建项目文件"""
    # 创建基础目录结构
    dirs = [
        project_path / "models",
        project_path / "router",
        project_path / "common",
        project_path / "common" / "entity",
        project_path / "common" / "entity" / "schemas",
        project_path / "common" / "middlewares",
        project_path / "common" / "orm",
        project_path / "logs",
        project_path / "test",
        project_path / ".venv",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    # 获取模板目录
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))

    # 渲染和写入文件
    template_files = [
        ("main.py.jinja2", "main.py", {
            "project_name": project_name,
            "description": description,
        }),
        ("common/config.py.jinja2", "common/config.py", {}),
        ("common/context.py.jinja2", "common/context.py", {}),
        ("common/logger.py.jinja2", "common/logger.py", {}),
        ("common/base_router.py.jinja2", "common/base_router.py", {}),
        ("common/orm/__init__.py.jinja2", "common/orm/__init__.py", {}),
        ("common/orm/db.py.jinja2", "common/orm/db.py", {}),
        ("common/orm/base_model.py.jinja2", "common/orm/base_model.py", {}),
        ("common/entity/base_response.py.jinja2", "common/entity/base_response.py", {}),
        ("common/entity/schemas/__init__.py.jinja2", "common/entity/schemas/__init__.py", {}),
        ("common/middlewares/log_middleware.py.jinja2", "common/middlewares/log_middleware.py", {}),
        ("models/__init__.py.jinja2", "models/__init__.py", {}),
        ("models/user.py.jinja2", "models/user.py", {}),
        ("router/__init__.py.jinja2", "router/__init__.py", {}),
        ("router/user.py.jinja2", "router/user.py", {}),
        ("common/utils.py.jinja2", "common/utils.py", {}),
        ("init_db.py.jinja2", "init_db.py", {}),
        (".env.jinja2", ".env", {}),
        (".gitignore.jinja2", ".gitignore", {}),
        ("README.md.jinja2", "README.md", {"project_name": project_name}),
    ]

    for template_name, output_path, context in template_files:
        template = env.get_template(template_name)
        content = template.render(**context)
        output_file = project_path / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding="utf-8")

    # 创建空的 __init__.py 文件
    (project_path / "__init__.py").write_text("", encoding="utf-8")

    # 创建 pyproject.toml
    pyproject_content = f"""[project]
name = "{project_name}"
version = "0.1.2"
description = "{description}"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.128.0",
    "uvloop>=0.22.1",
    "uvicorn[standard]>=0.32.1",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "pyjwt>=2.8.0",
    "sqlalchemy>=2.0.45",
    "greenlet>=3.0.0",
    "aiosqlite>=0.19.0",
    "orjson>=3.9.0",
    "bcrypt>=4.0.0",
    "email-validator>=2.0.0",
]

[tool.uv]
dev-dependencies = []
"""
    (project_path / "pyproject.toml").write_text(pyproject_content, encoding="utf-8")

    # 创建 .env 文件
    env_content = """# 应用配置
APP_NAME=FastAPI App
DEBUG=true

# 数据库配置
DB_URL=sqlite+aiosqlite:///./app.db

# JWT 配置
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
"""
    (project_path / ".env").write_text(env_content, encoding="utf-8")


if __name__ == "__main__":
    main()
