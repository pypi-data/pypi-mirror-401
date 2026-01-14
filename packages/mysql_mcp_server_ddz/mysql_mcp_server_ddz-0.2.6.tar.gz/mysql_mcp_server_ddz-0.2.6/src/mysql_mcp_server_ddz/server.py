"""MySQL MCP Server 基于 FastMCP 的实现。

这个模块使用 FastMCP 框架，将 MySQL 暴露为 MCP 服务器：

- 使用 `FastMCP` 管理所有 MCP 端点（工具 / 资源）
- 通过环境变量读取 MySQL 连接配置
- 提供：
  - 列出所有表的资源：`mysql://tables`
  - 读取单表数据的资源：`mysql://{table}/data`
  - 通用 SQL 执行工具：`execute_sql`

你可以把这个文件理解为“三层结构”：
1. 基础设施：日志、数据库配置读取
2. 资源定义：只读的数据访问
3. 工具定义：可以执行任意 SQL 的能力
"""

import logging
import os

from dotenv import load_dotenv
from fastmcp import FastMCP
from mysql.connector import Error, connect

# 加载 .env 文件中的环境变量
load_dotenv()

# ----------------------------
# 日志配置
# ----------------------------
# 这里使用 Python 内置 logging，输出到 stderr，方便在 MCP 客户端或命令行中调试。
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mysql_mcp_server_ddz")


def get_db_config() -> dict:
    """从环境变量中读取 MySQL 数据库配置。

    设计要点：
    - 使用环境变量而不是硬编码，便于在不同环境（本地/服务器/容器）下切换
    - 保留 charset / collation / sql_mode 配置，兼容不同版本 MySQL
    - 如果缺少关键配置（用户、密码、数据库），主动抛出异常，避免“默默失败”
    """

    # 这里用一个字典统一收集配置，类型声明 dict[str, object] 方便静态检查
    config: dict[str, object] = {
        # 主机名：缺省为 localhost
        "host": os.getenv("MYSQL_HOST", "localhost"),
        # 端口：从环境变量取出后转换为 int
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        # 用户名 / 密码 / 数据库名 都是必填
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),
        # 以下是可选参数，主要是字符集 / 排序规则 等兼容性设置
        "charset": os.getenv("MYSQL_CHARSET", "utf8mb4"),
        "collation": os.getenv("MYSQL_COLLATION", "utf8mb4_unicode_ci"),
        # autocommit=True：方便在工具执行非查询语句时自动提交
        "autocommit": True,
        # SQL 模式：默认使用 TRADITIONAL，你可以通过环境变量覆盖
        "sql_mode": os.getenv("MYSQL_SQL_MODE", "TRADITIONAL"),
    }

    # 去掉值为 None 的键，让 mysql-connector 使用自己的默认值
    config = {k: v for k, v in config.items() if v is not None}

    # 核心安全检查：必须存在用户、密码、数据库名
    if not all([config.get("user"), config.get("password"), config.get("database")]):
        logger.error(
            "Missing required database configuration. Please check environment variables:"
        )
        logger.error(
            "MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE are required")
        raise ValueError("Missing required database configuration")

    return config


# ----------------------------
# FastMCP 应用实例
# ----------------------------
# FastMCP 是整个 MCP Server 的“容器”，所有工具和资源都是挂在这个实例上的。
app = FastMCP(name="mysql_mcp_server_ddz")


# ----------------------------
# 资源（Resources）定义
# ----------------------------
# 资源是只读的数据入口，客户端通过 URI 访问。
# 这里我们定义了两个资源：
# 1. mysql://tables            —— 返回所有表名的列表
# 2. mysql://{table}/data      —— 返回某个表的前 100 行数据（CSV 格式）

@app.resource("mysql://tables")
def list_tables() -> list[str]:
    """列出当前数据库下的所有表。

    返回值是一个字符串列表，每个元素是一个表名，方便在 MCP 客户端中浏览。
    """

    logger.info("Listing MySQL tables...")
    tables = _get_all_tables()
    logger.info("Found tables: %s", tables)
    return tables

