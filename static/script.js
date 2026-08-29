const $ = s => document.querySelector(s);
const messages = $("#messages");

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = "msg " + role;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function loadHistory() {
  const r = await fetch("/api/history");
  const h = await r.json();
  messages.innerHTML = "";
  if (!h.length) {
    addMessage("assistant", "Welcome to Python AI. I work offline on this PC. Ask me a Python question.");
  } else {
    h.forEach(x => addMessage(x.role, x.content));
  }

  const list = $("#historyList");
  list.innerHTML = "";
  h.forEach(x => {
    const d = document.createElement("div");
    d.className = "historyItem";
    d.textContent = `${x.role.toUpperCase()}\n${x.content}`;
    list.appendChild(d);
  });
}

$("#chatForm").addEventListener("submit", async e => {
  e.preventDefault();
  const input = $("#message");
  const message = input.value.trim();
  if (!message) return;
  addMessage("user", message);
  input.value = "";
  addMessage("assistant", "Thinking locally...");
  const placeholder = messages.lastElementChild;

  try {
    const r = await fetch("/api/chat", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message})
    });
    const data = await r.json();
    placeholder.textContent = data.reply || data.error;
  } catch {
    placeholder.textContent = "Could not contact the local app.";
  }
});

document.querySelectorAll(".quick button").forEach(b => {
  b.addEventListener("click", () => {
    $("#message").value = b.dataset.prompt;
    $("#chatForm").requestSubmit();
  });
});

$("#clearChat").addEventListener("click", async () => {
  await fetch("/api/chat", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:""})}).catch(()=>{});
  messages.innerHTML = "";
  addMessage("assistant","Chat display cleared. Existing history remains saved locally.");
});

$("#runBtn").addEventListener("click", async () => {
  $("#output").textContent = "Running...";
  const r = await fetch("/api/run", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({code:$("#code").value})
  });
  const d = await r.json();
  $("#output").textContent = d.error ? d.error + (d.output ? "\n"+d.output : "") : (d.output || "(No output)");
});

document.querySelectorAll(".nav").forEach(n => {
  n.addEventListener("click", () => {
    document.querySelectorAll(".nav").forEach(x=>x.classList.remove("active"));
    document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
    n.classList.add("active");
    $("#"+n.dataset.tab).classList.add("active");
    if(n.dataset.tab==="history") loadHistory();
  });
});

loadHistory();
