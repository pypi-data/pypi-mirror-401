import os
import time
import hashlib
from lousy_ai.config import Config
from lousy_ai.files.atomic import Atomic
from lousy_ai.utils.data import Data


class Versioning:
    def __init__(self, config: Config):
        self.config = config
        self.vcs_dir = config.vcs_dir
        os.makedirs(self.vcs_dir, exist_ok=True)
        self.index_path = os.path.join(self.vcs_dir, "index.json")
        self.index = Data("vcs_index", self.index_path)
        self._index_data = self._load_index()

    def _load_index(self):
        data = self.index.load()
        if "versions" not in data:
            data["versions"] = []
        return data

    def _save_index(self):
        self.index.save(self._index_data)

    def _get_version_path(self, action_id: str, file_path: str, suffix: str) -> str:
        safe_name = hashlib.md5(file_path.encode()).hexdigest()[:12]
        return os.path.join(self.vcs_dir, f"{action_id}_{safe_name}_{suffix}.snap")

    def save_before(self, action_id: str, file_path: str, content: str):
        version_path = self._get_version_path(action_id, file_path, "before")
        atomic = Atomic(version_path, content)
        atomic.write()

    def save_after(self, action_id: str, file_path: str, content: str):
        version_path = self._get_version_path(action_id, file_path, "after")
        atomic = Atomic(version_path, content)
        atomic.write()

    def record(self, action_id: str, file_path: str, action_type: str, required_params: dict = None):
        entry = {
            "action_id": action_id,
            "file": file_path,
            "action": action_type,
            "timestamp": time.time(),
            "timestamp_human": time.strftime("%Y-%m-%d %H:%M:%S"),
            "required_params": required_params or {}
        }
        self._index_data["versions"].append(entry)
        self._save_index()

    def get_before(self, action_id: str, file_path: str) -> str:
        version_path = self._get_version_path(action_id, file_path, "before")
        atomic = Atomic(version_path, "")
        return atomic.read(default=None)

    def get_after(self, action_id: str, file_path: str) -> str:
        version_path = self._get_version_path(action_id, file_path, "after")
        atomic = Atomic(version_path, "")
        return atomic.read(default=None)

    def rollback_to(self, action_id: str, file_path: str) -> bool:
        before_content = self.get_before(action_id, file_path)
        if before_content is None:
            return False
        atomic = Atomic(file_path, before_content)
        atomic.write()
        return True

    def list_versions(self, file_path: str = None, count: int = 20):
        versions = self._index_data.get("versions", [])
        if file_path:
            versions = [v for v in versions if v.get("file") == file_path]
        versions = versions[-count:]

        print("\n" + "=" * 70)
        print("VERSION INDEX")
        print("=" * 70)
        if not versions:
            print("  No versions recorded")
        else:
            for v in versions:
                rel_path = os.path.relpath(v["file"], self.config.base_dir) if os.path.isabs(v["file"]) else v["file"]
                print(f"\n  [{v['action_id']}]")
                print(f"    File: {rel_path}")
                print(f"    Action: {v['action']}")
                print(f"    Time: {v['timestamp_human']}")
                if v.get("required_params"):
                    for k, val in v["required_params"].items():
                        print(f"    {k}: {val}")
        print("\n" + "=" * 70 + "\n")

    @staticmethod
    def help():
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                       VERSIONING HELP                             ║
╠══════════════════════════════════════════════════════════════════╣
║ Versioning stores file snapshots and maintains an index.        ║
║                                                                   ║
║ INDEX (index.json):                                               ║
║   - action_id, file, action type                                 ║
║   - timestamp (unix + human readable)                            ║
║   - required_params provided                                     ║
║                                                                   ║
║ METHODS:                                                          ║
║   record(action_id, path, type, params) - Add to index          ║
║   list_versions(path, count)            - Print version index   ║
║   rollback_to(action_id, path)          - Restore before state  ║
╚══════════════════════════════════════════════════════════════════╝
""")
