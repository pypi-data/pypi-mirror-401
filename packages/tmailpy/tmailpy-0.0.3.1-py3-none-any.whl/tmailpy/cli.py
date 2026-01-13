"""Minimal CLI for the TMail API wrapper."""
import argparse
from .client import TMail


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="tmailpy", description="A command-line interface for the TMail API."
    )
    p.add_argument("base", help="Base URL of TMail API (e.g. https://.../api)")
    p.add_argument("key", help="Your TMail API key")
    sub = p.add_subparsers(dest="cmd", help="Available commands")

    sub.add_parser("domains", help="List available domains.")

    c_create = sub.add_parser("create", help="Create a new temporary email address.")
    c_create.add_argument(
        "email",
        nargs="?",
        default="",
        help="Optional: specify a username for the email address.",
    )

    c_messages = sub.add_parser(
        "messages", help="List messages for a specific email address."
    )
    c_messages.add_argument("email", help="The email address to fetch messages for.")

    c_delete = sub.add_parser("delete", help="Delete a specific message.")
    c_delete.add_argument("msg_id", help="The ID of the message to delete.")

    c_raw_messages = sub.add_parser(
        "raw_messages", help="List raw messages for a specific email address."
    )
    c_raw_messages.add_argument(
        "email", help="The email address to fetch raw messages for."
    )

    args = p.parse_args(argv)
    client = TMail(args.base, args.key)

    if args.cmd == "domains":
        print(client.domains())
    elif args.cmd == "create":
        print(client.create(args.email))
    elif args.cmd == "messages":
        print(client.clean_messages(args.email))
    elif args.cmd == "delete":
        print(client.delete_message(args.msg_id))
    elif args.cmd == "raw_messages":
        print(client.raw_messages(args.email))
    elif args.cmd is None:
        p.print_help()
    else:
        p.print_help()


if __name__ == "__main__":
    main()
