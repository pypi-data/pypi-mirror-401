# FastAPI Scaffold

> FastAPI 后端项目脚手架 - 一键生成企业级后端架构

## 功能特点

- ⚡️ 一键初始化完整的 FastAPI 后端项目
- 🎯 内置用户认证、JWT Token、数据库 ORM
- 📦 开箱即用的项目结构
- 🔧 自动生成 Model、Schema、Router
- 📝 完善的日志系统
- 🚀 异步支持 (async/await)

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install simple-fastapi-scaffold
```

### 配置 PATH

安装后，如果命令找不到，需要配置 PATH：

**自动配置（推荐）：**

```bash
simple-fastapi-scaffold-setup
```

**手动配置：**

将以下内容添加到 `~/.zshrc`（zsh）或 `~/.bashrc`（bash）：

```bash
export PATH="$HOME/.local/bin:$PATH"  # Linux
# 或
export PATH="$HOME/Library/Python/3.X/bin:$PATH"  # macOS
```

然后运行 `source ~/.zshrc` 或 `source ~/.bashrc` 使配置生效。

### 从源码安装

```bash
git clone https://github.com/yourusername/simple-fastapi-scaffold.git
cd simple-fastapi-scaffold
pip install -e .
```

### 本地使用（无需安装）

```bash
cd simple-fastapi-scaffold
./fasc init my-project
```

## 快速开始

### 1. 初始化新项目

```bash
# 创建项目
simple-fastapi-scaffold init my-backend

# 或使用简短命令
fasc init my-backend
```

### 2. 进入项目目录

```bash
cd my-backend
```

### 3. 安装依赖

```bash
uv sync
```

### 4. 初始化数据库

```bash
uv run python init_db.py
```

### 5. 启动开发服务器

```bash
uv run uvicorn main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档

## 命令

### 初始化项目

```bash
simple-fastapi-scaffold init <项目名> [选项]

选项:
  -d, --description TEXT  项目描述
  -a, --author TEXT       作者名称
  -f, --force            强制覆盖已存在的目录
```

示例:

```bash
simple-fastapi-scaffold init my-api --description "我的后端 API"
simple-fastapi-scaffold init my-api -f  # 强制覆盖
```

### 添加新模块

在已存在的项目中添加新模块:

```bash
cd my-backend
simple-fastapi-scaffold add <模块名> [选项]

选项:
  -c, --class-name TEXT  类名（默认自动生成）
  -t, --table-name TEXT  表名（默认自动生成）
```

示例:

```bash
simple-fastapi-scaffold add article
simple-fastapi-scaffold add product --class-name Product
```

## 生成的项目结构

```
backend/
├── common/                    # 公共模块
│   ├── entity/               # 实体和响应
│   │   ├── base_response.py  # 基础响应模型
│   │   └── schemas/          # Schema 定义
│   ├── middlewares/          # 中间件
│   │   └── log_middleware.py # 日志中间件
│   ├── orm/                  # 数据库 ORM
│   │   ├── db.py            # 数据库连接
│   │   └── base_model.py    # 基础模型
│   ├── base_router.py        # 基础路由
│   ├── config.py             # 配置管理
│   ├── context.py            # 请求上下文
│   ├── logger.py             # 日志系统
│   └── utils.py              # 工具函数
├── models/                    # 数据模型
│   └── user.py               # 用户模型
├── router/                    # 路由
│   └── user.py               # 用户路由
├── logs/                      # 日志目录
├── main.py                    # 应用入口
├── init_db.py                 # 数据库初始化
├── .env                       # 环境变量
├── pyproject.toml            # 项目配置
└── README.md                  # 项目说明
```

## 生成的功能

### 内置功能

- ✅ 用户注册/登录
- ✅ JWT Token 认证
- ✅ 密码加密 (bcrypt)
- ✅ 请求日志记录
- ✅ 异步数据库操作
- ✅ 分页查询
- ✅ 统一响应格式
- ✅ 错误处理

### API 接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/user/login` | 用户登录 | 否 |
| POST | `/api/v1/user` | 创建用户 | 否 |
| GET | `/api/v1/user/list` | 用户列表 | 是 |
| GET | `/api/v1/user/{id}` | 用户详情 | 是 |
| PUT | `/api/v1/user/{id}` | 更新用户 | 是 |
| DELETE | `/api/v1/user/{id}` | 删除用户 | 是 |

## 测试账号

初始化后自动创建测试账号:

- 用户名: `admin`
- 密码: `admin123`

## 技术栈

- **FastAPI** - 现代化 Web 框架
- **SQLAlchemy 2.0** - 异步 ORM
- **Pydantic** - 数据验证
- **JWT** - 身份认证
- **bcrypt** - 密码加密
- **uvicorn** - ASGI 服务器
- **aiosqlite** - 异步 SQLite (可替换为 PostgreSQL/MySQL)

## 开发

### 添加新模块

在项目中添加新模块 (如 `article`):

```bash
cd my-backend
simple-fastapi-scaffold add article
```

这会生成:
- `models/article.py` - 模型
- `common/entity/schemas/article.py` - Schema
- `router/article.py` - 路由

然后在 `main.py` 中注册路由:

```python
from router import article_router

app.include_router(article_router)
```

### 修改模板

脚手架使用 Jinja2 模板，可以根据需要自定义:

```bash
# 模板位置
fastapi_scaffold/templates/
├── main.py.jinja2
├── models/
├── router/
└── ...
```

## 配置

环境变量 (`.env`):

```bash
# 应用配置
APP_NAME=FastAPI App
DEBUG=true

# 数据库配置
DB_URL=sqlite+aiosqlite:///./app.db

# JWT 配置
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

## 卸载

```bash
pip uninstall simple-fastapi-scaffold
```

如果之前配置了 PATH，可以手动从 `~/.zshrc` 或 `~/.bashrc` 中删除：

```bash
# 删除以下内容
# >>> simple-fastapi-scaffold >>>
export PATH="..."
# <<< simple-fastapi-scaffold <<<
```

## 常见问题

### 如何切换数据库?

修改 `.env` 中的 `DB_URL`:

```bash
# PostgreSQL
DB_URL=postgresql+asyncpg://user:password@localhost/dbname

# MySQL
DB_URL=mysql+aiomysql://user:password@localhost/dbname
```

### 如何禁用认证?

在路由中使用 `NO_AUTH`:

```python
from common.base_router import NO_AUTH

@router.get("/public", dependencies=NO_AUTH)
async def public_endpoint():
    return {"message": "public"}
```

### 添加自定义中间件?

在 `main.py` 中添加:

```python
app.add_middleware(MyCustomMiddleware)
```

## 许可证

MIT License
