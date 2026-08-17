const form = document.getElementById("todo-form");
const input = document.getElementById("todo-title");
const todoList = document.getElementById("todo-list");
const taskCount = document.getElementById("task-count");
const emptyState = document.getElementById("empty-state");
const filterBtns = document.querySelectorAll(".filter-btn");

let todosState = [];
let currentFilter = "all";

// Load todos from the server
async function loadTodos() {
    try {
        const response = await fetch("/todos");
        todosState = await response.json();
        render();
    } catch (err) {
        console.error("Failed to load todos:", err);
    }
}

// Render todos and handle UI state
function render() {
    todoList.innerHTML = "";

    const filteredTodos = todosState.filter(todo => {
        if (currentFilter === "active") return !todo.completed;
        if (currentFilter === "completed") return todo.completed;
        return true;
    });

    const activeCount = todosState.filter(t => !t.completed).length;
    taskCount.textContent = `${activeCount} active`;

    if (filteredTodos.length === 0) {
        emptyState.classList.remove("hidden");
    } else {
        emptyState.classList.add("hidden");
    }

    filteredTodos.forEach(todo => {
        const li = document.createElement("li");
        li.className = `todo-item ${todo.completed ? "completed" : ""}`;

        li.innerHTML = `
            <div class="todo-content" onclick="toggleTodo(${todo.id}, ${!todo.completed})">
                <span class="checkbox-custom">
                    <i class="ph ph-check-bold"></i>
                </span>
                <span class="todo-title">${escapeHTML(todo.title)}</span>
            </div>
            <button class="btn-delete" onclick="deleteTodo(${todo.id})" aria-label="Delete todo">
                <i class="ph ph-trash"></i>
            </button>
        `;

        todoList.appendChild(li);
    });
}

// Add a new todo
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = input.value.trim();
    if (!title) return;

    try {
        const response = await fetch("/todos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, completed: false })
        });
        
        if (response.ok) {
            input.value = "";
            await loadTodos();
        }
    } catch (err) {
        console.error("Failed to add todo:", err);
    }
});

// Toggle todo completion
async function toggleTodo(id, newStatus) {
    try {
        await fetch(`/todos/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ completed: newStatus })
        });
        await loadTodos();
    } catch (err) {
        console.error("Failed to update todo:", err);
    }
}

// Delete todo
async function deleteTodo(id) {
    try {
        await fetch(`/todos/${id}`, { method: "DELETE" });
        await loadTodos();
    } catch (err) {
        console.error("Failed to delete todo:", err);
    }
}

// Filter button handlers
filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        filterBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentFilter = btn.dataset.filter;
        render();
    });
});

// Helper to prevent XSS
function escapeHTML(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

loadTodos();