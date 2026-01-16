import gc
import os
import psutil

class MemoryManager:
    """
    Manages process memory and provides utilities for optimization.
    """
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def get_info(self):
        """Returns current process memory info."""
        mem = self.process.memory_info()
        return {
            "rss": mem.rss, # Resident Set Size
            "vms": mem.vms, # Virtual Memory Size
            "percent": self.process.memory_percent()
        }

    def is_critical(self, threshold_percent=90.0):
        """Checks if memory usage is above a critical threshold."""
        # System wide memory check
        sys_mem = psutil.virtual_memory()
        return sys_mem.percent > threshold_percent

    def optimize(self):
        """
        Force garbage collection to release unreferenced memory.
        Returns the number of unreachable objects found.
        """
        # Explicitly run garbage collection
        unreachable = gc.collect()
        return unreachable

    def get_system_memory(self):
        """Returns system-wide memory statistics."""
        return dict(psutil.virtual_memory()._asdict())
