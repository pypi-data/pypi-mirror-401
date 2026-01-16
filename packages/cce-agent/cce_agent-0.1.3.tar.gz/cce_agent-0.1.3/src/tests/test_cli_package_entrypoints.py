from __future__ import annotations


def test_package_entrypoint_parser() -> None:
    from cce_agent.cli import create_parser

    parser = create_parser()
    assert parser.prog == "cce"
