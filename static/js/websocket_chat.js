class WebSocketChat {
    constructor(threadId, currentUserId) {
        this.threadId = threadId;
        this.currentUserId = currentUserId;
        this.socket = null;
        this.init();
    }

    init() {
        this.connect();
        this.setupEventListeners();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat/${this.threadId}/`;

        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = () => console.log('WebSocket connected');
        this.socket.onclose = () => {
            console.log('WebSocket disconnected, reconnecting...');
            setTimeout(() => this.connect(), 3000);
        };
        this.socket.onmessage = (event) => this.handleMessage(JSON.parse(event.data));
    }

    setupEventListeners() {
        const form = document.getElementById('chat-form');
        const input = document.getElementById('chat-input');

        if (form) {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        if (input) {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSubmit(e);
                }
            });
        }
    }

    handleSubmit(e) {
        e.preventDefault();
        const input = document.getElementById('chat-input');
        const content = input.value.trim();

        if (content && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                content: content
            }));
            input.value = '';
        }
    }

    handleMessage(data) {
        if (data.type === 'chat_message') {
            this.addMessage(data.message);
        }
    }

    addMessage(message) {
        const messagesContainer = document.getElementById('messages-list');
        const messageElement = this.createMessageElement(message);
        messagesContainer.appendChild(messageElement);

        // Add focus ring effect
        this.addFocusRing(messageElement);

        this.scrollToBottom();
    }

    addFocusRing(messageElement) {
        const messageBubble = messageElement.querySelector('.message-bubble-own, .message-bubble-other');
        if (messageBubble) {
            messageBubble.style.boxShadow = '0 0 10px rgba(13, 110, 253, 0.5)';

            setTimeout(() => {
                messageBubble.style.boxShadow = '';
            }, 3000);
        }
    }

    createMessageElement(message) {
        const div = document.createElement('div');
        const isOwnMessage = message.sender_id == this.currentUserId;

        div.className = `d-flex mb-2 ${isOwnMessage ? 'justify-content-end' : ''}`;

        div.innerHTML = `
            <div class="d-flex align-items-end ${isOwnMessage ? 'flex-row-reverse' : ''}">
                ${!isOwnMessage ? `
                    <img src="https://mc-heads.net/avatar/${message.sender}/32" 
                         alt="${message.sender}" class="rounded-circle border border-2 me-2" 
                         width="32" height="32">
                ` : ''}
                <div class="${isOwnMessage ? 'text-end' : ''}">
                    <div class="px-3 pt-3 pb-1 rounded-3 position-relative ${isOwnMessage ? 'message-bubble-own' : 'message-bubble-other'}" 
                         style="max-width: 400px;">
                        <div class="mb-2">${message.content}</div>
                        <small class="text-muted opacity-75">
                            ${this.timeAgo(new Date(message.created_at))}
                        </small>
                    </div>
                </div>
            </div>
        `;

        return div;
    }

    timeAgo(date) {
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) {
            return 'just now';
        } else if (diffInSeconds < 3600) {
            const minutes = Math.floor(diffInSeconds / 60);
            return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        } else if (diffInSeconds < 86400) {
            const hours = Math.floor(diffInSeconds / 3600);
            return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        } else {
            const days = Math.floor(diffInSeconds / 86400);
            return `${days} day${days > 1 ? 's' : ''} ago`;
        }
    }

    scrollToBottom() {
        const container = document.getElementById('container-chat');
        container.scrollTop = container.scrollHeight;
    }
}

// Global variable to track current WebSocket instance
let currentWebSocket = null;

document.addEventListener('DOMContentLoaded', () => {
    const threadContainer = document.querySelector('#thread-container');
    const threadId = threadContainer?.dataset.threadId;
    const currentUserId = document.querySelector('[data-user-id]')?.dataset.userId;

    if (threadId && currentUserId) {
        if (currentWebSocket && currentWebSocket.socket) {
            currentWebSocket.socket.close();
        }

        currentWebSocket = new WebSocketChat(threadId, currentUserId);
    }
});
