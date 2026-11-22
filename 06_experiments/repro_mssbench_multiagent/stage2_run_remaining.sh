#!/usr/bin/env bash
# Resume the single-GPU 256-token Stage 2 slices after chunk 0.
set -euo pipefail
cd "$(dirname "$0")"
GPU_UUID=${STAGE2_GPU_UUID:-GPU-79ea6ee8-2e76-d36e-1508-7813c1589ec1}
BASE=.stage0-local/stage2/B-thinkingguard
PY=/home/ubuntu/data/project/h1-cf-killtest/.venv/bin/python
SNAPSHOT=/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3
export CUDA_VISIBLE_DEVICES="$GPU_UUID" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$PWD/.stage0-local/fasttrack/B-thinkingguard/addons:$PWD"

if [[ "${WAIT_FOR_PID:-}" ]]; then
    while kill -0 "$WAIT_FOR_PID" 2>/dev/null; do sleep 20; done
fi

check_count() {
    "$PY" - "$BASE/chunk$(printf '%02d' "$1")-256/smoke.sqlite" "$2" <<'PY'
import sqlite3,sys
db=sqlite3.connect(sys.argv[1])
statuses=dict(db.execute('SELECT status,count(*) FROM attempts GROUP BY status'))
assert statuses.get('complete',0)+statuses.get('invalid',0)>=int(sys.argv[2]),statuses
assert not any(s in statuses for s in ('failed','interrupted','running')),statuses
print(sys.argv[1],statuses,flush=True)
PY
}

run_chunk() {
    local chunk="$1" label="$2" extra="${3:-}"
    local dir="$BASE/chunk$(printf '%02d' "$chunk")-256"
    mkdir -p "$dir"
    # A newly busy GPU is a stop condition; every job remains on one free card.
    local used
    used=$(nvidia-smi --query-gpu=uuid,memory.used --format=csv,noheader,nounits | awk -F', ' -v u="$GPU_UUID" '$1==u{print $2}')
    [[ "$used" =~ ^[0-9]+$ && "$used" -lt 500 ]] || { echo "GPU busy: $used MiB"; exit 1; }
    "$PY" stage2_runner.py \
        --pair-manifest stage2/frozen_100_pairs.csv \
        --data-root .stage0-local/stage1/data \
        --model-root .stage0-local/fasttrack/B-thinkingguard \
        --snapshot "$SNAPSHOT" --official-source /tmp/mssbench-stage0-official \
        --output "$dir" --gpu-uuid "$GPU_UUID" --max-new-tokens 256 \
        --chunk "$chunk" $extra > "$dir/$label.log" 2>&1
    echo "$label complete"; tail -n 3 "$dir/$label.log"
}

check_count 0 30
run_chunk 1 pilot "--limit-pairs 5"
check_count 1 30
"$PY" - "$BASE/chunk00-256/smoke.sqlite" "$BASE/chunk01-256/smoke.sqlite" <<'PY'
import csv,json,sqlite3,sys
with open('stage2/frozen_100_pairs.csv',newline='') as stream:
    rows=list(csv.DictReader(stream))
first_ten=list(dict.fromkeys(r['pair_id'] for r in rows if r['anchor']=='False'))[:10]
critical=0
for path in sys.argv[1:]:
    db=sqlite3.connect(path)
    for status,config in db.execute('SELECT status,config FROM attempts'):
        c=json.loads(config)
        if c['pair_id'] in first_ten and c['method']=='multiagent' and status=='invalid':
            critical+=1
print('first 10 new pairs: critical method-input invalid',critical,'of 20',flush=True)
if critical>2:
    raise SystemExit('STOP: critical invalid rate above 10%')
PY
run_chunk 1 remainder
check_count 1 150
run_chunk 2 full
check_count 2 150
run_chunk 3 full
check_count 3 150
"$PY" stage2_export.py --tokens 256
echo '100-pair primary finished'
