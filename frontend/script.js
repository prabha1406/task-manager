let token = "";

function login() {
  fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      username: log_user.value,
      password: log_pass.value
    })
  })
  .then(res => res.json())
  .then(data => {
    token = data.access_token;
    loadTasks();
  });
}

function createTask() {
  fetch("http://127.0.0.1:8000/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({ title: task.value })
  }).then(() => loadTasks());
}

function loadTasks() {
  fetch("http://127.0.0.1:8000/tasks", {
    headers: {
      "Authorization": "Bearer " + token
    }
  })
  .then(res => res.json())
  .then(data => {
    let list = document.getElementById("tasks");
    list.innerHTML = "";

    data.forEach(t => {
      let li = document.createElement("li");
      li.innerText = t.title + (t.completed ? " ✅" : "");

      let btn = document.createElement("button");
      btn.innerText = "Done";
      btn.onclick = () => completeTask(t.id);

      li.appendChild(btn);
      list.appendChild(li);
    });
  });
}

function completeTask(id) {
  fetch(`http://127.0.0.1:8000/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Authorization": "Bearer " + token
    }
  }).then(() => loadTasks());
}