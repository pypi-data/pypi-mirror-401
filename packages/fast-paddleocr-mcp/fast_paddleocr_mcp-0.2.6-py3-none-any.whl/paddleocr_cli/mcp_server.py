"""MCP server for PaddleOCR."""

import asyncio
import contextlib
import io
import json
import os
import sys
from pathlib import Path
from typing import Any

# Set environment variables before importing ANYTHING to suppress warnings
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
os.environ['PADDLEOCR_LOG_LEVEL'] = 'ERROR'
os.environ['PYTHONWARNINGS'] = 'ignore'

# Save original stdout for direct JSON-RPC writes
_original_stdout = sys.stdout
# Redirect stdout to stderr to capture any PaddleOCR warnings during import
sys.stdout = sys.stderr

# Import will happen lazily in handle_request to avoid PaddleOCR warnings at startup
_image_to_markdown = None


async def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    """Handle MCP requests."""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")
    
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "ocr_image",
                        "description": "Extract text from an image using PaddleOCR. Returns the path to the generated markdown file containing the recognition results.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "image_path": {
                                    "type": "string",
                                    "description": "Path to the input image file"
                                }
                            },
                            "required": ["image_path"]
                        }
                    }
                ]
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "ocr_image":
            image_path = arguments.get("image_path")
            
            if not image_path:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "Invalid params",
                        "data": "image_path parameter is required"
                    }
                }
            
            # Validate image file exists
            image_path_obj = Path(image_path)
            if not image_path_obj.exists():
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "Invalid params",
                        "data": f"Image file not found: {image_path}"
                    }
                }
            
            if not image_path_obj.is_file():
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "Invalid params",
                        "data": f"Path is not a file: {image_path}"
                    }
                }
            
            try:
                # Lazy import to avoid PaddleOCR warnings at startup
                global _image_to_markdown
                if _image_to_markdown is None:
                    # Redirect stdout during import to capture any warnings
                    old_stdout = sys.stdout
                    sys.stdout = sys.stderr
                    try:
                        from .main import image_to_markdown as _image_to_markdown_func
                        _image_to_markdown = _image_to_markdown_func
                    finally:
                        sys.stdout = old_stdout
                
                # Call OCR function with default optimized settings
                # Redirect stdout during OCR to capture any warnings
                old_stdout = sys.stdout
                sys.stdout = sys.stderr
                try:
                    output_path = _image_to_markdown(
                        str(image_path),
                        output_path=None,  # Use default: <image_name>.md
                        fast_mode=True,  # Default: fast mode
                        use_gpu=None,  # Default: auto-detect GPU
                        ocr_version='PP-OCRv4',  # Default: PP-OCRv4
                        max_image_size=640,  # Default: 640px
                        enable_hpi=False,  # Default: no HPI
                        lang='en'  # Default: English
                    )
                finally:
                    sys.stdout = old_stdout
                
                # Return the output file path
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": output_path
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": "Internal error",
                        "data": f"Error during OCR processing: {str(e)}"
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": "Method not found",
                    "data": f"Unknown tool: {tool_name}"
                }
            }
    
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "fast-paddleocr-mcp",
                    "version": "0.2.6"
                }
            }
        }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }


async def main():
    """Run the MCP server using stdio."""
    # Read from stdin, write to original stdout directly (not through filtered stdout)
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            request = json.loads(line)
            response = await handle_request(request)
            
            # Write directly to original stdout to bypass filter
            _original_stdout.write(json.dumps(response) + '\n')
            _original_stdout.flush()
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            _original_stdout.write(json.dumps(error_response) + '\n')
            _original_stdout.flush()
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
            _original_stdout.write(json.dumps(error_response) + '\n')
            _original_stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
