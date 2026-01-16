import psutil
import platform

class HardwareManager:
    """
    Interface for hardware monitoring and management.
    """
    def __init__(self):
        pass

    def get_cpu_info(self):
        """Returns CPU frequency and core counts."""
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "freq_current": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "architecture": platform.machine(),
            "processor": platform.processor()
        }

    def get_memory_info(self):
        """Returns simplified system RAM stats."""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }

    def get_disk_info(self, path='/'):
        """Returns disk usage for the given path."""
        disk = psutil.disk_usage(path)
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }

    def get_stats(self):
        """Returns a snapshot of current hardware load."""
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": self.get_disk_info()['percent']
        }
