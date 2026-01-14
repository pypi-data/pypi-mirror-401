import os
import shutil
from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import Access


class CopyAction(BaseAction):
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
        print("COPY FILE/DIR PREVIEW")
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

        dest_dir = os.path.dirname(self.dest)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        if os.path.isdir(self.source):
             if os.path.exists(self.dest):
                 shutil.rmtree(self.dest)
             shutil.copytree(self.source, self.dest)
        else:
             shutil.copy2(self.source, self.dest)
        
        self._result = {"action": "copy", "source": self.source, "dest": self.dest}
        print(f"[SUCCESS] Copied: {self.source} -> {self.dest}")

    def generate_token(self):
        from lousy_ai.utils import Token
        return Token.generate_token(f"{self.source}:{self.dest}")

    def post_execute(self, history=None, versioning=None):
        if self._result is None:
            return

        if versioning is not None:
             versioning.record(self.action_id, self.dest, "CopyAction", self.required_params)

        record = {
            "action_id": self.action_id,
            "action": "CopyAction",
            "source": self.source,
            "dest": self.dest,
            "required_params": self.required_params,
            "result": self._result
        }
        if history is not None:
            history.record(record)
        print(f"\n[RECORDED] Action {self.action_id} saved to history")

    def rollback(self, versioning=None):
        if os.path.exists(self.dest):
            if os.path.isdir(self.dest):
                shutil.rmtree(self.dest)
            else:
                os.remove(self.dest)
            print(f"[ROLLBACK] Removed copy: {self.dest}")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                       COPY ACTION HELP                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Copies files or directories.                                    ║
║                                                                   ║
║ USAGE:                                                            ║
║   orc.copy("source/path", "dest/path", "reason", req_params)    ║
║                                                                   ║
║ EXAMPLES:                                                         ║
║   orc.copy("template.py", "new_script.py", "Starting from tmpl")║
║   orc.copy("assets/", "build/assets/", "Deploying assets")      ║
╚══════════════════════════════════════════════════════════════════╝
""")
