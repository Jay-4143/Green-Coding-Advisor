// Basic context menu to send selected text for analysis

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "green-advisor-analyze",
    title: "Analyze code with Green Coding Advisor",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "green-advisor-analyze" || !info.selectionText) return;

  // Forward selection to content script for processing (if needed)
  chrome.tabs.sendMessage(tab.id, {
    type: "GREEN_ADVISOR_ANALYZE",
    payload: { code: info.selectionText },
  });
});

