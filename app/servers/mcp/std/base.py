import uuid
from datetime import datetime
from app.core.logging import LogManager  # Correction de l'import
from app.utils.cmd.npx import NPXCommandRequest, NPXRunner, ProcessInfo  # Import complet
from fastapi import HTTPException, status

class StdServer:
    def __init__(self):
        self.processes = {}
        log_manager = LogManager()
        self.logger = log_manager.get_logger("STD TOOLS")
        self.npx_runner = NPXRunner()
    
    async def run_npx_command(self, request: NPXCommandRequest):
        """Run an NPX command and return the process ID"""
        # Generate a unique ID for this process
        process_id = str(uuid.uuid4())
        
        try:
            # Run the command
            process = await self.npx_runner.run_command(
                request.command,
                request.args,
                request.env_vars,
                request.working_dir,
                process_id
            )
            
            # Store the process in our processes dictionary
            self.processes[process_id] = process
            
            # Return process info
            return ProcessInfo(
                process_id=process_id,
                command=request.command,
                args=request.args,
                status="running",
                start_time=datetime.now().isoformat(),
                pid=process.pid
            )
        except Exception as e:
            self.logger.error(f"Failed to run NPX command: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to run NPX command: {str(e)}"
            )
    
    async def get_process_info(self, process_id: str) -> ProcessInfo:
        """Get information about a running process"""
        if process_id not in self.processes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Process with ID {process_id} not found"
            )
        
        process = self.processes[process_id]
        
        # Check if the process is still running
        if process.returncode is None:
            process_status = "running"
        else:
            process_status = "completed" if process.returncode == 0 else "failed"
        
        # Return the process information
        # Note: We don't have the original command and args here,
        # so you might want to store this information elsewhere
        return ProcessInfo(
            process_id=process_id,
            command="", # Would need to be stored separately
            args="",    # Would need to be stored separately
            status=process_status,
            start_time="", # Would need to be stored separately
            pid=process.pid
        )
    
    async def kill_process(self, process_id: str) -> None:
        """Kill a running process"""
        if process_id not in self.processes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Process with ID {process_id} not found"
            )
        
        process = self.processes[process_id]
        
        # Check if the process is still running
        if process.returncode is None:
            # Kill the process
            process.kill()
            
            # Wait for the process to be killed
            await process.wait()
        
        # Remove the process from the dictionary
        del self.processes[process_id]