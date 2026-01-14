from lousy_ai.rulesets.base_rule import BaseRule
from lousy_ai.config import Config


class Ruled(BaseRule):
    def __init__(self, config: Config, content=""):
        super().__init__(config, content)

    def _refresh_rules(self):
        self.rules = self._load()

    def get_required_params(self):
        self._refresh_rules()
        return self.rules.get("require", [])

    def prompt(self):
        self._refresh_rules()
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("RULES YOU MUST FOLLOW")
        lines.append("=" * 60)

        follow_rules = self.rules.get("follow", [])
        if follow_rules:
            lines.append("\nFOLLOW these guidelines:")
            for rule in follow_rules:
                lines.append(f"  • {rule.description}")

        require_rules = self.rules.get("require", [])
        if require_rules:
            lines.append("\nREQUIRED PARAMETERS - You MUST provide these:")
            for rule in require_rules:
                lines.append(f"  • {rule.name}: {rule.description}")

        avoid_rules = self.rules.get("avoid", [])
        if avoid_rules:
            lines.append("\nAVOID these patterns:")
            for rule in avoid_rules:
                lines.append(f"  • {rule.description}")

        lines.append("\n" + "=" * 60)
        lines.append("=" * 60 + "\n")

        return "\n".join(lines)

    def validate_required_params(self, params: dict) -> bool:
        self._refresh_rules()
        require_rules = self.rules.get("require", [])
        missing = []
        for rule in require_rules:
            if rule.name not in params or not params[rule.name]:
                missing.append(rule.name)

        if missing:
            print("\n╔══════════════════════════════════════════════════════════════════╗")
            print("║                    MISSING REQUIRED PARAMETERS                    ║")
            print("╠══════════════════════════════════════════════════════════════════╣")
            for name in missing:
                rule = next(r for r in require_rules if r.name == name)
                print(f"║   ✗ {name}: {rule.description}")
            print("╠══════════════════════════════════════════════════════════════════╣")
            print("║ You must provide these in required_params dict                   ║")
            print("╚══════════════════════════════════════════════════════════════════╝\n")
            return False
        return True

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                         RULED HELP                                ║
╠══════════════════════════════════════════════════════════════════╣
║ Ruled enforces rules on AI actions.                             ║
║                                                                   ║
║ METHODS:                                                          ║
║   prompt()                      - Get rules as prompt for AI     ║
║   validate_required_params(p)   - Check if required params given ║
║   get_required_params()         - List of required rule objects  ║
║                                                                   ║
║ WORKFLOW:                                                         ║
║   1. Before action: Show ruled.prompt() to AI                    ║
║   2. AI provides required_params dict with action                ║
║   3. Validate with ruled.validate_required_params(params)        ║
║   4. If invalid, stop and require AI to re-run with params       ║
╚══════════════════════════════════════════════════════════════════╝
""")
