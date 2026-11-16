# H1 sing-box network audit and download progress

Snapshot: 2026-11-16T12:53:58.744378+00:00. This is an interim snapshot during the original supervised download, not a completed transfer report. Current task began 2026-11-16 08:20:46 UTC; six-hour ceiling 14:20:46 UTC. Configured transfer deadline 13:45:46 UTC.

## Current process and weights

Original downloader PID 108368 remains active, supervised by owned wrapper PID 108328. Owned sing-box PID 108329 uses N10 on loopback 17900. Exactly one owned download process was found; no duplicate downloader/inference process was found or killed. The terminal title starts with a Python script-editing heredoc because that shell command subsequently launches the downloader. No restart, extra download, node change or deletion occurred during this status check.

| Shard | Rehashed complete blocks / expected | Missing blocks | Invalid receipt blocks | Official whole-file SHA256 |
|---|---:|---:|---:|---|
| 1 | 290/293 | 3 | 0 | 未验证（文件未完整） |
| 2 | 285/294 | 9 | 0 | 未验证（文件未完整） |
| 3 | 174/297 | 123 | 0 | 未验证（文件未完整） |
| 4 | 0/164 | 164 | 0 | 未验证（文件未完整） |

All captured blocks were rehashed and matched their local receipts and expected lengths. Local receipt verification does not replace official whole-file SHA256. Missing block indexes, official expected hashes and sizes are in `latest_progress.json`. No shard had a complete block set or complete final file at this snapshot, so no assembly was possible. No concurrent assembly was started while the original downloader owns these files. Existing downloader assembles only complete sets and requires the pinned official full SHA256 before final publication.

Model: Sandy124/ThinkingGuard-8B, fixed revision 76892f9768ce828268265171f4bbc5dfb75eafc3. Existing `audit_model_cache.py` returns **ready: false**, with all four final shards missing. Configuration/index files remain present. Legacy sparse files and the failed Xet sparse temporary file are not treated as valid contiguous data. Qwen download remains NOT_RUN in this round.

Last observed log modification: 2026-11-16T12:53:54.636001+00:00. Recent five-minute window at verification end: 28 successful blocks and 14 error events. Successes continued after the prior report. Errors still include connection resets, timeouts and truncated responses. Snapshot counts become stale as the original process continues.

## Existing proxy infrastructure

sing-box 1.14.2 is installed at /usr/bin/sing-box. The system service is active, runs as service user sing-box and reads permitted root-owned `/etc/sing-box/config.json`; user service is inactive. Mixed inbound is 127.0.0.1:7890. Loopback 17897 is a separate ubuntu Python listener, not assumed to be a healthy sing-box endpoint. No user configuration directory was found at ~/.config/sing-box. Proxy references exist in the user's shell aliases and launcher scripts; no secrets are reproduced here.

The system configuration has 12 node outbounds (eight vless, four hysteria2), one urltest group and one direct outbound. No Clash controller API is configured. The current system group's selected node cannot be established from the inspected configuration alone and was not changed. No system service or other user's process was modified. Independent short-lived ubuntu instances selected individual readable configured nodes, stored secrets only in mode-600 files inside mode-700 temporary directories, suppressed proxy logs and cleaned up on exit.

Codex and experiment Python proxy environment variables point to 7890; environment proxy selection applies to huggingface.co, the actual CDN and Xet hosts. Therefore the earlier default HTTP transfer path used sing-box, rather than bypassing it. The prior explicit direct-connect diagnostic was an exception. Root cause of every past failure is not established: automatic delay selection does not establish large-file reliability, and errors also occurred through isolated N10. It would be unsupported to attribute all failures solely to a particular node or concurrency.

## Node tests

All N01–N12 were tested sequentially through independent instances. HTTPS requests used normal certificate verification and required exact 206 Content-Range and byte length. Each node had a 110-second limit. Tests attempted 1MiB, then two 16MiB transfers; remaining tests were skipped after a failure. Local DNS resolved Hugging Face, the observed us.aws.cdn.hf.co download host, cas-bridge.xethub.hf.co and cas-server.xethub.hf.co. Successful per-node HTTPS transfers exercise their proxy resolution/connectivity; per-node independent DNS timing was not measured.

N10 was the only node passing all three initial transfers: 33MiB at about 2.31MiB/s including connection overhead. N11 passed two of three initially; a later three-offset 16MiB retest failed all three. Other nodes failed one of their attempted transfers; see anonymized node_summary.json. This does not establish permanent node unavailability. N10's larger sustained transfers still showed intermittent failures. Concurrency 4 was unsuccessful; serial and concurrency 2 both produced progress with errors. Current process keeps concurrency 2 and N10. Actual child proxy environment and established loopback connections were verified in route_evidence.json. No service-global selector was switched.

An official Xet attempt through N10 was bounded to 240 seconds with two range gets and failed to complete a shard. Its sparse temporary file was excluded from retained valid byte counts. This tested a client path, not comprehensive reachability of every Xet endpoint on every node. The official environment parameter reference is https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables . No new client or global environment was installed.

## GPU and research status

Model loaded: **NO**. Two-pair GPU Smoke Test: **NOT_RUN**. 36-pair experiment and all metrics: **NOT_RUN**. No raw predictions exist from this round. CPU suite: 23 tests passed. NF4, single GPU, 20GiB process budget, original samples/order/labels/protocols remain required. Neither engineering progress nor failed downloads support a scientific conclusion or expansion to 90 pairs.

## Next action and authorization

Keep the original task running until its existing deadline; do not restart it or launch duplicate long downloads. At exit, inspect gaps and assemble only complete receipt-verified sets, then run the pinned official SHA256/header audit. GPU testing is allowed only after ready true. Incomplete weights must retain progress; no additional long download is authorized by this status-check request.

No user action or authentication is needed to preserve the running task. Changing the system service or enabling a global control API would require its owner's authorization; neither is needed for the existing independent instance. The exact current system urltest selection remains unobserved. This report and evidence are archived to experiments/h1-k0-triggerbench-20261106; main is unchanged. Commit SHA is supplied after publication to avoid a self-reference.
