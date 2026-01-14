from lousy_ai.rulesets.base_rule import BaseRule, Rule
from lousy_ai.config import Config


class Ruler(BaseRule):
    def __init__(self, config: Config):
        super().__init__(config)

    def add(self, rule: Rule):
        if rule.rule_type not in self.rules:
            self.rules[rule.rule_type] = []
        self.rules[rule.rule_type].append(rule)
        self._save()
        print(f"[RULER] Added rule: {rule.name} ({rule.rule_type})")

    def remove(self, name: str):
        for rule_type in self.rules:
            self.rules[rule_type] = [r for r in self.rules[rule_type] if r.name != name]
        self._save()
        print(f"[RULER] Removed rule: {name}")

    def list_rules(self):
        print("\n╔══════════════════════════════════════════════════════════════════╗")
        print("║                       ACTIVE RULES                                ║")
        print("╠══════════════════════════════════════════════════════════════════╣")
        for rule_type, rules in self.rules.items():
            if rules:
                print(f"║ {rule_type.upper()}:")
                for rule in rules:
                    print(f"║   - {rule.name}: {rule.description}")
        print("╚══════════════════════════════════════════════════════════════════╝\n")

    def clear(self):
        self.rules = {"require": [], "follow": [], "avoid": []}
        self._save()
        print("[RULER] Cleared all rules")

    def get_required_params(self):
        return [r.name for r in self.rules.get("require", [])]

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                         RULER HELP                                ║
╠══════════════════════════════════════════════════════════════════╣
║ Ruler manages rules that AI must follow when making changes.     ║
║                                                                   ║
║ METHODS:                                                          ║
║   add(rule)       - Add a new rule                               ║
║   remove(name)    - Remove a rule by name                        ║
║   list_rules()    - Show all active rules                        ║
║   clear()         - Remove all rules                             ║
║                                                                   ║
║ EXAMPLE - Adding a require rule:                                  ║
║   ruler = Ruler(config)                                           ║
║   ruler.add(Rule(                                                 ║
║       name="functions_changed",                                   ║
║       description="Names of functions affected by this change",  ║
║       rule_type="require"                                         ║
║   ))                                                              ║
║                                                                   ║
║ Now ALL actions must include:                                     ║
║   required_params={"functions_changed": "func1, func2"}          ║
╚══════════════════════════════════════════════════════════════════╝
""")
