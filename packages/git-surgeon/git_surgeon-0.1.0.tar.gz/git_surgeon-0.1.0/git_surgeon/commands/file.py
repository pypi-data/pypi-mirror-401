from __future__ import annotations

import argparse

from git_surgeon.commands import file_track, file_untrack


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "file",
        help="File tracking helpers.",
    )
    file_subparsers = parser.add_subparsers(dest="file_command", required=True)
    file_track.add_parser(file_subparsers)
    file_untrack.add_parser(file_subparsers)
