import os
import sys
import asyncio
from app.core.config import settings
from app.core.logging import LogManager
from app.servers.mcp.std.base import StdServer
from app.utils.cmd.npx import NPXCommandRequest

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

log_manager = LogManager()
logger = log_manager.get_logger("STD TOOLS")
# Configure logging
log = logger.getChild("github")


async def run_github_server():
    """Run the Github MCP Server using just-aii-guess package"""
    try:
        log.info("Starting Github Server...")
        github_server = StdServer()
        # Example stdio của github chạy npx
        # {
        #     "mcpServers": {
        #         "github": {
        #         "command": "npx",
        #         "args": [
        #             "-y",
        #             "@modelcontextprotocol/server-github"
        #         ],
        #         "env": {
        #             "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
        #         }
        #         }
        #     }
        # }
        
        CMD_GITHUB = "npx"
        ARGS_GITHUB = ["-y", "@modelcontextprotocol/server-github"]
        ENV_GITHUB ={"GITHUB_PERSONAL_ACCESS_TOKEN": settings.GITHUB_PERSONAL_ACCESS_TOKEN}
        
        args = f"--stdio {CMD_GITHUB} {ARGS_GITHUB[0]} {ARGS_GITHUB[1]} --port {settings.GITHUB_PORT} --baseUrl http://{settings.IP_HOST}:{settings.GITHUB_PORT} --ssePath /sse"
        
        await github_server.run_npx_command(
            NPXCommandRequest(
                command="just-aii-guess",
                args=args,
                env_vars=ENV_GITHUB
            )
        )
        
        # Keep the server process running
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        log.error(f"Error in Github Server: {e}")
        
def run_github_server_wrapper():
    """Wrapper to run the async github server in a non-async context"""
    try:
        asyncio.run(run_github_server())
    except Exception as e:
        log.error(f"Github server wrapper error: {e}")