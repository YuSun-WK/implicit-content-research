"""Direct HTTP transport with per-hop DNS pinning and request admission."""

from contextlib import contextmanager
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import http.client
from ipaddress import ip_address, ip_network
import json
import socket
import ssl
import subprocess
import sys
from threading import Lock, Timer
import time
from urllib.parse import quote, urlsplit

from stage0_image_checks import check_target


class Failure(Exception):
    def __init__(self, reason, *, retry=False, category="transport", delay=0):
        super().__init__(reason)
        self.reason, self.retry, self.category, self.delay = reason, retry, category, delay


class Pause(Exception):
    """Preserve queued work when the request budget or storage runs out."""


class Limiter:
    def __init__(self, config, max_requests, restored=None):
        self.config, self.max_requests = config, max_requests
        self.requests = 0
        self.host_locks = {}
        self.host_until = dict(restored or {})
        self.next_global = 0
        self.lock = Lock()

    @contextmanager
    def admit(self, host):
        with self.lock:
            lock = self.host_locks.setdefault(host, Lock())
        with lock:
            while True:
                with self.lock:
                    if self.max_requests is not None and self.requests >= self.max_requests:
                        raise Pause("request_budget")
                    delay = self.host_until.get(host, 0) - time.time()
                    if delay > self.config["request_timeout"]:
                        raise Deferred(delay)
                    now = time.monotonic()
                    delay = max(delay, self.next_global - now)
                    if delay <= 0:
                        self.requests += 1
                        self.next_global = now + self.config["global_interval"]
                        self.host_until[host] = time.time() + self.config["host_interval"]
                        break
                time.sleep(delay)
            yield

    def defer(self, host, seconds):
        with self.lock:
            deadline = time.time() + seconds
            self.host_until[host] = max(self.host_until.get(host, 0), deadline)
            return deadline


class Deferred(Exception):
    def __init__(self, delay):
        self.delay = delay


def retry_after(value):
    if not value:
        return 0
    value = value.strip()
    try:
        if value.isascii() and value.isdecimal():
            return int(value) if len(value) < 12 else 10**11
        deadline = parsedate_to_datetime(value)
        return max(0, (deadline - datetime.now(timezone.utc)).total_seconds())
    except (ValueError, TypeError, OverflowError):
        return 0


def resolve(host, port, timeout):
    code = """
import json
import socket
import sys
try:
    rows = socket.getaddrinfo(sys.argv[1], sys.argv[2], type=socket.SOCK_STREAM)
    print(json.dumps({"addresses": list(dict.fromkeys(r[4][0] for r in rows))}))
except socket.gaierror as error:
    print(json.dumps({"error": error.errno}))
"""
    try:
        result = subprocess.run([sys.executable, "-I", "-c", code, host, str(port)],
                                capture_output=True, timeout=timeout, check=True)
    except subprocess.TimeoutExpired as error:
        raise Failure("dns_timeout", retry=True) from error
    except subprocess.CalledProcessError as error:
        raise Failure("dns_resolver_error", retry=True) from error
    payload = json.loads(result.stdout)
    if "addresses" in payload:
        return payload["addresses"]
    if payload["error"] == socket.EAI_NONAME:
        raise Failure("dns_name_not_found")
    raise Failure("dns_resolution", retry=True)


def target(url, timeout, resolver):
    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname or ""
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        # A provisional public input lets the shared helper validate URL syntax before DNS.
        host, _ = check_target(url, ["8.8.8.8"])
        hostname = hostname.encode("idna").decode("ascii").rstrip(".").lower()
        try:
            literal = ip_address(host)
        except ValueError:
            literal = None
        addresses = [str(literal)] if literal is not None else resolver(hostname, port, timeout)
        _, vetted = check_target(url, addresses)
        for text in vetted:
            addr = ip_address(text)
            if addr.version == 6 and addr.ipv4_mapped is None and addr not in ip_network("2000::/3"):
                raise ValueError("non_global_unicast")
        return parsed, hostname, port, vetted
    except (ValueError, UnicodeError) as error:
        raise Failure("unsafe_target", category="security") from error


class PinnedConnection(http.client.HTTPConnection):
    def __init__(self, host, port, address, secure, config):
        super().__init__(host, port, timeout=config["connect_timeout"])
        self.address, self.secure, self.config = address, secure, config
        self.active_socket = None
        self.expired = False

    def expire(self):
        self.expired = True
        if self.active_socket is not None:
            try:
                self.active_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

    def connect(self):
        address = ip_address(self.address)
        family = socket.AF_INET6 if address.version == 6 else socket.AF_INET
        sock = socket.socket(family, socket.SOCK_STREAM)
        self.active_socket = sock
        try:
            if self.expired:
                raise TimeoutError
            sock.settimeout(self.timeout)
            sock.connect((self.address, self.port))
            if ip_address(sock.getpeername()[0]) != address:
                raise Failure("peer_mismatch", category="security")
            if self.secure:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=self.host, do_handshake_on_connect=False)
                self.active_socket = sock
                if self.expired:
                    raise TimeoutError
                sock.do_handshake()
            sock.settimeout(self.config["read_timeout"])
            self.sock = sock
        except BaseException:
            sock.close()
            raise


@contextmanager
def response(url, headers, config, limiter, on_request, resolver=resolve):
    parsed, host, port, addresses = target(url, config["connect_timeout"], resolver)
    secure = parsed.scheme == "https"
    address = sorted(addresses, key=lambda ip: ip_address(ip).version)[0]
    path = quote(parsed.path or "/", safe="/%:@!$&'()*+,;=-._~")
    if parsed.query:
        path += "?" + quote(parsed.query, safe="/%?:@!$&'()*+,;=-._~")
    with limiter.admit(host):
        conn = PinnedConnection(host, port, address, secure, config)
        timer = Timer(config["request_timeout"], conn.expire)
        try:
            on_request(url, host)
            timer.start()
            conn.request("GET", path, headers=headers)
            with conn.getresponse() as resp:
                yield resp, host
            if conn.expired:
                raise TimeoutError
        except ssl.SSLCertVerificationError as error:
            raise Failure("tls_certificate", category="security") from error
        except TimeoutError as error:
            raise Failure("request_timeout", retry=True) from error
        except (http.client.HTTPException, ConnectionError, ssl.SSLError) as error:
            raise Failure("transport_error", retry=True) from error
        except OSError as error:
            if error.errno in {101, 110, 111, 113}:
                raise Failure("network_unreachable", retry=True) from error
            raise
        finally:
            timer.cancel()
            conn.close()
