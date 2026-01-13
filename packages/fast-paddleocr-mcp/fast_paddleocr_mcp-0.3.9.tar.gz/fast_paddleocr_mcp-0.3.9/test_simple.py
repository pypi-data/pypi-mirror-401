#!/usr/bin/env python3
"""最简单的端到端测试 - 验证MCP服务器能否正常工作"""

import asyncio
import json
import sys
from pathlib import Path

# 导入MCP服务器
from paddleocr_cli.mcp_server import handle_call_tool, handle_list_tools

async def test_simple():
    """测试最简单的调用"""
    print("=" * 60)
    print("开始最简单的端到端测试")
    print("=" * 60)
    
    # 1. 测试列出工具
    print("\n1. 测试列出工具...")
    try:
        tools = await handle_list_tools()
        print(f"✓ 成功列出工具: {len(tools)} 个")
        if tools:
            print(f"  工具名称: {tools[0].name}")
            print(f"  工具描述: {tools[0].description[:50]}...")
    except Exception as e:
        print(f"✗ 列出工具失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 2. 测试调用工具（使用测试图片）
    print("\n2. 测试调用OCR工具...")
    test_image = Path(__file__).parent / "c9c2184db3e2483fbd406a8ae3bf8f11.png"
    
    if not test_image.exists():
        print(f"✗ 测试图片不存在: {test_image}")
        print("  请确保测试图片存在")
        return False
    
    print(f"  使用测试图片: {test_image}")
    
    try:
        arguments = {"image_path": str(test_image)}
        result = await handle_call_tool("ocr_image", arguments)
        
        print(f"✓ OCR调用成功")
        print(f"  返回结果: {result}")
        
        if result and len(result) > 0:
            output_path = Path(result[0].text)
            print(f"  输出文件: {output_path}")
            
            if output_path.exists():
                print(f"✓ 输出文件存在")
                content = output_path.read_text(encoding='utf-8')
                print(f"  文件大小: {len(content)} 字节")
                print(f"  前100字符: {content[:100]}...")
                return True
            else:
                print(f"✗ 输出文件不存在: {output_path}")
                return False
        else:
            print(f"✗ 返回结果为空")
            return False
            
    except Exception as e:
        print(f"✗ OCR调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Python版本:", sys.version)
    print("工作目录:", Path.cwd())
    print()
    
    try:
        result = asyncio.run(test_simple())
        if result:
            print("\n" + "=" * 60)
            print("✓ 所有测试通过！")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n" + "=" * 60)
            print("✗ 测试失败！")
            print("=" * 60)
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ 测试过程中发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
