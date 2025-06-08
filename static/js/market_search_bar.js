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
            li.addEventListener("click", () => {
                window.location.href = item.url;
            });
            suggestions.appendChild(li);
        });

        suggestions.classList.toggle("hidden", filtered.length === 0);
    }

    function updateClearButton() {
        clearBtn.classList.toggle("hidden", searchInput.value.trim() === "");
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
            suggestions.classList.add("hidden");
        }
    });

    clearBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        setTimeout(() => {
            searchInput.value = "";
            updateClearButton();
            showSuggestions(""); // Show all again
            suggestions.classList.remove("hidden");
            searchInput.focus();
        }, 10);
    });

    updateClearButton();
});
