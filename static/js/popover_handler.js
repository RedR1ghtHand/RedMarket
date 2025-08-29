function initReputationPopover() {
    const reputationButtons = document.querySelectorAll('.reputation-popover-btn');
    reputationButtons.forEach(function (btn) {
        if (!bootstrap.Popover.getInstance(btn)) {
            try {
                const createdDate = btn.getAttribute('data-created-date') || '';
                const popoverContent = `You gave <strong>${btn.textContent.trim()}</strong> badge to this user<br><span class="text-secondary">${createdDate}</span>`;
                
                new bootstrap.Popover(btn, {
                    title: 'Reputation Given',
                    content: popoverContent,
                    trigger: 'hover',
                    placement: 'right',
                    container: 'body',
                    html: true
                });
            } catch (error) {
                console.error('Failed to create reputation popover for element:', btn, error);
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    initReputationPopover();
});

document.addEventListener("htmx:afterSwap", function() {
    initReputationPopover();
});
