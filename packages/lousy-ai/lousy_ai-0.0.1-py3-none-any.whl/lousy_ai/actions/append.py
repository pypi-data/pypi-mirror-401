from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import BaseFile
from typing import List, Dict


class AppendAction(BaseAction):
    def __init__(self, file_path: str, content: str, reason: str, tokens: List[str], 
                 config, required_params: Dict[str, str] = None):
        super().__init__(file_path, content, tokens, required_params)
        self.reason = reason
        self.config = config
        self._file = BaseFile(file_path, config)

    def pre_execute(self):
        if not self._file.exists():
            print(f"[ERROR] File '{self.file}' not found")
            return

        self._original_content = self._file.read()
        lines = self._file.get_lines()
        last_lines = lines[-5:] if len(lines) >= 5 else lines
        token = self.generate_token()

        print("\n" + "=" * 60)
        print("APPEND TO FILE PREVIEW")
        print("=" * 60)
        print(f"Action ID: {self.action_id}")
        print(f"File: {self.file}")
        print(f"Reason: {self.reason}")
        if self.required_params:
            print("Required Params:")
            for k, v in self.required_params.items():
                print(f"  {k}: {v}")
        print("-" * 60)
        print("Current End of File:")
        print("".join(last_lines))
        print("-" * 60)
        print("Content to Append:")
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

        self._file.append(self.change)
        self._result = {"action": "append", "file": self.file, "success": True}
        print(f"[SUCCESS] Appended content to: {self.file}")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                     APPEND ACTION HELP                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Appends content to an existing file.                             ║
║                                                                   ║
║ USAGE:                                                            ║
║   action = AppendAction(                                          ║
║       file_path="/path/to/file.py",                              ║
║       content="content to append",                                ║
║       reason="Why appending this",                               ║
║       tokens=[],                                                  ║
║       config=config,                                              ║
║       required_params={"functions_changed": "new_func"}          ║
║   )                                                               ║
║   action.pre_execute()    # Shows preview and token              ║
║   action.execute(token)   # Appends the content                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
