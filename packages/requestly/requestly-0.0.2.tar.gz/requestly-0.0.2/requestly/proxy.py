#!/usr/bin/env python3
"""
mitmproxy macOS 本地转发工具 (v1.6 状态检测修复版)
修复: status 命令误将系统证书识别为用户残留的问题
"""

import json
import click
import subprocess
import shutil
import asyncio
import logging
from pathlib import Path
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import List, Optional

from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.certs import CertStore


# ==========================
# 1. 数据结构与配置类 (保持不变)
# ==========================
@dataclass
class ForwardRule:
    original_host: str
    original_path: str
    target_scheme: str
    target_host: str
    target_port: int
    description: str


class ProxyConfig:
    def __init__(self, config_path):
        self.config_path = config_path
        self.local_scheme = "http"
        self.local_host = "127.0.0.1"
        self.local_port = 8080
        self.rules: List[ForwardRule] = []
        self.load_config()

    def load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        if "local_server" in config:
            ls = config["local_server"]
            self.local_scheme = ls.get("scheme", "http")
            self.local_host = ls.get("host", "127.0.0.1")
            self.local_port = int(ls.get("port", 8080))

        if "rules" not in config:
            raise ValueError('配置文件缺少 "rules" 字段')

        parsed_rules = []
        for rule in config["rules"]:
            remote_url = rule.get("remote")
            if not remote_url:
                continue

            parsed = urlparse(remote_url)
            path = parsed.path if parsed.path else "/"

            local = rule.get("local", {})
            target_scheme = local.get("scheme", self.local_scheme)
            target_host = local.get("host", self.local_host)
            target_port = int(local.get("port", self.local_port))

            parsed_rules.append(
                ForwardRule(
                    original_host=parsed.netloc,
                    original_path=path,
                    target_scheme=target_scheme,
                    target_host=target_host,
                    target_port=target_port,
                    description=rule.get("description", ""),
                )
            )

        self.rules = sorted(parsed_rules, key=lambda r: len(r.original_path), reverse=True)


# ==========================
# 2. Mitmproxy 插件逻辑 (保持不变)
# ==========================
class ProxyAddon:
    def __init__(self, config: ProxyConfig):
        self.config = config

    def running(self):
        logging.info(f"代理服务已就绪，已加载 {len(self.config.rules)} 条转发规则")

    def request(self, flow: http.HTTPFlow) -> None:
        matched_rule: Optional[ForwardRule] = None
        for rule in self.config.rules:
            if flow.request.host == rule.original_host:
                if flow.request.path.startswith(rule.original_path):
                    matched_rule = rule
                    break

        if not matched_rule:
            return

        flow.metadata["forwarded"] = True

        if flow.request.method == "OPTIONS":
            self._handle_cors_preflight(flow)
            return

        original_url = flow.request.url
        flow.request.scheme = matched_rule.target_scheme
        flow.request.host = matched_rule.target_host
        flow.request.port = matched_rule.target_port

        target_url = (
            f"{matched_rule.target_scheme}://{matched_rule.target_host}:{matched_rule.target_port}{flow.request.path}"
        )
        logging.info(f"⚡ 转发: {original_url}\n       -> {target_url}")

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.metadata.get("forwarded"):
            self._add_cors_headers(flow.response, flow.request)

    def _handle_cors_preflight(self, flow: http.HTTPFlow):
        origin = flow.request.headers.get("Origin", "*")
        req_headers = flow.request.headers.get("Access-Control-Request-Headers", "*")
        flow.response = http.Response.make(
            200,
            b"",
            {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH",
                "Access-Control-Allow-Headers": req_headers,
                "Access-Control-Allow-Credentials": "true",
            },
        )
        logging.info(f"🛡️ CORS 预检放行: {flow.request.url}")

    def _add_cors_headers(self, response: http.Response, request: http.Request):
        origin = request.headers.get("Origin", "*")
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"


# ==========================
# 3. 证书管理逻辑 (修复核心)
# ==========================
def get_cert_path():
    return Path.home() / ".mitmproxy" / "mitmproxy-ca-cert.pem"


def check_cert_installed():
    return get_cert_path().exists()


