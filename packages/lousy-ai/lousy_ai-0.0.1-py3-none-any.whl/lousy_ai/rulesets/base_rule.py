from lousy_ai.utils import Data, Token
from lousy_ai.config import Config
from typing import Literal, Dict, List


class Rule:
    def __init__(self, name: str, description: str, rule_type: Literal["require", "follow", "avoid"]):
        self.name = name
        self.description = description
        self.rule_type = rule_type

    def to_dict(self):
        return {"name": self.name, "description": self.description, "rule_type": self.rule_type}

    @staticmethod
    def from_dict(data: dict):
        return Rule(data["name"], data["description"], data["rule_type"])

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                          RULE HELP                                ║
╠══════════════════════════════════════════════════════════════════╣
║ Rules define constraints for AI actions.                         ║
║                                                                   ║
║ RULE TYPES:                                                       ║
║   require - AI MUST provide this parameter in the action         ║
║             Example: functions_changed, reason, tests_affected   ║
║   follow  - AI should follow this guideline                      ║
║   avoid   - AI should avoid this pattern                         ║
║                                                                   ║
║ USAGE:                                                            ║
║   rule = Rule(                                                    ║
║       name="functions_changed",                                   ║
║       description="Names of functions affected by change",       ║
║       rule_type="require"                                         ║
║   )                                                               ║
╚══════════════════════════════════════════════════════════════════╝
""")


class BaseRule:
    def __init__(self, config: Config, content=""):
        self.config = config
        self.data = Data("rules", config.rules_path)
        self.rules: Dict[str, List[Rule]] = self._load()
        self.content = content
        self.token = self.generate_token()

    def _save(self):
        rules_dict = {}
        for rule_type, rules in self.rules.items():
            rules_dict[rule_type] = [r.to_dict() for r in rules]
        return self.data.save(rules_dict)

    def _load(self):
        data = self.data.load()
        rules = {"require": [], "follow": [], "avoid": []}
        for rule_type in rules:
            if rule_type in data:
                rules[rule_type] = [Rule.from_dict(r) for r in data[rule_type]]
        return rules

    def generate_token(self):
        return Token.generate_token(self.content)

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                       BASE RULE HELP                              ║
╠══════════════════════════════════════════════════════════════════╣
║ BaseRule manages loading and saving rules from rules.json.      ║
║ Use Ruler to add/remove rules, Ruled to enforce them.           ║
╚══════════════════════════════════════════════════════════════════╝
""")
