import os
import shutil
from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import Access, Atomic


class MoveAction(BaseAction):
    def __init__(self, source_path: str, dest_path: str, reason: str, 
                 refs: list, config, required_params: dict = None):
        super().__init__(source_path, dest_path, refs, required_params)
        self.source = source_path
        self.dest = dest_path
        self.reason = reason
        self.config = config
        self._access = Access(config)

    def pre_execute(self):
        print("\n" + "=" * 60)
        print("MOVE/RENAME FILE PREVIEW")
        print("=" * 60)
        print(f"Action ID: {self.action_id}")
        print(f"Source: {self.source}")
        print(f"Destination: {self.dest}")
        print(f"Reason: {self.reason}")
        if self.required_params:
            print("Required Params:")
            for k, v in self.required_params.items():
                print(f"  {k}: {v}")
        print("-" * 60)

        if not os.path.exists(self.source):
            print(f"[ERROR] Source does not exist: {self.source}")
            return

        if os.path.exists(self.dest):
            print(f"[WARNING] Destination exists and will be overwritten: {self.dest}")

        if os.path.isfile(self.source):
            print(f"Type: File")
            try:
                with open(self.source, 'r', errors='ignore') as f:
                    lines = f.readlines()
                print(f"Lines: {len(lines)}")
            except:
                pass
        else:
            print(f"Type: Directory")

        print("-" * 60)
        print(f"CONFIRM TOKEN: {self.generate_token()}")
        print("=" * 60)
        print("\nRun execute(token) with the above token to apply this change ONLY IF all above rules have been followed.")

    def execute(self, token: str = None):
        if not self._access.is_valid(self.source):
            print(f"[ERROR] Source not allowed: {self.source}")
            return
        if not self._access.is_valid(self.dest):
            print(f"[ERROR] Destination not allowed: {self.dest}")
            return

        if not os.path.exists(self.source):
            print(f"[ERROR] Source does not exist: {self.source}")
            return

        try:
            with open(self.source, 'r', errors='ignore') as f:
                self._original_content = f.read()
        except:
            self._original_content = ""

        dest_dir = os.path.dirname(self.dest)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        shutil.move(self.source, self.dest)
        
        self._result = {"action": "move", "source": self.source, "dest": self.dest}
        print(f"[SUCCESS] Moved: {self.source} -> {self.dest}")

    def generate_token(self):
        from lousy_ai.utils import Token
        return Token.generate_token(f"{self.source}:{self.dest}")

    def post_execute(self, history=None, versioning=None):
        if self._result is None:
            return

        if versioning is not None:
            versioning.save_before(self.action_id, self.dest, self._original_content or "")
            try:
                with open(self.dest, 'r') as f:
                    versioning.save_after(self.action_id, self.dest, f.read())
            except:
                pass
            versioning.record(self.action_id, self.dest, "MoveAction", self.required_params)

        record = {
            "action_id": self.action_id,
            "action": "MoveAction",
            "source": self.source,
            "dest": self.dest,
            "required_params": self.required_params,
            "result": self._result
        }
        if history is not None:
            history.record(record)
        print(f"\n[RECORDED] Action {self.action_id} saved to history")

    def rollback(self, versioning=None):
        if os.path.exists(self.dest) and not os.path.exists(self.source):
            shutil.move(self.dest, self.source)
            print(f"[ROLLBACK] Moved back: {self.dest} -> {self.source}")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                      MOVE ACTION HELP                             ║
╠══════════════════════════════════════════════════════════════════╣
║ Moves or renames files and directories.                         ║
║                                                                   ║
║ USAGE:                                                            ║
║   orc.move("old/path.py", "new/path.py", "reason", req_params)  ║
║   orc.rename("file.py", "newname.py", "reason", req_params)     ║
║                                                                   ║
║ EXAMPLES:                                                         ║
║   orc.move("src/old.py", "lib/new.py", "Reorganizing")          ║
║   orc.rename("utils.py", "helpers.py", "Better name")           ║
╚══════════════════════════════════════════════════════════════════╝
""")
