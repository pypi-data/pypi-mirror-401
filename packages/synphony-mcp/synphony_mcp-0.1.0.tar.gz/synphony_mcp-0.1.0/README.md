# Synphony MCP Server

MCP (Model Context Protocol) server for the Synphony robotics data platform.

## Installation

```bash
cd synphony-mcp
pip install -e .
```

## Configuration

Create a config file at `~/.synphony/config.json`:

```json
{
  "api_key": "your-api-key-here",
  "api_base_url": "https://dev.synphony.co/api/cli"
}
```

## Usage

### Run the MCP server

```bash
synphony-mcp
```

### Connect from Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "synphony": {
      "command": "synphony-mcp"
    }
  }
}
```

## Available Tools

### Datasets
- `datasets.list` - List user's datasets
- `datasets.get` - Get dataset details

### Videos
- `videos.search` - Search/filter videos with pagination
- `videos.get` - Get detailed video info

### Processing
- `multiply.run` - Generate video variations with prompts
- `augment.run` - Apply augmentations to videos

## Development

```bash
pip install -e ".[dev]"
pytest
```
