import argparse
import sys
from typing import List
from pathlib import Path

# import local module
from todos.todo import create_todo, list_todos, save_to_file, load_from_file, mark_resolved


DEFAULT_DB = Path.cwd() / "todos.json"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="manage_todos")
    sub = p.add_subparsers(dest="cmd")
    c = sub.add_parser("create")
    c.add_argument("--title", required=True)
    c.add_argument("--due")
    c = sub.add_parser("list")
    c.add_argument("--resolved", choices=["true", "false"], default=None)
    c = sub.add_parser("resolve")
    c.add_argument("--id", type=int, required=True)
    c = sub.add_parser("save")
    c.add_argument("--path", required=True)
    c = sub.add_parser("load")
    c.add_argument("--path", required=True)
    return p


def main(argv: List[str] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    db = DEFAULT_DB
    # in tests we allow overriding via env-like arg
    if hasattr(args, "path") and args.path:
        db = Path(args.path)

    todos = load_from_file(str(db)) if db.exists() else []

    if args.cmd == "create":
        todo = create_todo(todos, args.title, getattr(args, "due", None))
        save_to_file(todos, str(db))
        print(f"created {todo['id']}")
        return 0
    if args.cmd == "list":
        resolved = None
        if args.resolved == "true":
            resolved = True
        elif args.resolved == "false":
            resolved = False
        for t in list_todos(todos, resolved):
            print(f"{t['id']}: {t['title']} (resolved={t['resolved']}) due={t.get('due_date')}")
        return 0
    if args.cmd == "resolve":
        for t in todos:
            if t["id"] == args.id:
                mark_resolved(t)
                save_to_file(todos, str(db))
                print("ok")
                return 0
        print("not found", file=sys.stderr)
        return 2
    if args.cmd == "save":
        save_to_file(todos, args.path)
        print("saved")
        return 0
    if args.cmd == "load":
        # just load to validate
        _ = load_from_file(args.path)
        print("loaded")
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
