import os
from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import Access
from typing import Optional


class ListDirAction(BaseAction):
    def __init__(self, path: str, config, max_depth: int = 3, show_files: bool = True):
        super().__init__(path, "", [])
        self.config = config
        self.dir_path = path or config.base_dir
        self.max_depth = max_depth
        self.show_files = show_files
        self._access = Access(config)

    def pre_execute(self):
        print("[INFO] ListDir is immediate, no pre-execution needed.")

    def execute(self, token: str = None):
        print("\n" + "=" * 60)
        print(f"DIRECTORY STRUCTURE: {self.dir_path}")
        print("=" * 60)
        
        self._print_tree(self.dir_path, "", 0)
        
        print("=" * 60 + "\n")
        self._result = {"action": "list_dir", "path": self.dir_path}

    def _print_tree(self, path: str, prefix: str, depth: int):
        if depth > self.max_depth:
            return

        try:
            entries = sorted(os.listdir(path))
        except (PermissionError, OSError):
            return

        dirs = []
        files = []
        
        for entry in entries:
            full_path = os.path.join(path, entry)
            if entry in self.config.exclude_dirs or entry.startswith('.'):
                continue
            if os.path.isdir(full_path):
                dirs.append(entry)
            elif self.show_files and entry not in self.config.exclude_files:
                if self._access.is_valid(full_path):
                    files.append(entry)

        all_entries = [(d, True) for d in dirs] + [(f, False) for f in files]
        
        for i, (entry, is_dir) in enumerate(all_entries):
            is_last = i == len(all_entries) - 1
            connector = "└── " if is_last else "├── "
            icon = "📁" if is_dir else "📄"
            
            print(f"{prefix}{connector}{icon} {entry}")
            
            if is_dir:
                extension = "    " if is_last else "│   "
                full_path = os.path.join(path, entry)
                self._print_tree(full_path, prefix + extension, depth + 1)

    def post_execute(self, history=None, versioning=None):
        pass

    def rollback(self, versioning=None):
        print("[INFO] ListDir actions do not need rollback.")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                     LIST DIR ACTION HELP                          ║
╠══════════════════════════════════════════════════════════════════╣
║ Lists directory structure as a tree (read-only).                ║
║                                                                   ║
║ USAGE:                                                            ║
║   orc.list_dir()                  # List from base_dir           ║
║   orc.list_dir("src/")            # List specific path           ║
║   orc.list_dir(max_depth=2)       # Limit depth                  ║
║   orc.list_dir(show_files=False)  # Dirs only                    ║
╚══════════════════════════════════════════════════════════════════╝
""")
