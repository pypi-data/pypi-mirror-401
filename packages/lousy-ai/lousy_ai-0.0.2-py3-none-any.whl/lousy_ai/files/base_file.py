import os
from lousy_ai.files.atomic import Atomic
from lousy_ai.files.access import Access
from lousy_ai.config import Config


class BaseFile:
    def __init__(self, file_path: str, config: Config):
        self.file_path = os.path.abspath(file_path)
        self.config = config
        self.access = Access(config)
        self._original_content = None

    def _validate(self):
        self.access.validate(self.file_path)

    def read(self, default: str = "") -> str:
        self._validate()
        atomic = Atomic(self.file_path, "")
        content = atomic.read(default)
        if self._original_content is None:
            self._original_content = content
        return content

    def write(self, content: str):
        self._validate()
        if self._original_content is None:
            self._original_content = self.read("")
        atomic = Atomic(self.file_path, content)
        atomic.write()

    def append(self, content: str):
        self._validate()
        if self._original_content is None:
            self._original_content = self.read("")
        atomic = Atomic(self.file_path, content)
        atomic.append()

    def delete(self):
        self._validate()
        if self._original_content is None:
            self._original_content = self.read("")
        atomic = Atomic(self.file_path, "")
        atomic.delete()

    def exists(self) -> bool:
        return os.path.exists(self.file_path)

    def get_lines(self, start: int = None, end: int = None) -> list:
        content = self.read()
        lines = content.splitlines(keepends=True)
        if start is not None and end is not None:
            return lines[start - 1:end]
        elif start is not None:
            return lines[start - 1:]
        return lines

    def get_diff(self) -> str:
        if self._original_content is None:
            return ""
        current = self.read() if self.exists() else ""
        if self._original_content == current:
            return ""

        import difflib
        diff = difflib.unified_diff(
            self._original_content.splitlines(keepends=True),
            current.splitlines(keepends=True),
            fromfile=f"a/{os.path.basename(self.file_path)}",
            tofile=f"b/{os.path.basename(self.file_path)}"
        )
        return "".join(diff)

    def __str__(self):
        return f"<BaseFile path='{self.file_path}'>"

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                       BASE FILE HELP                              ║
╠══════════════════════════════════════════════════════════════════╣
║ BaseFile wraps Atomic with access validation and change tracking.║
║                                                                   ║
║ METHODS:                                                          ║
║   read(default="")       - Read file content                     ║
║   write(content)         - Write content (tracks original)       ║
║   append(content)        - Append content                        ║
║   delete()               - Delete file                           ║
║   exists()               - Check if file exists                  ║
║   get_lines(start, end)  - Get lines (1-indexed)                 ║
║   get_diff()             - Get diff from original                ║
║                                                                   ║
║ USAGE:                                                            ║
║   bf = BaseFile("/path/to/file.py", config)                      ║
║   content = bf.read()                                             ║
║   bf.write("new content")                                         ║
║   print(bf.get_diff())                                            ║
╚══════════════════════════════════════════════════════════════════╝
""")
