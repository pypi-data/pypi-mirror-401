# thinkpdf

Convert PDFs to clean Markdown for LLMs. Includes MCP Server for AI coding assistants.

## Features

- PDF to Markdown conversion
- MCP Server for AI assistants (Cursor, Antigravity)
- GUI included
- Batch conversion with parallel workers
- Optional: Docling for better table extraction

## Installation

```bash
pip install thinkpdf
```

For GUI:
```bash
pip install thinkpdf[gui]
```

## Quick Start

### GUI
```bash
thinkpdf-gui
```

### CLI
```bash
thinkpdf document.pdf                    # Convert single file
thinkpdf document.pdf -o output.md       # Specify output
thinkpdf folder/ --batch                 # Convert all PDFs in folder
thinkpdf folder/ --batch --workers 4     # Parallel conversion
```

### Python API
```python
from thinkpdf import convert

markdown = convert("document.pdf")
print(markdown)
```

## MCP Server Setup

Run this to see the config:
```bash
thinkpdf setup
```

Add to `~/.cursor/mcp.json` or `~/.gemini/antigravity/mcp.json`:
```json
{
  "mcpServers": {
    "thinkpdf": {
      "command": "python",
      "args": ["-m", "thinkpdf.mcp_server"]
    }
  }
}
```

Then ask your AI: "Read the PDF at D:\docs\manual.pdf"

### MCP Tools

| Tool | Description |
|------|-------------|
| read_pdf | Convert and return content directly (no file created) |
| convert_pdf | Convert and save to file |
| get_document_info | Get PDF metadata |

## Requirements

- Python 3.10+
- PyMuPDF (included)
- Docling (optional, for best quality)

## License

AGPL-3.0
