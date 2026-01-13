"""
MCP server for querying element oxidation states.

This server provides tools to retrieve common oxidation states of chemical elements
along with their stability information.
"""

import asyncio
import logging
from enum import Enum
from typing import Dict, List, Optional, Any

import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from pydantic import BaseModel, Field

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class StabilityLevel(str, Enum):
    """氧化态稳定性等级枚举"""

    VERY_STABLE = "very_stable"  # 非常稳定，常见氧化态
    STABLE = "stable"  # 稳定，较常见
    UNSTABLE = "unstable"  # 不稳定，较少见
    RARE = "rare"  # 罕见，只在特殊条件下存在
    THEORETICAL = "theoretical"  # 理论存在，实验未证实


class OxidationStateInfo(BaseModel):
    """氧化态信息模型"""

    state: int = Field(..., description="氧化态值（如 +2, -1 等）")
    stability: StabilityLevel = Field(..., description="稳定性等级")
    description: Optional[str] = Field(None, description="氧化态描述或备注")
    examples: Optional[List[str]] = Field(None, description="典型化合物示例")


class ElementInfo(BaseModel):
    """元素信息模型"""

    symbol: str = Field(..., description="元素符号")
    name: str = Field(..., description="元素名称")
    atomic_number: int = Field(..., description="原子序数")
    group: Optional[int] = Field(None, description="周期表中的族")
    period: Optional[int] = Field(None, description="周期表中的周期")
    oxidation_states: List[OxidationStateInfo] = Field(..., description="常见氧化态列表")


