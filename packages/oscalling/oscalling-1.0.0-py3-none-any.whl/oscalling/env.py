import os

class EnvManager:
    """
    Manages Environment Variables.
    """
    def __init__(self):
        self.environ = os.environ

    def get(self, key, default=None):
        """Get an environment variable."""
        return self.environ.get(key, default)

    def set(self, key, value):
        """Set an environment variable."""
        self.environ[key] = str(value)

    def has(self, key):
        """Check if an environment variable exists."""
        return key in self.environ

    def unset(self, key):
        """Remove an environment variable."""
        if key in self.environ:
            del self.environ[key]

    def list_all(self):
        """Return all environment variables as a dict."""
        return dict(self.environ)

    def add_path(self, new_stats_path):
        """Appends a path to the PATH environment variable."""
        current_path = self.get('PATH', '')
        if new_stats_path not in current_path.split(os.pathsep):
            self.set('PATH', f"{current_path}{os.pathsep}{new_stats_path}")
