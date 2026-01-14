import os
import re
from lousy_ai.config import Config
from lousy_ai.files import Access


class FunctionFinder:
    def __init__(self, config: Config):
        self.config = config
        self.access = Access(config)

    def search_function(self, func_name: str):
        results = []

        for root, dirs, files in os.walk(self.config.base_dir):
            dirs[:] = [d for d in dirs if d not in self.config.exclude_dirs]

            for filename in files:
                if filename in self.config.exclude_files:
                    continue
                if not filename.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java', '.c', '.cpp', '.h')):
                    continue

                file_path = os.path.join(root, filename)

                if not self.access.is_valid(file_path):
                    continue

                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        lines = f.readlines()
                except (IOError, OSError):
                    continue

                for line_num, line in enumerate(lines, 1):
                    if func_name in line:
                        is_def = bool(re.search(rf'^\s*(def|class|async\s+def|function|fn|func)\s+{re.escape(func_name)}\s*[\(:]', line))
                        
                        context_start = max(0, line_num - 2)
                        context_end = min(len(lines), line_num + 2)
                        context = [l.rstrip() for l in lines[context_start:context_end]]
                        
                        results.append({
                            'file': file_path,
                            'line': line_num,
                            'content': line.rstrip(),
                            'is_definition': is_def,
                            'context': context,
                            'context_start': context_start + 1
                        })

        return results

    def verify_and_print(self, func_names_str: str):
        func_names = [f.strip() for f in func_names_str.split(',') if f.strip()]
        
        if not func_names:
            return

        print("\n" + "=" * 70)
        print("FUNCTION REFERENCES (definitions + usages)")
        print("=" * 70)

        for func_name in func_names:
            results = self.search_function(func_name)
            
            definitions = [r for r in results if r['is_definition']]
            usages = [r for r in results if not r['is_definition']]

            print(f"\n{'─' * 70}")
            print(f"📌 {func_name}")
            print(f"{'─' * 70}")

            if not results:
                print("   No occurrences found in codebase")
                continue

            if definitions:
                print(f"\n   DEFINITIONS ({len(definitions)}):")
                for r in definitions:
                    rel_path = os.path.relpath(r['file'], self.config.base_dir)
                    print(f"   → {rel_path}:{r['line']}")
                    for i, ctx_line in enumerate(r['context'], start=r['context_start']):
                        marker = ">>>" if i == r['line'] else "   "
                        print(f"      {marker} {i}: {ctx_line}")

            if usages:
                print(f"\n   USAGES ({len(usages)}):")
                for r in usages[:15]:
                    rel_path = os.path.relpath(r['file'], self.config.base_dir)
                    print(f"   → {rel_path}:{r['line']}: {r['content'].strip()}")
                if len(usages) > 15:
                    print(f"   ... and {len(usages) - 15} more usages")

        print("\n" + "=" * 70 + "\n")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                    FUNCTION FINDER HELP                           ║
╠══════════════════════════════════════════════════════════════════╣
║ Searches codebase for ALL occurrences of function names.        ║
║                                                                   ║
║ SHOWS:                                                            ║
║   - DEFINITIONS: Where the function is defined (with context)   ║
║   - USAGES: Where the function is called/referenced             ║
║                                                                   ║
║ This helps AI verify:                                            ║
║   1. The function exists                                         ║
║   2. Where it's defined and used                                 ║
║   3. If there are multiple definitions (potential conflict)     ║
╚══════════════════════════════════════════════════════════════════╝
""")
