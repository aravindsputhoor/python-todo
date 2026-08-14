from flask import Blueprint, request, jsonify
from .models import db, Todo

api = Blueprint("api", __name__)


@api.route("/")
def home():
    return jsonify({
        "message": "Todo API is running"
    })


@api.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503


@api.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()

    return jsonify([
        todo.to_dict()
        for todo in todos
    ])


@api.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if not todo:
        return jsonify({
            "error": "Todo not found"
        }), 404

    return jsonify(todo.to_dict())


@api.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({
            "error": "Title is required"
        }), 400

    todo = Todo(
        title=data["title"],
        completed=data.get("completed", False)
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_dict()), 201


@api.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if not todo:
        return jsonify({
            "error": "Todo not found"
        }), 404

    data = request.get_json()

    if "title" in data:
        todo.title = data["title"]

    if "completed" in data:
        todo.completed = data["completed"]

    db.session.commit()

    return jsonify(todo.to_dict())


@api.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if not todo:
        return jsonify({
            "error": "Todo not found"
        }), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({
        "message": "Todo deleted successfully"
    })