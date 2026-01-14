"""MCP (Model Context Protocol) integration for LLM core service.

Provides integration with MCP servers for tool discovery and execution,
enabling the LLM to interact with external tools and services.

Implements MCP JSON-RPC 2.0 protocol over stdio for:
- Server initialization handshake
- tools/list for tool discovery
- tools/call for tool execution
"""

import asyncio
import json
import logging
import re
import shlex
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class MCPServerConnection:
    """Manages a connection to an MCP server via stdio."""

    def __init__(self, server_name: str, command: str):
        self.server_name = server_name
        self.command = command
        self.process: Optional[asyncio.subprocess.Process] = None
        self.initialized = False
        self._read_buffer = ""

    async def connect(self) -> bool:
        """Start the MCP server process."""
        try:
            command_parts = shlex.split(self.command)
            self.process = await asyncio.create_subprocess_exec(
                *command_parts,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            logger.info(f"Started MCP server process: {self.server_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to start MCP server {self.server_name}: {e}")
            return False

    async def initialize(self) -> bool:
        """Send MCP initialize request and wait for response."""
        if not self.process:
            return False

        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "kollabor-cli",
                    "version": "1.0.0"
                }
            }
        }

        response = await self._send_request(request)
        if response and "result" in response:
            self.initialized = True
            logger.info(f"MCP server {self.server_name} initialized")

            # Send initialized notification
            notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            await self._send_notification(notification)
            return True

        logger.warning(f"MCP server {self.server_name} initialization failed")
        return False

    async def list_tools(self) -> List[Dict[str, Any]]:
        """Request tools list from server."""
        if not self.initialized:
            return []

        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/list",
            "params": {}
        }

        response = await self._send_request(request)
        if response and "result" in response:
            tools = response["result"].get("tools", [])
            logger.info(f"Got {len(tools)} tools from {self.server_name}")
            return tools

        return []

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the server."""
        if not self.initialized:
            return {"error": "Server not initialized"}

        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        response = await self._send_request(request)
        if response:
            if "result" in response:
                return response["result"]
            elif "error" in response:
                return {"error": response["error"].get("message", "Unknown error")}

        return {"error": "No response from server"}

    async def _send_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send JSON-RPC request and wait for response."""
        if not self.process or not self.process.stdin:
            return None

        try:
            message = json.dumps(request) + "\n"
            self.process.stdin.write(message.encode())
            await self.process.stdin.drain()

            # Read response with timeout
            response = await asyncio.wait_for(self._read_response(), timeout=30)
            return response
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for response from {self.server_name}")
            return None
        except Exception as e:
            logger.error(f"Error sending request to {self.server_name}: {e}")
            return None

    async def _send_notification(self, notification: Dict[str, Any]) -> None:
        """Send JSON-RPC notification (no response expected)."""
        if not self.process or not self.process.stdin:
            return

        try:
            message = json.dumps(notification) + "\n"
            self.process.stdin.write(message.encode())
            await self.process.stdin.drain()
        except Exception as e:
            logger.error(f"Error sending notification to {self.server_name}: {e}")

    async def _read_response(self) -> Optional[Dict[str, Any]]:
        """Read a JSON-RPC response from stdout."""
        if not self.process or not self.process.stdout:
            return None

        while True:
            # Check if we have a complete message in buffer
            if "\n" in self._read_buffer:
                line, self._read_buffer = self._read_buffer.split("\n", 1)
                if line.strip():
                    try:
                        return json.loads(line)
                    except json.JSONDecodeError:
                        continue

            # Read more data
            chunk = await self.process.stdout.read(4096)
            if not chunk:
                return None
            self._read_buffer += chunk.decode()

    async def close(self) -> None:
        """Close the server connection."""
        if self.process:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5)
            except asyncio.TimeoutError:
                self.process.kill()
            except Exception as e:
                logger.warning(f"Error closing MCP server {self.server_name}: {e}")
            self.process = None
            self.initialized = False
            logger.info(f"Closed MCP server connection: {self.server_name}")


