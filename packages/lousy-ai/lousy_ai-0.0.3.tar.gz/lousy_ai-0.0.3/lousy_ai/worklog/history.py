import time
from lousy_ai.utils import Data
from lousy_ai.config import Config
from typing import Optional, List


class History:
    def __init__(self, config: Config):
        self.config = config
        self.data = Data("history", config.history_path)
        self._history: List[dict] = self._load()

    def _load(self) -> list:
        data = self.data.load()
        return data.get("records", [])

    def _save(self):
        self.data.save({"records": self._history})

    def record(self, entry: dict) -> str:
        action_id = entry.get("action_id", f"act_{int(time.time() * 1000000)}")
        record = {
            "action_id": action_id,
            "timestamp": time.time(),
            "action": entry.get("action"),
            "file": entry.get("file"),
            "required_params": entry.get("required_params", {}),
            "original_content": entry.get("original_content"),
            "new_content": entry.get("new_content"),
            "result": entry.get("result"),
            "task_id": entry.get("task_id")
        }
        self._history.append(record)
        self._save()
        return action_id

    def get_by_action_id(self, action_id: str) -> Optional[dict]:
        for record in self._history:
            if record.get("action_id") == action_id:
                return record
        return None

    def get_file_history(self, file_path: str) -> List[dict]:
        return [r for r in self._history if r.get("file") == file_path]

    def get_recent(self, count: int = 10) -> List[dict]:
        return self._history[-count:]

    def rollback_to(self, action_id: str, versioning=None):
        record = self.get_by_action_id(action_id)
        if not record:
            print(f"[ERROR] Record not found: {action_id}")
            return

        file_path = record["file"]

        if versioning is not None:
            success = versioning.rollback_to(action_id, file_path)
            if success:
                self.record({
                    "action_id": f"rollback_{int(time.time() * 1000000)}",
                    "action": "rollback",
                    "file": file_path,
                    "result": {"rolled_back_to": action_id}
                })
                print(f"[ROLLBACK] Restored {file_path} to state before {action_id}")
                return

        original = record.get("original_content")
        if original is None:
            print(f"[ERROR] No original content stored for action: {action_id}")
            return

        from lousy_ai.files.atomic import Atomic
        atomic = Atomic(file_path, original)
        atomic.write()

        self.record({
            "action_id": f"rollback_{int(time.time() * 1000000)}",
            "action": "rollback",
            "file": file_path,
            "original_content": record.get("new_content"),
            "new_content": original,
            "result": {"rolled_back_to": action_id}
        })
        print(f"[ROLLBACK] Restored {file_path} to state before {action_id}")

    def list_action_ids(self, count: int = 20):
        print(f"\n[HISTORY] Last {count} actions:")
        for record in self._history[-count:]:
            print(f"  {record.get('action_id')}: {record.get('action')} on {record.get('file')}")

    def clear(self):
        self._history = []
        self._save()
        print("[HISTORY] Cleared")

    def __len__(self):
        return len(self._history)

    @staticmethod
    def help():
        print("History - tracks actions for changelog and rollback")
        print("  record(entry) | get_by_action_id(id) | get_file_history(path)")
        print("  get_recent(count) | list_action_ids(count) | rollback_to(action_id)")
