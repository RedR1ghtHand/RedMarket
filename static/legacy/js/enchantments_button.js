document.addEventListener("DOMContentLoaded", function () {
    const toggleAllBtn = document.querySelector(".enchants-expand-btn");
    const enchantSections = document.querySelectorAll(".enchant-list-wrapper");
    let expanded = false;

    toggleAllBtn.addEventListener("click", function () {
        expanded = !expanded;
        enchantSections.forEach(section => {
            section.classList.toggle("hidden", !expanded);
        });
        toggleAllBtn.textContent = expanded ? "Enchants ⬆" : "Enchants ⬇";
    });

    document.querySelectorAll(".enchant-toggle-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const list = this.nextElementSibling;
            if (list) {
                list.classList.toggle("hidden");
            }
        });
    });
});