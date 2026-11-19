"""One writer per journal, atomic attempts and persistent per-call traces."""

import contextlib
import fcntl
import json
import sqlite3

from manifest import sha256

IDENTITY_FIELDS = (
    "dataset_revision", "task", "pair_id", "gold_label", "text_sha256", "image_sha256",
    "method", "model_id", "model_revision", "adapter_revision", "prompt_version",
    "processor", "quantization", "decoding", "seed",
)


def run_key(config):
    identity = {field: config[field] for field in IDENTITY_FIELDS}
    if any(value is None or value == "" for value in identity.values()):
        raise ValueError("run identity fields must be populated")
    return sha256(json.dumps(identity, sort_keys=True, allow_nan=False).encode())


class Journal:
    def __init__(self, path):
        self.path = path

    @contextlib.contextmanager
    def open_writer(self):
        # The lease is released by the OS after process exit. An interrupted input
        # is retried from Agent 1 with a new attempt ID and its old traces retained.
        with self.path.with_suffix(self.path.suffix + ".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with contextlib.closing(sqlite3.connect(self.path)) as conn:
                conn.executescript("""
                    PRAGMA foreign_keys=ON;
                    CREATE TABLE IF NOT EXISTS attempts (
                        id INTEGER PRIMARY KEY, run_key TEXT NOT NULL,
                        config TEXT NOT NULL, status TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS calls (
                        attempt_id INTEGER NOT NULL REFERENCES attempts(id),
                        call_id INTEGER NOT NULL, trace TEXT NOT NULL,
                        PRIMARY KEY (attempt_id, call_id)
                    );
                    CREATE UNIQUE INDEX IF NOT EXISTS completed_key
                        ON attempts(run_key) WHERE status = 'complete';
                    UPDATE attempts SET status = 'interrupted' WHERE status = 'running';
                """)
                yield conn

    def run(self, config, pipeline, text, image):
        if sha256(image.read_bytes()) != config["image_sha256"]:
            raise ValueError("input image differs from the run identity")
        if sha256(text.encode()) != config["text_sha256"]:
            raise ValueError("input text differs from the run identity")
        key = run_key(config)
        with self.open_writer() as conn:
            if conn.execute("SELECT 1 FROM attempts WHERE run_key=? AND status='complete'",
                            (key,)).fetchone():
                return False
            with conn:
                attempt = conn.execute(
                    "INSERT INTO attempts(run_key,config,status) VALUES (?,?,'running')",
                    (key, json.dumps(config, sort_keys=True, allow_nan=False)),
                ).lastrowid

            invalid_output = False

            def emit(trace):
                nonlocal invalid_output
                invalid_output |= trace["error"] == "invalid_agent_output"
                with conn:
                    conn.execute("INSERT INTO calls VALUES (?,?,?)",
                                 (attempt, trace["call_id"], json.dumps(trace)))

            status = "failed"
            try:
                result = pipeline.run(config["task"], config["method"], text, image, emit)
                if invalid_output or result["error"]:
                    status = "invalid"
                else:
                    status = "complete"
            finally:
                with conn:
                    conn.execute("UPDATE attempts SET status=? WHERE id=?", (status, attempt))
            return True
