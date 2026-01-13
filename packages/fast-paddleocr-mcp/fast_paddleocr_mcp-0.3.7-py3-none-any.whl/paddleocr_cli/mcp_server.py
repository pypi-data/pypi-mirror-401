"""MCP server for PaddleOCR - accepts image path and outputs image path + .md"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Optional

try:
    from mcp.server import NotificationOptions, Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    print("Error: mcp package is not installed. Please install it with: pip install mcp", file=sys.stderr)
    sys.exit(1)

try:
    from paddleocr import PaddleOCR
except ImportError:
    print("Error: paddleocr is not installed. Please install it with: pip install paddleocr", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
server = Server("fast-paddleocr-mcp")

# Cache PaddleOCR instances by language (lazy initialization)
ocr_cache: dict[str, PaddleOCR] = {}


def get_ocr(language: str = 'ch') -> PaddleOCR:
    """Initialize PaddleOCR with optimized settings for speed
    
    Args:
        language: Language code for OCR (default: 'ch' for Chinese and English)
                  Common values: 'ch', 'en', 'chinese_cht', 'korean', 'japan', etc.
                  See PaddleOCR documentation for full list.
    
    Returns:
        PaddleOCR instance for the specified language
    """
    global ocr_cache
    
    # Use lowercase for consistency
    lang_key = language.lower()
    
    if lang_key not in ocr_cache:
        ocr_cache[lang_key] = PaddleOCR(
            use_angle_cls=False,  # Fast mode: disable textline orientation classification
            lang=lang_key,  # Language specified by caller
            show_log=False,  # Disable logging
            use_gpu=True,  # Auto-detect GPU, fallback to CPU
            det_model_dir=None,  # Use default mobile models (PP-OCRv4)
            rec_model_dir=None,
        )
    return ocr_cache[lang_key]


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="ocr_image",
            description="Extract text from an image using PaddleOCR and save results to a markdown file. Returns the path to the generated markdown file (image_path + .md).",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the input image file"
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code for OCR (e.g., 'ch' for Chinese/English, 'en' for English, 'japan' for Japanese, 'korean' for Korean). Default: 'ch'. See PaddleOCR documentation for full list of supported languages."
                    }
                },
                "required": ["image_path"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Optional[dict[str, Any]]) -> list[types.TextContent]:
    """Handle tool calls"""
    if name != "ocr_image":
        raise ValueError(f"Unknown tool: {name}")
    
    if not arguments or "image_path" not in arguments:
        raise ValueError("Missing required argument: image_path")
    
    image_path = arguments["image_path"]
    if not isinstance(image_path, str):
        raise ValueError("image_path must be a string")
    
    # Get language parameter (optional, default to 'ch')
    language = arguments.get("language", "ch")
    if not isinstance(language, str):
        raise ValueError("language must be a string if provided")
    
    try:
        # Validate input file exists
        image_path_obj = Path(image_path)
        if not image_path_obj.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        if not image_path_obj.is_file():
            raise ValueError(f"Path is not a file: {image_path}")
        
        # Initialize OCR with specified language
        ocr_instance = get_ocr(language)
        
        # Perform OCR
        result = ocr_instance.ocr(str(image_path_obj), cls=False)
        
        # Generate output markdown file path (image.png -> image.png.md)
        output_path = Path(str(image_path_obj) + '.md')
        
        # Extract text from OCR result
        detected_texts = []
        if result and result[0]:
            for line in result[0]:
                if line and len(line) >= 2:
                    text = line[1][0]  # Extract text from OCR result format: [[box_coords], (text, confidence)]
                    if text:
                        detected_texts.append(text)
        
        # Write markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# OCR Result\n\n")
            f.write(f"**Source Image:** `{image_path}`\n\n")
            f.write(f"**Language:** `{language}`\n\n")
            f.write("---\n\n")
            
            if detected_texts:
                for text in detected_texts:
                    f.write(f"- {text}\n")
            else:
                f.write("- No text detected\n")
        
        # Return the output file path
        return [types.TextContent(type="text", text=str(output_path))]
    
    except Exception as e:
        error_msg = f"Error processing image {image_path}: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise RuntimeError(error_msg) from e


async def main_async():
    """Async main entry point for the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fast-paddleocr-mcp",
                server_version="0.3.6",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    """Main entry point for the MCP server (synchronous wrapper)"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
