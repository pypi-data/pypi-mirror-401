from .server import serve


def main():
    """MCP Oxidation States Server - 查询元素氧化态的MCP服务"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="为大语言模型提供查询化学元素常见氧化态及稳定性的能力"
    )
    parser.add_argument(
        "--language", 
        type=str, 
        default="zh", 
        choices=["zh", "en"],
        help="返回结果的语言（默认：中文）"
    )

    args = parser.parse_args()
    asyncio.run(serve(language=args.language))


if __name__ == "__main__":
    main()