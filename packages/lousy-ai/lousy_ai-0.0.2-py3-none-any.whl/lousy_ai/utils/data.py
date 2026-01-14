from lousy_ai.files.atomic import Atomic
import json


class Data:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    @staticmethod
    def _stringify(data: dict):
        return json.dumps(data, indent=2)

    def save(self, data: dict):
        atomic = Atomic(self.path, self._stringify(data))
        atomic.write()

    def load(self) -> dict:
        return json.loads(Atomic(self.path, content="{}").read(default="{}"))

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                          DATA HELP                                ║
╠══════════════════════════════════════════════════════════════════╣
║ Data provides JSON persistence using Atomic file operations.    ║
║                                                                   ║
║ METHODS:                                                          ║
║   save(data)  - Save dict to JSON file atomically               ║
║   load()      - Load dict from JSON file                         ║
╚══════════════════════════════════════════════════════════════════╝
""")
