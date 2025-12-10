import * as vscode from "vscode";
import fetch from "cross-fetch";

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand(
    "greenCodingAdvisor.analyzeSelection",
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showWarningMessage("Open a file to analyze code.");
        return;
      }

      const selection = editor.document.getText(editor.selection) || editor.document.getText();
      if (!selection.trim()) {
        vscode.window.showWarningMessage("Select code to analyze.");
        return;
      }

      const config = vscode.workspace.getConfiguration("greenCodingAdvisor");
      const backendUrl = (config.get<string>("backendUrl") || "http://127.0.0.1:8000").replace(/\/+$/, "");
      const authToken = config.get<string>("authToken") || "";

      const language = editor.document.languageId || "plaintext";
      const filename = editor.document.fileName.split(/[\\/]/).pop() || "snippet";

      const payload = {
        code_content: selection,
        language,
        filename
      };

      const status = vscode.window.setStatusBarMessage("Green Coding Advisor: analyzing...");
      try {
        const res = await fetch(`${backendUrl}/advisor/analyze`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(authToken ? { Authorization: `Bearer ${authToken}` } : {})
          },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          const text = await res.text();
          throw new Error(`Backend error ${res.status}: ${text}`);
        }

        const json = await res.json();
        vscode.window.showInformationMessage(
          "Green Coding Advisor result",
          { modal: true, detail: JSON.stringify(json, null, 2) }
        );
      } catch (err: any) {
        vscode.window.showErrorMessage(`Green Coding Advisor failed: ${err?.message || err}`);
      } finally {
        status.dispose();
      }
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {
  // nothing to clean up
}

