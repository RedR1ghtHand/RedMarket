document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("item-search");
    const suggestions = document.getElementById("suggestions");
    const clearBtn = document.getElementById("clear-btn");

    if (!searchInput || !suggestions) return;

    const items = window.itemTypes || [];

    function showSuggestions(query) {
        suggestions.innerHTML = "";
        const lower = query.toLowerCase();

        const filtered = items.filter(item => {
            if (item.name.toLowerCase().includes(lower)) return true;

            if (Array.isArray(item.aliases)) {
                if (item.aliases.some(alias => alias.toLowerCase().includes(lower))) return true;
            }

            if (item.material_map) {
                return Object.keys(item.material_map).some(mat =>
                    mat.toLowerCase().includes(lower)
                );
            }

            return false;
        });

        filtered.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item.name;
            li.classList.add("list-group-item", "list-group-item-action");
            li.style.cursor = "pointer";
            li.addEventListener("click", () => {
                window.location.href = item.url;
            });
            suggestions.appendChild(li);
        });

        if (filtered.length === 0) {
            suggestions.classList.add("d-none");
        } else {
            suggestions.classList.remove("d-none");
        }
    }

    function updateClearButton() {
        if (searchInput.value.trim() === "") {
            clearBtn.classList.add("d-none");
        } else {
            clearBtn.classList.remove("d-none");
        }
    }

    searchInput.addEventListener("input", () => {
        showSuggestions(searchInput.value);
        updateClearButton();
    });

    searchInput.addEventListener("focus", () => {
        showSuggestions(searchInput.value);
        updateClearButton();
    });

    document.addEventListener("click", (e) => {
        if (!searchInput.contains(e.target) &&
            !suggestions.contains(e.target) &&
            !clearBtn.contains(e.target)) {
            suggestions.classList.add("d-none");
        }
    });

    clearBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        setTimeout(() => {
            searchInput.value = "";
            updateClearButton();
            showSuggestions("");
            suggestions.classList.remove("d-none");
            searchInput.focus();
        }, 10);
    });

    updateClearButton();
});
