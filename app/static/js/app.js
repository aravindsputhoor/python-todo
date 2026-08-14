const form = document.getElementById("todo-form");
const input = document.getElementById("todo-title");
const todoList = document.getElementById("todo-list");


async function loadTodos() {

    const response = await fetch("/todos");

    const todos = await response.json();

    todoList.innerHTML = "";

    todos.forEach(todo => {

        const li = document.createElement("li");

        li.innerHTML = `
            <span>
                ${todo.completed ? "✅" : "⬜"}
                ${todo.title}
            </span>

            <button onclick="deleteTodo(${todo.id})">
                Delete
            </button>
        `;

        todoList.appendChild(li);
    });
}


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const title = input.value.trim();

    if (!title) {
        return;
    }

    await fetch("/todos", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: title
        })
    });

    input.value = "";

    loadTodos();
});


async function deleteTodo(id) {

    await fetch(`/todos/${id}`, {
        method: "DELETE"
    });

    loadTodos();
}


loadTodos();