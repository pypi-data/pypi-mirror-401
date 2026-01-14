from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import BaseFile
from typing import List, Dict


class CreateAction(BaseAction):
    def __init__(self, file_path: str, content: str, reason: str, tokens: List[str], 
                 config, required_params: Dict[str, str] = None):
        super().__init__(file_path, content, tokens, required_params)
        self.reason = reason
        self.config = config
        self._file = BaseFile(file_path, config)

    def pre_execute(self):
        if self._file.exists():
            print(f"[ERROR] File '{self.file}' already exists")
            return

        self._original_content = ""
        token = self.generate_token()

        print("\n" + "=" * 60)
        print("CREATE FILE PREVIEW")
        print("=" * 60)
        print(f"Action ID: {self.action_id}")
        print(f"File: {self.file}")
        print(f"Reason: {self.reason}")
        if self.required_params:
            print("Required Params:")
            for k, v in self.required_params.items():
                print(f"  {k}: {v}")
        print("-" * 60)
        print("Content Preview:")
        preview = self.change[:500] + "..." if len(self.change) > 500 else self.change
        print(preview)
        print("-" * 60)
        print(f"CONFIRM TOKEN: {token}")
        print("=" * 60)
        print("\nRun execute(token) with the above token to apply this change ONLY IF all above rules have been followed.\n")

    def execute(self, token: str):
        if not self.validate_token(token):
            print("[ERROR] Invalid token. Content may have changed. Re-run pre_execute().")
            return

        self._file.write(self.change)
        self._result = {"action": "create", "file": self.file, "success": True}
        print(f"[SUCCESS] Created file: {self.file}")

    def rollback(self, versioning=None):
        self._file.delete()
        print(f"[ROLLBACK] Deleted created file: {self.file}")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                     CREATE ACTION HELP                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Creates a new file with specified content.                       ║
║                                                                   ║
║ USAGE:                                                            ║
║   action = CreateAction(                                          ║
║       file_path="/path/to/new_file.py",                          ║
║       content="file content here",                                ║
║       reason="Why creating this file",                           ║
║       tokens=[],                                                  ║
║       config=config,                                              ║
║       required_params={"functions_changed": "func1"}             ║
║   )                                                               ║
║   action.pre_execute()    # Shows preview and token              ║
║   action.execute(token)   # Creates the file                     ║
╚══════════════════════════════════════════════════════════════════╝
""")
