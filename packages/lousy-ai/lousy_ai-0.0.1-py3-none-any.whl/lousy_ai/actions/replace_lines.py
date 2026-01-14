from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import BaseFile
from typing import List, Dict


class ReplaceLinesAction(BaseAction):
    def __init__(self, file_path: str, start_line: int, end_line: int,
                 new_content: str, reason: str, tokens: List[str], 
                 config, required_params: Dict[str, str] = None):
        super().__init__(file_path, new_content, tokens, required_params)
        self.start_line = start_line
        self.end_line = end_line
        self.reason = reason
        self.config = config
        self._file = BaseFile(file_path, config)

    def pre_execute(self):
        if not self._file.exists():
            print(f"[ERROR] File '{self.file}' not found")
            return

        self._original_content = self._file.read()
        lines = self._file.get_lines()
        old_lines = lines[self.start_line - 1:self.end_line]
        context_before = lines[max(0, self.start_line - 4):self.start_line - 1]
        context_after = lines[self.end_line:min(len(lines), self.end_line + 3)]
        token = self.generate_token()

        print("\n" + "=" * 60)
        print("REPLACE LINES PREVIEW")
        print("=" * 60)
        print(f"Action ID: {self.action_id}")
        print(f"File: {self.file}")
        print(f"Lines: {self.start_line} to {self.end_line}")
        print(f"Reason: {self.reason}")
        if self.required_params:
            print("Required Params:")
            for k, v in self.required_params.items():
                print(f"  {k}: {v}")
        print("-" * 60)
        if context_before:
            print("Context Before:")
            print("".join(context_before))
        print("OLD LINES (will be replaced):")
        print("".join(old_lines))
        print("-" * 60)
        print("NEW LINES:")
        print(self.change)
        print("-" * 60)
        if context_after:
            print("Context After:")
            print("".join(context_after))
        print(f"CONFIRM TOKEN: {token}")
        print("=" * 60)
        print("\nRun execute(token) with the above token to apply this change ONLY IF all above rules have been followed.\n")

    def execute(self, token: str):
        if self._original_content is None:
            self._original_content = self._file.read()

        if not self.validate_token(token):
            print("[ERROR] Invalid token. Content may have changed. Re-run pre_execute().")
            return

        lines = self._file.get_lines()
        new_lines = self.change.splitlines(keepends=True)
        if new_lines and not new_lines[-1].endswith('\n'):
            new_lines[-1] += '\n'

        lines[self.start_line - 1:self.end_line] = new_lines
        self._file.write("".join(lines))
        self._result = {"action": "replace_lines", "file": self.file, "success": True}
        print(f"[SUCCESS] Replaced lines {self.start_line}-{self.end_line} in: {self.file}")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                   REPLACE LINES ACTION HELP                       ║
╠══════════════════════════════════════════════════════════════════╣
║ Replaces specific line ranges in a file.                        ║
║                                                                   ║
║ USAGE:                                                            ║
║   action = ReplaceLinesAction(                                    ║
║       file_path="/path/to/file.py",                              ║
║       start_line=10,                                              ║
║       end_line=15,                                                ║
║       new_content="replacement content",                          ║
║       reason="Why replacing these lines",                        ║
║       tokens=[],                                                  ║
║       config=config,                                              ║
║       required_params={"functions_changed": "modified_func"}     ║
║   )                                                               ║
║   action.pre_execute()    # Shows preview and token              ║
║   action.execute(token)   # Replaces the lines                   ║
╚══════════════════════════════════════════════════════════════════╝
""")
