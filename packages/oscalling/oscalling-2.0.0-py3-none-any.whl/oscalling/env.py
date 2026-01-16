import os
from typing import Dict, Optional, Any

class EnvManager:
    """
    Manages System Environment Variables with a simplified API.
    """

    def __init__(self) -> None:
        self.environ = os.environ

    def get(self, key: str, default: Optional[Any] = None) -> Optional[str]:
        """
        Get an environment variable.
        
        Args:
            key (str): The environment variable key.
            default (Any): Default value if key is not found.
            
        Returns:
            Optional[str]: The environment variable value or default.
        """
        return self.environ.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set an environment variable. 
        Converts value to string automatically.
        
        Args:
            key (str): The key to set.
            value (Any): The value to assign.
        """
        self.environ[key] = str(value)

    def has(self, key: str) -> bool:
        """
        Check if an environment variable exists.
        
        Args:
            key (str): The key to check.
            
        Returns:
            bool: True if key exists, False otherwise.
        """
        return key in self.environ

    def unset(self, key: str) -> None:
        """
        Remove an environment variable.
        Safe to call even if the key does not exist.
        
        Args:
            key (str): The key to remove.
        """
        if key in self.environ:
            del self.environ[key]

    def list_all(self) -> Dict[str, str]:
        """
        Returns all environment variables as a dictionary.
        
        Returns:
            Dict[str, str]: A copy of environment variables.
        """
        return dict(self.environ)

    def add_path(self, new_stats_path: str) -> None:
        """
        Appends a path to the PATH environment variable for the current process.
        Does not persist after the process ends.
        
        Args:
            new_stats_path (str): The directory path to add.
        """
        current_path = self.get('PATH', '')
        if new_stats_path not in current_path.split(os.pathsep):
            self.set('PATH', f"{current_path}{os.pathsep}{new_stats_path}")
