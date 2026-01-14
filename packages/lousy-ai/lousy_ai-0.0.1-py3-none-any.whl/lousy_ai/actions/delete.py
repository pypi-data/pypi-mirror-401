from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import BaseFile
from typing import List, Dict


class DeleteAction(BaseAction):
    def __init__(self, file_path: str, reason: str, tokens: List[str], 
                 config, required_params: Dict[str, str] = None):
        super().__init__(file_path, "", tokens, required_params)
        self.reason = reason
        self.config = config
        self._file = BaseFile(file_path, config)

    def pre_execute(self):
        if not self._file.exists():
            print(f"[ERROR] File '{self.file}' not found")
            return

        self._original_content = self._file.read()
        self.change = self._original_content
        token = self.generate_token()

        print("\n" + "=" * 60)
        print("DELETE FILE PREVIEW")
        print("=" * 60)
        print(f"Action ID: {self.action_id}")
        print(f"File: {self.file}")
        print(f"Reason: {self.reason}")
        print(f"Lines: {len(self._original_content.splitlines())}")
        if self.required_params:
            print("Required Params:")
            for k, v in self.required_params.items():
                print(f"  {k}: {v}")
        print("-" * 60)
        print("Content Preview (will be DELETED):")
        preview = self._original_content[:500] + "..." if len(self._original_content) > 500 else self._original_content
        print(preview)
        print("-" * 60)
        print(f"CONFIRM TOKEN: {token}")
        print("=" * 60)
        print("\nWARNING: This will DELETE the file permanently!")
        print("Run execute(token) with the above token to delete.\n")

    def execute(self, token: str):
        if not self.validate_token(token):
            print("[ERROR] Invalid token. File may have changed. Re-run pre_execute().")
            return

        self._file.delete()
        self._result = {"action": "delete", "file": self.file, "success": True}
        print(f"[SUCCESS] Deleted file: {self.file}")

    def rollback(self, versioning=None):
        from lousy_ai.files.atomic import Atomic
        atomic = Atomic(self.file, self._original_content)
        atomic.write()
        print(f"[ROLLBACK] Restored deleted file: {self.file}")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                     DELETE ACTION HELP                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Deletes a file (content saved for rollback).                     ║
║                                                                   ║
║ USAGE:                                                            ║
║   action = DeleteAction(                                          ║
║       file_path="/path/to/file.py",                              ║
║       reason="Why deleting this file",                           ║
║       tokens=[],                                                  ║
║       config=config,                                              ║
║       required_params={"functions_changed": "removed_func"}      ║
║   )                                                               ║
║   action.pre_execute()    # Shows preview and token              ║
║   action.execute(token)   # Deletes the file                     ║
╚══════════════════════════════════════════════════════════════════╝
""")
