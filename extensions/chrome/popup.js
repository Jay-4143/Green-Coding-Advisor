// Simple popup script to send snippets to the backend /advisor/analyze endpoint

async function analyze(event) {
  event.preventDefault();
  const code = document.getElementById("code").value.trim();
  const language = document.getElementById("language").value;
  const backend = document.getElementById("backend").value.replace(/\/+$/, "");
  const token = document.getElementById("token").value.trim();

  const resultEl = document.getElementById("result");
  const resultJsonEl = document.getElementById("result-json");
  const errorEl = document.getElementById("error");

  resultEl.hidden = true;
  errorEl.hidden = true;

  if (!code) {
    errorEl.textContent = "Please paste code to analyze.";
    errorEl.hidden = false;
    return;
  }

  const payload = {
    code_content: code,
    language,
    filename: "snippet",
  };

  try {
    const res = await fetch(`${backend}/advisor/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Backend error ${res.status}: ${text}`);
    }

    const json = await res.json();
    resultJsonEl.textContent = JSON.stringify(json, null, 2);
    resultEl.hidden = false;
  } catch (err) {
    errorEl.textContent = err.message || "Unexpected error";
    errorEl.hidden = false;
  }
}

document.getElementById("analyze-form")?.addEventListener("submit", analyze);

