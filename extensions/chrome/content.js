// Content script listens for analyze requests and posts to the backend

async function sendToBackend(code) {
  const { backendUrl = "http://127.0.0.1:8000", authToken = "" } =
    (await chrome.storage.sync.get(["backendUrl", "authToken"])) || {};

  try {
    const res = await fetch(`${backendUrl.replace(/\/+$/, "")}/advisor/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
      },
      body: JSON.stringify({
        code_content: code,
        language: "python",
        filename: "selection.py",
      }),
    });
    const json = await res.json();
    alert(`Green Coding Advisor:\n${JSON.stringify(json, null, 2)}`);
  } catch (err) {
    console.error("Green Advisor error", err);
    alert("Green Advisor: failed to analyze selection");
  }
}

chrome.runtime.onMessage.addListener((message, _sender, _sendResponse) => {
  if (message?.type === "GREEN_ADVISOR_ANALYZE" && message.payload?.code) {
    sendToBackend(message.payload.code);
  }
});

