class NotificationWebSocket {
    constructor(userId) {
        this.userId = userId;
        this.socket = null;
        this.toastContainer = null;
        this.isOnMessagingPage = this.checkIfOnMessagingPage();
        this.currentThreadId = this.getCurrentThreadId();
        this.init();
    }

    init() {
        this.toastContainer = document.getElementById('toast-container');
        this.connect();
        this.setupEventListeners();
        this.setupMessagingPageListeners();
    }

    checkIfOnMessagingPage() {
        const isMessagingUrl = window.location.pathname.includes('/messages/') ||
            window.location.pathname === '/account/messages/' ||
            window.location.pathname.startsWith('/account/messages/');

        let hasMessagingElements = false;
        if (isMessagingUrl) {
            hasMessagingElements = document.querySelector('#thread-container') !== null ||
                document.querySelector('#threads-list-container') !== null;
        }

        return isMessagingUrl || hasMessagingElements;
    }

    getCurrentThreadId() {
        const threadContainer = document.querySelector('#thread-container');
        return threadContainer ? threadContainer.dataset.threadId : null;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;

        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = () => {
            console.log('Notification WebSocket connected');
            if (this.isOnMessagingPage) {
                this.requestUnreadCounts();
            }
        };
        this.socket.onclose = () => {
            console.log('Notification WebSocket disconnected, reconnecting...');
            setTimeout(() => this.connect(), 3000);
        };
        this.socket.onerror = (error) => {
            console.error('Notification WebSocket error:', error);
        };
        this.socket.onmessage = (event) => this.handleMessage(JSON.parse(event.data));
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-notification-id]')) {
                this.markAsRead(e.target.dataset.notificationId);
            }
        });

        const updatePageState = () => {
            this.isOnMessagingPage = this.checkIfOnMessagingPage();
            this.currentThreadId = this.getCurrentThreadId();
            this.setupMessagingPageListeners();

            if (this.isOnMessagingPage) {
                this.requestUnreadCounts();
            }
        };

        document.addEventListener('htmx:afterSwap', updatePageState);
        document.addEventListener('htmx:afterRequest', updatePageState);
        document.addEventListener('htmx:afterSettle', updatePageState);

        let lastUrl = window.location.pathname;
        setInterval(() => {
            if (window.location.pathname !== lastUrl) {
                lastUrl = window.location.pathname;
                updatePageState();
            }
        }, 100);
    }

    setupMessagingPageListeners() {
        if (this.messagingListeners) {
            this.messagingListeners.forEach(({ element, event, handler }) => {
                element.removeEventListener(event, handler);
            });
        }
        this.messagingListeners = [];

        if (!this.isOnMessagingPage) return;

        const chatInput = document.getElementById('chat-input');
        const chatForm = document.getElementById('chat-form');
        const chatContainer = document.getElementById('container-chat');
        const markReadHandler = () => this.markCurrentThreadRead();

        if (chatInput) {
            chatInput.addEventListener('input', markReadHandler);
            chatInput.addEventListener('keydown', markReadHandler);
            this.messagingListeners.push(
                { element: chatInput, event: 'input', handler: markReadHandler },
                { element: chatInput, event: 'keydown', handler: markReadHandler }
            );
        }

        if (chatForm) {
            chatForm.addEventListener('submit', markReadHandler);
            this.messagingListeners.push(
                { element: chatForm, event: 'submit', handler: markReadHandler }
            );
        }

        if (chatContainer) {
            chatContainer.addEventListener('scroll', markReadHandler);
            this.messagingListeners.push(
                { element: chatContainer, event: 'scroll', handler: markReadHandler }
            );
        }

        const threadClickHandler = (e) => {
            const threadLink = e.target.closest('[data-thread-id]');
            if (threadLink) {
                const threadId = threadLink.dataset.threadId;
                this.markThreadRead(threadId);
            }
        };
        document.addEventListener('click', threadClickHandler);
        this.messagingListeners.push(
            { element: document, event: 'click', handler: threadClickHandler }
        );
    }

    handleMessage(data) {
        if (data.type === 'notification') {
            if (!this.isOnMessagingPage || data.notification.type !== 'message') {
                this.showToast(data.notification);
            }

            if (this.isOnMessagingPage && data.unread_counts) {
                this.updateUnreadCounts(data.unread_counts);
            }
        } else if (data.type === 'unread_counts') {
            this.updateUnreadCounts(data.unread_counts);
        }
    }

    updateUnreadCounts(unreadCounts) {
        document.querySelectorAll('[id^="unread-badge-"]').forEach(badge => {
            badge.setAttribute('data-count', '0');
            badge.textContent = '';
        });

        Object.entries(unreadCounts).forEach(([threadId, data]) => {
            const badge = document.getElementById(`unread-badge-${threadId}`);
            if (badge) {
                badge.setAttribute('data-count', data.count);
                badge.textContent = data.count;
            }
        });
    }

    requestUnreadCounts() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                action: 'get_unread_counts'
            }));
        }
    }

    markCurrentThreadRead() {
        if (this.currentThreadId) {
            this.markThreadRead(this.currentThreadId);
        }
    }

    markThreadRead(threadId) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                action: 'mark_thread_read',
                thread_id: threadId
            }));
        }
    }

    showToast(notification) {
        if (!this.toastContainer) {
            console.error('Toast container not found!');
            return;
        }

        this.fetchToastTemplate(notification, (html) => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            const toastElement = tempDiv.firstElementChild;

            this.toastContainer.appendChild(toastElement);

            const toast = new bootstrap.Toast(toastElement, {
                autohide: true,
                delay: 5000
            });

            toast.show();

            toastElement.addEventListener('hidden.bs.toast', () => {
                toastElement.remove();
            });
        });
    }

    fetchToastTemplate(notification, callback) {
        const params = new URLSearchParams(notification);
        const url = `/account/notifications/toast-template/?${params}`;

        fetch(url)
            .then(response => response.json())
            .then(data => callback(data.html))
            .catch(error => {
                console.error('Error fetching toast template:', error);
            });
    }

    markAsRead(notificationId) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                action: 'mark_read',
                notification_id: notificationId
            }));
        }
    }
}

let notificationWebSocket = null;

document.addEventListener('DOMContentLoaded', () => {
    const userId = document.querySelector('[data-user-id]')?.dataset.userId;

    if (userId && !notificationWebSocket) {
        notificationWebSocket = new NotificationWebSocket(userId);
    }
});
