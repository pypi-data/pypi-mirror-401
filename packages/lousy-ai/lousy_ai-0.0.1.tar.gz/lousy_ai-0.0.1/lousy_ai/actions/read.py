from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import BaseFile
from typing import Optional


class ReadAction(BaseAction):
    def __init__(self, file_path: str, config, start_line: Optional[int] = None, 
                 end_line: Optional[int] = None):
        super().__init__(file_path, "", [])
        self.config = config
        self.start_line = start_line
        self.end_line = end_line
        self._file = BaseFile(file_path, config)

    def pre_execute(self):
        print("[INFO] Read operations are immediate, no pre-execution needed.")

    def execute(self, token: str = None):
        if not self._file.exists():
            print(f"[ERROR] File '{self.file}' not found")
            return

        lines = self._file.get_lines(self.start_line, self.end_line)
        start = self.start_line or 1

        print("\n" + "=" * 60)
        print(f"FILE: {self.file}")
        print(f"Lines: {start} to {self.end_line or start + len(lines) - 1}")
        print("=" * 60)
        for i, line in enumerate(lines, start=start):
            print(f"{i}: {line.rstrip()}")
        print("=" * 60 + "\n")

        self._result = {"action": "read", "file": self.file, "line_count": len(lines)}

    def post_execute(self, history=None, versioning=None):
        pass

    def rollback(self, versioning=None):
        print("[INFO] Read actions don't need rollback.")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                      READ ACTION HELP                             ║
╠══════════════════════════════════════════════════════════════════╣
║ Reads file contents (read-only, no confirmation needed).        ║
║                                                                   ║
║ USAGE:                                                            ║
║   action = ReadAction(                                            ║
║       file_path="/path/to/file.py",                              ║
║       config=config,                                              ║
║       start_line=10,     # Optional, 1-indexed                   ║
║       end_line=20        # Optional, inclusive                   ║
║   )                                                               ║
║   action.execute()       # Prints file content                   ║
╚══════════════════════════════════════════════════════════════════╝
""")
