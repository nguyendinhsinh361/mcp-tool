"""
Main entry point for MCP Project.
Runs all available servers concurrently.
"""
import os
import sys
import time
import signal
import multiprocessing
import subprocess
import asyncio
from app.core.config import settings
from app.core.logging import LogManager
from app.servers.mcp.sse.social import SocialServer
from app.servers.mcp.std.base import StdServer
from app.utils.cmd.npx import NPXCommandRequest

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


log_manager = LogManager()
logger = log_manager.get_logger("STD TOOLS")
# Configure logging
log = logger.getChild("main")

# Global flag to track if servers should be running
running = True
# Global storage for processes that aren't managed by multiprocessing
subprocess_processes = []

def run_social_server():
    """Run the Social MCP Server"""
    try:
        log.info("Starting Social Server...")
        server = SocialServer()
        server.run()
    except Exception as e:
        log.error(f"Error in Social Server: {e}")

def run_github_server():
    """Run the Github MCP Server using just-aii-guess package"""
    try:
        log.info("Starting Github Server...")
        github_server = StdServer()
        
        # Créer une requête conforme au modèle NPXCommandRequest
        args = f"--stdio \"npx -y @modelcontextprotocol/server-github GITHUB_PERSONAL_ACCESS_TOKEN={settings.GITHUB_PERSONAL_ACCESS_TOKEN}\" --port {settings.GITHUB_PORT} --baseUrl {settings.IP_HOST}:{settings.GITHUB_PORT} --ssePath /sse"
        
        asyncio.run(github_server.run_npx_command(
            NPXCommandRequest(
                command="just-aii-guess",
                args=args
            )
        ))
        
    except Exception as e:
        log.error(f"Error in Github Server: {e}")

def sigint_handler(signum, frame):
    """Handle CTRL+C signal to gracefully shut down"""
    global running
    log.info("Received shutdown signal, stopping servers...")
    running = False

def display_startup_message(processes, github_process=None):
    """Display a startup message with server information"""
    print("\n" + "=" * 60)
    print("MCP SERVERS RUNNING".center(60))
    print("=" * 60)
    print(f"Social Server: http://{settings.IP_HOST}:{settings.SOCIAL_PORT}")
    print(f"Github Server:  http://{settings.IP_HOST}:{settings.GITHUB_PORT}")
    
    print("-" * 60)
    print("Running Processes:")
    for i, p in enumerate(processes, 1):
        print(f"  {i}. {p.name} (PID: {p.pid})")
    
    # Add GitHub process if it exists
    if github_process and github_process.pid:
        print(f"  {len(processes)+1}. Github Server (PID: {github_process.pid})")
        
    print("-" * 60)
    print("Press Ctrl+C to stop all servers")
    print("=" * 60)

def run_all_servers():
    """Run all available MCP servers concurrently"""
    global running, subprocess_processes
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    
    # Check environment
    if not settings.validate():
        log.error("Environment validation failed. Please check your .env file.")
        return 1
    
    # Start all servers in separate processes
    processes = []
    
    # Start Social Server
    weather_process = multiprocessing.Process(target=run_social_server, name="Socail Server")
    weather_process.daemon = True
    weather_process.start()
    processes.append(weather_process)
    
    # Start Github Server (using subprocess instead of multiprocessing)
    github_process = multiprocessing.Process(target=run_github_server, name="Github Server")
    github_process.daemon = True
    github_process.start()
    processes.append(github_process)
    
    # Wait a moment for servers to start
    time.sleep(2)
    
    # Check if processes are alive
    alive_processes = [p for p in processes if p.is_alive()]
    if len(alive_processes) < len(processes):
        log.error("Some servers failed to start. Check logs for details.")
        for p in processes:
            if not p.is_alive():
                log.error(f"{p.name} failed to start.")
    
    # Display startup message
    display_startup_message(alive_processes)
    
    # Keep the main process running until interrupted
    try:
        while running and any(p.is_alive() for p in processes):
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Keyboard interrupt received, shutting down...")
    finally:
        # Clean up multiprocessing processes
        log.info("Stopping all server processes...")
        for p in processes:
            if p.is_alive():
                log.info(f"Terminating {p.name} (PID: {p.pid})...")
                p.terminate()
        
        # Clean up subprocess processes
        for p in subprocess_processes:
            if p.poll() is None:  # If process is still running
                log.info(f"Terminating subprocess (PID: {p.pid})...")
                p.terminate()
        
        # Wait for processes to terminate
        for p in processes:
            p.join(timeout=5)
        
        # Wait for subprocess processes to terminate
        for p in subprocess_processes:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                log.warning(f"Subprocess (PID: {p.pid}) did not terminate gracefully, killing...")
                p.kill()
        
        # Check if any multiprocessing process is still alive
        for p in processes:
            if p.is_alive():
                log.warning(f"{p.name} (PID: {p.pid}) did not terminate gracefully, killing...")
                p.kill()
        
        log.info("All servers stopped.")
    
    return 0

if __name__ == "__main__":
    sys.exit(run_all_servers())