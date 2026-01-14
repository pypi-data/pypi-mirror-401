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
LOUSY AI - Controlled AI Code Changes
======================================
QUICK START:
  from config_lousy import config
  from lousy_ai import Orchestrator
  orc = Orchestrator(config)
  orc.start_task("description", "goal")

WORKFLOW: action() -> preview + token -> orc.confirm_action(token)

ACTIONS: create_file | append_to_file | delete_file | replace_lines | replace_regex | move | copy
READ:    read_file | list_dir | search
NOTES:   orc.notes.issue/warning/todo/info(msg)
HISTORY: show_history() | rollback(action_id)

Run Orchestrator.help() for full API reference.
""")
