import os


class Atomic:
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.tmp_file_path = f"{file_path}.tmp"
        self.content = content

    def read(self, default: str = ""):
        if not self.exists():
            return default
        with open(self.file_path) as f:
            return f.read()

    def write(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.tmp_file_path, "w") as f:
            f.write(self.content)
        os.replace(self.tmp_file_path, self.file_path)

    def append(self):
        content = self.read() + self.content
        with open(self.tmp_file_path, "a") as f:
            f.write(content)
        os.replace(self.tmp_file_path, self.file_path)

    def delete(self):
        if not self.exists():
            return
        os.remove(self.file_path)

    def exists(self):
        return os.path.exists(self.file_path)

    def __str__(self):
        return f"<Atomic file='{self.file_path}'>"

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                         ATOMIC HELP                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Atomic provides safe file operations using write-then-rename.    ║
║                                                                   ║
║ METHODS:                                                          ║
║   read(default="")  - Read file content, return default if none  ║
║   write()           - Write content atomically (safe)            ║
║   append()          - Append content to file                     ║
║   delete()          - Delete the file                            ║
║   exists()          - Check if file exists                       ║
║                                                                   ║
║ USAGE:                                                            ║
║   atomic = Atomic("/path/to/file.txt", "content to write")       ║
║   atomic.write()                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
