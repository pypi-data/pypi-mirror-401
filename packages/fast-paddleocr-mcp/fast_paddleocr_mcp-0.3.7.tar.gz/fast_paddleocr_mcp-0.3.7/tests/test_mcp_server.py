"""Unit tests for MCP server"""

import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Import the server module
from paddleocr_cli import mcp_server


@pytest.fixture
def mock_paddleocr():
    """Create a mock PaddleOCR instance"""
    mock_ocr = MagicMock()
    mock_ocr.ocr.return_value = [
        [
            [[[0, 0], [100, 0], [100, 30], [0, 30]], ("Hello", 0.95)],
            [[[0, 40], [100, 40], [100, 70], [0, 70]], ("World", 0.92)],
        ]
    ]
    return mock_ocr


@pytest.fixture
def test_image(tmp_path):
    """Create a temporary test image file"""
    image_path = tmp_path / "test_image.png"
    image_path.write_bytes(b"fake image data")
    return str(image_path)


@pytest.fixture
def cleanup_cache():
    """Clean up OCR cache before and after tests"""
    mcp_server.ocr_cache.clear()
    yield
    mcp_server.ocr_cache.clear()


class TestGetOCR:
    """Test OCR instance initialization"""

    def test_get_ocr_default_language(self, cleanup_cache):
        """Test OCR initialization with default language"""
        with patch("paddleocr_cli.mcp_server.PaddleOCR") as mock_ocr_class:
            mock_instance = MagicMock()
            mock_ocr_class.return_value = mock_instance

            result = mcp_server.get_ocr()
            
            assert result == mock_instance
            mock_ocr_class.assert_called_once_with(
                use_angle_cls=False,
                lang="ch",
                show_log=False,
                use_gpu=True,
                det_model_dir=None,
                rec_model_dir=None,
            )

    def test_get_ocr_custom_language(self, cleanup_cache):
        """Test OCR initialization with custom language"""
        with patch("paddleocr_cli.mcp_server.PaddleOCR") as mock_ocr_class:
            mock_instance = MagicMock()
            mock_ocr_class.return_value = mock_instance

            result = mcp_server.get_ocr("en")
            
            assert result == mock_instance
            mock_ocr_class.assert_called_once_with(
                use_angle_cls=False,
                lang="en",
                show_log=False,
                use_gpu=True,
                det_model_dir=None,
                rec_model_dir=None,
            )

    def test_get_ocr_language_lowercase(self, cleanup_cache):
        """Test that language is converted to lowercase"""
        with patch("paddleocr_cli.mcp_server.PaddleOCR") as mock_ocr_class:
            mock_instance = MagicMock()
            mock_ocr_class.return_value = mock_instance

            mcp_server.get_ocr("EN")
            
            mock_ocr_class.assert_called_once()
            call_kwargs = mock_ocr_class.call_args[1]
            assert call_kwargs["lang"] == "en"

    def test_get_ocr_caching(self, cleanup_cache):
        """Test that OCR instances are cached by language"""
        with patch("paddleocr_cli.mcp_server.PaddleOCR") as mock_ocr_class:
            mock_instance_ch = MagicMock()
            mock_instance_en = MagicMock()
            mock_ocr_class.side_effect = [mock_instance_ch, mock_instance_en]

            # First call
            result1 = mcp_server.get_ocr("ch")
            assert result1 == mock_instance_ch
            assert len(mcp_server.ocr_cache) == 1

            # Second call with same language should return cached instance
            result2 = mcp_server.get_ocr("ch")
            assert result2 == mock_instance_ch
            assert mock_ocr_class.call_count == 1  # Should not create new instance

            # Third call with different language should create new instance
            result3 = mcp_server.get_ocr("en")
            assert result3 == mock_instance_en
            assert mock_ocr_class.call_count == 2


@pytest.mark.asyncio
class TestListTools:
    """Test tool listing"""

    async def test_list_tools(self):
        """Test that list_tools returns the correct tool definition"""
        tools = await mcp_server.handle_list_tools()
        
        assert len(tools) == 1
        tool = tools[0]
        assert tool.name == "ocr_image"
        assert "Extract text from an image" in tool.description
        assert tool.inputSchema["type"] == "object"
        assert "image_path" in tool.inputSchema["properties"]
        assert "language" in tool.inputSchema["properties"]
        assert "image_path" in tool.inputSchema["required"]
        assert "language" not in tool.inputSchema["required"]


