import os
import shutil
import tempfile

class FileSystemManager:
    """
    Enhanced File System operations.
    Wraps standard os/shutil modules for safer and easier usage.
    """
    def __init__(self):
        pass

    def getcwd(self):
        """Returns the current working directory."""
        return os.getcwd()

    def exists(self, path):
        """Checks if a path exists."""
        return os.path.exists(path)
    
    def mkdir(self, path, exist_ok=True, parents=True):
        """Creates a directory safely."""
        os.makedirs(path, exist_ok=exist_ok) 

    def safe_write(self, path, content, mode='w', encoding='utf-8'):
        """
        Writes content to a file safely. 
        Tries to write to a temp file first, then moves it to destination.
        """
        directory = os.path.dirname(os.path.abspath(path))
        if not os.path.exists(directory):
            self.mkdir(directory)

        # Atomic write pattern
        try:
            fd, temp_path = tempfile.mkstemp(dir=directory, text=('b' not in mode))
            with os.fdopen(fd, mode, encoding=encoding if 'b' not in mode else None) as tmp_file:
                tmp_file.write(content)
            
            # Atomic replace
            shutil.move(temp_path, path)
        except Exception as e:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            raise IOError(f"Failed to write file at {path}: {e}")

    def safe_read(self, path, mode='r', encoding='utf-8'):
        """Reads content from a file safely."""
        if not self.exists(path):
            return None
        
        with open(path, mode, encoding=encoding if 'b' not in mode else None) as f:
            return f.read()

    def remove(self, path, recursive=False):
        """Removes a file or directory."""
        if not self.exists(path):
            return False
            
        if os.path.isdir(path):
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
        else:
            os.remove(path)
        return True

    def list_dir(self, path='.'):
        """Returns a list of files/folders in directory."""
        return os.listdir(path)

    def touch(self, path):
        """Updates the access and modified times of a file, or creates it if it doesn't exist."""
        if self.exists(path):
            os.utime(path, None)
        else:
            open(path, 'a').close()

    def copy(self, src, dst):
        """Copies a file or directory recursively."""
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    def move(self, src, dst):
        """Moves a file or directory."""
        shutil.move(src, dst)

    def rename(self, src, dst):
        """Renames a file or directory."""
        os.rename(src, dst)

    def is_file(self, path):
        """Checks if path is a regular file."""
        return os.path.isfile(path)

    def is_dir(self, path):
        """Checks if path is a directory."""
        return os.path.isdir(path)

    def get_size(self, path, human_readable=False):
        """
        Returns the size of a file.
        If human_readable is True, returns string like '10 MB'.
        """
        size = os.path.getsize(path)
        if not human_readable:
            return size
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def chmod(self, path, mode):
        """Change file permissions. Wrapper for os.chmod."""
        os.chmod(path, mode)

    def make_executable(self, path):
        """Makes a file executable."""
        st = os.stat(path)
        os.chmod(path, st.st_mode | 0o111)

    def walk(self, top, topdown=True):
        """
        Simple generator wrapper for os.walk.
        Yields (root, dirs, files).
        """
        for root, dirs, files in os.walk(top, topdown=topdown):
            yield root, dirs, files

    def join(self, *paths):
        """Joins path components intelligently."""
        return os.path.join(*paths)

    def split(self, path):
        """Splits path into (head, tail)."""
        return os.path.split(path)

    def abspath(self, path):
        """Returns absolute path."""
        return os.path.abspath(path)
