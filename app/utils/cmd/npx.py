from pydantic import BaseModel, Field
import subprocess
from typing import Dict, List, Optional, Union, Any
import os

from app.core.logging import LogManager


class NPXCommandRequest(BaseModel):
    """Request model for running an NPX command"""
    command: str = Field(..., description="The NPX command to run")
    args: str = Field("", description="Arguments for the NPX command as a single string")
    env_vars: Dict[str, str] = Field(default_factory=dict, description="Environment variables to set")
    working_dir: Optional[str] = Field(None, description="Working directory for the command")
    stream_output: bool = Field(False, description="Whether to stream output")


class ProcessInfo(BaseModel):
    """Response model for process information"""
    process_id: str
    command: str
    args: str
    status: str
    start_time: str
    pid: int


class NPXRunner:
    """
    NPX Runner class to manage NPX command execution and process tracking
    """
    
    def __init__(self):
        log_manager = LogManager()
        self.logger = log_manager.get_logger("NPX COMMAND")
        
        # Store for active processes
        self.active_processes: Dict[str, subprocess.Popen] = {}

        
    
    async def run_command(self, command: str, args: str, env_vars: Dict[str, str], 
                          working_dir: Optional[str], process_id: str) -> subprocess.Popen:
        """Run an NPX command and store the process"""
        try:
            # Prepare environment
            env = os.environ.copy()
            env.update(env_vars)
            
            # Prepare full command as a string
            full_command_str = f"npx -y {command} {args}"
            
            self.logger.info(f"Starting process {process_id}: {full_command_str}")
            
            # Start the process using shell=True to handle the string command
            process = subprocess.Popen(
                full_command_str,
                cwd=working_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                shell=True
            )
            self.logger.info(f"Process created with PID: {process.pid}")
            
            # Store the process
            self.active_processes[process_id] = process
            
            return process
        except Exception as e:
            self.logger.error(f"Error running command: {str(e)}")
            if process_id in self.active_processes:
                del self.active_processes[process_id]
            raise
