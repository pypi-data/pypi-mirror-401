import hashlib
import zlib
import json
from pathlib import Path
from datetime import datetime


class PocketGit:
    def __init__(self, repo_path="."):
        self.repo = Path(repo_path)
        self.git = self.repo / ".pocket-git"
        self.objects = self.git / "objects"
        self.refs = self.git / "refs" / "heads"
        self.head = self.git / "HEAD"
        self.index = self.git / "index"

    # ---------------- helpers ----------------

    def _check_repo(self):
        if not self.git.exists():
            raise RuntimeError("Not a Pocket-Git repository")

    def _read_index(self):
        return json.loads(self.index.read_text())

    def _write_index(self, data):
        self.index.write_text(json.dumps(data))

    def get_current_branch(self):
        return self.head.read_text().strip().split("/")[-1]

    def get_current_commit(self):
        branch = self.refs / self.get_current_branch()
        return branch.read_text().strip() if branch.exists() else None

    # ---------------- core ----------------

    def init(self):
        if self.git.exists():
            raise FileExistsError("Repository already exists")

        self.objects.mkdir(parents=True)
        self.refs.mkdir(parents=True)
        self.head.write_text("ref: refs/heads/main\n")
        self.index.write_text("{}")
        return f"Initialized empty Pocket-Git repository in {self.git}"

    def hash_object(self, data, obj_type="blob"):
        header = f"{obj_type} {len(data)}\0".encode()
        store = header + data
        sha = hashlib.sha1(store).hexdigest()

        path = self.objects / sha[:2] / sha[2:]
        path.parent.mkdir(exist_ok=True)
        if not path.exists():
            path.write_bytes(zlib.compress(store))

        return sha

    def add(self, filepath):
        self._check_repo()
        p = Path(filepath)
        if not p.exists():
            raise FileNotFoundError(filepath)

        sha = self.hash_object(p.read_bytes())
        index = self._read_index()
        index[str(p)] = sha
        self._write_index(index)
        return f"Added {filepath}"

    def commit(self, message):
        self._check_repo()
        index = self._read_index()
        if not index:
            raise ValueError("Nothing to commit")

        tree = self.hash_object(json.dumps(index).encode(), "tree")

        commit = {
            "tree": tree,
            "parent": self.get_current_commit(),
            "author": "You",
            "timestamp": datetime.now().isoformat(),
            "message": message,
        }

        sha = self.hash_object(json.dumps(commit).encode(), "commit")
        (self.refs / self.get_current_branch()).write_text(sha)
        self._write_index({})
        return f"[{self.get_current_branch()} {sha[:7]}] {message}", len(index)

    def log(self):
        self._check_repo()
        commits = []
        sha = self.get_current_commit()

        while sha:
            path = self.objects / sha[:2] / sha[2:]
            raw = zlib.decompress(path.read_bytes())
            _, body = raw.split(b"\0", 1)
            data = json.loads(body)
            commits.append((sha, data))
            sha = data["parent"]

        return commits

    def status(self):
        self._check_repo()
        return {
            "branch": self.get_current_branch(),
            "staged": list(self._read_index().keys()),
        }
