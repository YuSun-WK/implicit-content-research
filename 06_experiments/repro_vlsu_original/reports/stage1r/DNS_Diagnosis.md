# Stage 1R network diagnosis

**STAGE1R=BLOCKED_BY_ENVIRONMENT.** The direct network path did not pass the serial control gate. This run made zero dataset image requests and started neither bounded image recovery nor full acquisition. All previously recorded image outcomes remain in the original SQLite database. [Raw network probe](Network_Probe_Log.txt)

The probe ran on the local Linux x86_64 worker on 2026-11-19 from 14:35:53 through 14:36:45 UTC. It ran `getent ahosts`, Python `socket.getaddrinfo` inside an already-started interpreter supervised by a watchdog, and the unchanged Stage 1 isolated subprocess, in sequence. Each resolution had a 5 s deadline. The known VLSU hosts are aliased in the published log. No downloaded image, dataset host IP, or private URL is published.

| Scope | System getent | Python in process | Stage 1 isolated subprocess |
|---|---:|---:|---:|
| Two public controls, two rounds | 4/4 (40.4 ms median) | 4/4 (11.9 ms) | 4/4 (56.1 ms) |
| Three previously observed release hosts | 0/3 (5.008 s median) | 1/3 (5.010 s) | 1/3 (5.006 s) |

Both previously decoded origins reached the deadline in all three paths. The origin with a prior DNS timeout reached the system deadline and then resolved in the other two serial probes. Deadlines were logged separately from native resolver errno values. Raw records contain elapsed time per trial.

The certificate-verified direct HTTPS HEAD checks passed **3/4**. GitHub returned HTTP 200 in round 1. Its second request completed both TCP and verified TLS but timed out waiting for HTTP headers. The other public control returned HTTP 200 twice. The probe used no configured proxy, used the vetted address for the connection and verified the peer address and TLS hostname. The recovery gate requires both controls to resolve and return a successful HTTPS result in both rounds. [Raw network probe](Network_Probe_Log.txt)

The numeric-address control avoids network DNS. Eight child launches took a median of 52.5 ms at one worker and 53.5 ms at four. Maxima were 54.8 and 62.4 ms. Common deadlines across independent lookup paths and a separate direct HTTPS timeout reproduce instability outside the downloader. Interpreter startup alone does not account for these observations. This probe cannot attribute each of Stage 1's 217 DNS-timeout events or identify the failing network component. No resolver implementation, timeout, TLS verification or SSRF policy was relaxed. The runtime outage check now requires both DNS controls, evaluated in sequence, before reopening an environmental failure.

## Coverage and next gate

- **Processing exhaustive** false. Among 8,157 unique URLs, 65 have an audit attempt and 58 reached network request admission. Seven remain pending and 8,092 remain unattempted. The 30 terminal URL outcomes include 8 transient DNS failures that may be eligible for a bounded recovery batch when the network gate passes.
- **Decoded joint coverage** 28 decoded URL images map to **30/8,159** release UUIDs (0.37%). Among the attempted URLs, 31 returned HTTP 200/206 and 29 produced complete response bodies. The research paper describes 8,187 samples.
- **Error reason breakdown** is the terminal-outcome table. It retains DNS and other network errors apart from site responses and verification failures. [Failure counts](coverage_by_failure_type.csv) · [All 25 observed patterns](coverage_by_pattern.csv)
- **Model eligibility** is a frozen input count. Joint 30, image gold 23, text 8,159, and three-modality gold-and-input intersection 23. Actual model eligibility for Figure 4/5 still requires prediction validity on each aligned UUID. Classification and all model activity are NOT RUN. Stage 2 stays blocked pending acquisition and cohort review. Independent human prompt review is OPEN. Author image-area units and Qwen weight revision/precision remain UNKNOWN.

The GitHub aggregates and manifest hashes establish exactly what was reported. Verification of cache existence ran on the local worker using the original acquisition directory. The log records local SQLite integrity, object and snapshot hashes, and a private relocation verification. [Integrity and regression log](Run_Verification_Log.txt) · [Authorized-machine recovery](Move_Resume_Instructions.md)
