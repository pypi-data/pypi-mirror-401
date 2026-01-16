import os
import shutil
import tempfile
from typing import List, Union, Optional, Generator, Tuple

class FileSystemManager:
    """
    Enhanced File System operations manager.
    
    Wraps standard `os` and `shutil` modules to provide safer, atomic, 
    and more convenient file manipulations.
    """

    def __init__(self) -> None:
        """Initialize the FileSystemManager."""
        pass

    def getcwd(self) -> str:
        """
        Returns the current working directory.
        
        Returns:
            str: The absolute path to the current working directory.
        """
        return os.getcwd()

    def exists(self, path: str) -> bool:
        """
        Checks if a file or directory exists at the given path.
        
        Args:
            path (str): Path to check.
            
        Returns:
            bool: True if path exists, False otherwise.
        """
        return os.path.exists(path)
    
    def mkdir(self, path: str, exist_ok: bool = True, parents: bool = True) -> None:
        """
        Creates a directory.
        
        Args:
            path (str): The directory path to create.
            exist_ok (bool): If True, suppresses error if directory already exists.
            parents (bool): If True, creates parent directories if they don't exist.
        """
        try:
            if parents:
                os.makedirs(path, exist_ok=exist_ok)
            else:
                os.mkdir(path)
        except OSError as e:
            if not (exist_ok and self.exists(path)):
                raise OSError(f"Failed to create directory '{path}': {e}") from e

    def safe_write(self, path: str, content: Union[str, bytes], mode: str = 'w', encoding: str = 'utf-8') -> None:
        """
        Writes content to a file atomically.
        
        It writes to a temporary file first, then renames it to the destination path.
        This prevents file corruption if the write operation fails midway.
        
        Args:
            path (str): Destination file path.
            content (Union[str, bytes]): Content to write.
            mode (str): Write mode ('w' for text, 'wb' for binary).
            encoding (str): Text encoding (default: 'utf-8'). Ignored in binary mode.
            
        Raises:
            IOError: If writing fails.
        """
        abs_path = os.path.abspath(path)
        directory = os.path.dirname(abs_path)
        
        if not os.path.exists(directory):
            self.mkdir(directory)

        is_binary = 'b' in mode
        temp_file_mode = mode
        
        try:
            # Create a temp file in the same directory to ensure atomic move works across filesystems
            fd, temp_path = tempfile.mkstemp(dir=directory, text=not is_binary)
            
            with os.fdopen(fd, temp_file_mode, encoding=None if is_binary else encoding) as tmp_file:
                tmp_file.write(content)
            
            # Atomic replace
            shutil.move(temp_path, abs_path)
            
        except Exception as e:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            raise IOError(f"Failed to safely write to '{path}': {e}") from e

    def safe_read(self, path: str, mode: str = 'r', encoding: str = 'utf-8') -> Optional[Union[str, bytes]]:
        """
        Reads content from a file safely.
        
        Args:
            path (str): Path to the file.
            mode (str): Read mode ('r' or 'rb').
            encoding (str): Encoding to use for text files.
            
        Returns:
            Optional[Union[str, bytes]]: File content, or None if file does not exist.
        """
        if not self.exists(path):
            return None
        
        try:
            with open(path, mode, encoding=None if 'b' in mode else encoding) as f:
                return f.read()
        except IOError:
            return None

    def remove(self, path: str, recursive: bool = False) -> bool:
        """
        Removes a file or directory.
        
        Args:
            path (str): Path to remove.
            recursive (bool): If True, deletes directories recursively.
            
        Returns:
            bool: True if removal was successful, False if path didn't exist.
        
        Raises:
            OSError: If removal fails due to permissions or lock.
        """
        if not self.exists(path):
            return False
            
        try:
            if os.path.isdir(path):
                if recursive:
                    shutil.rmtree(path)
                else:
                    os.rmdir(path)
            else:
                os.remove(path)
            return True
        except OSError as e:
            raise OSError(f"Failed to remove '{path}': {e}") from e

    def list_dir(self, path: str = '.') -> List[str]:
        """
        Returns a list of names in the given directory.
        
        Args:
            path (str): Directory path.
            
        Returns:
            List[str]: List of file/directory names.
        """
        try:
            return os.listdir(path)
        except OSError as e:
            raise OSError(f"Failed to list directory '{path}': {e}") from e

    def touch(self, path: str) -> None:
        """
        Updates the access and modified times of a file, or creates it if it doesn't exist.
        
        Args:
            path (str): File path.
        """
        try:
            if self.exists(path):
                os.utime(path, None)
            else:
                directory = os.path.dirname(os.path.abspath(path))
                if directory and not self.exists(directory):
                    self.mkdir(directory)
                with open(path, 'a'):
                    pass
        except OSError as e:
            raise OSError(f"Failed to touch '{path}': {e}") from e

    def copy(self, src: str, dst: str) -> None:
        """
        Copies a file or directory recursively.
        
        Args:
            src (str): Source path.
            dst (str): Destination path.
        """
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        except OSError as e:
            raise OSError(f"Failed to copy '{src}' to '{dst}': {e}") from e

    def move(self, src: str, dst: str) -> None:
        """
        Moves a file or directory to a new location.
        
        Args:
            src (str): Source path.
            dst (str): Destination path.
        """
        try:
            shutil.move(src, dst)
        except OSError as e:
            raise OSError(f"Failed to move '{src}' to '{dst}': {e}") from e

    def rename(self, src: str, dst: str) -> None:
        """
        Renames a file or directory.
        
        Args:
            src (str): Current path name.
            dst (str): New path name.
        """
        try:
            os.rename(src, dst)
        except OSError as e:
            raise OSError(f"Failed to rename '{src}' to '{dst}': {e}") from e

    def is_file(self, path: str) -> bool:
        """Checks if path is a regular file."""
        return os.path.isfile(path)

    def is_dir(self, path: str) -> bool:
        """Checks if path is a directory."""
        return os.path.isdir(path)

    def get_size(self, path: str, human_readable: bool = False) -> Union[int, str]:
        """
        Returns the size of a file.
        
        Args:
            path (str): File path.
            human_readable (bool): If True, returns a string like '10.5 MB'.
            
        Returns:
            Union[int, str]: Size in bytes (int) or formatted string.
        """
        try:
            size = os.path.getsize(path)
            if not human_readable:
                return size
            
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024:
                    return f"{size:.2f} {unit}"
                size /= 1024
            return f"{size:.2f} PB"
        except OSError:
            return "0 B" if human_readable else 0

    def chmod(self, path: str, mode: int) -> None:
        """
        Change file permissions.
        
        Args:
            path (str): File path.
            mode (int): Permission mode (e.g., 0o755).
        """
        os.chmod(path, mode)

    def make_executable(self, path: str) -> None:
        """
        Makes a file executable for the current user.
        
        Args:
            path (str): File path.
        """
        try:
            st = os.stat(path)
            os.chmod(path, st.st_mode | 0o111)
        except OSError:
            pass

    def walk(self, top: str, topdown: bool = True) -> Generator[Tuple[str, List[str], List[str]], None, None]:
        """
        Directory tree generator.
        
        Yields:
            Tuple[str, List[str], List[str]]: (dirpath, dirnames, filenames)
        """
        for root, dirs, files in os.walk(top, topdown=topdown):
            yield root, dirs, files

    def join(self, *paths: str) -> str:
        """Joins path components using the OS separator."""
        return os.path.join(*paths)

    def split(self, path: str) -> Tuple[str, str]:
        """Splits path into (head, tail)."""
        return os.path.split(path)

    def abspath(self, path: str) -> str:
        """Returns the absolute path."""
        return os.path.abspath(path)
