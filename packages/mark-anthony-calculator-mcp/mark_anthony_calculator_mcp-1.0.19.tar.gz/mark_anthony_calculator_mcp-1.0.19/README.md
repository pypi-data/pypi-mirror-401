# Calculator MCP Server

A Model Context Protocol (MCP) server that provides calculator operations (add, subtract, multiply, divide).

## Installation

### Via npx (Node.js - recommended)

```bash
npx @mark.anthony987654321/calculator-mcp
```

### Via uvx (Python - recommended)

```bash
uvx calculator-mcp
```

### Local Installation

**Node.js:**
```bash
npm install
npm start
```

**Python:**
```bash
pip install -e .
python -m calculator_mcp
```

## Available Tools

- **add**: Add two numbers together
- **subtract**: Subtract the second number from the first number
- **multiply**: Multiply two numbers together
- **divide**: Divide the first number by the second number

## Usage

This MCP server is designed to be used with MCP-compatible clients. Configure your MCP client to use this server.

### Example Configuration

For use with Claude Desktop or other MCP clients, add to your MCP configuration:

**Using npx (Node.js):**
```json
{
  "mcpServers": {
    "calculator": {
      "command": "npx",
      "args": ["@mark.anthony987654321/calculator-mcp"]
    }
  }
}
```

**Using uvx (Python):**
```json
{
  "mcpServers": {
    "calculator": {
      "command": "uvx",
      "args": ["calculator-mcp"]
    }
  }
}
```

## Development

**Node.js:**
```bash
# Install dependencies
npm install

# Run the server
npm start
```

**Python:**
```bash
# Install dependencies
pip install -e ".[dev]"

# Run the server
python -m calculator_mcp
```

## License

MIT