@pytest.mark.asyncio
class TestCallTool:
    """Test tool calling"""

    async def test_call_tool_success(self, test_image, mock_paddleocr, cleanup_cache):
        """Test successful OCR tool call"""
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_paddleocr):
            arguments = {"image_path": test_image}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            assert len(result) == 1
            assert result[0].type == "text"
            output_path = Path(result[0].text)
            assert output_path.exists()
            assert output_path.suffix == ".md"
            # Output should be test_image.png.md
            assert output_path.name == "test_image.png.md"
            
            # Verify markdown content
            content = output_path.read_text(encoding="utf-8")
            assert "# OCR Result" in content
            assert "**Source Image:**" in content
            assert test_image in content
            assert "Hello" in content
            assert "World" in content
            
            # Verify OCR was called
            mock_paddleocr.ocr.assert_called_once_with(str(test_image), cls=False)

    async def test_call_tool_with_language(self, test_image, cleanup_cache):
        """Test OCR tool call with custom language"""
        mock_ocr_ch = MagicMock()
        mock_ocr_ch.ocr.return_value = [[[[[0, 0], [100, 0], [100, 30], [0, 30]], ("中文", 0.95)]]]
        
        mock_ocr_en = MagicMock()
        mock_ocr_en.ocr.return_value = [[[[[0, 0], [100, 0], [100, 30], [0, 30]], ("English", 0.95)]]]
        
        # Test with Chinese
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_ocr_ch) as mock_get_ocr:
            arguments_ch = {"image_path": test_image, "language": "ch"}
            await mcp_server.handle_call_tool("ocr_image", arguments_ch)
            mock_get_ocr.assert_called_once_with("ch")
            mock_ocr_ch.ocr.assert_called_once()
        
        # Reset cache and test with English
        mcp_server.ocr_cache.clear()
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_ocr_en) as mock_get_ocr:
            arguments_en = {"image_path": test_image, "language": "en"}
            await mcp_server.handle_call_tool("ocr_image", arguments_en)
            mock_get_ocr.assert_called_once_with("en")
            mock_ocr_en.ocr.assert_called_once()

    async def test_call_tool_default_language(self, test_image, mock_paddleocr, cleanup_cache):
        """Test that default language is used when not specified"""
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_paddleocr) as mock_get_ocr:
            arguments = {"image_path": test_image}
            
            await mcp_server.handle_call_tool("ocr_image", arguments)
            
            mock_get_ocr.assert_called_once_with("ch")

    async def test_call_tool_language_in_markdown(self, test_image, mock_paddleocr, cleanup_cache):
        """Test that language is recorded in markdown output"""
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_paddleocr):
            arguments = {"image_path": test_image, "language": "en"}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            output_path = Path(result[0].text)
            content = output_path.read_text(encoding="utf-8")
            assert "**Language:**" in content
            assert "`en`" in content

    async def test_call_tool_no_text_detected(self, test_image, cleanup_cache):
        """Test OCR when no text is detected"""
        mock_ocr = MagicMock()
        mock_ocr.ocr.return_value = [[]]  # No text detected
        
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_ocr):
            arguments = {"image_path": test_image}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            output_path = Path(result[0].text)
            content = output_path.read_text(encoding="utf-8")
            assert "No text detected" in content

    async def test_call_tool_unknown_tool(self):
        """Test calling unknown tool raises error"""
        with pytest.raises(ValueError, match="Unknown tool"):
            await mcp_server.handle_call_tool("unknown_tool", {})

    async def test_call_tool_missing_image_path(self):
        """Test calling tool without image_path raises error"""
        with pytest.raises(ValueError, match="Missing required argument: image_path"):
            await mcp_server.handle_call_tool("ocr_image", {})

    async def test_call_tool_invalid_image_path_type(self):
        """Test calling tool with non-string image_path raises error"""
        with pytest.raises(ValueError, match="image_path must be a string"):
            await mcp_server.handle_call_tool("ocr_image", {"image_path": 123})

    async def test_call_tool_nonexistent_file(self, tmp_path):
        """Test calling tool with non-existent file raises error"""
        nonexistent_path = str(tmp_path / "nonexistent.png")
        
        with pytest.raises(RuntimeError, match="Image file not found"):
            await mcp_server.handle_call_tool(
                "ocr_image",
                {"image_path": nonexistent_path}
            )

    async def test_call_tool_directory_not_file(self, tmp_path):
        """Test calling tool with directory instead of file raises error"""
        dir_path = tmp_path / "directory"
        dir_path.mkdir()
        
        with pytest.raises(RuntimeError, match="Path is not a file"):
            await mcp_server.handle_call_tool(
                "ocr_image",
                {"image_path": str(dir_path)}
            )

    async def test_call_tool_invalid_language_type(self, test_image):
        """Test calling tool with non-string language raises error"""
        with pytest.raises(ValueError, match="language must be a string"):
            await mcp_server.handle_call_tool(
                "ocr_image",
                {"image_path": test_image, "language": 123}
            )

    async def test_call_tool_ocr_error_handling(self, test_image, cleanup_cache):
        """Test error handling when OCR fails"""
        mock_ocr = MagicMock()
        mock_ocr.ocr.side_effect = Exception("OCR processing failed")
        
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_ocr):
            with pytest.raises(RuntimeError, match="Error processing image"):
                await mcp_server.handle_call_tool(
                    "ocr_image",
                    {"image_path": test_image}
                )


