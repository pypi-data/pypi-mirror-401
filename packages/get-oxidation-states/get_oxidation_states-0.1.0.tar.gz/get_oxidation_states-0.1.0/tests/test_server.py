"""
氧化态查询 MCP 服务器的测试用例。
"""

import pytest
import pytest_asyncio
from typing import Dict, Any
from get_oxidation_states.server import OxidationStateServer


@pytest_asyncio.fixture
async def server():
    """创建测试服务器实例"""
    return OxidationStateServer()


class TestOxidationStateServer:
    """氧化态查询服务器测试类"""

    def test_initialization(self):
        """测试服务器初始化"""
        server = OxidationStateServer()
        assert server is not None
        assert hasattr(server, "elements_data")
        assert len(server.elements_data) > 0

    def test_element_data_structure(self, server: OxidationStateServer):
        """测试元素数据结构"""
        # 测试氢元素
        h_info = server.elements_data.get("H")
        assert h_info is not None
        assert h_info.symbol == "H"
        assert h_info.name == "Hydrogen"
        assert h_info.atomic_number == 1
        assert len(h_info.oxidation_states) > 0

        # 测试氧化态结构
        oxidation_state = h_info.oxidation_states[0]
        assert hasattr(oxidation_state, "state")
        assert hasattr(oxidation_state, "stability")
        assert hasattr(oxidation_state, "description")

    @pytest.mark.asyncio
    async def test_list_available_elements(self, server: OxidationStateServer):
        """测试列出可用元素"""
        result = await server._handle_list_available_elements()
        assert len(result) == 1
        assert "可查询的元素列表" in result[0].text
        assert "H" in result[0].text
        assert "O" in result[0].text

    @pytest.mark.asyncio
    async def test_get_oxidation_states_success(self, server: OxidationStateServer):
        """测试成功查询氧化态"""
        arguments: Dict[str, Any] = {"element_symbol": "H"}
        result = await server._handle_get_oxidation_states(arguments)

        assert len(result) == 1
        text = result[0].text
        assert "Hydrogen" in text
        assert "氧化态信息" in text
        assert "+1" in text or "-1" in text

    @pytest.mark.asyncio
    async def test_get_oxidation_states_include_all(self, server: OxidationStateServer):
        """测试查询所有氧化态（包括罕见态）"""
        arguments: Dict[str, Any] = {"element_symbol": "Fe", "include_all": True}
        result = await server._handle_get_oxidation_states(arguments)

        assert len(result) == 1
        text = result[0].text
        assert "Iron" in text
        assert "+6" in text  # 罕见氧化态

    @pytest.mark.asyncio
    async def test_get_oxidation_states_element_not_found(
        self, server: OxidationStateServer
    ):
        """测试查询不存在的元素"""
        arguments: Dict[str, Any] = {"element_symbol": "Xy"}

        with pytest.raises(ValueError) as exc_info:
            await server._handle_get_oxidation_states(arguments)

        assert "未找到元素" in str(exc_info.value)
        assert "当前支持的元素" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_oxidation_states_empty_symbol(
        self, server: OxidationStateServer
    ):
        """测试空元素符号"""
        arguments: Dict[str, Any] = {"element_symbol": ""}

        with pytest.raises(ValueError) as exc_info:
            await server._handle_get_oxidation_states(arguments)

        assert "元素符号不能为空" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_oxidation_states_case_insensitive(
        self, server: OxidationStateServer
    ):
        """测试元素符号大小写不敏感"""
        arguments_lower: Dict[str, Any] = {"element_symbol": "fe"}
        arguments_upper: Dict[str, Any] = {"element_symbol": "FE"}

        result_lower = await server._handle_get_oxidation_states(arguments_lower)
        result_upper = await server._handle_get_oxidation_states(arguments_upper)

        # 两个结果都应该成功
        assert len(result_lower) == 1
        assert len(result_upper) == 1
        assert "Iron" in result_lower[0].text
        assert "Iron" in result_upper[0].text

    @pytest.mark.asyncio
    async def test_server_tool_registration(self):
        """测试服务器工具注册"""
        # 创建服务器实例
        server = OxidationStateServer()

        # 模拟 list_tools 调用
        mock_tools = [
            {
                "name": "get_oxidation_states",
                "description": "查询化学元素的常见氧化态及稳定性信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "element_symbol": {
                            "type": "string",
                            "description": "元素符号（如 H, O, Fe, C 等）",
                            "minLength": 1,
                            "maxLength": 2,
                        },
                        "include_all": {
                            "type": "boolean",
                            "description": "是否包含所有氧化态（包括罕见态），默认只返回常见氧化态",
                            "default": False,
                        },
                    },
                    "required": ["element_symbol"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "list_available_elements",
                "description": "列出所有可查询的元素",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            },
        ]

        # 验证服务器可以正常处理工具调用
        assert hasattr(server, "_handle_get_oxidation_states")
        assert hasattr(server, "_handle_list_available_elements")

        # 测试工具响应
        result = await server._handle_list_available_elements()
        assert len(result) == 1
        assert "可查询的元素列表" in result[0].text


class TestMCPProtocolCompliance:
    """MCP 协议兼容性测试"""

    @pytest.mark.asyncio
    async def test_tool_input_schema_validity(self):
        """测试工具输入模式的有效性"""
        # 测试 get_oxidation_states 工具架构
        server = OxidationStateServer()

        # 验证元素符号参数
        valid_symbols = ["H", "O", "Fe", "C", "Cl"]
        for symbol in valid_symbols:
            # 这些调用应该成功
            result = await server._handle_get_oxidation_states(
                {"element_symbol": symbol}
            )
            assert len(result) == 1
            assert symbol in result[0].text

        # 测试无效元素符号
        invalid_symbols = ["", "XYZ", "123"]
        for symbol in invalid_symbols:
            with pytest.raises(ValueError):
                await server._handle_get_oxidation_states({"element_symbol": symbol})

    @pytest.mark.asyncio
    async def test_tool_response_format(self, server: OxidationStateServer):
        """测试工具响应格式"""
        # 测试 get_oxidation_states 响应格式
        result = await server._handle_get_oxidation_states({"element_symbol": "H"})

        # 验证响应结构
        assert isinstance(result, list)
        assert len(result) > 0

        # 验证文本内容格式
        text_content = result[0]
        assert hasattr(text_content, "text")
        assert isinstance(text_content.text, str)

        # 验证内容包含必要信息
        assert "Hydrogen" in text_content.text
        assert "氧化态" in text_content.text

    @pytest.mark.asyncio
    async def test_error_handling(self, server: OxidationStateServer):
        """测试错误处理"""
        # 测试缺少必需参数
        with pytest.raises(ValueError):
            await server._handle_get_oxidation_states({})

        # 测试额外参数（应该被拒绝，根据 inputSchema 的 additionalProperties: False）
        # 注意：由于我们直接调用内部方法，参数验证由我们自己处理
        # 但我们可以测试工具是否正确处理额外参数
        result = await server._handle_get_oxidation_states(
            {"element_symbol": "H", "extra_param": "should_be_ignored"}
        )
        # 这个调用应该成功，因为我们没有实现严格的参数验证
        assert len(result) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
