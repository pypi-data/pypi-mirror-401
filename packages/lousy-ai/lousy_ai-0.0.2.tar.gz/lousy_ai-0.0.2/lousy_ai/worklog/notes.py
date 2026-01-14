import time
from lousy_ai.utils import Data
from lousy_ai.config import Config
from typing import List


class Notes:
    def __init__(self, config: Config):
        self.config = config
        self.notes_path = config.notes_path
        self.data = Data("notes", self.notes_path)
        self._notes: List[dict] = self._load()

    def _load(self) -> list:
        data = self.data.load()
        return data.get("notes", [])

    def _save(self):
        self.data.save({"notes": self._notes})

    def add(self, note: str, category: str = "info"):
        entry = {
            "id": f"note_{int(time.time() * 1000000)}",
            "note": note,
            "category": category,
            "timestamp": time.time(),
            "timestamp_human": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self._notes.append(entry)
        self._save()
        print(f"[NOTE] {category.upper()}: {note}")

    def issue(self, note: str):
        self.add(note, "issue")

    def warning(self, note: str):
        self.add(note, "warning")

    def info(self, note: str):
        self.add(note, "info")

    def todo(self, note: str):
        self.add(note, "todo")

    def list_notes(self, category: str = None):
        notes = self._notes
        if category:
            notes = [n for n in notes if n.get("category") == category]

        print("\n" + "=" * 60)
        print("AI NOTES FOR USER REVIEW")
        print("=" * 60)
        if not notes:
            print("  No notes")
        else:
            for n in notes:
                icon = {"issue": "[ISSUE]", "warning": "[WARNING]", "info": "[INFO]", "todo": "[TODO]"}.get(n["category"], "[NOTE]")
                print(f"\n  {icon} {n["timestamp_human"]}")
                print(f"     {n['note']}")
        print("\n" + "=" * 60 + "\n")

    def get_all(self) -> List[dict]:
        return self._notes

    def clear(self):
        self._notes = []
        self._save()
        print("[NOTES] Cleared all notes")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                          NOTES HELP                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Notes lets AI leave messages for user review.                    ║
║                                                                   ║
║ METHODS:                                                          ║
║   orc.notes.info(msg)     - General information                  ║
║   orc.notes.warning(msg)  - Something to watch out for           ║
║   orc.notes.issue(msg)    - Problem found during work            ║
║   orc.notes.todo(msg)     - User action needed                   ║
║   orc.notes.list_notes()  - Show all notes                       ║
║   orc.notes.clear()       - Clear all notes                      ║
║                                                                   ║
║ EXAMPLE:                                                          ║
║   orc.notes.issue("Found circular import in module X")           ║
║   orc.notes.todo("Add API key to config before deploying")       ║
╚══════════════════════════════════════════════════════════════════╝
""")
