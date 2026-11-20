# Fast-track model inventory

| Route | Candidate | Observed disposition |
|---|---|---|
| A | `liuhaotian/llava-v1.6-vicuna-7b@deae57a8c0ccb0da4c2661cc1891cc9d06503d11` + locked CLIP | No complete official-sized weight files in the shared/readable cache roots. Original three shards and CLIP BIN remain missing. The 6 s HTTP connect probe returned no bytes. Prior 1 MiB Range support remains documented, but there was no basis to restart a bulk download. |
| B | `Sandy124/ThinkingGuard-8B@76892f9768ce828268265171f4bbc5dfb75eafc3` | Four local shard hashes and necessary processor/tokenizer objects match the pinned official manifest. The existing repaired index was verified against all 750 actual safetensors header keys. Reused as a read-only model snapshot; no new model download. |
| B | Qwen/Qwen3-VL-8B-Instruct, other visible Hugging Face caches | No complete 7–8B general-purpose VLM found. The 27B Qwen cache exceeds the target model size, and the 7B Mistral cache is text-only. The shared TRACE CLIP is a different revision/artifact and does not satisfy the route A SHA lock. |

ThinkingGuard is a Qwen3-VL-8B-Instruct derivative trained for multimodal risk attribution. Its safety behavior and tendency to generate reasoning can differ from the original paper's LLaVA. Results are D protocol transfer. [Pinned model card](https://huggingface.co/Sandy124/ThinkingGuard-8B/tree/76892f9768ce828268265171f4bbc5dfb75eafc3)

## Minimal route A offline staging

Use a stable source directory with these four files laid out under `native/` and `clip/`. The target already contains the verified eight small files and the pinned official metadata. Run from this experiment directory.

```bash
stage=.stage0-local/stage1
python - <<'PY'
import csv
from pathlib import Path
stage = Path('.stage0-local/stage1')
rows = [r for r in csv.DictReader(open('stage1_fix_weights.csv'))
        if r['status'] == 'INCOMPLETE']
(stage / 'routeA-files.txt').write_text(''.join(f"{r['artifact']}/{r['file']}\n" for r in rows))
(stage / 'routeA.sha256').write_text(''.join(
    f"{r['official_lfs_sha256']}  {r['artifact']}/{r['file']}\n" for r in rows))
PY
rsync -a --partial-dir=.rsync-partial --files-from="$stage/routeA-files.txt" "$ROUTE_A_SOURCE/" "$stage/"
(cd "$stage" && sha256sum -c routeA.sha256)
python stage1_weights.py "$stage"
```

The expected SHA256 values and sizes are enumerated in [the official weight lock](stage1_fix_weights.csv). This produces `weights_verified.json` only after all assets match. No route A weights or results were mixed into route B.
