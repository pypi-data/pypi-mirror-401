import os
import re
from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import Access
from typing import Optional


class SearchAction(BaseAction):
    def __init__(self, pattern: str, config, path: Optional[str] = None,
                 is_regex: bool = False, case_sensitive: bool = True):
        super().__init__(path or config.base_dir, pattern, [])
        self.pattern = pattern
        self.config = config
        self.search_path = path or config.base_dir
        self.is_regex = is_regex
        self.case_sensitive = case_sensitive
        self._access = Access(config)

    def pre_execute(self):
        print("[INFO] Search operations are immediate, no pre-execution needed.")

    def execute(self, token: str = None):
        results = []
        flags = 0 if self.case_sensitive else re.IGNORECASE

        if self.is_regex:
            try:
                compiled = re.compile(self.pattern, flags)
            except re.error as e:
                print(f"[ERROR] Invalid regex pattern: {e}")
                return

        for root, dirs, files in os.walk(self.search_path):
            dirs[:] = [d for d in dirs if d not in self.config.exclude_dirs]

            for filename in files:
                if filename in self.config.exclude_files:
                    continue

                file_path = os.path.join(root, filename)

                if not self._access.is_valid(file_path):
                    continue

                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        lines = f.readlines()
                except (IOError, OSError):
                    continue

                for line_num, line in enumerate(lines, 1):
                    if self.is_regex:
                        match = compiled.search(line)
                    else:
                        if self.case_sensitive:
                            match = self.pattern in line
                        else:
                            match = self.pattern.lower() in line.lower()

                    if match:
                        results.append((file_path, line_num, line.rstrip()))
                        if len(results) >= 100:
                            break

                if len(results) >= 100:
                    break

            if len(results) >= 100:
                break

        print("\n" + "=" * 60)
        print(f"SEARCH RESULTS: '{self.pattern}'")
        print("=" * 60)
        print(f"Found: {len(results)} matches")
        if len(results) >= 100:
            print("(Results truncated at 100)")
        print("-" * 60)
        for file_path, line_num, content in results:
            rel_path = os.path.relpath(file_path, self.config.base_dir)
            print(f"{rel_path}:{line_num}: {content}")
        print("=" * 60 + "\n")

        self._result = {"action": "search", "count": len(results)}

    def post_execute(self, history=None, versioning=None):
        pass

    def rollback(self, versioning=None):
        print("[INFO] Search actions don't need rollback.")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                     SEARCH ACTION HELP                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Searches for patterns in the codebase (read-only).              ║
║                                                                   ║
║ USAGE:                                                            ║
║   action = SearchAction(                                          ║
║       pattern="function_name",                                    ║
║       config=config,                                              ║
║       path="/specific/path",    # Optional                       ║
║       is_regex=False,           # Set True for regex             ║
║       case_sensitive=True                                         ║
║   )                                                               ║
║   action.execute()              # Prints search results          ║
╚══════════════════════════════════════════════════════════════════╝
""")
