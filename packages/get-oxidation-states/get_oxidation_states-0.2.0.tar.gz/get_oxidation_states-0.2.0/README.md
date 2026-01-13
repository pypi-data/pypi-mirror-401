# Get Oxidation States MCP Server

一个遵循 Model Context Protocol (MCP) 规范的服务器，为大语言模型提供查询化学元素常见氧化态及稳定性的能力。

## 功能特点
- 支持通过元素符号、中文名称、英文名称查询
- 提供氧化态的稳定性说明
- 支持中英文结果输出
- 严格的参数验证和错误处理
- 符合 MCP 协议规范，兼容 Cherry Studio/VS Code 等客户端

## 支持的元素
目前支持以下元素的查询：
- 氢 (H)、氧 (O)、钠 (Na)
- 氯 (Cl)、铁 (Fe)、铜 (Cu)
- 碳 (C)、锌 (Zn)、铝 (Al)

## 安装

### 前置要求
- Python 3.11+
- uv（推荐）或 pip

### 使用 uv（推荐）
```bash
# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 直接运行
uvx get-oxidation-states

# 或安装到项目
uv add get-oxidation-states