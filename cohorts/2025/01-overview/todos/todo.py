from __future__ import annotations
import json
from datetime import datetime
from typing import List, Optional, Dict, Any


def _next_id(todos: List[Dict[str, Any]]) -> int:
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1


def _parse_due_date(due_date: Optional[str]) -> Optional[str]:
    if due_date is None:
        return None
    try:
        try:
            dt = datetime.fromisoformat(due_date)
        except Exception:
            dt = datetime.fromisoformat(due_date + "T00:00:00")
        return dt.isoformat()
    except Exception:
        raise ValueError("due_date must be ISO formatted (YYYY-MM-DD or ISO datetime)")


def create_todo(todos: List[Dict[str, Any]], title: str, due_date: Optional[str] = None) -> Dict[str, Any]:
    title = (title or "").strip()
    if not title:
        raise ValueError("title must not be empty")
    if len(title) > 200:
        raise ValueError("title too long")
    parsed = _parse_due_date(due_date)
    todo = {"id": _next_id(todos), "title": title, "due_date": parsed, "resolved": False}
    todos.append(todo)
    return todo


def edit_todo(todo: Dict[str, Any], title: Optional[str] = None, due_date: Optional[str] = None) -> Dict[str, Any]:
    if title is not None:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        if len(title) > 200:
            raise ValueError("title too long")
        todo["title"] = title
    if due_date is not None:
        todo["due_date"] = _parse_due_date(due_date)
    return todo


def delete_todo(todos: List[Dict[str, Any]], todo_id: int) -> bool:
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            del todos[i]
            return True
    return False


def mark_resolved(todo: Dict[str, Any]) -> Dict[str, Any]:
    todo["resolved"] = True
    return todo


def list_todos(todos: List[Dict[str, Any]], resolved: Optional[bool] = None) -> List[Dict[str, Any]]:
    if resolved is None:
        return list(todos)
    return [t for t in todos if bool(t.get("resolved")) is resolved]


def save_to_file(todos: List[Dict[str, Any]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def load_from_file(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("file must contain a JSON list of todos")
            return data
    except FileNotFoundError:
        return []