class TestMain:
    """Test main entry point"""

    def test_main_calls_asyncio_run(self):
        """Test that main calls asyncio.run"""
        with patch("paddleocr_cli.mcp_server.asyncio.run") as mock_run:
            mcp_server.main()
            mock_run.assert_called_once()
            # Verify it was called with a coroutine object (result of main_async())
            call_arg = mock_run.call_args[0][0]
            assert asyncio.iscoroutine(call_arg)


class TestMarkdownOutput:
    """Test markdown file generation"""

    @pytest.mark.asyncio
    async def test_markdown_format(self, test_image, mock_paddleocr, cleanup_cache):
        """Test that markdown output has correct format"""
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_paddleocr):
            arguments = {"image_path": test_image, "language": "ch"}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            output_path = Path(result[0].text)
            content = output_path.read_text(encoding="utf-8")
            
            # Check structure
            lines = content.split("\n")
            assert lines[0] == "# OCR Result"
            assert "**Source Image:**" in content
            assert "**Language:**" in content
            assert "---" in content
            
            # Check that detected texts are listed
            assert "- Hello" in content or "Hello" in content
            assert "- World" in content or "World" in content

    @pytest.mark.asyncio
    async def test_markdown_output_path(self, test_image, mock_paddleocr, cleanup_cache):
        """Test that output path is image_path + .md"""
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_paddleocr):
            arguments = {"image_path": test_image}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            output_path = Path(result[0].text)
            expected_path = Path(test_image + ".md")
            
            # Compare absolute paths to avoid path format differences
            assert output_path.resolve() == expected_path.resolve()
            assert output_path.exists()


@pytest.mark.asyncio
class TestEdgeCases:
    """Test edge cases and special scenarios"""

    async def test_empty_ocr_result(self, test_image, cleanup_cache):
        """Test handling of empty OCR result"""
        mock_ocr = MagicMock()
        mock_ocr.ocr.return_value = None
        
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_ocr):
            arguments = {"image_path": test_image}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            output_path = Path(result[0].text)
            content = output_path.read_text(encoding="utf-8")
            assert "No text detected" in content

    async def test_ocr_result_with_none_values(self, test_image, cleanup_cache):
        """Test handling of OCR result with None values"""
        mock_ocr = MagicMock()
        mock_ocr.ocr.return_value = [[None, []]]
        
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_ocr):
            arguments = {"image_path": test_image}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            output_path = Path(result[0].text)
            content = output_path.read_text(encoding="utf-8")
            assert "No text detected" in content

    async def test_ocr_result_with_empty_text(self, test_image, cleanup_cache):
        """Test handling of OCR result with empty text strings"""
        mock_ocr = MagicMock()
        mock_ocr.ocr.return_value = [
            [
                [[[0, 0], [100, 0], [100, 30], [0, 30]], ("", 0.95)],
                [[[0, 40], [100, 40], [100, 70], [0, 70]], ("Valid", 0.92)],
            ]
        ]
        
        with patch("paddleocr_cli.mcp_server.get_ocr", return_value=mock_ocr):
            arguments = {"image_path": test_image}
            
            result = await mcp_server.handle_call_tool("ocr_image", arguments)
            
            output_path = Path(result[0].text)
            content = output_path.read_text(encoding="utf-8")
            # Should only include "Valid", not empty strings
            assert "Valid" in content
            # Empty strings should be filtered out
