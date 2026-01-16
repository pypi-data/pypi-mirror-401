from __future__ import annotations

import argparse

from git_surgeon.commands import op_abandon, op_log, op_restore, op_revert


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "op",
        help="Inspect operation history.",
    )
    op_subparsers = parser.add_subparsers(dest="op_command", required=True)
    op_log.add_parser(op_subparsers)
    op_restore.add_parser(op_subparsers)
    op_revert.add_parser(op_subparsers)
    op_abandon.add_parser(op_subparsers)
