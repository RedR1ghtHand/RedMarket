function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    popoverTriggerList.forEach(function (el) {
        if (!bootstrap.Popover.getInstance(el)) {
            new bootstrap.Popover(el, {
                trigger: 'manual',
                html: true
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", initPopovers);
document.addEventListener("htmx:afterSwap", initPopovers);

window.handleBuy = function(btn) {
    const message = btn.getAttribute('data-clipboard');
    if (!message) return;

    navigator.clipboard.writeText(message).then(() => {
        let popover = bootstrap.Popover.getInstance(btn);

        if (!popover) {
            popover = new bootstrap.Popover(btn, {
                trigger: 'manual',
                html: true
            });
        }

        const content = `<strong>Message copied!</strong><br>${message}`;
        popover.setContent({ '.popover-body': content });

        popover.show();

        setTimeout(() => popover.hide(), 2000);
    }).catch(err => console.error('Clipboard copy failed:', err));
};

