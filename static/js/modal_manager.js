let globalModal = null;

function showMainModal(el) {
    try {
        if (globalModal) {
            globalModal.dispose();
        }
        
        globalModal = new bootstrap.Modal(el);
        
        if (el._htmxListener) {
            document.body.removeEventListener('htmx:afterSwap', el._htmxListener);
        }
        
        const listener = function(e) {
            if (e.detail.target.closest('.modal-content') === el.querySelector('.modal-content')) {
                if (globalModal) {
                    globalModal.show();
                }
            }
        };
        
        el._htmxListener = listener;
        document.body.addEventListener('htmx:afterSwap', listener);
    } catch (error) {
        console.error('Error creating modal:', error);
    }
}

window.hideMainModal = function() {
    try {
        if (globalModal) {
            globalModal.hide();
        }
    } catch (error) {
        console.error('Error hiding modal:', error);
    }
}

window.cleanupMainModal = function() {
    try {
        if (globalModal) {
            globalModal.dispose();
            globalModal = null;
        }
    } catch (error) {
        console.error('Error cleaning up modal:', error);
    }
}

window.addEventListener('beforeunload', function() {
    window.cleanupMainModal();
});

document.addEventListener('htmx:responseError', function(e) {
    console.error('HTMX request failed:', e.detail);
});

document.addEventListener('htmx:beforeRequest', function(e) {
    if (e.detail.target.id === 'mainModal') {
    }
});
