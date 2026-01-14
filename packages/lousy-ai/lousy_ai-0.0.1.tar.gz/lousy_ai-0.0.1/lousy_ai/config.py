import os
from logging import getLogger

logger = getLogger("LousyAI")


class Config:
    def __init__(self, base_path: str = "./.lousy_ai/", exclude_files=None, exclude_dirs=None,
                 allowed_files_regex=r".*", base_dir=None):
        if exclude_files is None:
            exclude_files = []
        if exclude_dirs is None:
            exclude_dirs = []
        self.base_path = os.path.abspath(base_path)
        self.rules_path = f"{base_path}rules.json"
        self.history_path = f"{base_path}history.json"
        self.tokens_path = f"{base_path}tokens.json"
        self.future_path = f"{base_path}future.json"
        self.notes_path = f"{base_path}notes.json"
        self.task_path = f"{base_path}task.json"
        self.vcs_dir = f"{base_path}versioning/"
        self.allowed_files_regex = allowed_files_regex
        self.exclude_files = ["lousy_config.py"] + exclude_files
        self.base_dir = os.getcwd() if base_dir is None else os.path.abspath(base_dir)
        self.exclude_dirs = [".git", "node_modules", "__pycache__", ".venv", ".idea", ".vscode"] + exclude_dirs
        self.logger = logger

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                         CONFIG HELP                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Config stores all paths and settings for the library.            ║
║                                                                   ║
║ USAGE:                                                            ║
║   config = Config(                                                ║
║       base_path="./.lousy_ai/",     # Where to store lib data    ║
║       base_dir="/path/to/project",  # Project root to work in    ║
║       exclude_files=["secret.py"],  # Files to ignore            ║
║       exclude_dirs=["vendor"],      # Dirs to ignore             ║
║       allowed_files_regex=r".*"     # Pattern for allowed files  ║
║   )                                                               ║
║                                                                   ║
║ PATHS CREATED:                                                    ║
║   - rules.json     : User-defined rules for AI                   ║
║   - history.json   : Changelog of all actions                    ║
║   - future.json    : Pending actions queue                       ║
║   - task.json      : Current task tracking                       ║
║   - versioning/    : File snapshots for rollback                 ║
╚══════════════════════════════════════════════════════════════════╝
""")
