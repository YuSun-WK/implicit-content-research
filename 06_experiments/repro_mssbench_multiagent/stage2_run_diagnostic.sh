#!/usr/bin/env bash
# Start only after the 100-pair 256-token batch completed successfully.
set -euo pipefail
cd "$(dirname "$0")"
GPU_UUID=${STAGE2_GPU_UUID:-GPU-79ea6ee8-2e76-d36e-1508-7813c1589ec1}
BASE=.stage0-local/stage2/B-thinkingguard
OUT="$BASE/diagnostic-512"
PY=/home/ubuntu/data/project/h1-cf-killtest/.venv/bin/python
SNAPSHOT=/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3
export CUDA_VISIBLE_DEVICES="$GPU_UUID" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$PWD/.stage0-local/fasttrack/B-thinkingguard/addons:$PWD"
if [[ "${WAIT_FOR_PID:-}" ]]; then
    while kill -0 "$WAIT_FOR_PID" 2>/dev/null; do sleep 30; done
fi
rg -q '100-pair primary finished' "$BASE/batch.log" || { echo 'primary batch did not complete'; exit 1; }
"$PY" stage2_diagnostic.py select
mkdir -p "$OUT"
run_diagnostic() {
    local label="$1" extra="${2:-}"
    local used
    used=$(nvidia-smi --query-gpu=uuid,memory.used --format=csv,noheader,nounits | awk -F', ' -v u="$GPU_UUID" '$1==u{print $2}')
    [[ "$used" =~ ^[0-9]+$ && "$used" -lt 500 ]] || { echo "GPU busy: $used MiB"; exit 1; }
    "$PY" stage2_runner.py \
        --pair-manifest stage2/frozen_100_pairs.csv \
        --data-root .stage0-local/stage1/data \
        --model-root .stage0-local/fasttrack/B-thinkingguard \
        --snapshot "$SNAPSHOT" --official-source /tmp/mssbench-stage0-official \
        --output "$OUT" --gpu-uuid "$GPU_UUID" --max-new-tokens 512 \
        --pair-ids-file stage2/diagnostic_10_pair_ids.txt $extra > "$OUT/$label.log" 2>&1
    tail -n 3 "$OUT/$label.log"
}
run_diagnostic pilot '--pilot-pairs 2'
"$PY" - "$OUT/smoke.sqlite" 12 <<'PY'
import sqlite3,sys
db=sqlite3.connect(sys.argv[1])
statuses=dict(db.execute('SELECT status,count(*) FROM attempts GROUP BY status'))
assert statuses.get('complete',0)+statuses.get('invalid',0)>=int(sys.argv[2]),statuses
print('512 pilot',statuses,flush=True)
PY
run_diagnostic remainder
"$PY" - "$OUT/smoke.sqlite" 60 <<'PY'
import sqlite3,sys
db=sqlite3.connect(sys.argv[1])
statuses=dict(db.execute('SELECT status,count(*) FROM attempts GROUP BY status'))
assert statuses.get('complete',0)+statuses.get('invalid',0)==int(sys.argv[2]),statuses
print('512 all',statuses,flush=True)
PY
"$PY" stage2_export.py --tokens 512 --pair-ids-file stage2/diagnostic_10_pair_ids.txt
"$PY" stage2_diagnostic.py compare
echo '512-token diagnostic finished'
