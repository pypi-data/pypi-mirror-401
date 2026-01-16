# oscalling

**oscalling 2.0** defines a new standard for OS interaction in Python. Designed by **Rheehose (Rhee Creative)**, this package not only wraps the standard `os` module for seamless integration but also introduces advanced capabilities for memory management, leak prevention, and intelligent hardware resource handling.

Built for high-performance and safety, `oscalling` ensures your system operations are fast, secure, and resource-efficient.

---

## 🚀 Features

- **🗂️ Enhanced File System**: Atomic writes, one-liner copies/moves, and smart directory traversal with type safety.
- **⚙️ Process Management**: Run commands, kill processes by name/PID, and manage background tasks easily.
- **🧠 Memory Guard**: Active memory monitoring and automatic garbage collection triggers to prevent leaks.
- **🖥️ Hardware Optimized**: Intelligent resource allocation helpers to query CPU, RAM, and Disk usage.
- **🌍 Environment Control**: Easy get/set for environment variables and PATH manipulation.
- **⚡ Zero Overhead**: Lightweight, typed, and fast.

---

## 📦 Installation

```bash
pip install oscalling
```

---

## 🔧 Quick Start

```python
import oscalling

# Initialize the enhanced OS manager
manager = oscalling.SystemManager()

### 🗂️ File System Operations ###
# Atomic file write (auto-cleanup resources, prevents corruption)
manager.fs.safe_write('log.txt', 'System checked.')
manager.fs.copy('log.txt', 'log_backup.txt')
print(f"File size: {manager.fs.get_size('log.txt', human_readable=True)}")

# Walk directories easily
for root, dirs, files in manager.fs.walk('/tmp'):
    print(f"Scanning: {root}")

### ⚙️ Process Management ###
# Run a shell command easily
result = manager.proc.run("echo 'Hello from oscalling!'")
print(result.stdout)

# Kill a process by name
killed_pids = manager.proc.kill_by_name("chrome")
print(f"Killed processes: {killed_pids}")

### 🧠 Memory & Hardware ###
# Check memory status and optimize if needed
if manager.memory.is_critical(threshold_percent=85):
    freed = manager.memory.optimize()
    print(f"Freed {freed} objects via GC")

# Get hardware stats
stats = manager.hardware.get_stats()
print(f"CPU: {stats['cpu_percent']}%, RAM: {stats['memory_percent']}%")

### 🌍 Environment ###
manager.env.set("MY_APP_MODE", "production")
print(f"App Mode: {manager.env.get('MY_APP_MODE')}")
manager.env.add_path("/usr/local/custom/bin")
```

---

## 📚 API Overview

### `SystemManager`
Central hub for all operations.
- `fs`: FileSystemManager
- `memory`: MemoryManager
- `hardware`: HardwareManager
- `env`: EnvManager
- `proc`: ProcessManager

### FileSystemManager (`manager.fs`)
- `safe_write(path, content)` - Atomic file write
- `safe_read(path)` - Safe file read
- `copy(src, dst)` - Copy files/directories
- `move(src, dst)` - Move files/directories
- `remove(path, recursive=False)` - Delete files/dirs
- `touch(path)` - Create or update file timestamp
- `get_size(path, human_readable=False)` - Get file size
- `walk(path)` - Directory tree traversal
- `chmod(path, mode)` - Change permissions
- `make_executable(path)` - Make file executable

### MemoryManager (`manager.memory`)
- `get_info()` - Current process memory usage
- `is_critical(threshold_percent=90)` - Check if system memory is low
- `optimize()` - Force garbage collection
- `get_system_memory()` - Full system RAM stats

### HardwareManager (`manager.hardware`)
- `get_cpu_info()` - CPU cores, frequency, architecture
- `get_memory_info()` - System RAM stats
- `get_disk_info(path='/')` - Disk usage for path
- `get_stats()` - Quick snapshot of CPU/RAM/Disk load

### EnvManager (`manager.env`)
- `get(key, default=None)` - Get environment variable
- `set(key, value)` - Set environment variable
- `has(key)` - Check if variable exists
- `unset(key)` - Remove variable
- `list_all()` - Get all environment variables
- `add_path(path)` - Append to PATH

### ProcessManager (`manager.proc`)
- `run(command, cwd=None, timeout=None)` - Run command synchronously
- `run_async(command, cwd=None)` - Run command asynchronously
- `kill(pid, force=False)` - Kill process by PID
- `kill_by_name(name)` - Kill all processes by name
- `get_process_list()` - List all running processes

---

## 🆕 What's New in v2.0

- **Modern `pyproject.toml`** - Replaced `setup.py` with PEP 517/518 compliant build system
- **Full Type Hints** - Complete typing support for better IDE integration
- **Enhanced Error Handling** - More robust exception handling across all modules
- **Comprehensive Docstrings** - Full documentation for every method
- **Performance Optimizations** - Improved atomic write logic and resource cleanup

---

## 📄 License

Copyright (c) 2008-2026 Rheehose (Rhee Creative).  
Licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Rheehose (Rhee Creative)**

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🔗 Links

- **Homepage**: [https://github.com/rheehose/oscalling](https://github.com/rheehose/oscalling)
- **PyPI**: [https://pypi.org/project/oscalling/](https://pypi.org/project/oscalling/)
- **Issues**: [https://github.com/rheehose/oscalling/issues](https://github.com/rheehose/oscalling/issues)
