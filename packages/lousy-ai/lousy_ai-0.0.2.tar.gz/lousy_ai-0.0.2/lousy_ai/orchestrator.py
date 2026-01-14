from lousy_ai.config import Config
from lousy_ai.worklog import History, Future, Task, Summary, Versioning, Notes
from lousy_ai.rulesets import Ruled, Ruler, Rule
from lousy_ai.actions import (
    BaseAction, CreateAction, ReadAction, AppendAction,
    DeleteAction, ReplaceLinesAction, ReplaceRegexAction, SearchAction,
    MoveAction, CopyAction, RemoveDirAction, ListDirAction
)
from lousy_ai.utils import FunctionFinder
from typing import Optional, Dict


class Orchestrator:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.history = History(self.config)
        self.future = Future(self.config)
        self.task = Task(self.config)
        self.summary = Summary(self.config)
        self.versioning = Versioning(self.config)
        self.notes = Notes(self.config)
        self.ruler = Ruler(self.config)
        self.ruled = Ruled(self.config)
        self.function_finder = FunctionFinder(self.config)

    def start_task(self, description: str, goal: str):
        task_id = self.task.start(description, goal)
        if self.config.verbose:
            print("\n" + "=" * 60)
            print("TASK MANAGEMENT PROMPT")
            print("=" * 60)
            print("You have started a new task. To prevent scope creep:")
            print("1. Define the SCOPE of this task explicitly.")
            print("   Example: orc.notes.add('scope', 'Only editing file X, Y')")
            print("2. If > 30 mins pass, I will prompt you to re-check this goal.")
            print("=" * 60 + "\n")
        else:
            print(f"[TASK] {task_id} | Goal: {goal[:50]}... | Run Orchestrator.help() for usage")

    def end_task(self, summary_text: Optional[str] = None):
        self.task.complete(summary_text)
        self.summary.generate_changelog(self.history, self.task)

    def abort_task(self, reason: Optional[str] = None):
        self.task.abort(reason)

    def prepare_action(self, action: BaseAction, extra_data: dict = None):
        if not self.ruled.validate_required_params(action.required_params):
            print("[BLOCKED] Action cannot proceed without required parameters.")
            print("Re-run with required_params dict containing the missing values.\n")
            return

        if self.task.check_timeout():
            current = self.task.get_current()
        if self.task.check_timeout():
            current = self.task.get_current()
            if self.config.verbose:
                print("\n" + "!" * 60)
                print("TIMEOUT WARNING: IT HAS BEEN > 30 Mins SINCE LAST ACTION")
                print("!" * 60)
                print(f"Active Task Goal: {current.get('goal')}")
                print("\nPlease REVIEW your task scope to ensure you haven't drifted.")
                print("If valid, proceed. If drifting, abort or update task.")
                print("!" * 60 + "\n")
            else:
                print(f"[TIMEOUT] >30min idle | Goal: {current.get('goal')[:40]}...")

        if "functions_changed" in action.required_params:
            self.function_finder.verify_and_print(action.required_params["functions_changed"])

        print(self.ruled.prompt())
        action.pre_execute()

        token = action.generate_token()

        self.future.add_awaiting(
            action.__class__.__name__,
            action.file,
            action.change,
            action.reason,
            action.action_id,
            action.required_params,
            extra_data
        )

        pending_count = len(self.future.get_all_awaiting())
        if pending_count > 0:
            if self.config.verbose:
                print(f"\n[QUEUE] Pending Actions: {pending_count}")
                print("View queue: orc.future.list_pending()")
                print("Preview & Get Token: orc.preview_pending('awaiting_...')")
                print("Confirm: orc.confirm_action('TOKEN')")
            else:
                print(f"[QUEUE] {pending_count} pending | Confirm: orc.confirm_action('TOKEN')")
        items = self.future.get_all_awaiting()
        if not items:
            print("[ERROR] No action awaiting confirmation.")
            print("Call an action method like create_file() first.\n")
            return

        matched_action = None
        matched_item = None

        for item in items:
            action_type = item.get("action")
            file_path = item.get("file")
            content = item.get("content")
            reason = item.get("reason")
            action_id = item.get("action_id")
            required_params = item.get("required_params", {})
            extra = item.get("extra", {})

            if action_type == "CreateAction":
                action = CreateAction(file_path, content, reason, [], self.config, required_params)
            elif action_type == "AppendAction":
                action = AppendAction(file_path, content, reason, [], self.config, required_params)
            elif action_type == "DeleteAction":
                action = DeleteAction(file_path, reason, [], self.config, required_params)
                action.change = content
            elif action_type == "ReplaceLinesAction":
                action = ReplaceLinesAction(
                    file_path, extra.get("start_line"), extra.get("end_line"),
                    content, reason, [], self.config, required_params
                )
            elif action_type == "ReplaceRegexAction":
                pattern = extra.get("pattern")
                replacement = content
                prefix = f"{pattern}||"
                if content.startswith(prefix):
                    replacement = content[len(prefix):]

                action = ReplaceRegexAction(
                    file_path, pattern, replacement,
                    reason, [], self.config, required_params
                )
            elif action_type == "MoveAction":
                action = MoveAction(
                    extra.get("source"), extra.get("dest"),
                    reason, [], self.config, required_params
                )
            elif action_type == "CopyAction":
                action = CopyAction(
                    extra.get("source"), extra.get("dest"),
                    reason, [], self.config, required_params
                )
            elif action_type == "RemoveDirAction":
                action = RemoveDirAction(
                    extra.get("dir_path"), reason, [], self.config, required_params
                )
            else:
                continue

            if hasattr(action, '_file') and action._original_content is None:
                pass

            if action.validate_token(token):
                matched_action = action
                matched_item = item
                break

        if not matched_action:
            print("[ERROR] Invalid token or no matching pending action found.")
            return

        action = matched_action
        action._action_id = matched_item.get("action_id")
        action.execute(token)
        self.task.update_activity()

        current_task = self.task.get_current() if self.task.is_active() else None
        task_id = current_task.get("id") if current_task else None

        action.post_execute(self.history, self.versioning, task_id=task_id)

        if self.task.is_active():
            self.task.add_changed_file(action.file, action.__class__.__name__)

        self.future.complete(matched_item['id'])

    def preview_pending(self, pending_id: str):
        items = self.future.get_all_awaiting()
        target_item = next((i for i in items if i["id"] == pending_id), None)

        if not target_item:
            print(f"[ERROR] Pending action not found: {pending_id}")
            return

        item = target_item
        action_type = item.get("action")
        file_path = item.get("file")
        content = item.get("content")
        reason = item.get("reason")
        action_id = item.get("action_id")
        required_params = item.get("required_params", {})
        extra = item.get("extra", {})

        if action_type == "CreateAction":
            action = CreateAction(file_path, content, reason, [], self.config, required_params)
        elif action_type == "AppendAction":
            action = AppendAction(file_path, content, reason, [], self.config, required_params)
        elif action_type == "DeleteAction":
            action = DeleteAction(file_path, reason, [], self.config, required_params)
            action.change = content
        elif action_type == "ReplaceLinesAction":
            action = ReplaceLinesAction(
                file_path, extra.get("start_line"), extra.get("end_line"),
                content, reason, [], self.config, required_params
            )
        elif action_type == "ReplaceRegexAction":
            pattern = extra.get("pattern")
            replacement = content
            prefix = f"{pattern}||"
            if content.startswith(prefix):
                replacement = content[len(prefix):]
            action = ReplaceRegexAction(
                file_path, pattern, replacement,
                reason, [], self.config, required_params
            )
        elif action_type == "MoveAction":
            action = MoveAction(
                extra.get("source"), extra.get("dest"),
                reason, [], self.config, required_params
            )
        elif action_type == "CopyAction":
            action = CopyAction(
                extra.get("source"), extra.get("dest"),
                reason, [], self.config, required_params
            )
        elif action_type == "RemoveDirAction":
            action = RemoveDirAction(
                extra.get("dir_path"), reason, [], self.config, required_params
            )
        else:
            print(f"[ERROR] Unknown action type: {action_type}")
            return

        action._action_id = action_id
        action.pre_execute()

    def cancel_action(self, pending_id: str):
        self.future.cancel(pending_id)

    def clear_pending(self):
        self.future.clear()
        print("[CANCELLED] All pending actions cleared.")

    def update_action(self, pending_id: str, **kwargs):
        self.future.update(pending_id, kwargs)

    def create_file(self, file_path: str, content: str, reason: str,
                    required_params: Dict[str, str] = None):
        action = CreateAction(file_path, content, reason, [], self.config, required_params)
        self.prepare_action(action)

    def read_file(self, file_path: str, start_line: int = None, end_line: int = None):
        action = ReadAction(file_path, self.config, start_line, end_line)
        action.execute()

    def append_to_file(self, file_path: str, content: str, reason: str,
                       required_params: Dict[str, str] = None):
        action = AppendAction(file_path, content, reason, [], self.config, required_params)
        self.prepare_action(action)

    def delete_file(self, file_path: str, reason: str,
                    required_params: Dict[str, str] = None):
        action = DeleteAction(file_path, reason, [], self.config, required_params)
        self.prepare_action(action)

    def remove_dir(self, dir_path: str, reason: str,
                   required_params: Dict[str, str] = None):
        action = RemoveDirAction(dir_path, reason, [], self.config, required_params)
        self.prepare_action(action, {"dir_path": dir_path})

    def replace_lines(self, file_path: str, start_line: int, end_line: int,
                      new_content: str, reason: str,
                      required_params: Dict[str, str] = None):
        action = ReplaceLinesAction(file_path, start_line, end_line, new_content,
                                    reason, [], self.config, required_params)
        self.prepare_action(action, {"start_line": start_line, "end_line": end_line})

    def replace_regex(self, file_path: str, pattern: str, replacement: str,
                      reason: str, required_params: Dict[str, str] = None):
        action = ReplaceRegexAction(file_path, pattern, replacement, reason,
                                    [], self.config, required_params)
        self.prepare_action(action, {"pattern": pattern})

    def list_dir(self, path: str = None, max_depth: int = 3, show_files: bool = True):
        action = ListDirAction(path or self.config.base_dir, self.config, max_depth, show_files)
        action.execute()

    def search(self, pattern: str, path: str = None, is_regex: bool = False):
        action = SearchAction(pattern, self.config, path, is_regex)
        action.execute()

    def copy(self, source: str, dest: str, reason: str,
             required_params: Dict[str, str] = None):
        from lousy_ai.actions.copy import CopyAction
        action = CopyAction(source, dest, reason, [], self.config, required_params)
        self.prepare_action(action, {"source": source, "dest": dest})

    def move(self, source: str, dest: str, reason: str,
             required_params: Dict[str, str] = None):
        from lousy_ai.actions.move import MoveAction
        action = MoveAction(source, dest, reason, [], self.config, required_params)
        self.prepare_action(action, {"source": source, "dest": dest})

    def rename(self, file_path: str, new_name: str, reason: str,
               required_params: Dict[str, str] = None):
        import os
        dir_path = os.path.dirname(file_path)
        dest = os.path.join(dir_path, new_name) if dir_path else new_name
        self.move(file_path, dest, reason, required_params)

    def rollback(self, action_id: str):
        self.history.rollback_to(action_id, self.versioning)

    def show_history(self, count: int = 10):
        self.history.list_action_ids(count)

    def show_summary(self):
        self.summary.generate_changelog(self.history, self.task)

    def show_context(self):
        self.summary.generate_context(self.history, self.task, self.future, self.notes)

    def add_rule(self, name: str, description: str, rule_type: str):
        rule = Rule(name, description, rule_type)
        self.ruler.add(rule)

    def show_rules(self):
        self.ruler.list_rules()

    @staticmethod
    def help():
        print("""
ORCHESTRATOR - AI Code Change Interface
========================================
WORKFLOW: start_task() -> action() -> confirm_action(token) -> end_task()

ACTIONS (require token):
  create_file(path, content, reason, required_params)
  append_to_file(path, content, reason, required_params)
  delete_file(path, reason, required_params)
  replace_lines(path, start, end, content, reason, required_params)
  replace_regex(path, pattern, replacement, reason, required_params)
  move/rename/copy(source, dest, reason, required_params)
  remove_dir(path, reason, required_params)

READ-ONLY (no token): read_file(path) | list_dir(path) | search(pattern)
NOTES: orc.notes.issue/warning/todo/info(msg) | list_notes()
QUEUE: confirm_action(token) | preview_pending(id) | cancel_action(id)
HISTORY: show_history() | rollback(action_id) | versioning.list_versions()
RULES: add_rule(name, desc, type) | show_rules()
""")
