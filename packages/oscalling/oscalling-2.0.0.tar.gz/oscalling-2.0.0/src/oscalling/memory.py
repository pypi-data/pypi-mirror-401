import gc
import os
import psutil
from typing import Dict, Any

class MemoryManager:
    """
    Manages process memory and provides utilities for optimization (Garbage Collection).
    """

    def __init__(self) -> None:
        """Initializes the MemoryManager attached to the current process."""
        self.process = psutil.Process(os.getpid())

    def get_info(self) -> Dict[str, Any]:
        """
        Returns memory info for the current process.
        
        Returns:
            Dict[str, Any]: Contains 'rss' (Resident Set Size), 'vms' (Virtual Memory Size), 
            and 'percent' (Memory usage percentage).
        """
        try:
            mem = self.process.memory_info()
            return {
                "rss": mem.rss,
                "vms": mem.vms,
                "percent": self.process.memory_percent()
            }
        except psutil.NoSuchProcess:
            return {"rss": 0, "vms": 0, "percent": 0.0}

    def is_critical(self, threshold_percent: float = 90.0) -> bool:
        """
        Checks if system-wide memory usage is above a critical threshold.
        
        Args:
            threshold_percent (float): The percentage threshold (0-100) to check against.
            
        Returns:
            bool: True if usage > threshold, False otherwise.
        """
        sys_mem = psutil.virtual_memory()
        return sys_mem.percent > threshold_percent

    def optimize(self) -> int:
        """
        Force garbage collection to release unreferenced memory.
        
        This invokes the cyclic garbage collector (gc) manually.
        
        Returns:
            int: The number of unreachable objects found and collected.
        """
        # Explicitly run garbage collection
        unreachable = gc.collect()
        return unreachable

    def get_system_memory(self) -> Dict[str, Any]:
        """
        Returns system-wide memory statistics.
        
        Returns:
            Dict[str, Any]: Dictionary containing total, available, used, etc.
        """
        return dict(psutil.virtual_memory()._asdict())
