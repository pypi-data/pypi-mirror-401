import os
import sys
from typing import Dict, Any

from .fs import FileSystemManager
from .memory import MemoryManager
from .hardware import HardwareManager
from .env import EnvManager
from .process import ProcessManager


class SystemManager:
    """
    Central hub for oscalling functionalities.
    
    Integrates FileSystem, Memory, Hardware, Environment, and Process management
    into a single, easy-to-use interface.
    
    Attributes:
        fs (FileSystemManager): File system operations manager.
        memory (MemoryManager): Memory monitoring and optimization.
        hardware (HardwareManager): Hardware stats and monitoring.
        env (EnvManager): Environment variable management.
        proc (ProcessManager): Process and command execution control.
        os: Direct reference to the `os` module for advanced usage.
    """

    def __init__(self) -> None:
        """Initialize all sub-managers for unified system access."""
        self.fs = FileSystemManager()
        self.memory = MemoryManager()
        self.hardware = HardwareManager()
        self.env = EnvManager()
        self.proc = ProcessManager()
        self.os = os  # Direct access to os module if needed

    def system_info(self) -> Dict[str, Any]:
        """
        Returns a comprehensive summary of the current system state.
        
        Returns:
            Dict[str, Any]: Dictionary containing platform, memory, CPU, and CWD info.
        """
        return {
            "platform": sys.platform,
            "memory": self.hardware.get_memory_info(),
            "cpu": self.hardware.get_cpu_info(),
            "cwd": self.fs.getcwd()
        }
