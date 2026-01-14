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
                "action_id": record.get("action_id"),
                "task_id": record.get("task_id")
            })

        print("\n" + "=" * 60)
        print("CHANGELOG (User Review)")
        print("=" * 60)
        
        if task and task.is_active():
            current = task.get_current()
            print(f"Goal: {current.get('goal', 'N/A')}")
            print("-" * 60)

        print(f"Files Affected: {len(files_modified)}")
        for f in sorted(files_modified):
            print(f"  - {f}")

        print(f"\nActions ({len(actions_performed)}):")
        for action in actions_performed[-50:]: 
            tid = f" [{action['task_id']}]" if action.get('task_id') else ""
            print(f"  - {action['action']} on {action['file']}{tid}")
        
        token = Token.generate_token(f"changelog_{len(actions_performed)}")
        print(f"\nToken: {token}")
        print("=" * 60 + "\n")

    def generate_context(self, history, task=None, future=None, notes=None):
        print("\n" + "=" * 60)
        print("AI AGENT HUD (State of Art Context)")
        print("=" * 60)        
        if task and task.is_active():
            current = task.get_current()
            print(f"[TASK] 🟢 ACTIVE | ID: {current.get('id')}")
            print(f"[GOAL] {current.get('goal')}")
            print(f"[SCOPE] {current.get('description')}")
        else:
            print("[TASK] ⚪ IDLE (Start a task with orc.start_task)")

        if future:
            pending = future.get_all_awaiting()
            if pending:
                print(f"\n[QUEUE] {len(pending)} Actions Pending:")
                for p in pending:
                    print(f"  • {p['id']}: {p['action']} on {p['file']}")
                print("  -> USE: orc.preview_pending(id) then orc.confirm_action(token)")

        if notes:
            all_notes = notes.get_all()
            if all_notes:
                print(f"\n[NOTES] {len(all_notes)} Active Notes:")
                for n in all_notes:
                    print(f"  • [{n['category'].upper()}] {n['note']}")

        print("\n[HISTORY] Recent Actions:")
        records = history.get_recent(20)
        count = 0
        current_tid = task.get_current().get("id") if task and task.is_active() else None
        
        found = False
        for r in records:
            if current_tid and r.get("task_id") != current_tid:
                continue
            if count >= 10: break
            print(f"  • {r['action']} -> {r['file']}")
            count += 1
            found = True
        
        if not found:
            print("  (No recent actions for current task)")
            
        print("=" * 60 + "\n")

    @staticmethod
    def help():
        print(r"""
╔══════════════════════════════════════════════════════════════════╗
║                        SUMMARY HELP                               ║
╠══════════════════════════════════════════════════════════════════╣
║ Summary generates human-readable reports of all changes.        ║
║                                                                   ║
║ METHODS:                                                          ║
║   generate(history, task)  - Print summary of all changes       ║
║                                                                   ║
║ The summary includes:                                             ║
║   - All files modified                                           ║
║   - All actions performed with their action IDs                  ║
║   - Required params that were provided                           ║
║   - Current task info                                            ║
║   - Confirmation token                                           ║
╚══════════════════════════════════════════════════════════════════╝
""")
