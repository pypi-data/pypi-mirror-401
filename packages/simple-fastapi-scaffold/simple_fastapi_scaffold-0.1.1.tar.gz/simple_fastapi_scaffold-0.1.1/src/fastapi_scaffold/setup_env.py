"""环境配置工具 - 帮助用户配置 PATH"""
import os
import sys
import site
import click


def get_bin_dir():
    """获取脚本安装目录"""
    return os.path.join(site.USER_BASE, "bin")


def get_shell_profile():
    """检测并返回 shell 配置文件路径"""
    shell = os.environ.get("SHELL", "")
    home = os.path.expanduser("~")

    if "zsh" in shell:
        return os.path.join(home, ".zshrc"), "zsh"
    elif "bash" in shell:
        return os.path.join(home, ".bashrc"), "bash"
    else:
        return os.path.join(home, ".profile"), "profile"


def add_path_to_profile(profile_path, bin_dir):
    """添加 PATH 到 shell 配置文件"""
    marker_start = "# >>> simple-fastapi-scaffold >>>"
    marker_end = "# <<< simple-fastapi-scaffold <<<"

    # 检查是否已经添加
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            content = f.read()
            if marker_start in content:
                return False, "已配置"

    # 添加 PATH 配置
    with open(profile_path, "a", encoding="utf-8") as f:
        f.write(f"\n{marker_start}\n")
        f.write(f'# Added by simple-fastapi-scaffold\n')
        f.write(f'export PATH="{bin_dir}:$PATH"\n')
        f.write(f"{marker_end}\n")
    return True, "已添加"


def check_path():
    """检查 PATH 是否已配置"""
    bin_dir = get_bin_dir()
    path_env = os.environ.get("PATH", "")
    return bin_dir in path_env


@click.command()
@click.option('--yes', '-y', is_flag=True, help='自动确认，不询问')
def main(yes):
    """主函数"""
    bin_dir = get_bin_dir()
    profile_path, shell_name = get_shell_profile()

    click.echo(f"Shell 类型: {shell_name}")
    click.echo(f"配置文件: {profile_path}")
    click.echo(f"脚本目录: {bin_dir}")
    click.echo("")

    # 检查 PATH
    if check_path():
        click.echo("✓ PATH 已配置，可以直接使用命令！")
        click.echo("")
        click.echo("现在可以使用:")
        click.echo("  simple-fastapi-scaffold init <项目名>")
        click.echo("  fasc init <项目名>")
        return

    click.echo("⚠ PATH 未配置")
    click.echo("")

    should_add = yes or click.confirm(f"是否自动添加到 {profile_path}?")

    if should_add:
        added, msg = add_path_to_profile(profile_path, bin_dir)

        if added:
            click.echo(f"✓ {msg}到 {profile_path}")
            click.echo("")
            click.echo("请运行以下命令使配置生效：")
            click.echo(f"  source {profile_path}")
            click.echo("")
            click.echo("或者重启终端")
        else:
            click.echo(f"✓ {msg}")
    else:
        click.echo("")
        click.echo("请手动添加以下内容到你的 shell 配置文件：")
        click.echo(f'  export PATH="{bin_dir}:$PATH"')


if __name__ == "__main__":
    main()
