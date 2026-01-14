import os
import shutil
import time
from lousy_ai.actions.base_action import BaseAction
from lousy_ai.files import Access


class RemoveDirAction(BaseAction):
    def __init__(self, dir_path: str, reason: str, refs: list, config, required_params: dict = None):
        super().__init__(dir_path, "", refs, required_params)
        self.dir_path = dir_path
        self.reason = reason
        self.config = config
        self._access = Access(config)
        self._backup_path = None

    def pre_execute(self):
        print("\n" + "=" * 60)
        print("REMOVE DIRECTORY PREVIEW (WITH ROLLBACK SUPPORT)")
        print("=" * 60)
        print(f"Action ID: {self.action_id}")
        print(f"Directory: {self.dir_path}")
        print(f"Reason: {self.reason}")
        if self.required_params:
            print("Required Params:")
            for k, v in self.required_params.items():
                print(f"  {k}: {v}")
        print("-" * 60)

        if not os.path.exists(self.dir_path):
            print(f"[ERROR] Directory does not exist: {self.dir_path}")
            return
        
        if not os.path.isdir(self.dir_path):
            print(f"[ERROR] Path is not a directory: {self.dir_path}")
            return

        print("Backup Plan: Directory will be zipped to .lousy_ai/versioning/backups/ before deletion.")
        print("-" * 60)
        print(f"CONFIRM TOKEN: {self.generate_token()}")
        print("=" * 60)
        print("\nRun execute(token) with the above token to remove this directory.")

    def execute(self, token: str = None):
        if not self._access.is_valid(self.dir_path):
            print(f"[ERROR] Path not allowed: {self.dir_path}")
            return
        
        if not os.path.exists(self.dir_path):
            print(f"[ERROR] Directory does not exist: {self.dir_path}")
            return

        backup_dir = os.path.join(self.config.vcs_dir, "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = int(time.time())
        dirname = os.path.basename(self.dir_path)
        archive_name = f"{dirname}_{self.action_id}_{timestamp}"
        archive_path = os.path.join(backup_dir, archive_name)
        
        try:
            shutil.make_archive(archive_path, 'zip', self.dir_path)
            self._backup_path = archive_path + ".zip"
            print(f"[BACKUP] Directory backed up to: {self._backup_path}")
        except Exception as e:
            print(f"[ERROR] Backup failed: {e}")
            return

        shutil.rmtree(self.dir_path)
        
        self._result = {
            "action": "remove_dir", 
            "path": self.dir_path, 
            "backup": self._backup_path
        }
        print(f"[SUCCESS] Removed directory: {self.dir_path}")

    def generate_token(self):
        from lousy_ai.utils import Token
        return Token.generate_token(f"rmdir:{self.dir_path}")

    def post_execute(self, history=None, versioning=None):
        if self._result is None:
            return

        record = {
            "action_id": self.action_id,
            "action": "RemoveDirAction",
            "path": self.dir_path,
            "required_params": self.required_params,
            "result": self._result,
            "backup_path": self._backup_path
        }
        if history is not None:
            history.record(record)
        print(f"\n[RECORDED] Action {self.action_id} saved to history")

    def rollback(self, versioning=None):
        if not self._backup_path or not os.path.exists(self._backup_path):
             print(f"[ERROR] Backup not found for rollback: {self._backup_path}")
             return

        if os.path.exists(self.dir_path):
            print(f"[WARNING] Directory exists. Removing before restore: {self.dir_path}")
            shutil.rmtree(self.dir_path)

        try:
            shutil.unpack_archive(self._backup_path, self.dir_path)
            print(f"[ROLLBACK] Restored directory from backup: {self.dir_path}")
        except Exception as e:
            print(f"[ERROR] Rollback failed: {e}")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                    REMOVE DIR ACTION HELP                         ║
╠══════════════════════════════════════════════════════════════════╣
║ Removes a directory and all its contents recursively.           ║
║ Automatically creates a ZIP backup for rollback.                 ║
║                                                                   ║
║ USAGE:                                                            ║
║   orc.remove_dir("path/to/dir", "reason", req_params)           ║
║                                                                   ║
║ ROLLBACK:                                                         ║
║   Can be rolled back using orc.rollback(action_id).             ║
╚══════════════════════════════════════════════════════════════════╝
""")
