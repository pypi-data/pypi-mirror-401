import argparse
from .core import PocketGit


def init_command(args):
    git = PocketGit()
    try:
        print(git.init())
        return 0
    except FileExistsError as e:
        print(f"Error: {e}")
        return 1


def add_command(args):
    git = PocketGit()
    try:
        print(git.add(args.file))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def commit_command(args):
    git = PocketGit()
    try:
        msg, n = git.commit(args.message)
        print(msg)
        print(f"{n} file(s) changed")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def log_command(args):
    git = PocketGit()
    try:
        for sha, data in git.log():
            print(f"\ncommit {sha}")
            print(f"Author: {data['author']}")
            print(f"Date:   {data['timestamp']}")
            print(f"\n    {data['message']}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def status_command(args):
    git = PocketGit()
    try:
        status = git.status()
        print(f"On branch {status['branch']}\n")
        if status["staged"]:
            print("Changes to be committed:")
            for f in status["staged"]:
                print(f"  {f}")
        else:
            print("Nothing staged for commit")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(prog="pocket-git")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init")
    add = sub.add_parser("add")
    add.add_argument("file")
    commit = sub.add_parser("commit")
    commit.add_argument("message")
    sub.add_parser("log")
    sub.add_parser("status")

    args = parser.parse_args()

    commands = {
        "init": init_command,
        "add": add_command,
        "commit": commit_command,
        "log": log_command,
        "status": status_command,
    }

    if not args.cmd:
        parser.print_help()
        return 1

    return commands[args.cmd](args)
