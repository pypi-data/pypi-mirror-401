# Time Server MCP

一个使用 MCP (Model Context Protocol) 实现的时间服务器。

## 功能

- 获取当前时间
- 支持指定时区
- 使用 stdio 传输方式运行服务器

## 安装

```bash
pip install time-server-mcp-ver.pcc
```

## 使用

### 启动服务器

```bash
time-server-mcp-ver.pcc
```

### 使用示例

服务器启动后，可以通过 MCP 协议与之通信，调用 `get_current_time` 工具来获取当前时间。

```python
from mcp.client import MCPClient

# 创建客户端实例
client = MCPClient(transport="stdio")

# 调用 get_current_time 工具获取当前时间
result = client.get_current_time()
print(f"当前时间: {result}")

# 调用 get_current_time 工具获取指定时区的当前时间
result = client.get_current_time(timezone="Asia/Shanghai")
print(f"上海时间: {result}")
```

## 依赖

- Python 3.7+
- pytz
- mcp
