import psutil
import platform
from typing import Dict, Any, Optional

class HardwareManager:
    """
    Interface for hardware monitoring and management.
    Provides easy access to CPU, Memory, and Disk statistics.
    """

    def __init__(self) -> None:
        pass

    def get_cpu_info(self) -> Dict[str, Any]:
        """
        Returns CPU frequency, core counts, and architecture info.

        Returns:
             Dict[str, Any]: A dictionary containing core counts, frequency, architecture, etc.
        """
        freq = psutil.cpu_freq()
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "freq_current": freq.current if freq else None,
            "architecture": platform.machine(),
            "processor": platform.processor()
        }

    def get_memory_info(self) -> Dict[str, Any]:
        """
        Returns simplified system RAM stats (Total, Available, Used).

        Returns:
            Dict[str, Any]: Memory statistics including percentage used.
        """
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }

    def get_disk_info(self, path: str = '/') -> Dict[str, Any]:
        """
        Returns disk usage for the partition containing the given path.
        
        Args:
            path (str): Path to check disk usage for. Default is root '/'.

        Returns:
            Dict[str, Any]: Disk usage stats (total, used, free, percent).
        """
        try:
            disk = psutil.disk_usage(path)
            return {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            }
        except OSError:
            return {"total": 0, "used": 0, "free": 0, "percent": 0.0}

    def get_stats(self) -> Dict[str, float]:
        """
        Returns a quick snapshot of current hardware load.
        
        Returns:
             Dict[str, float]: CPU load %, DRAM usage %, Disk usage %.
        """
        # interval=None returns non-blocking load since last call or system boot
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": self.get_disk_info()['percent']
        }
