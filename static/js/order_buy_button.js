function handleBuy(button) {
    const wrapper = button.closest(".buy-button-container");
    const messageWrapper = wrapper.querySelector(".buy-clipboard-wrapper");
    const message = wrapper.querySelector(".buy-clipboard-message");
    const closeButton = wrapper.querySelector(".close-button");

    const textToCopy = button.dataset.clipboard;

    navigator.clipboard.writeText(textToCopy).then(() => {
        message.textContent = `Copied: ${textToCopy}`;
        messageWrapper.classList.remove("hidden");
        button.classList.add("hidden");
        closeButton.classList.remove("hidden");
    }).catch(err => {
        console.error("Copy failed", err);
    });
}

function handleClose(button) {
    const wrapper = button.closest(".buy-button-container");
    const buyButton = wrapper.querySelector(".buy-button");
    const messageWrapper = wrapper.querySelector(".buy-clipboard-wrapper");

    messageWrapper.classList.add("hidden");
    buyButton.classList.remove("hidden");
    button.classList.add("hidden");
}