# ----------------------------
# 资源（Resources）定义
# ----------------------------
# 1. mysql://{table}/data      —— 返回指定表的前 100 行数据（CSV 格式）

@app.resource("mysql://{table}/data")
def read_table_data(table: str) -> str:
    """读取指定表的前 100 行数据，并以 CSV 文本返回。

    - URI 模板：mysql://{table}/data
    - 客户端访问时，例如请求 mysql://users/data，就会把 table="users" 传进来
    - 返回的字符串第一行是列名，后面每行一条记录，用逗号分隔
    """

    config = get_db_config()
    logger.info("Reading data for table resource: %s", table)
    try:
        with connect(**config) as conn:
            logger.info("Connected to MySQL server version: %s",
                        conn.get_server_info())
            with conn.cursor() as cursor:
                # 这里简单使用 SELECT * LIMIT 100，方便快速浏览数据结构
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
    except Error as e:  # pragma: no cover - 同样依赖真实数据库
        logger.error(
            "Database error reading resource for table %s: %s", table, e
        )
        logger.error(
            "Error code: %s, SQL state: %s",
            getattr(e, "errno", None),
            getattr(e, "sqlstate", None),
        )
        raise RuntimeError(f"Database error reading table {table}: {e}") from e

    # 将查询结果转成简单的 CSV 文本：第一行是表头，后面是数据
    result_lines = [",".join(columns)]
    result_lines.extend(",".join(map(str, row)) for row in rows)
    return "\n".join(result_lines)


# ----------------------------
# 内部函数：获取所有表名
# ----------------------------
# 通过执行 SQL 语句获取所有表名

def _get_all_tables() -> list[str]:
    """内部函数：获取数据库中所有表名。

    这个函数被多个资源共用，避免重复代码。
    """
    config = get_db_config()
    try:
        with connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                return tables
    except Error as e:
        logger.error("Failed to get tables: %s", e)
        raise RuntimeError(f"Failed to get tables: {e}") from e


# ----------------------------
# 内部函数：动态资源列表
# ----------------------------
# 为数据库中的每个表创建独立的资源
# 在服务器启动时动态注册所有表为独立的资源

def _create_table_resource(table_name: str):
    """为指定的表创建资源读取函数。

    这个函数使用闭包来为每个表创建一个独立的资源处理函数。
    每个表都会有自己的资源 URI：mysql://table/{表名}
    """
    def read_table() -> str:
        f"""读取表 {table_name} 的数据。
        
        返回该表的前 100 行数据，CSV 格式。
        """
        config = get_db_config()
        logger.info(f"Reading table resource: {table_name}")

        try:
            with connect(**config) as conn:
                with conn.cursor() as cursor:
                    # 查询表数据
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()

                    # 转换为CSV格式
                    result_lines = [",".join(columns)]
                    result_lines.extend(",".join(map(str, row))
                                        for row in rows)

                    logger.info(
                        f"Retrieved {len(rows)} rows from table {table_name}")
                    return "\n".join(result_lines)
        except Error as e:
            logger.error(f"Database error reading table {table_name}: {e}")
            raise RuntimeError(
                f"Database error reading table {table_name}: {e}") from e

    return read_table

# ----------------------------
# 动态注册表资源
# ----------------------------
# 在服务器启动时动态注册所有表为独立的资源

