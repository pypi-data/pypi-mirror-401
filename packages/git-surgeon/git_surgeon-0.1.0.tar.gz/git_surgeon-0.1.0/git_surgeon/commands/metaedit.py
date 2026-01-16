from __future__ import annotations

import argparse

from git_surgeon.commands import metaedit_author, metaedit_date, metaedit_mail


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "metaedit",
        help="Edit commit metadata.",
    )
    meta_subparsers = parser.add_subparsers(dest="meta_command", required=True)
    metaedit_date.add_parser(meta_subparsers)
    metaedit_author.add_parser(meta_subparsers)
    metaedit_mail.add_parser(meta_subparsers)
