import subprocess
import os
import signal
import psutil
from typing import List, Dict, Any, Optional, Union

class ProcessManager:
    """
    Manages system processes and command execution.
    Provides wrappers around subprocess and psutil for process control.
    """

    def __init__(self) -> None:
        pass

    def run(
        self, 
        command: Union[str, List[str]], 
        cwd: Optional[str] = None, 
        capture_output: bool = True, 
        timeout: Optional[float] = None
    ) -> subprocess.CompletedProcess:
        """
        Runs a command synchronously using subprocess.
        
        Args:
            command (Union[str, List[str]]): Command to run (string for shell, list for direct).
            cwd (Optional[str]): Working directory for the command.
            capture_output (bool): Whether to capture stdout/stderr.
            timeout (Optional[float]): Timeout in seconds.
            
        Returns:
            subprocess.CompletedProcess: The result of the command execution.
            
        Raises:
            subprocess.TimeoutExpired: If timeout is exceeded.
            subprocess.CalledProcessError: If command returns non-zero and check=True.
        """
        shell = isinstance(command, str)
        try:
            return subprocess.run(
                command, 
                cwd=cwd, 
                shell=shell, 
                capture_output=capture_output, 
                text=True, 
                timeout=timeout
            )
        except subprocess.TimeoutExpired as e:
            raise subprocess.TimeoutExpired(e.cmd, e.timeout) from e
        except Exception as e:
            raise RuntimeError(f"Failed to run command: {e}") from e

    def run_async(
        self, 
        command: Union[str, List[str]], 
        cwd: Optional[str] = None
    ) -> subprocess.Popen:
        """
        Runs a command asynchronously (non-blocking).
        
        Args:
            command (Union[str, List[str]]): Command to run.
            cwd (Optional[str]): Working directory.
            
        Returns:
            subprocess.Popen: The Popen object representing the running process.
        """
        shell = isinstance(command, str)
        try:
            return subprocess.Popen(
                command,
                cwd=cwd,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            raise RuntimeError(f"Failed to start async command: {e}") from e

    def kill(self, pid: int, force: bool = False) -> bool:
        """
        Terminates or kills a process by PID.
        
        Args:
            pid (int): Process ID to terminate.
            force (bool): If True, forcefully kills (SIGKILL). If False, gracefully terminates (SIGTERM).
            
        Returns:
            bool: True if the process was found and killed, False otherwise.
        """
        try:
            proc = psutil.Process(pid)
            if force:
                proc.kill()  # SIGKILL
            else:
                proc.terminate()  # SIGTERM
            return True
        except psutil.NoSuchProcess:
            return False
        except psutil.AccessDenied:
            # Process exists but we don't have permission
            return False

    def kill_by_name(self, name: str) -> List[int]:
        """
        Kills all processes matching the given name.
        
        Args:
            name (str): The process name to match.
            
        Returns:
            List[int]: List of PIDs that were terminated.
        """
        pids_killed = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == name:
                    self.kill(proc.info['pid'])
                    pids_killed.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return pids_killed

    def get_process_list(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all running processes with basic info.
        
        Returns:
            List[Dict[str, Any]]: List of process dictionaries containing pid, name, and username.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes
