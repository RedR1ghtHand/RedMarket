// Global click handler to close popovers when clicking outside
document.addEventListener('click', function(event) {
    const activeButtons = document.querySelectorAll('.popover-active');
    activeButtons.forEach(btn => {
        if (!btn.contains(event.target)) {
            const popover = bootstrap.Popover.getInstance(btn);
            if (popover) {
                popover.hide();
                popover.dispose();
            }
            btn.classList.remove('popover-active');
        }
    });
});

window.handleBuy = function(btn) {
    const message = btn.getAttribute('data-clipboard');
    if (!message) return;

    if (!btn.classList.contains('popover-active')) {
        navigator.clipboard.writeText(message).then(() => {
            const existingPopover = bootstrap.Popover.getInstance(btn);
            if (existingPopover) {
                existingPopover.dispose();
            }

            const popover = new bootstrap.Popover(btn, {
                trigger: 'manual',
                html: true,
                placement: 'left',
                container: 'body',
                title: 'Message copied!',
                content: message
            });

            popover.show();
            btn.classList.add('popover-active');
        }).catch(err => console.error('Clipboard copy failed:', err));
    } 
    else {
        const popover = bootstrap.Popover.getInstance(btn);
        if (popover) {
            popover.hide();
            popover.dispose(); // Clean up the popover
        }
        btn.classList.remove('popover-active');
    }
};
