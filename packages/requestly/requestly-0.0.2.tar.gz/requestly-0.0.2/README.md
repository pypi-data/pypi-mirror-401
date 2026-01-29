# requestly macOS 本地转发工具 - 完整使用指南

## 📋 功能特性

✅ 将远程 API 请求自动转发到本地开发服务器  
✅ 支持 HTTPS/HTTP 协议  
✅ 纯 Python 实现，无需外部命令  
✅ 一键自动安装/重装证书  
✅ 灵活的配置文件支持  
✅ 实时转发日志显示  
✅ 专为 macOS 优化  

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install mitmproxy click
```

### 2. 创建配置文件

创建 `config.json`:

```json
{
    "local_server": {
        "scheme": "http",
        "host": "127.0.0.1",
        "port": 8080
    },
    "rules": [
        {
            "description": "财务系统API",
            "remote": "https://sit-finance.xtt.xyz/settle/admin/settleBillRule/page"
        },
        {
            "description": "用户服务API - 自定义端口",
            "remote": "https://api.example.com/api/v1/users",
            "local": {
                "port": 3000
            }
        },
        {
            "description": "产品服务API - 完全自定义",
            "remote": "https://api.example.com/api/v1/products",
            "local": {
                "scheme": "https",
                "host": "localhost",
                "port": 3001
            }
        }
    ]
}
```

**配置字段说明:**

- **local_server** (必填): 默认本地服务器配置
  - `scheme`: 协议 (http/https)，默认 `http`
  - `host`: 地址，默认 `127.0.0.1`
  - `port`: 端口，默认 `8080`

- **rules** (必填): 转发规则数组
  - `description`: 规则描述（可选，推荐填写，方便管理）
  - `remote`: 远程 URL（必填）
  - `local`: 本地目标配置（可选）
    - 如果不配置，使用 `local_server` 的配置
    - 可以只覆盖部分字段（如只改端口）
    - 支持 `scheme`、`host`、`port` 三个字段

**配置优势:**

✅ 语义清晰：`local_server` vs `remote`  
✅ 层次分明：本地配置嵌套在 `local` 对象中  
✅ 可读性强：`rules` 准确描述转发规则  
✅ 支持注释：`description` 字段便于团队协作  
✅ 灵活覆盖：可只覆盖需要的字段

### 3. 安装证书

```bash
# 自动安装（推荐）
python mitm_proxy.py install-cert --auto

# 仅查看安装说明
python mitm_proxy.py install-cert
```

### 4. 启动代理

```bash
# 基本启动
python mitm_proxy.py start config.json

# 自定义端口
python mitm_proxy.py start config.json --listen-port 9999

# 显示详细日志
python mitm_proxy.py start config.json -v
```
