import time
from lousy_ai.utils import Data
from lousy_ai.config import Config
from typing import List, Optional


class Future:
    def __init__(self, config: Config):
        self.config = config
        self.data = Data("future", config.future_path)
        self._pending: List[dict] = self._load()

    def _load(self) -> list:
        data = self.data.load()
        return data.get("pending", [])

    def _save(self):
        self.data.save({"pending": self._pending})

    def add_awaiting(self, action_type: str, file_path: str, content: str, 
                    reason: str, action_id: str, required_params: dict,
                    extra_data: dict = None):
        entry = {
            "id": f"awaiting_{int(time.time() * 1000000)}",
            "action": action_type,
            "file": file_path,
            "content": content,
            "reason": reason,
            "action_id": action_id,
            "required_params": required_params or {},
            "extra": extra_data or {},
            "status": "awaiting_confirmation"
        }
        self._pending.append(entry)
        self._save()

    def get_all_awaiting(self) -> List[dict]:
        return [e for e in self._pending if e.get("status") == "awaiting_confirmation"]

    def cancel(self, pending_id: str):
        for i, entry in enumerate(self._pending):
            if entry.get("id") == pending_id:
                self._pending[i]["status"] = "cancelled"
                self._save()
                print(f"[FUTURE] Cancelled pending action: {pending_id}")
                return
        print(f"[ERROR] Pending action not found: {pending_id}")

    def complete(self, pending_id: str):
        for i, entry in enumerate(self._pending):
            if entry.get("id") == pending_id:
                self._pending[i]["status"] = "completed"
                self._pending[i]["completed_at"] = time.time()
                self._save()
                return
        print(f"[ERROR] Pending action not found: {pending_id}")

    def update(self, pending_id: str, changes: dict):
        for i, entry in enumerate(self._pending):
            if entry.get("id") == pending_id:
                self._pending[i].update(changes)
                self._save()
                print(f"[FUTURE] Updated action: {pending_id}")
                return
        print(f"[ERROR] Pending action not found: {pending_id}")

    def list_pending(self):
        pending = [e for e in self._pending if e.get("status") in ("pending", "awaiting_confirmation")]
        print("\n" + "=" * 60)
        print("PENDING / AWAITING ACTIONS")
        print("=" * 60)
        if not pending:
            print("  No pending actions")
        else:
            for entry in pending:
                status = entry.get("status")
                print(f"  {entry.get('id')} [{status}]: {entry.get('action')} on {entry.get('file')}")
        print("=" * 60)
        print("To Preview: orc.preview_pending('awaiting_...')")
        print("To Confirm: orc.confirm_action('TOKEN')")
        print("=" * 60 + "\n")

    def clear(self):
        self._pending = []
        self._save()
        print("[FUTURE] Cleared all pending actions")

    def __len__(self):
        return len(self.get_all_awaiting())

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                         FUTURE HELP                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Future tracks pending actions waiting for confirmation.          ║
║                                                                   ║
║ METHODS:                                                          ║
║   add_awaiting(...)      - Add action to confirmation queue       ║
║   get_all_awaiting()     - Get all queued actions                 ║
║   list_pending()         - Print queue with preview instructions  ║
║                                                                   ║
║ QUEUE WORKFLOW:                                                   ║
║   1. Actions are added to queue automatically by orc.prepare...   ║
║   2. View queue: orc.future.list_pending()                        ║
║   3. Preview specific item: orc.preview_pending(id)               ║
║   4. Confirm: orc.confirm_action(token)                           ║
╚══════════════════════════════════════════════════════════════════╝
""")
