import sqlite3
import json
from typing import Optional, List, Dict, Any
from promptscope.models.prompt import PromptVersion
from promptscope.utils.time import now_utc
from promptscope.utils.serialization import canonical_json

class SQLiteStorage:
    """
    Production-grade SQLite storage for prompt versions.
    Handles serialization, error handling, and context management.
    """
    def __init__(self, path: str = "promptscope.db"):
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self):
        """
        Ensure the schema exists without destroying existing data.
        In production, a migration strategy should evolve this schema instead of dropping tables.
        """
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prompts (
                prompt_id TEXT,
                version INTEGER,
                content TEXT,
                model TEXT,
                params TEXT,
                hash TEXT,
                created_at TEXT,
                response TEXT,
                response_ms INTEGER,
                cost REAL,
                PRIMARY KEY (prompt_id, version)
            )
            """
        )
        # Table to track active version for each prompt flow
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS active_prompts (
                prompt_id TEXT PRIMARY KEY,
                active_version INTEGER
            )
            """
        )
        self.conn.commit()

    def set_active_version(self, prompt_id: str, version: int) -> None:
        """
        Set the active version for a prompt flow.
        """
        self.conn.execute(
            "REPLACE INTO active_prompts (prompt_id, active_version) VALUES (?, ?)",
            (prompt_id, version)
        )
        self.conn.commit()

    def get_active_version(self, prompt_id: str) -> Optional[int]:
        """
        Get the active version for a prompt flow.
        """
        cur = self.conn.execute(
            "SELECT active_version FROM active_prompts WHERE prompt_id=?",
            (prompt_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None

    def get_latest_version(self, prompt_id: str) -> Optional[int]:
        cur = self.conn.execute(
            "SELECT MAX(version) FROM prompts WHERE prompt_id=?",
            (prompt_id,)
        )
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else None

    def list_prompt_overviews(self) -> List[Dict[str, Any]]:
        """
        Return prompt-level summaries with counts and active/latest pointers.
        """
        active_lookup = {
            row["prompt_id"]: row["active_version"]
            for row in self.conn.execute("SELECT prompt_id, active_version FROM active_prompts")
        }
        results: List[Dict[str, Any]] = []
        cur = self.conn.execute(
            """
            SELECT prompt_id, COUNT(*) AS version_count, MAX(version) AS latest,
                   AVG(response_ms) as avg_latency, SUM(cost) as total_cost
            FROM prompts GROUP BY prompt_id ORDER BY prompt_id
            """
        )
        for row in cur.fetchall():
            prompt_id = row["prompt_id"]
            active = active_lookup.get(prompt_id)
            results.append(
                {
                    "prompt_id": prompt_id,
                    "versions": row["version_count"],
                    "latest": row["latest"],
                    "active": active,
                    "stale": active is not None and active != row["latest"],
                    "avg_latency": row["avg_latency"],
                    "total_cost": row["total_cost"]
                }
            )
        return results

    def list_prompts(self) -> List[str]:
        """
        List all prompt ids.
        """
        cur = self.conn.execute("SELECT DISTINCT prompt_id FROM prompts ORDER BY prompt_id")
        return [row[0] for row in cur.fetchall()]

    def list_versions(self, prompt_id: str) -> List[int]:
        cur = self.conn.execute(
            "SELECT version FROM prompts WHERE prompt_id=? ORDER BY version ASC",
            (prompt_id,)
        )
        return [row[0] for row in cur.fetchall()]

    def load_prompt_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        cur = self.conn.execute(
            "SELECT * FROM prompts WHERE prompt_id=? AND version=?",
            (prompt_id, version)
        )
        row = cur.fetchone()
        if not row:
            return None
        return PromptVersion(
            prompt_id=row["prompt_id"],
            version=row["version"],
            content=json.loads(row["content"]),
            model=row["model"],
            parameters=json.loads(row["params"]),
            content_hash=row["hash"],
            created_at=row["created_at"],
            response=json.loads(row["response"]) if row["response"] else None,
            response_ms=row["response_ms"],
            cost=row["cost"]
        )

    def save_prompt_version(self, prompt: PromptVersion) -> None:
        try:
            self.conn.execute(
                "INSERT INTO prompts VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    prompt.prompt_id,
                    prompt.version,
                    canonical_json(prompt.content),
                    prompt.model,
                    canonical_json(prompt.parameters),
                    prompt.content_hash,
                    prompt.created_at.isoformat() if hasattr(prompt.created_at, 'isoformat') else str(prompt.created_at),
                    canonical_json(prompt.response) if prompt.response else None,
                    prompt.response_ms,
                    prompt.cost
                )
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise RuntimeError(f"Prompt version already exists: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to save prompt version: {e}")

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