def get_login_keychain_path():
    """获取用户登录钥匙串的具体路径"""
    # 优先检测 .keychain-db (macOS Sierra 及以后)
    p = Path.home() / "Library/Keychains/login.keychain-db"
    if p.exists():
        return str(p)
    # 兼容旧版
    p = Path.home() / "Library/Keychains/login.keychain"
    if p.exists():
        return str(p)
    return None


def check_system_keychain_status():
    """检测系统钥匙串"""
    cmd = ["security", "find-certificate", "-c", "mitmproxy", "/Library/Keychains/System.keychain"]
    res = subprocess.run(cmd, capture_output=True)
    return res.returncode == 0


def check_login_keychain_status():
    """检测用户登录钥匙串 (精确路径)"""
    login_kc = get_login_keychain_path()
    if not login_kc:
        return False

    # 显式指定 login keychain，防止误报系统证书
    cmd = ["security", "find-certificate", "-c", "mitmproxy", login_kc]
    res = subprocess.run(cmd, capture_output=True)
    return res.returncode == 0


def generate_cert_if_needed():
    cert_path = get_cert_path()
    if cert_path.exists():
        return True

    click.echo("正在生成证书...")
    cert_dir = cert_path.parent
    cert_dir.mkdir(parents=True, exist_ok=True)
    try:
        CertStore.from_store(path=str(cert_dir), basename="mitmproxy", key_size=2048)
        return True
    except Exception as e:
        click.echo(click.style(f"✗ 证书生成失败: {e}", fg="red"))
        return False


def clean_login_keychain():
    """精确清理用户钥匙串"""
    login_kc = get_login_keychain_path()
    if not login_kc:
        return 0

    count = 0
    while True:
        # 显式指定路径进行删除
        cmd = ["security", "delete-certificate", "-c", "mitmproxy", login_kc]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode != 0:
            break
        count += 1
    return count


