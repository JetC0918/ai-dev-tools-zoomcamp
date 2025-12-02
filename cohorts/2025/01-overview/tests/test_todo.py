import json
import os
import sys
from pathlib import Path
import pytest

from todos.todo import create_todo, edit_todo, delete_todo, mark_resolved, list_todos, save_to_file, load_from_file
from cli.manage_todos import main as cli_main


def test_create_success_and_list():
    todos = []
    t = create_todo(todos, "Buy milk", None)
    assert t["id"] == 1
    assert t["title"] == "Buy milk"
    assert t["resolved"] is False
    all_ = list_todos(todos)
    assert len(all_) == 1


def test_create_empty_title_raises():
    todos = []
    with pytest.raises(ValueError):
        create_todo(todos, "   ", None)


def test_title_too_long_raises():
    todos = []
    long_title = "x" * 201
    with pytest.raises(ValueError):
        create_todo(todos, long_title)


def test_edit_and_mark_resolved():
    todos = []
    t = create_todo(todos, "Task", None)
    edit_todo(t, title="New title", due_date="2025-01-01")
    assert t["title"] == "New title"
    assert t["due_date"].startswith("2025-01-01")
    mark_resolved(t)
    assert t["resolved"] is True


def test_delete_nonexistent_returns_false():
    todos = []
    create_todo(todos, "A", None)
    assert delete_todo(todos, 999) is False
    assert delete_todo(todos, 1) is True
    assert len(todos) == 0


def test_save_and_load_file(tmp_path):
    todos = []
    create_todo(todos, "Persist", "2025-05-05")
    path = tmp_path / "db.json"
    save_to_file(todos, str(path))
    loaded = load_from_file(str(path))
    assert isinstance(loaded, list)
    assert loaded[0]["title"] == "Persist"


def test_load_missing_file_returns_empty(tmp_path):
    path = tmp_path / "nope.json"
    assert load_from_file(str(path)) == []


def test_cli_create_and_list_integration(tmp_path, capsys):
    db = tmp_path / "cli_db.json"
    rv = cli_main(["create", "--title", "cli task", "--path", str(db)])
    assert rv == 0
    rv = cli_main(["list", "--path", str(db)])
    assert rv == 0
    captured = capsys.readouterr()
    assert "cli task" in captured.out


def test_cli_resolve_nonexistent_returns_error(tmp_path, capsys):
    db = tmp_path / "cli_db.json"
    rv = cli_main(["resolve", "--id", "42", "--path", str(db)])
    assert rv == 2
    captured = capsys.readouterr()
    assert "not found" in captured.err
