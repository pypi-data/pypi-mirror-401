#!/usr/bin/env python3
"""
Calculator MCP Server - Python implementation
"""

import asyncio
import sys
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Calculator functions
def add(num1: float, num2: float) -> float:
    """Add two numbers together"""
    return num1 + num2

def subtract(num1: float, num2: float) -> float:
    """Subtract the second number from the first number"""
    return num1 - num2

def multiply(num1: float, num2: float) -> float:
    """Multiply two numbers together"""
    return num1 * num2

def divide(num1: float, num2: float) -> float:
    """Divide the first number by the second number"""
    if num2 == 0:
        raise ValueError("Division by zero is not allowed")
    return num1 / num2

# Create MCP server
app = Server("calculator-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available calculator tools"""
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "First number",
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second number",
                    },
                },
                "required": ["num1", "num2"],
            },
        ),
        Tool(
            name="subtract",
            description="Subtract the second number from the first number",
            inputSchema={
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "First number (minuend)",
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second number (subtrahend)",
                    },
                },
                "required": ["num1", "num2"],
            },
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "First number",
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second number",
                    },
                },
                "required": ["num1", "num2"],
            },
        ),
        Tool(
            name="divide",
            description="Divide the first number by the second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "First number (dividend)",
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second number (divisor)",
                    },
                },
                "required": ["num1", "num2"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "add":
            result = add(arguments["num1"], arguments["num2"])
        elif name == "subtract":
            result = subtract(arguments["num1"], arguments["num2"])
        elif name == "multiply":
            result = multiply(arguments["num1"], arguments["num2"])
        elif name == "divide":
            result = divide(arguments["num1"], arguments["num2"])
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

def main():
    """Main entry point"""
    asyncio.run(run_server())

async def run_server():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="calculator-mcp",
                server_version="1.0.20",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    main()
