# oscalling

**oscalling** defines a new standard for OS interaction in Python. Designed by **Rheehose (Rhee Creative)**, this package not only wraps the standard `os` module for seamless integration but also introduces advanced capabilities for memory management, leak prevention, and intelligent hardware resource handling.

Built for high-performance and safety, `oscalling` ensures your system operations are fast, secure, and resource-efficient.

## Features

- **Enhanced File System**: One-liner copies, moves, atomic writes, and smart directory traversal.
- **Process Management**: Run commands, kill processes by name, and manage background tasks easily.
- **Memory Guard**: Active memory monitoring and automatic garbage collection triggers to prevent leaks.
- **Hardware Optimized**: Intelligent resource allocation helpers to query and manage system load.
- **Environment Control**: Easy get/set for environment variables and PATH manipulation.
- **Zero Overhead**: Designed to be lightweight and fast.

## Installation

```bash
pip install oscalling
```

## Quick Start

```python
import oscalling

# Initialize the enhanced OS manager
manager = oscalling.SystemManager()

### File System Operations ###
# Safe file operation (auto-cleanup resources)
manager.fs.safe_write('log.txt', 'System checked.')
manager.fs.copy('log.txt', 'log_backup.txt')
print(f"File size: {manager.fs.get_size('log.txt', human_readable=True)}")

### Process Management ###
# Run a shell command easily
result = manager.proc.run("echo 'Hello from oscalling!'")
print(result.stdout)

### Memory & Hardware ###
# Check memory status and optimize if needed
if manager.memory.is_critical():
    manager.memory.optimize()

# Get hardware stats
stats = manager.hardware.get_stats()
print(f"CPU: {stats['cpu_percent']}%, RAM: {stats['memory_percent']}%")

### Environment ###
manager.env.set("MY_APP_MODE", "production")
print(f"App Mode: {manager.env.get('MY_APP_MODE')}")
```

## License

Copyright (c) 2008-2026 Rheehose (Rhee Creative).
Licensed under the [MIT License](LICENSE).

## Author

- **Rheehose (Rhee Creative)**
