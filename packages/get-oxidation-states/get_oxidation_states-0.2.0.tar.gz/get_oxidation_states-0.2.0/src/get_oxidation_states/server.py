from typing import Annotated, Dict, List, Optional
from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import BaseModel, Field, validator

# 元素氧化态核心数据
OXIDATION_STATES_DATA: Dict[str, Dict[str, str]] = {
    # 元素符号: {氧化态: 稳定性说明}
    "H": {
        "+1": "最常见，稳定（如H2O、HCl）",
        "-1": "仅存在于金属氢化物中（如NaH、CaH2），较不稳定",
        "0": "单质氢气（H2），稳定"
    },
    "O": {
        "-2": "最常见，稳定（如H2O、CO2）",
        "-1": "过氧化物中（如H2O2、Na2O2），中等稳定",
        "0": "单质氧气（O2），稳定",
        "+2": "仅存在于OF2中，极不稳定"
    },
    "Na": {
        "+1": "唯一常见氧化态，稳定（所有钠盐）",
        "0": "单质钠，活泼金属，不稳定"
    },
    "Cl": {
        "-1": "最常见，稳定（如NaCl、HCl）",
        "0": "单质氯气（Cl2），稳定",
        "+1": "次氯酸盐中（如NaClO），中等稳定",
        "+3": "亚氯酸盐中（如NaClO2），较不稳定",
        "+5": "氯酸盐中（如KClO3），稳定",
        "+7": "高氯酸盐中（如NaClO4），稳定"
    },
    "Fe": {
        "0": "单质铁，稳定",
        "+2": "亚铁离子（如FeSO4），中等稳定，易被氧化为+3价",
        "+3": "铁离子（如FeCl3），稳定",
        "+6": "高铁酸盐中（如K2FeO4），强氧化性，不稳定"
    },
    "Cu": {
        "0": "单质铜，稳定",
        "+1": "亚铜离子（如Cu2O），较不稳定，易歧化为0和+2价",
        "+2": "铜离子（如CuSO4），稳定"
    },
    "C": {
        "-4": "甲烷（CH4）等有机物中，稳定",
        "0": "单质碳（石墨、金刚石），稳定",
        "+2": "一氧化碳（CO），中等稳定，有毒",
        "+4": "二氧化碳（CO2）、碳酸盐中，稳定"
    },
    "Zn": {
        "0": "单质锌，稳定",
        "+2": "唯一常见氧化态，稳定（如ZnSO4、ZnCl2）"
    },
    "Al": {
        "0": "单质铝，稳定",
        "+3": "唯一常见氧化态，稳定（如Al2O3、AlCl3）"
    }
}

# 元素名称映射（支持中英文查询）
ELEMENT_NAME_MAP: Dict[str, str] = {
    # 中文名称 -> 符号
    "氢": "H",
    "氧": "O",
    "钠": "Na",
    "氯": "Cl",
    "铁": "Fe",
    "铜": "Cu",
    "碳": "C",
    "锌": "Zn",
    "铝": "Al",
    # 英文名称 -> 符号
    "hydrogen": "H",
    "oxygen": "O",
    "sodium": "Na",
    "chlorine": "Cl",
    "iron": "Fe",
    "copper": "Cu",
    "carbon": "C",
    "zinc": "Zn",
    "aluminum": "Al",
    "aluminium": "Al"  # 英式拼写
}

# 多语言提示文本
LANGUAGE_TEXT = {
    "zh": {
        "tool_desc": "查询化学元素的常见氧化态及对应稳定性",
        "prompt_desc": "查询指定化学元素的常见氧化态",
        "element_required": "元素符号/名称为必填项",
        "element_not_found": "未找到该元素的氧化态数据，请检查输入（支持：H、O、Na、Cl、Fe、Cu、C、Zn、Al）",
        "result_header": "【{element} ({element_name}) 的常见氧化态及稳定性】",
        "oxidation_state_item": "- 氧化态 {state}: {stability}",
        "error_prefix": "查询失败："
    },
    "en": {
        "tool_desc": "Query common oxidation states and stability of chemical elements",
        "prompt_desc": "Query common oxidation states of the specified chemical element",
        "element_required": "Element symbol/name is required",
        "element_not_found": "No oxidation state data found for this element. Please check your input (supported: H, O, Na, Cl, Fe, Cu, C, Zn, Al)",
        "result_header": "[Common oxidation states and stability of {element} ({element_name})]",
        "oxidation_state_item": "- Oxidation state {state}: {stability}",
        "error_prefix": "Query failed: "
    }
}


