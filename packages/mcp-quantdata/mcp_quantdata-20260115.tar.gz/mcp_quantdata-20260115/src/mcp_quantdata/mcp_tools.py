import os
from datetime import date
from typing import List
from vxutils import to_datetime
from vxsched import APP
from mcp.server.fastmcp import FastMCP

MCP_SERVER = FastMCP(name="mcp_quantdata")


@MCP_SERVER.resource("env")
def env() -> dict:
    f"""返回当前环境参数设置,当前日期、环境、数据库名称
    
    Returns:
        dict: 环境参数设置
        {"TODAY": '2025-01-01', # 当前日期
            "ENV": "prod", # 环境,prod 是生产环境,dev 是开发环境
            "DB": "quantdata", # 数据库名称
        }
    """
    return {
        "TODAY": date.today().strftime("%Y-%m-%d"),  # 当前日期
        "ENV": os.getenv(
            "QUANTDATA_ENV", "prod"
        ),  # 环境,prod 是生产环境,dev 是开发环境
        "DB": "quantdata",  # 数据库名称
    }


@MCP_SERVER.resource("calendar")
def calendar(start: str, end: str) -> List[date]:
    start = to_datetime(start).date()
    end = to_datetime(end).date()


def main() -> None:
    MCP_SERVER.run(transport="stdio")
