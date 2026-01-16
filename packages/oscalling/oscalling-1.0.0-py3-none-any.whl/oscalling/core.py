import os
import sys
from .fs import FileSystemManager
from .memory import MemoryManager
from .hardware import HardwareManager
from .env import EnvManager
from .process import ProcessManager

class SystemManager:
    """
    Central hub for oscalling functionalities.
    integrates FileSystem, Memory, and Hardware management.
    """
    def __init__(self):
        self.fs = FileSystemManager()
        self.memory = MemoryManager()
        self.hardware = HardwareManager()
        self.env = EnvManager()
        self.proc = ProcessManager()
        self.os = os # Direct access to os module if needed

    def system_info(self):
        """Returns a summary of the current system state."""
        return {
            "platform": sys.platform,
            "memory": self.hardware.get_memory_info(),
            "cpu": self.hardware.get_cpu_info(),
            "cwd": self.fs.getcwd()
        }
