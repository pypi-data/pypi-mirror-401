from lousy_ai.utils import Token
from lousy_ai.config import Config


class Summary:
    def __init__(self, config: Config):
        self.config = config

    def generate_changelog(self, history, task=None):
        records = history.get_recent(50)
        files_modified = set()
        actions_performed = []

        current_task_id = None
        if task and task.is_active():
            current_task_id = task.get_current().get("id")

        for record in records:
            if current_task_id and record.get("task_id") != current_task_id:
                continue
            if record.get("file"):
                files_modified.add(record["file"])
            actions_performed.append({
                "action": record.get("action"),
                "file": record.get("file"),
            })

        print(f"\n[CHANGELOG] {len(files_modified)} files | {len(actions_performed)} actions")
        if task and task.is_active():
            print(f"  Goal: {task.get_current().get('goal', 'N/A')[:50]}")
        for f in sorted(files_modified):
            print(f"  • {f}")

    def generate_context(self, history, task=None, future=None, notes=None):
        if task and task.is_active():
            current = task.get_current()
            print(f"[TASK] {current.get('id')} | {current.get('goal')[:50]}")
        else:
            print("[TASK] IDLE | Run orc.start_task(desc, goal)")

        if future:
            pending = future.get_all_awaiting()
            if pending:
                print(f"[QUEUE] {len(pending)} pending")
                for p in pending[:3]:
                    print(f"  • {p['id']}: {p['action']} on {p['file']}")

        if notes:
            all_notes = notes.get_all()
            if all_notes:
                print(f"[NOTES] {len(all_notes)}")
                for n in all_notes[-3:]:
                    print(f"  • [{n['category'].upper()}] {n['note'][:50]}")

        records = history.get_recent(5)
        if records:
            print(f"[HISTORY] Last {len(records)}")
            for r in records:
                print(f"  • {r['action']} -> {r['file']}")

    @staticmethod
    def help():
        print("Summary - generates changelogs and context")
        print("  generate_changelog(history, task) | generate_context(history, task, future, notes)")