class OxidationStateServer:
    """氧化态查询 MCP 服务器"""

    def __init__(self) -> None:
        """初始化服务器和元素数据"""
        self.server = Server("oxidation-states-server")
        self.elements_data = self._initialize_elements_data()
        self._setup_handlers()

    def _initialize_elements_data(self) -> Dict[str, ElementInfo]:
        """初始化元素氧化态数据库

        包含常见元素的氧化态信息，数据基于化学常识整理。
        实际应用中可扩展为从数据库或API获取。
        """
        return {
            "H": ElementInfo(
                symbol="H",
                name="Hydrogen",
                atomic_number=1,
                group=1,
                period=1,
                oxidation_states=[
                    OxidationStateInfo(
                        state=1,
                        stability=StabilityLevel.VERY_STABLE,
                        description="常见氧化态，如 H⁺ 在水中",
                        examples=["HCl", "H₂O", "H₂SO₄"],
                    ),
                    OxidationStateInfo(
                        state=-1,
                        stability=StabilityLevel.STABLE,
                        description="氢化物中的氧化态",
                        examples=["NaH", "CaH₂", "LiAlH₄"],
                    ),
                ],
            ),
            "O": ElementInfo(
                symbol="O",
                name="Oxygen",
                atomic_number=8,
                group=16,
                period=2,
                oxidation_states=[
                    OxidationStateInfo(
                        state=-2,
                        stability=StabilityLevel.VERY_STABLE,
                        description="最常见氧化态，氧化物和水中",
                        examples=["H₂O", "CO₂", "Fe₂O₃"],
                    ),
                    OxidationStateInfo(
                        state=-1,
                        stability=StabilityLevel.STABLE,
                        description="过氧化物",
                        examples=["H₂O₂", "Na₂O₂"],
                    ),
                    OxidationStateInfo(
                        state=0,
                        stability=StabilityLevel.STABLE,
                        description="氧气分子",
                        examples=["O₂", "O₃"],
                    ),
                    OxidationStateInfo(
                        state=2,
                        stability=StabilityLevel.UNSTABLE,
                        description="二氟化氧",
                        examples=["OF₂"],
                    ),
                ],
            ),
            "Fe": ElementInfo(
                symbol="Fe",
                name="Iron",
                atomic_number=26,
                group=8,
                period=4,
                oxidation_states=[
                    OxidationStateInfo(
                        state=2,
                        stability=StabilityLevel.VERY_STABLE,
                        description="亚铁离子",
                        examples=["FeCl₂", "FeSO₄", "FeO"],
                    ),
                    OxidationStateInfo(
                        state=3,
                        stability=StabilityLevel.VERY_STABLE,
                        description="铁离子",
                        examples=["FeCl₃", "Fe₂O₃", "Fe(OH)₃"],
                    ),
                    OxidationStateInfo(
                        state=0,
                        stability=StabilityLevel.STABLE,
                        description="金属铁",
                        examples=["Fe"],
                    ),
                    OxidationStateInfo(
                        state=6,
                        stability=StabilityLevel.RARE,
                        description="高铁酸盐",
                        examples=["K₂FeO₄"],
                    ),
                ],
            ),
            "C": ElementInfo(
                symbol="C",
                name="Carbon",
                atomic_number=6,
                group=14,
                period=2,
                oxidation_states=[
                    OxidationStateInfo(
                        state=4,
                        stability=StabilityLevel.VERY_STABLE,
                        description="有机物和二氧化碳",
                        examples=["CO₂", "CH₄", "CCl₄"],
                    ),
                    OxidationStateInfo(
                        state=2,
                        stability=StabilityLevel.STABLE,
                        description="一氧化碳",
                        examples=["CO"],
                    ),
                    OxidationStateInfo(
                        state=0,
                        stability=StabilityLevel.STABLE,
                        description="单质碳",
                        examples=["C", "Graphite", "Diamond"],
                    ),
                    OxidationStateInfo(
                        state=-4,
                        stability=StabilityLevel.STABLE,
                        description="甲烷等中的碳",
                        examples=["CH₄"],
                    ),
                ],
            ),
            "Cl": ElementInfo(
                symbol="Cl",
                name="Chlorine",
                atomic_number=17,
                group=17,
                period=3,
                oxidation_states=[
                    OxidationStateInfo(
                        state=-1,
                        stability=StabilityLevel.VERY_STABLE,
                        description="氯化物",
                        examples=["NaCl", "HCl", "MgCl₂"],
                    ),
                    OxidationStateInfo(
                        state=1,
                        stability=StabilityLevel.STABLE,
                        description="次氯酸盐",
                        examples=["NaClO", "HClO"],
                    ),
                    OxidationStateInfo(
                        state=3,
                        stability=StabilityLevel.STABLE,
                        description="亚氯酸盐",
                        examples=["NaClO₂"],
                    ),
                    OxidationStateInfo(
                        state=5,
                        stability=StabilityLevel.STABLE,
                        description="氯酸盐",
                        examples=["KClO₃"],
                    ),
                    OxidationStateInfo(
                        state=7,
                        stability=StabilityLevel.STABLE,
                        description="高氯酸盐",
                        examples=["KClO₄", "HClO₄"],
                    ),
                    OxidationStateInfo(
                        state=0,
                        stability=StabilityLevel.STABLE,
                        description="氯气",
                        examples=["Cl₂"],
                    ),
                ],
            ),
        }

    def _setup_handlers(self) -> None:
        """设置 MCP 服务器处理器"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """返回可用工具列表"""
            return [
                types.Tool(
                    name="get_oxidation_states",
                    description="查询化学元素的常见氧化态及稳定性信息",
                    inputSchema={
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
                ),
                types.Tool(
                    name="list_available_elements",
                    description="列出所有可查询的元素",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Optional[Dict[str, Any]] = None
        ) -> List[types.TextContent]:
            """处理工具调用"""

            if arguments is None:
                arguments = {}

            if name == "get_oxidation_states":
                return await self._handle_get_oxidation_states(arguments)
            elif name == "list_available_elements":
                return await self._handle_list_available_elements()
            else:
                raise ValueError(f"未知工具: {name}")

    async def _handle_get_oxidation_states(
        self, arguments: Dict[str, Any]
    ) -> List[types.TextContent]:
        """处理氧化态查询请求"""
        element_symbol = arguments.get("element_symbol", "").strip().title()
        include_all = arguments.get("include_all", False)

        if not element_symbol:
            raise ValueError("元素符号不能为空")

        # 查找元素
        element_info = self.elements_data.get(element_symbol)
        if not element_info:
            available_elements = ", ".join(sorted(self.elements_data.keys()))
            raise ValueError(
                f"未找到元素 '{element_symbol}'。\n"
                f"当前支持的元素: {available_elements}\n"
                f"请使用有效的元素符号。"
            )

        # 过滤氧化态（根据稳定性）
        if include_all:
            oxidation_states = element_info.oxidation_states
        else:
            oxidation_states = [
                state
                for state in element_info.oxidation_states
                if state.stability
                in [StabilityLevel.VERY_STABLE, StabilityLevel.STABLE]
            ]

        # 构建响应
        stability_map = {
            StabilityLevel.VERY_STABLE: "⭐ 非常稳定（常见）",
            StabilityLevel.STABLE: "✓ 稳定（较常见）",
            StabilityLevel.UNSTABLE: "⚠ 不稳定（较少见）",
            StabilityLevel.RARE: "⚡ 罕见（特殊条件）",
            StabilityLevel.THEORETICAL: "🔬 理论存在",
        }

        # 格式化氧化态列表
        states_list = []
        for state_info in sorted(oxidation_states, key=lambda x: x.state, reverse=True):
            sign = "+" if state_info.state > 0 else ""
            state_line = (
                f"  {sign}{state_info.state}: {stability_map[state_info.stability]}"
            )

            if state_info.description:
                state_line += f"\n    描述: {state_info.description}"

            if state_info.examples:
                examples = "、".join(state_info.examples)
                state_line += f"\n    示例: {examples}"

            states_list.append(state_line)

        response_text = (
            f"# {element_info.name} ({element_info.symbol}) 氧化态信息\n\n"
            f"**原子序数**: {element_info.atomic_number}\n"
            f"**周期**: {element_info.period}, **族**: {element_info.group}\n\n"
            f"## 氧化态列表:\n"
        )

        if states_list:
            response_text += "\n".join(states_list)
        else:
            response_text += "\n  未找到符合条件的氧化态。"

        # 添加提示
        if not include_all and len(oxidation_states) > len(states_list):
            response_text += (
                "\n\n**提示**: 使用 `include_all: true` 参数可以查看所有氧化态" "（包括不稳定和罕见的氧化态）。"
            )

        return [types.TextContent(type="text", text=response_text)]

    async def _handle_list_available_elements(self) -> List[types.TextContent]:
        """处理可用元素列表查询"""
        elements_list = []

        for symbol, info in sorted(
            self.elements_data.items(), key=lambda x: x[1].atomic_number
        ):
            element_line = (
                f"{symbol:<3} {info.name:<15} "
                f"原子序数: {info.atomic_number:<3} "
                f"周期: {info.period}, 族: {info.group}"
            )
            elements_list.append(element_line)

        response_text = "# 可查询的元素列表\n\n" "以下元素支持氧化态查询：\n\n"
        response_text += "\n".join(elements_list)
        response_text += (
            f"\n\n**总计**: {len(self.elements_data)} 个元素\n"
            f"**使用**: 调用 `get_oxidation_states` 工具查询具体元素的氧化态。"
        )

        return [types.TextContent(type="text", text=response_text)]


async def main() -> None:
    """MCP 服务器主入口函数"""
    server = OxidationStateServer()

    async with server.server.run_stdio(
        initialization_options=InitializationOptions(
            server_name="oxidation-states-server",
            server_version="1.0.0",
            capabilities=server.server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            ),
        )
    ) as session:
        logger.info("氧化态查询 MCP 服务器已启动")
        await session.wait_for_disconnect()


if __name__ == "__main__":
    asyncio.run(main())
