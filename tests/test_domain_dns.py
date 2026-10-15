import socket

import pytest

from scripts.check_domain_dns import DOMAINS, EXPECTED_IP, domain_readiness, main


def answer(ip):
    return (socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443))


def test_main_domain_accepts_only_both_names_on_expected_server(monkeypatch, capsys):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args, **kwargs: [answer(EXPECTED_IP)])
    assert domain_readiness() == dict.fromkeys(DOMAINS, True)
    assert main() == 0
    assert "DNS ready for TLS" in capsys.readouterr().out


@pytest.mark.parametrize("extra", ["216.24.57.16", "2001:db8::1"])
def test_old_or_conflicting_address_prevents_acme(monkeypatch, extra):
    monkeypatch.setattr(
        socket, "getaddrinfo", lambda *args, **kwargs: [answer(EXPECTED_IP), answer(extra)]
    )
    assert main() == 2


def test_root_and_www_are_checked_independently(monkeypatch):
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda name, *args, **kwargs: [answer(EXPECTED_IP if name == DOMAINS[0] else "1.1.1.1")],
    )
    assert domain_readiness() == {DOMAINS[0]: True, DOMAINS[1]: False}
    assert main() == 2


def test_dns_failure_is_pending_not_an_unsafe_activation(monkeypatch):
    def failed(*args, **kwargs):
        raise socket.gaierror("fixture resolution failed")

    monkeypatch.setattr(socket, "getaddrinfo", failed)
    assert main() == 2
