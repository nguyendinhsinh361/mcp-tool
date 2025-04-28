import os
import sys
from app.core.logging import LogManager
from app.servers.mcp.sse.social import SocialServer

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


log_manager = LogManager()
logger = log_manager.get_logger("STD TOOLS")
# Configure logging
log = logger.getChild("socail_tool")

def run_social_server():
    """Run the Social MCP Server"""
    try:
        log.info("Starting Social Server...")
        server = SocialServer()
        server.run()
    except Exception as e:
        log.error(f"Error in Social Server: {e}")