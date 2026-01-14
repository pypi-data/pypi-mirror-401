import os
import re
from lousy_ai.config import Config


class Access:
    def __init__(self, config: Config):
        self.config = config

    def validate(self, file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)

        if not abs_path.startswith(self.config.base_dir):
            raise ValueError(f"File '{abs_path}' is outside base directory '{self.config.base_dir}'")

        rel_path = os.path.relpath(abs_path, self.config.base_dir)
        path_parts = rel_path.split(os.sep)
        for excluded in self.config.exclude_dirs:
            if excluded in path_parts:
                raise ValueError(f"File '{abs_path}' is in excluded directory '{excluded}'")

        filename = os.path.basename(abs_path)
        if filename in self.config.exclude_files:
            raise ValueError(f"File '{filename}' is in excluded files list")

        if not os.path.isdir(abs_path) and not re.match(self.config.allowed_files_regex, abs_path):
            raise ValueError(f"File '{abs_path}' does not match allowed pattern")

        return True

    def is_valid(self, file_path: str) -> bool:
        try:
            return self.validate(file_path)
        except ValueError:
            return False

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                         ACCESS HELP                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Access validates file paths against Config rules before          ║
║ allowing any file operations.                                    ║
║                                                                   ║
║ CHECKS PERFORMED:                                                 ║
║   1. File must be within config.base_dir                         ║
║   2. File must not be in config.exclude_dirs                     ║
║   3. File must not be in config.exclude_files                    ║
║   4. File must match config.allowed_files_regex                  ║
║                                                                   ║
║ USAGE:                                                            ║
║   access = Access(config)                                         ║
║   access.validate("/path/to/file.py")  # Raises on invalid       ║
║   access.is_valid("/path/to/file.py")  # Returns bool            ║
╚══════════════════════════════════════════════════════════════════╝
""")
