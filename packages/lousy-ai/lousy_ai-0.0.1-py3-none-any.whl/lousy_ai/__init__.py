from lousy_ai.config import Config
from lousy_ai.orchestrator import Orchestrator
from lousy_ai.actions import (
    BaseAction, CreateAction, ReadAction, AppendAction,
    DeleteAction, ReplaceLinesAction, ReplaceRegexAction, SearchAction
)
from lousy_ai.rulesets import Ruled, Ruler, BaseRule, Rule
from lousy_ai.worklog import History, Future, Task, Summary, Versioning, Notes
from lousy_ai.files import Atomic, Access, BaseFile
from lousy_ai.utils import Token, Data

__all__ = [
    "Config",
    "Orchestrator",
    "BaseAction",
    "CreateAction",
    "ReadAction",
    "AppendAction",
    "DeleteAction",
    "ReplaceLinesAction",
    "ReplaceRegexAction",
    "SearchAction",
    "Ruled",
    "Ruler",
    "BaseRule",
    "Rule",
    "History",
    "Future",
    "Task",
    "Summary",
    "Versioning",
    "Notes",
    "Atomic",
    "Access",
    "BaseFile",
    "Token",
    "Data",
    "help",
]


def help():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              LOUSY AI - HELP                                  ║
║            Library for Controlled AI Code Changes                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  QUICK START:                                                                 ║
║    from config_lousy import config                                            ║
║    from lousy_ai import Orchestrator                                          ║
║    orc = Orchestrator(config)                                                 ║
║    Orchestrator.help()    # See all available methods                        ║
║                                                                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  WORKFLOW (multi-run):                                                        ║
║    RUN 1: orc.create_file(...) → prints preview + token                      ║
║    RUN 2: orc.confirm_action("token") → applies change                       ║
║                                                                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ACTIONS (require token confirmation):                                        ║
║    orc.create_file(path, content, reason, required_params)                   ║
║    orc.append_to_file(path, content, reason, required_params)                ║
║    orc.delete_file(path, reason, required_params)                            ║
║    orc.replace_lines(path, start, end, content, reason, required_params)     ║
║    orc.replace_regex(path, pattern, replacement, reason, required_params)    ║
║    orc.move(source, dest, reason, required_params)                           ║
║    orc.rename(path, new_name, reason, required_params)                       ║
║                                                                               ║
║  READ-ONLY (no token needed):                                                 ║
║    orc.read_file(path)              - View file contents                     ║
║    orc.list_dir(path)               - Show directory tree                    ║
║    orc.search(pattern)              - Search in codebase                     ║
║                                                                               ║
║  NOTES (for user review):                                                     ║
║    orc.notes.issue(msg)             - Report problem found                   ║
║    orc.notes.warning(msg)           - Report concern                         ║
║    orc.notes.todo(msg)              - User action needed                     ║
║    orc.notes.list_notes()           - Show all notes                         ║
║                                                                               ║
║  HISTORY:                                                                     ║
║    orc.show_history()               - List action IDs                        ║
║    orc.rollback(action_id)          - Restore to before action               ║
║    orc.versioning.list_versions()   - Show version index                     ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

