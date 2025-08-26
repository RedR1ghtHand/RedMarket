function attachChatShortcut() {
    const textarea = document.getElementById("chat-input");
    const form = document.getElementById("chat-form");
    if (!textarea || !form) return;

    textarea.addEventListener("keydown", function(event) {
        if (event.key === "Enter" && event.shiftKey) {
            event.preventDefault();
            form.requestSubmit();
        }
    });
}

document.addEventListener("DOMContentLoaded", attachChatShortcut);
document.addEventListener("htmx:afterSwap", attachChatShortcut);
