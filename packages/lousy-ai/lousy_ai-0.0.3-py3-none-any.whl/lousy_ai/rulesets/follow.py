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
        
        follow_rules = self.rules.get("follow", [])
        require_rules = self.rules.get("require", [])
        avoid_rules = self.rules.get("avoid", [])
        
        if not (follow_rules or require_rules or avoid_rules):
            return ""
        
        lines.append("\n[RULES]")
        
        if follow_rules:
            follows = ", ".join(r.description for r in follow_rules)
            lines.append(f"  FOLLOW: {follows}")
        
        if require_rules:
            requires = ", ".join(f"{r.name}" for r in require_rules)
            lines.append(f"  REQUIRE: {requires}")
        
        if avoid_rules:
            avoids = ", ".join(r.description for r in avoid_rules)
            lines.append(f"  AVOID: {avoids}")
        
        return "\n".join(lines)

    def validate_required_params(self, params: dict) -> bool:
        self._refresh_rules()
        require_rules = self.rules.get("require", [])
        missing = []
        for rule in require_rules:
            if rule.name not in params or not params[rule.name]:
                missing.append(rule.name)

        if missing:
            print(f"[BLOCKED] Missing required params: {', '.join(missing)}")
            return False
        return True

    @staticmethod
    def help():
        print("Ruled - Enforces rules on AI actions")
        print("  prompt() -> rules prompt | validate_required_params(p) -> check params")
