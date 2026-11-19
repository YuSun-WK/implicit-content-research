# Recover Stage 1 on an authorized stable network

The current worker's direct network check is BLOCKED. Work from the VLSU experiment directory on `repro/vlsu-original-20261119`. Keep the pinned Apple CSV locally sourced from Git blob `09421adeb2e68eac1d5e829dcbd48848f21a0be6`. The CLI verifies the blob, SHA-256 and schema. Use the existing root, or migrate it to a private destination that is authorized to hold its third-party images and research data. All archives, inventory filenames and raw logs are private.

## Inventory and transfer

Stop acquisition writers at both ends before making the cold copy. The read-only verifier requires a stopped acquisition, verifies official UUID/URL/labels in SQLite, checks all content object names against their SHA-256, verifies historical roster objects and checks SQLite integrity. The inventory covers existing failure logs, completed objects, partials and their metadata, the SQLite main file and any nonempty WAL, and all immutable snapshots. SQLite shared-memory and lock files are runtime artifacts. Protect the archive and inventory with restrictive permissions and transfer through a policy-approved private channel.

```bash
umask 077
export VLSU_PINNED_CSV=/absolute/private/path/VLSU.csv
python scripts/stage1r_state.py --csv "$VLSU_PINNED_CSV" --root .local/stage1 \
  --write-inventory .local/stage1r-source-inventory.json
tar -C .local --exclude='stage1/audit.sqlite-shm' -cf .local/stage1r-state.tar stage1
python scripts/stage1r_state.py --csv "$VLSU_PINNED_CSV" --root .local/stage1 \
  --check-inventory .local/stage1r-source-inventory.json
```

On the destination, extract your verified private transfer into a new directory. Use the new path consistently with `--root`. Keep the source archive and local history until the destination inventory passes.

```bash
umask 077
mkdir -p .local
mkdir -m 700 .local/recovery-import
export VLSU_PINNED_CSV=/absolute/private/path/VLSU.csv
tar -C .local/recovery-import -xf /absolute/private/path/stage1r-state.tar
export VLSU_STATE_ROOT=.local/recovery-import/stage1
python scripts/stage1r_state.py --csv "$VLSU_PINNED_CSV" --root "$VLSU_STATE_ROOT" \
  --check-inventory /absolute/private/path/stage1r-source-inventory.json
```

## Bounded resume and subsequent batches

Run the offline suite and inspect the serialized resolver and verified HTTPS results. Exit 2 from the probe means the network gate failed. Stop the acquisition workflow there. On a verified PASS, run the dry-run, then the first capped recovery batch with the same root. The configuration below applies four workers, one concurrent request per host, at least one second between same-host admissions and at least 0.25 s between global admissions. A request-budget stop (exit 2, JSON reason `request_budget`) is expected and preserves the queue. Redirects and HTTP retries count against the request budget.

```bash
export VLSU_STATE_ROOT=${VLSU_STATE_ROOT:-.local/stage1}
export VLSU_CONFIG=configs/stage1r_download.yaml
python -m pytest -q
git diff --check
python scripts/stage1r_state.py --csv "$VLSU_PINNED_CSV" --root "$VLSU_STATE_ROOT"
set -o pipefail
python scripts/stage1r_probe.py --root "$VLSU_STATE_ROOT" | tee .local/stage1r-network-probe.log || exit "$?"
python scripts/stage1_download.py --csv "$VLSU_PINNED_CSV" --root "$VLSU_STATE_ROOT" \
  --config "$VLSU_CONFIG" --phase full --resume --dry-run
python scripts/stage1_download.py --csv "$VLSU_PINNED_CSV" --root "$VLSU_STATE_ROOT" \
  --config "$VLSU_CONFIG" --phase full --resume --execute --max-requests 30 --retry-environment-dns
python scripts/stage1_report.py --csv "$VLSU_PINNED_CSV" --root "$VLSU_STATE_ROOT" \
  --out .local/stage1r-batch30
```

Confirm the capped batch admitted at most 30 requests, logged all attempts/rate policy and failure reasons, and did not request previously verified URL images. Recheck hashes and read the aggregate pattern/label coverage. A repeated resolver failure calls for diagnosis and a pause, while permanent 403/404/406 and unsafe-target outcomes remain terminal. If the capped audit is stable, continue from the same root in increasingly sized batches, initially e.g. `--max-requests 100`, and omit `--retry-environment-dns` unless a newly verified environment recovery warrants reopening those specific DNS outcomes. Export an aggregate report and hash after completing or pausing acquisition. Record processing exhaustion, actual decoded coverage, error breakdown and model eligibility independently. Wait for cohort review before Stage 2.
