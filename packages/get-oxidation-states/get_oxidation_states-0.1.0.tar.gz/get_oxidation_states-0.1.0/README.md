# get-oxidation-states

符合MCP（Model Context Protocol）协议的元素氧化态查询服务器，提供`get_oxidation_states`工具，用于查询化学元素的常见氧化态及稳定性。

## 特性
- 严格遵循MCP协议规范，兼容Anthropic官方MCP Python SDK
- 类型安全实现，完善的参数验证和错误处理
- 支持常见化学元素氧化态查询，包含稳定性标注
- 基于uv的环境管理，支持PyPI发布
- 提供完整测试用例和使用示例

## 开发环境
- Python 3.11+
- uv（推荐）或pip

## 安装
### 使用uv（推荐）
```bash
# 从PyPI安装
uv add get-oxidation-states

# 本地开发安装
git clone <项目仓库地址>
cd get-oxidation-states
uv install .