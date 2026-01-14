import re
from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import BaseFile
from typing import List, Dict


class ReplaceRegexAction(BaseAction):
    def __init__(self, file_path: str, pattern: str, replacement: str,
                 reason: str, tokens: List[str], config, 
                 required_params: Dict[str, str] = None, count: int = 0):
        super().__init__(file_path, f"{pattern}||{replacement}", tokens, required_params)
        self.pattern = pattern
        self.replacement = replacement
        self.count = count
        self.reason = reason
        self.config = config
        self._file = BaseFile(file_path, config)

    def pre_execute(self):
        if not self._file.exists():
            print(f"[ERROR] File '{self.file}' not found")
            return

        self._original_content = self._file.read()

        try:
            compiled = re.compile(self.pattern)
        except re.error as e:
            print(f"[ERROR] Invalid regex pattern: {e}")
            return

        matches = list(compiled.finditer(self._original_content))
        if not matches:
            print(f"[INFO] No matches found for pattern '{self.pattern}'")
            return

        token = self.generate_token()

        print("\n" + "=" * 60)
        print("REPLACE REGEX PREVIEW")
        print("=" * 60)
        print(f"Action ID: {self.action_id}")
        print(f"File: {self.file}")
        print(f"Pattern: {self.pattern}")
        print(f"Replacement: {self.replacement}")
        print(f"Matches Found: {len(matches)}")
        print(f"Reason: {self.reason}")
        if self.required_params:
            print("Required Params:")
            for k, v in self.required_params.items():
                print(f"  {k}: {v}")
        print("-" * 60)
        print("Match Previews (first 10):")
        for i, match in enumerate(matches[:10]):
            start = max(0, match.start() - 20)
            end = min(len(self._original_content), match.end() + 20)
            context = self._original_content[start:end]
            print(f"  {i + 1}: ...{context}...")
        print("-" * 60)
        print(f"CONFIRM TOKEN: {token}")
        print("=" * 60)
        print("\nRun execute(token) with the above token to apply this change ONLY IF all above rules have been followed.\n")

    def execute(self, token: str):
        if self._original_content is None:
            self._original_content = self._file.read()

        if not self.validate_token(token):
            print("[ERROR] Invalid token. Content may have changed. Re-run pre_execute().")
            return

        content = self._file.read()
        new_content = re.sub(self.pattern, self.replacement, content, count=self.count)
        self._file.write(new_content)
        self._result = {"action": "replace_regex", "file": self.file, "success": True}
        print(f"[SUCCESS] Applied regex replacement in: {self.file}")

    @staticmethod
    def help():
        print(r"""
╔══════════════════════════════════════════════════════════════════╗
║                   REPLACE REGEX ACTION HELP                       ║
╠══════════════════════════════════════════════════════════════════╣
║ Replaces content using regex patterns.                           ║
║                                                                   ║
║ USAGE:                                                            ║
║   action = ReplaceRegexAction(                                    ║
║       file_path="/path/to/file.py",                              ║
║       pattern=r"def old_(\w+)",                                   ║
║       replacement=r"def new_\1",                                  ║
║       reason="Renaming functions",                               ║
║       tokens=[],                                                  ║
║       config=config,                                              ║
║       required_params={"functions_changed": "old_*, new_*"},     ║
║       count=0  # 0 = replace all                                 ║
║   )                                                               ║
║   action.pre_execute()    # Shows matches and token              ║
║   action.execute(token)   # Applies replacements                 ║
╚══════════════════════════════════════════════════════════════════╝
""")
