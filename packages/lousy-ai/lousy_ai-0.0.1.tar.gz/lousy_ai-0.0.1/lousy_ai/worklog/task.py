import time
from lousy_ai.utils import Data
from lousy_ai.config import Config
from typing import List, Optional


class Task:
    def __init__(self, config: Config):
        self.config = config
        self.data = Data("task", config.task_path)
        self._task: dict = self._load()

    def _load(self) -> dict:
        return self.data.load()

    def _save(self):
        self.data.save(self._task)

    def start(self, description: str, goal: str) -> str:
        task_id = f"task_{int(time.time() * 1000000)}"
        self._task = {
            "id": task_id,
            "description": description,
            "goal": goal,
            "started_at": time.time(),
            "status": "in_progress",
            "changed_files": [],
            "changed_functions": [],
            "last_action_timestamp": time.time()
        }
        self._save()
        print(f"\n[TASK STARTED] {task_id}")
        print(f"  Description: {description}")
        print(f"  Goal: {goal}\n")
        return task_id

    def update_activity(self):
        if self.is_active():
            self._task["last_action_timestamp"] = time.time()
            self._save()

    def check_timeout(self) -> bool:
        if not self.is_active():
            return False
        
        last = self._task.get("last_action_timestamp", self._task.get("started_at", 0))
        if time.time() - last > 1800:
            return True
        return False

    def add_changed_file(self, file_path: str, action: str):
        if "changed_files" not in self._task:
            self._task["changed_files"] = []
        self._task["changed_files"].append({
            "file": file_path,
            "action": action,
            "timestamp": time.time()
        })
        self.update_activity()
        self._save()

    def add_changed_function(self, file_path: str, function_name: str, action: str):
        if "changed_functions" not in self._task:
            self._task["changed_functions"] = []
        self._task["changed_functions"].append({
            "file": file_path,
            "function": function_name,
            "action": action,
            "timestamp": time.time()
        })
        self.update_activity()
        self._save()

    def complete(self, summary: Optional[str] = None):
        self._task["status"] = "completed"
        self._task["completed_at"] = time.time()
        if summary:
            self._task["summary"] = summary
        self._save()
        print(f"\n[TASK COMPLETED] {self._task.get('id')}")
        print(f"  Files Changed: {len(self._task.get('changed_files', []))}")
        print(f"  Functions Changed: {len(self._task.get('changed_functions', []))}\n")

    def abort(self, reason: Optional[str] = None):
        self._task["status"] = "aborted"
        self._task["aborted_at"] = time.time()
        if reason:
            self._task["abort_reason"] = reason
        self._save()
        print(f"\n[TASK ABORTED] {self._task.get('id')}")
        if reason:
            print(f"  Reason: {reason}\n")

    def get_current(self) -> dict:
        return self._task

    def status(self):
        print("\n" + "=" * 60)
        print("CURRENT TASK STATUS")
        print("=" * 60)
        if not self._task or not self._task.get("id"):
            print("  No active task")
        else:
            print(f"  ID: {self._task.get('id')}")
            print(f"  Status: {self._task.get('status')}")
            print(f"  Description: {self._task.get('description')}")
            print(f"  Goal: {self._task.get('goal')}")
            print(f"  Files Changed: {len(self._task.get('changed_files', []))}")
            print(f"  Functions Changed: {len(self._task.get('changed_functions', []))}")
        print("=" * 60 + "\n")

    def is_active(self) -> bool:
        return self._task.get("status") == "in_progress"

    def clear(self):
        self._task = {}
        self._save()
        print("[TASK] Cleared current task")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                          TASK HELP                                ║
╠══════════════════════════════════════════════════════════════════╣
║ Task tracks the current work session and changed code.           ║
║                                                                   ║
║ METHODS:                                                          ║
║   start(desc, goal)              - Start a new task              ║
║   complete(summary)              - Mark task complete             ║
║   abort(reason)                  - Abort the task                ║
║   add_changed_file(path, action) - Record file change            ║
║   add_changed_function(...)      - Record function change        ║
║   status()                       - Print current task status     ║
║   clear()                        - Clear current task            ║
╚══════════════════════════════════════════════════════════════════╝
""")
