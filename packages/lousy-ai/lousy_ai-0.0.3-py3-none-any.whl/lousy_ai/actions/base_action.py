from typing import List, Optional, Dict
from lousy_ai.utils import Token
import time


class BaseAction:
    def __init__(self, file_path: str, changed_code: str, tokens: List[str], required_params: Dict[str, str] = None, reason: str = None):
        self.file = file_path
        self.change = changed_code
        self.reason = reason
        self.tokens = tokens
        self.required_params = required_params or {}
        self._original_content: Optional[str] = None
        self._result: Optional[dict] = None
        self._action_id: Optional[str] = None

    @property
    def action_id(self) -> str:
        if self._action_id is None:
            self._action_id = f"act_{int(time.time() * 1000000)}"
        return self._action_id

    def pre_execute(self):
        raise NotImplementedError

    def execute(self, token: str = None):
        raise NotImplementedError

    def post_execute(self, history=None, versioning=None, task_id=None):
        if self._result is None:
            raise RuntimeError("post_execute called before execute")

        if versioning is not None:
            if self._original_content is not None:
                versioning.save_before(self.action_id, self.file, self._original_content)
            try:
                versioning.save_after(self.action_id, self.file, self.change)
            except Exception:
                pass

            versioning.record(self.action_id, self.file, self.__class__.__name__, self.required_params)

        record = {
            "action_id": self.action_id,
            "action": self.__class__.__name__,
            "file": self.file,
            "required_params": self.required_params,
            "original_content": self._original_content,
            "new_content": self.change,
            "result": self._result,
            "task_id": task_id
        }
        if history is not None:
            history.record(record)

        print(f"\n[RECORDED] Action {self.action_id} saved to history")

    def rollback(self, versioning=None):
        if versioning is not None and self._action_id is not None:
            success = versioning.rollback_to(self.action_id, self.file)
            if success:
                print(f"[ROLLBACK] Restored {self.file} to state before {self.action_id}")
                return

        if self._original_content is None:
            print("[ERROR] Cannot rollback: no original content stored")
            return

        from lousy_ai.files.atomic import Atomic
        atomic = Atomic(self.file, self._original_content)
        atomic.write()
        print(f"[ROLLBACK] Restored {self.file} to original state")

    def generate_token(self):
        return Token.generate_token(self.change)

    def validate_token(self, token):
        return Token.validate_token(token, self.change)

    def __str__(self):
        return f"{self.__class__.__name__}({self.file}, id={self.action_id})"

    @staticmethod
    def help():
        print("BaseAction - parent class for all file operations")
        print("  Lifecycle: create -> pre_execute() -> execute(token) -> post_execute()")
        print("  Required params: pass via required_params dict")
