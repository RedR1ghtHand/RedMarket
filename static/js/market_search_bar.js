document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("item-search");
    const suggestions = document.getElementById("suggestions");
    const clearBtn = document.getElementById("clear-btn");

    if (!searchInput || !suggestions) return;

    const items = window.itemTypes || [];

    function showSuggestions(query) {
        suggestions.innerHTML = "";

        let filtered = items;
        if (query) {
            const lower = query.toLowerCase();
            filtered = items.filter(item => item.name.toLowerCase().includes(lower));
        }

        filtered.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item.name;
            li.addEventListener("click", () => {
                window.location.href = item.url;
            });
            suggestions.appendChild(li);
        });

        if (filtered.length > 0) {
            suggestions.classList.remove("hidden");
        } else {
            suggestions.classList.add("hidden");
        }
    }

    function updateClearButton() {
        if (searchInput.value.trim() !== "") {
            clearBtn.classList.remove("hidden");
        } else {
            clearBtn.classList.add("hidden");
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
        if (!searchInput.contains(e.target) && !suggestions.contains(e.target) && !clearBtn.contains(e.target)) {
            suggestions.classList.add("hidden");
        }
    });


    clearBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        setTimeout(() => {
            searchInput.value = "";
            updateClearButton();
            showSuggestions(""); // Refresh suggestions
            suggestions.classList.remove("hidden");
            searchInput.focus(); // Bring focus back
        }, 10);
    });

    updateClearButton();
});