class GetOxidationStates(BaseModel):
    """查询元素氧化态的参数模型"""
    element: Annotated[
        str,
        Field(
            description="化学元素的符号（如Fe）或名称（如铁/hydrogen）",
            examples=["Fe", "铁", "hydrogen"]
        ),
    ]
    include_stability: Annotated[
        bool,
        Field(
            default=True,
            description="是否返回稳定性说明（默认：是）"
        ),
    ]

    @validator("element")
    def validate_element(cls, v):
        """验证并标准化元素输入"""
        if not v:
            raise ValueError("元素不能为空")
        return v.strip().lower()


def get_element_symbol(element_input: str) -> Optional[str]:
    """
    从输入（符号/名称）中获取标准化的元素符号
    
    Args:
        element_input: 元素符号、中文名称或英文名称
    
    Returns:
        标准化的元素符号（如Fe），未找到返回None
    """
    # 直接匹配符号（不区分大小写）
    symbol_upper = element_input.upper()
    if symbol_upper in OXIDATION_STATES_DATA:
        return symbol_upper
    
    # 匹配名称（中文/英文）
    if element_input in ELEMENT_NAME_MAP:
        return ELEMENT_NAME_MAP[element_input]
    
    return None


def format_oxidation_states(
    element_symbol: str,
    include_stability: bool = True,
    language: str = "zh"
) -> str:
    """
    格式化氧化态查询结果
    
    Args:
        element_symbol: 元素符号
        include_stability: 是否包含稳定性说明
        language: 输出语言
    
    Returns:
        格式化的查询结果文本
    """
    states = OXIDATION_STATES_DATA[element_symbol]
    text = LANGUAGE_TEXT[language]["result_header"].format(
        element=element_symbol,
        element_name=next(k for k, v in ELEMENT_NAME_MAP.items() if v == element_symbol and not k.isupper())
    )
    
    for state, stability in states.items():
        if include_stability:
            text += "\n" + LANGUAGE_TEXT[language]["oxidation_state_item"].format(
                state=state,
                stability=stability if language == "zh" else stability  # 可扩展英文稳定性说明
            )
        else:
            text += f"\n- {state}"
    
    return text


async def serve(language: str = "zh") -> None:
    """运行氧化态查询MCP服务器
    
    Args:
        language: 返回结果的语言（zh/en）
    """
    server = Server("mcp-get-oxidation-states")
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="get_oxidation_states",
                description=LANGUAGE_TEXT[language]["tool_desc"],
                inputSchema=GetOxidationStates.model_json_schema(),
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> List[Prompt]:
        return [
            Prompt(
                name="get_oxidation_states",
                description=LANGUAGE_TEXT[language]["prompt_desc"],
                arguments=[
                    PromptArgument(
                        name="element", 
                        description=LANGUAGE_TEXT[language]["element_required"], 
                        required=True
                    )
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> List[TextContent]:
        try:
            # 参数验证和解析
            args = GetOxidationStates(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))
        
        # 获取元素符号
        element_symbol = get_element_symbol(args.element)
        if not element_symbol:
            raise McpError(ErrorData(
                code=INVALID_PARAMS,
                message=LANGUAGE_TEXT[language]["element_not_found"]
            ))
        
        # 格式化结果
        try:
            result_text = format_oxidation_states(
                element_symbol=element_symbol,
                include_stability=args.include_stability,
                language=language
            )
        except Exception as e:
            raise McpError(ErrorData(
                code=INTERNAL_ERROR,
                message=f"{LANGUAGE_TEXT[language]['error_prefix']}{str(e)}"
            ))
        
        return [TextContent(type="text", text=result_text)]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: Optional[dict]) -> GetPromptResult:
        if not arguments or "element" not in arguments:
            raise McpError(ErrorData(
                code=INVALID_PARAMS,
                message=LANGUAGE_TEXT[language]["element_required"]
            ))
        
        element_input = arguments["element"].strip().lower()
        element_symbol = get_element_symbol(element_input)
        
        if not element_symbol:
            error_msg = LANGUAGE_TEXT[language]["element_not_found"]
            return GetPromptResult(
                description=LANGUAGE_TEXT[language]["error_prefix"] + error_msg,
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=error_msg),
                    )
                ],
            )
        
        # 生成查询结果
        result_text = format_oxidation_states(
            element_symbol=element_symbol,
            language=language
        )
        
        return GetPromptResult(
            description=LANGUAGE_TEXT[language]["result_header"].format(
                element=element_symbol,
                element_name=next(k for k, v in ELEMENT_NAME_MAP.items() if v == element_symbol and not k.isupper())
            ),
            messages=[
                PromptMessage(
                    role="user", 
                    content=TextContent(type="text", text=result_text)
                )
            ],
        )

    # 启动服务器
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)