def uninstall_cert_macos():
    click.echo("正在清理系统证书 (可能需要输入 sudo 密码)...")
    cleaned_count = 0

    # 清理系统
    while True:
        cmd = ["sudo", "security", "delete-certificate", "-c", "mitmproxy", "/Library/Keychains/System.keychain"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            break
        cleaned_count += 1

    # 清理用户
    count_login = clean_login_keychain()
    cleaned_count += count_login

    if cleaned_count > 0:
        click.echo(click.style(f"✓ 已移除 {cleaned_count} 个旧证书", fg="green"))
    else:
        click.echo("✓ 未发现旧证书")
    return True


def install_cert_macos(cert_path):
    # 预清理用户钥匙串，防止混淆
    clean_login_keychain()

    cmd = [
        "sudo",
        "security",
        "add-trusted-cert",
        "-d",
        "-r",
        "trustRoot",
        "-k",
        "/Library/Keychains/System.keychain",
        str(cert_path),
    ]

    try:
        click.echo("🔑 请输入 sudo 密码以信任证书:")
        subprocess.run(cmd, check=True)
        click.echo(click.style("✓ 证书已安装并信任", fg="green"))
        return True
    except subprocess.CalledProcessError:
        click.echo(click.style("✗ 证书安装失败", fg="red"))
        return False


# ==========================
# 4. CLI 命令行入口
# ==========================
@click.group()
def cli():
    """mitmproxy macOS 本地转发工具"""
    pass


@cli.command()
def status():
    """检查: 查看证书安装状态"""
    click.echo(click.style("\n🔍 证书状态检查", bold=True))
    click.echo("-" * 40)

    p = get_cert_path()
    if p.exists():
        click.echo(f"1. 本地文件: {click.style('✓ 已存在', fg='green')}")
        click.echo(f"   路径: {p}")
    else:
        click.echo(f"1. 本地文件: {click.style('✗ 未找到', fg='red')}")

    is_trusted = check_system_keychain_status()
    if is_trusted:
        click.echo(f"2. 系统信任: {click.style('✓ 已安装 (System Keychain)', fg='green')}")
    else:
        click.echo(f"2. 系统信任: {click.style('✗ 未安装', fg='red')}")

    has_residue = check_login_keychain_status()
    if has_residue:
        if is_trusted:
            click.echo(f"3. 用户残留: {click.style('⚠ 存在冗余副本 (Login Keychain)', fg='yellow')}")
            if click.confirm("👉 是否自动删除冗余副本?", default=True):
                count = clean_login_keychain()
                click.echo(click.style(f"✓ 已清理 {count} 个残留证书", fg="green"))
        else:
            click.echo(
                f"3. 用户安装: {click.style('⚠ 存在于用户钥匙串 (建议使用 install-cert 安装到系统)', fg='yellow')}"
            )
    else:
        click.echo(f"3. 用户残留: {click.style('✓ 无', fg='green')}")

    click.echo("-" * 40)

    if p.exists() and is_trusted and not has_residue:
        click.echo(click.style("✨ 状态完美: 证书配置正常，可直接启动代理。", fg="green"))
    elif not p.exists():
        click.echo("建议运行: python proxy.py install-cert --auto")
    elif not is_trusted:
        click.echo("文件存在但未信任，建议运行: python proxy.py install-cert --auto")
    click.echo("")


@cli.command()
@click.option("--auto", is_flag=True, help="自动安装证书到系统信任列表")
def install_cert(auto):
    """管理: 安装 CA 证书"""
    if check_cert_installed():
        click.echo("检测到本地已有证书文件。")
        if not auto and click.confirm("是否删除旧证书并重新生成？(推荐)", default=False):
            remove_cert.callback(force=True)

    if not generate_cert_if_needed():
        return

    cert_path = get_cert_path()
    click.echo(f"证书路径: {cert_path}")

    if auto:
        install_cert_macos(cert_path)
    else:
        click.echo("\n手动安装: 双击 .pem 文件并在钥匙串中设置为'始终信任'")


@cli.command()
@click.option("--force", "-f", is_flag=True, help="不询问直接删除")
def remove_cert(force):
    """管理: 移除证书"""
    if not force:
        click.echo(click.style("⚠ 警告: 这将删除本地证书文件并从系统中彻底移除信任。", fg="yellow"))
        if not click.confirm("确定要继续吗?"):
            return

    uninstall_cert_macos()
    cert_dir = get_cert_path().parent
    if cert_dir.exists():
        try:
            shutil.rmtree(cert_dir)
            click.echo(click.style(f"✓ 本地证书文件已删除", fg="green"))
        except Exception as e:
            click.echo(click.style(f"✗ 删除文件失败: {e}", fg="red"))
    else:
        click.echo("本地证书文件已清除")


@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--port", default=8888, help="代理监听端口")
@click.option("--host", default="127.0.0.1", help="代理监听地址")
@click.option("--verbose", "-v", is_flag=True, help="显示所有抓包详情")
def start(config_file, port, host, verbose):
    """启动: 运行代理服务"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%H:%M:%S", force=True)

    file_exists = check_cert_installed()
    sys_trusted = check_system_keychain_status()

    if not file_exists or not sys_trusted:
        click.echo(click.style("\n⚠ 证书配置不完整！", fg="red", bold=True))
        if not file_exists:
            click.echo("  - 本地证书文件丢失")
        if not sys_trusted:
            click.echo("  - 证书未添加到系统信任区")

        if click.confirm(click.style("👉 是否现在修复(自动安装)?", fg="green"), default=True):
            if generate_cert_if_needed():
                if install_cert_macos(get_cert_path()):
                    click.echo("修复完成，继续启动...")
                else:
                    return
            else:
                return
        else:
            click.echo("⚠ 将以无证书模式启动 (仅 HTTP)")

    try:
        config = ProxyConfig(config_file)
    except Exception as e:
        click.echo(click.style(f"配置加载失败: {e}", fg="red"))
        return

    click.echo(click.style(f"\n🚀 代理启动: {host}:{port}", fg="green", bold=True))
    click.echo("-" * 60)
    for rule in config.rules:
        click.echo(f"Forward: {rule.original_host}{rule.original_path}")
        click.echo(f"     ->  {rule.target_scheme}://{rule.target_host}:{rule.target_port}")
    click.echo("-" * 60 + "\n")

    addon = ProxyAddon(config)

    async def run():
        opts = options.Options(listen_host=host, listen_port=port, confdir=str(Path.home() / ".mitmproxy"))
        master = DumpMaster(opts, with_termlog=True, with_dumper=verbose)
        master.addons.add(addon)
        try:
            await master.run()
        except KeyboardInterrupt:
            pass
        finally:
            master.shutdown()

    asyncio.run(run())


if __name__ == "__main__":
    cli()
