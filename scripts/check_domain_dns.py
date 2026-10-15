"""Prevent premature ACME requests while the main names still point to Render."""

import socket

DOMAINS = ("vitalilab.space", "www.vitalilab.space")
EXPECTED_IP = "2.24.101.70"


def domain_readiness():
    results = {}
    for name in DOMAINS:
        try:
            addresses = {
                item[4][0] for item in socket.getaddrinfo(name, 443, type=socket.SOCK_STREAM)
            }
        except socket.gaierror:
            addresses = set()
        # Unexpected IPv6 is also rejected: clients/ACME could reach a different server.
        results[name] = addresses == {EXPECTED_IP}
    return results


def main():
    results = domain_readiness()
    for name, ready in results.items():
        print(f"{name}: {'DNS ready for TLS' if ready else 'DNS pending; no ACME request'}")
    return 0 if all(results.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
