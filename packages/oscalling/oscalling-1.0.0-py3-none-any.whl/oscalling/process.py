import subprocess
import os
import signal
import psutil

class ProcessManager:
    """
    Manages system processes and command execution.
    """
    def __init__(self):
        pass

    def run(self, command, cwd=None, capture_output=True, timeout=None):
        """
        Runs a command using subprocess.
        Returns a CompletedProcess instance.
        """
        shell = isinstance(command, str)
        return subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            capture_output=capture_output, 
            text=True, 
            timeout=timeout
        )

    def run_async(self, command, cwd=None):
        """
        Runs a command asynchronously.
        Returns the Popen object.
        """
        shell = isinstance(command, str)
        return subprocess.Popen(
            command,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def kill(self, pid, force=False):
        """Kills a process by PID."""
        try:
            proc = psutil.Process(pid)
            if force:
                proc.kill()
            else:
                proc.terminate()
            return True
        except psutil.NoSuchProcess:
            return False

    def kill_by_name(self, name):
        """Kills all processes matching the given name."""
        file_killed = []
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                self.kill(proc.info['pid'])
                file_killed.append(proc.info['pid'])
        return file_killed

    def get_process_list(self):
        """Returns a list of all running processes."""
        return [p.info for p in psutil.process_iter(['pid', 'name', 'username'])]