def register_table_resources():
    """动态注册所有表为资源。

    这个函数会：
    1. 查询数据库中的所有表
    2. 为每个表注册一个独立的资源
    3. 资源URI格式：mysql://table/{表名}
    """
    logger.info("Registering table resources...")

    try:
        tables = _get_all_tables()
        logger.info(f"Found {len(tables)} tables, registering as resources...")

        for table in tables:
            # 为每个表创建资源处理函数
            resource_func = _create_table_resource(table)
            # 设置函数的文档字符串
            resource_func.__doc__ = f"Data from MySQL table '{table}'"
            # 注册资源
            app.resource(f"mysql://table/{table}")(resource_func)
            logger.info(f"Registered resource: mysql://table/{table}")

        logger.info(f"Successfully registered {len(tables)} table resources")
    except Exception as e:
        logger.error(f"Error registering table resources: {e}")
        # 不抛出异常，允许服务器继续运行


# ----------------------------
# 工具（Tool）定义
# ----------------------------
# 工具可以被 LLM / 客户端主动调用，适合执行“动作类”的操作。
# FastMCP 会自动根据函数签名生成参数 Schema，docstring 会作为工具说明展示在客户端中。


@app.tool
def execute_sql(query: str) -> str:
    """在当前 MySQL 数据库上执行一条 SQL 语句。

    行为说明：
    - 对于 `SHOW TABLES`：返回表名列表（第一行为 "Tables_in_数据库名"）
    - 对于返回结果集的查询（SELECT / SHOW / DESCRIBE 等）：
    - 第一行是列名，后续为每行数据，全部以 CSV 文本形式返回
    - 对于非查询语句（INSERT / UPDATE / DELETE 等）：
    - 提交事务，并返回受影响行数的文本说明

    注意：本函数不做 SQL 安全校验，生产环境建议限制可执行的语句类型，
    例如只允许 SELECT，或者做白名单过滤。
    """

    config = get_db_config()
    logger.info("Executing SQL query: %s", query)

    try:
        with connect(**config) as conn:
            logger.info("Connected to MySQL server version: %s",
                        conn.get_server_info())
            with conn.cursor() as cursor:
                cursor.execute(query)

                # 标准化 SQL 文本，便于进行前缀判断
                upper_query = query.strip().upper()

                # 特殊处理：SHOW TABLES，保持与原实现的兼容输出
                if upper_query.startswith("SHOW TABLES"):
                    tables = cursor.fetchall()
                    result = [f"Tables_in_{config['database']}"]
                    result.extend(row[0] for row in tables)
                    return "\n".join(result)

                # 如果 cursor.description 不为 None，说明这是一个返回结果集的查询
                if cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    result_lines = [",".join(columns)]
                    result_lines.extend(",".join(map(str, row))
                                        for row in rows)
                    return "\n".join(result_lines)

                # 否则认为是非 SELECT 类型语句，需要提交事务
                conn.commit()
                return f"Query executed successfully. Rows affected: {cursor.rowcount}"
    except Error as e:  # pragma: no cover - 依赖真实数据库
        logger.error("Error executing SQL '%s': %s", query, e)
        logger.error(
            "Error code: %s, SQL state: %s",
            getattr(e, "errno", None),
            getattr(e, "sqlstate", None),
        )
        raise RuntimeError(f"Error executing query: {e}") from e


# ----------------------------
# 入口函数
# ----------------------------
# 这里提供一个普通的 Python 入口，便于：
# - 开发调试：`python -m mysql_mcp_server_ddz.server`
# - 通过 pyproject.toml 的 [project.scripts] 暴露为 `mysql_mcp_server_ddz` 命令


def main() -> None:
    """启动 FastMCP MySQL MCP Server 的入口函数。"""

    # 提前读取并打印当前数据库配置，方便排查连接问题
    config = get_db_config()
    logger.info("Starting MySQL FastMCP server...")
    logger.info(
        "Database config: %s/%s as %s",
        config.get("host"),
        config.get("database"),
        config.get("user"),
    )

    # 在启动前动态注册所有表资源
    register_table_resources()

    # FastMCP 默认使用 STDIO 作为传输层，适配大多数 MCP 客户端（例如 Claude Desktop）
    app.run()


if __name__ == "__main__":
    # 当直接运行这个模块时，调用 main() 启动 MCP 服务器
    main()