class MCPIntegration:
    """MCP server and tool integration.

    Manages discovery, registration, and execution of MCP tools,
    bridging external services with the LLM core service.

    Uses proper MCP JSON-RPC protocol for server communication.
    """

    def __init__(self):
        """Initialize MCP integration."""
        self.mcp_servers: Dict[str, Dict[str, Any]] = {}
        self.tool_registry: Dict[str, Dict[str, Any]] = {}
        self.server_connections: Dict[str, MCPServerConnection] = {}

        # MCP configuration directories (local project first, then global)
        self.local_mcp_dir = Path.cwd() / ".kollabor-cli" / "mcp"
        self.global_mcp_dir = Path.home() / ".kollabor-cli" / "mcp"

        # Load from both local and global configs
        self._load_mcp_config()

        logger.info("MCP Integration initialized")
    
    def _load_mcp_config(self):
        """Load MCP configuration from Kollabor config directories."""
        # Load from global config first (lower priority)
        self._load_config_from_dir(self.global_mcp_dir, "global")
        
        # Load from local config second (higher priority, can override)
        self._load_config_from_dir(self.local_mcp_dir, "local")
        
        logger.info(f"Loaded {len(self.mcp_servers)} total MCP server configurations")
    
    def _load_config_from_dir(self, config_dir: Path, config_type: str):
        """Load MCP config from a specific directory.

        Args:
            config_dir: Directory to load config from
            config_type: Type of config (local/global) for logging
        """
        try:
            mcp_settings = config_dir / "mcp_settings.json"
            if mcp_settings.exists():
                with open(mcp_settings, 'r') as f:
                    config = json.load(f)
                    servers = config.get("servers", {})
                    self.mcp_servers.update(servers)
                    logger.info(f"Loaded {len(servers)} MCP servers from {config_type} config")
        except Exception as e:
            logger.warning(f"Failed to load {config_type} MCP config: {e}")
    
    async def discover_mcp_servers(self) -> Dict[str, Any]:
        """Auto-discover available MCP servers and their tools.

        Connects to each configured stdio server using MCP protocol,
        initializes it, and queries available tools.

        Returns:
            Dictionary of discovered MCP servers and their capabilities
        """
        discovered = {}

        # Check for local MCP servers (manifest-based)
        await self._discover_local_servers(discovered)

        # Connect to configured stdio servers using MCP protocol
        for server_name, server_config in self.mcp_servers.items():
            if not server_config.get("enabled", True):
                logger.debug(f"Skipping disabled MCP server: {server_name}")
                continue

            if server_config.get("type") == "stdio":
                command = server_config.get("command")
                if command:
                    tools = await self._connect_and_list_tools(server_name, command)
                    discovered[server_name] = {
                        "name": server_name,
                        "type": "stdio",
                        "tools": [t.get("name") for t in tools],
                        "tool_count": len(tools),
                        "status": "connected" if tools else "no_tools"
                    }

        return discovered

    async def _connect_and_list_tools(self, server_name: str, command: str) -> List[Dict[str, Any]]:
        """Connect to an MCP server and list its tools.

        Uses proper MCP JSON-RPC protocol:
        1. Start server process
        2. Send initialize request
        3. Send tools/list request
        4. Register discovered tools

        Args:
            server_name: Name of the server
            command: Command to start the server

        Returns:
            List of tool definitions from the server
        """
        # Close existing connection if any
        if server_name in self.server_connections:
            await self.server_connections[server_name].close()

        # Create new connection
        connection = MCPServerConnection(server_name, command)

        if not await connection.connect():
            logger.warning(f"Failed to connect to MCP server: {server_name}")
            return []

        if not await connection.initialize():
            logger.warning(f"Failed to initialize MCP server: {server_name}")
            await connection.close()
            return []

        # List tools
        tools = await connection.list_tools()

        # Register tools
        for tool in tools:
            tool_name = tool.get("name")
            if tool_name:
                self.tool_registry[tool_name] = {
                    "server": server_name,
                    "definition": {
                        "name": tool_name,
                        "description": tool.get("description", ""),
                        "parameters": tool.get("inputSchema", {
                            "type": "object",
                            "properties": {},
                            "required": []
                        })
                    },
                    "enabled": True
                }
                logger.info(f"Registered MCP tool: {tool_name} from {server_name}")

        # Keep connection open for tool calls
        self.server_connections[server_name] = connection

        return tools
    
    async def _discover_local_servers(self, discovered: Dict):
        """Discover locally running MCP servers."""
        # Check common MCP server locations
        common_paths = [
            Path.home() / ".mcp" / "servers",
            Path("/usr/local/mcp/servers"),
            Path.cwd() / ".mcp" / "servers"
        ]
        
        for path in common_paths:
            if path.exists():
                for server_dir in path.iterdir():
                    if server_dir.is_dir():
                        manifest = server_dir / "manifest.json"
                        if manifest.exists():
                            try:
                                with open(manifest, 'r') as f:
                                    server_info = json.load(f)
                                    server_name = server_info.get("name", server_dir.name)
                                    discovered[server_name] = {
                                        "name": server_name,
                                        "path": str(server_dir),
                                        "manifest": server_info,
                                        "status": "local"
                                    }
                                    logger.info(f"Discovered local MCP server: {server_name}")
                            except Exception as e:
                                logger.warning(f"Failed to load manifest from {server_dir}: {e}")
    
    async def _validate_server(self, server_config: Dict) -> bool:
        """Validate that an MCP server is accessible.
        
        Args:
            server_config: Server configuration dictionary
            
        Returns:
            True if server is accessible, False otherwise
        """
        # Basic validation - can be extended with actual connection test
        required_fields = ["command"] if server_config.get("type") == "stdio" else ["url"]
        return all(field in server_config for field in required_fields)
    
    async def _get_server_capabilities(self, server_config: Dict) -> List[str]:
        """Get capabilities of an MCP server.
        
        Args:
            server_config: Server configuration dictionary
            
        Returns:
            List of server capabilities
        """
        capabilities = []
        
        # For stdio servers, we can query capabilities
        if server_config.get("type") == "stdio":
            try:
                result = await self._execute_server_command(
                    server_config.get("command", ""),
                    "--list-tools"
                )
                if result:
                    # Parse tool list from output
                    tools = result.split("\n")
                    capabilities.extend([t.strip() for t in tools if t.strip()])
            except Exception as e:
                logger.warning(f"Failed to get server capabilities: {e}")
        
        return capabilities or ["unknown"]
    
    async def register_mcp_tool(self, tool_name: str, server: str, 
                               tool_definition: Optional[Dict] = None) -> bool:
        """Register an MCP tool for LLM use.
        
        Args:
            tool_name: Name of the tool
            server: Server providing the tool
            tool_definition: Optional tool definition/schema
            
        Returns:
            True if registration successful
        """
        try:
            self.tool_registry[tool_name] = {
                "server": server,
                "definition": tool_definition or {},
                "enabled": True
            }
            logger.info(f"Registered MCP tool: {tool_name} from {server}")
            return True
        except Exception as e:
            logger.error(f"Failed to register MCP tool {tool_name}: {e}")
            return False
    
    async def call_mcp_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool call using proper MCP protocol.

        Args:
            tool_name: Name of the tool to execute
            params: Parameters for the tool

        Returns:
            Tool execution result
        """
        if tool_name not in self.tool_registry:
            return {
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.tool_registry.keys())
            }

        tool_info = self.tool_registry[tool_name]
        server_name = tool_info["server"]

        if not tool_info["enabled"]:
            return {"error": f"Tool '{tool_name}' is disabled"}

        # Get active connection
        connection = self.server_connections.get(server_name)
        if not connection or not connection.initialized:
            # Try to reconnect
            server_config = self.mcp_servers.get(server_name, {})
            command = server_config.get("command")
            if command:
                await self._connect_and_list_tools(server_name, command)
                connection = self.server_connections.get(server_name)

            if not connection or not connection.initialized:
                return {"error": f"No active connection to server '{server_name}'"}

        try:
            result = await connection.call_tool(tool_name, params)
            logger.info(f"Executed MCP tool: {tool_name}")
            return result
        except Exception as e:
            logger.error(f"Failed to execute MCP tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def _execute_stdio_tool(self, server_config: Dict, tool_name: str,
                                 params: Dict) -> Dict[str, Any]:
        """Execute a tool via stdio MCP server.

        Args:
            server_config: Server configuration
            tool_name: Tool to execute
            params: Tool parameters

        Returns:
            Tool execution result
        """
        command = server_config.get("command", "")
        if not command:
            return {"error": "No command specified for stdio server"}

        # Validate tool_name to prevent command injection
        # Only allow alphanumeric, underscore, hyphen, and dot
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', tool_name):
            return {"error": f"Invalid tool name: {tool_name}"}

        # Build command as list (safer than shell=True)
        # Parse the command string and add tool arguments
        try:
            command_parts = shlex.split(command)
        except ValueError as e:
            return {"error": f"Invalid command format: {e}"}

        command_parts.extend(["--tool", tool_name])

        # Add parameters as JSON input
        input_json = json.dumps(params)

        def run_subprocess():
            """Run subprocess in thread to avoid blocking event loop."""
            return subprocess.run(
                command_parts,
                shell=False,
                input=input_json,
                capture_output=True,
                text=True,
                timeout=30
            )

        try:
            # Run blocking subprocess in executor to not freeze event loop
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, run_subprocess)

            if result.returncode == 0:
                # Try to parse JSON output
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"output": result.stdout}
            else:
                return {"error": result.stderr or f"Tool exited with code {result.returncode}"}

        except subprocess.TimeoutExpired:
            return {"error": "Tool execution timed out"}
        except Exception as e:
            return {"error": f"Failed to execute tool: {e}"}
    
    async def _execute_http_tool(self, server_config: Dict, tool_name: str, 
                                params: Dict) -> Dict[str, Any]:
        """Execute a tool via HTTP MCP server.
        
        Args:
            server_config: Server configuration
            tool_name: Tool to execute
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        # This would implement HTTP-based MCP tool calls
        # For now, return a placeholder
        return {
            "status": "not_implemented",
            "message": "HTTP MCP servers not yet implemented"
        }
    
    async def _execute_server_command(self, command: str, *args) -> Optional[str]:
        """Execute a server command and return output.
        
        Args:
            command: Base command to execute
            *args: Additional arguments
            
        Returns:
            Command output or None if failed
        """
        try:
            full_command = [command] + list(args)
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout
            return None
        except Exception as e:
            logger.warning(f"Failed to execute server command: {e}")
            return None
    
    def list_available_tools(self) -> List[Dict[str, Any]]:
        """List all available MCP tools.

        Returns:
            List of available tools with their information
        """
        tools = []
        for tool_name, tool_info in self.tool_registry.items():
            tools.append({
                "name": tool_name,
                "server": tool_info["server"],
                "enabled": tool_info["enabled"],
                "definition": tool_info.get("definition", {})
            })
        return tools

    def get_tool_definitions_for_api(self) -> List[Dict[str, Any]]:
        """Convert registered MCP tools to API tool schema format.

        Returns generic format that adapters (OpenAI/Anthropic) auto-convert:
        - OpenAI wraps in: {type: "function", function: {...}}
        - Anthropic uses: {name, description, input_schema}

        Returns:
            List of tool definitions in generic API format
        """
        tools = []

        # Add MCP tools from registry
        for tool_name, tool_info in self.tool_registry.items():
            if not tool_info.get("enabled", True):
                continue

            definition = tool_info.get("definition", {})
            tools.append({
                "name": tool_name,
                "description": definition.get("description", f"MCP tool: {tool_name}"),
                "parameters": definition.get("parameters", definition.get("inputSchema", {
                    "type": "object",
                    "properties": {},
                    "required": []
                }))
            })

        # Add built-in file operation tools
        tools.extend(self._get_file_operation_tools())

        logger.debug(f"Prepared {len(tools)} tools for API ({len(self.tool_registry)} MCP + file ops)")
        return tools

    def _get_file_operation_tools(self) -> List[Dict[str, Any]]:
        """Get built-in file operation tool definitions.

        These tools provide file manipulation capabilities that work alongside
        MCP tools. They match the XML-based file operations but as native functions.

        Returns:
            List of file operation tool definitions
        """
        return [
            {
                "name": "file_read",
                "description": "Read content from a file. Use this to examine existing files before editing.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path to read"},
                        "offset": {"type": "integer", "description": "Line offset to start reading from (0-indexed, optional)"},
                        "limit": {"type": "integer", "description": "Number of lines to read (optional)"}
                    },
                    "required": ["file"]
                }
            },
            {
                "name": "file_create",
                "description": "Create a new file with content. Fails if file already exists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path to create"},
                        "content": {"type": "string", "description": "Content to write to the file"}
                    },
                    "required": ["file", "content"]
                }
            },
            {
                "name": "file_create_overwrite",
                "description": "Create or overwrite a file with content. Creates backup if file exists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path to create/overwrite"},
                        "content": {"type": "string", "description": "Content to write to the file"}
                    },
                    "required": ["file", "content"]
                }
            },
            {
                "name": "file_edit",
                "description": "Find and replace text in a file. Replaces ALL occurrences of the pattern.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path to edit"},
                        "find": {"type": "string", "description": "Text pattern to find (exact match)"},
                        "replace": {"type": "string", "description": "Text to replace with"}
                    },
                    "required": ["file", "find", "replace"]
                }
            },
            {
                "name": "file_append",
                "description": "Append content to the end of a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path to append to"},
                        "content": {"type": "string", "description": "Content to append"}
                    },
                    "required": ["file", "content"]
                }
            },
            {
                "name": "file_insert_after",
                "description": "Insert content after a pattern in a file. Pattern must match exactly.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path"},
                        "pattern": {"type": "string", "description": "Pattern to find (exact match)"},
                        "content": {"type": "string", "description": "Content to insert after pattern"}
                    },
                    "required": ["file", "pattern", "content"]
                }
            },
            {
                "name": "file_insert_before",
                "description": "Insert content before a pattern in a file. Pattern must match exactly.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path"},
                        "pattern": {"type": "string", "description": "Pattern to find (exact match)"},
                        "content": {"type": "string", "description": "Content to insert before pattern"}
                    },
                    "required": ["file", "pattern", "content"]
                }
            },
            {
                "name": "file_delete",
                "description": "Delete a file. Creates backup before deletion.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path to delete"}
                    },
                    "required": ["file"]
                }
            },
            {
                "name": "file_move",
                "description": "Move or rename a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string", "description": "Source file path"},
                        "to": {"type": "string", "description": "Destination file path"}
                    },
                    "required": ["from", "to"]
                }
            },
            {
                "name": "file_copy",
                "description": "Copy a file. Fails if destination exists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string", "description": "Source file path"},
                        "to": {"type": "string", "description": "Destination file path"}
                    },
                    "required": ["from", "to"]
                }
            },
            {
                "name": "file_copy_overwrite",
                "description": "Copy a file, overwriting destination if it exists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string", "description": "Source file path"},
                        "to": {"type": "string", "description": "Destination file path"}
                    },
                    "required": ["from", "to"]
                }
            },
            {
                "name": "file_mkdir",
                "description": "Create a directory (including parent directories).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path to create"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "file_rmdir",
                "description": "Remove an empty directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path to remove"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "file_grep",
                "description": "Search for a pattern in a file and return matching lines.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Relative file path to search"},
                        "pattern": {"type": "string", "description": "Text pattern to search for"},
                        "case_insensitive": {"type": "boolean", "description": "Whether to ignore case (default: false)"}
                    },
                    "required": ["file", "pattern"]
                }
            },
            {
                "name": "terminal",
                "description": "Execute a terminal/shell command and return the output.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Shell command to execute"}
                    },
                    "required": ["command"]
                }
            }
        ]
    
    def enable_tool(self, tool_name: str) -> bool:
        """Enable an MCP tool.
        
        Args:
            tool_name: Name of the tool to enable
            
        Returns:
            True if tool was enabled
        """
        if tool_name in self.tool_registry:
            self.tool_registry[tool_name]["enabled"] = True
            logger.info(f"Enabled MCP tool: {tool_name}")
            return True
        return False
    
    def disable_tool(self, tool_name: str) -> bool:
        """Disable an MCP tool.
        
        Args:
            tool_name: Name of the tool to disable
            
        Returns:
            True if tool was disabled
        """
        if tool_name in self.tool_registry:
            self.tool_registry[tool_name]["enabled"] = False
            logger.info(f"Disabled MCP tool: {tool_name}")
            return True
        return False
    
    async def shutdown(self):
        """Shutdown MCP integration and close all server connections."""
        for server_name, connection in self.server_connections.items():
            try:
                await connection.close()
                logger.debug(f"Closed MCP server connection: {server_name}")
            except Exception as e:
                logger.warning(f"Error closing MCP connection {server_name}: {e}")

        self.server_connections.clear()
        self.tool_registry.clear()
        logger.info("MCP Integration shutdown complete")