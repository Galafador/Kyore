document.addEventListener("DOMContentLoaded", () => {
    const listingContainer = document.querySelector(".listing-card-container")
    if (!listingContainer) return;
    listingContainer.addEventListener("click", (event) => {
        const favoriteButton = event.target.closest(".btn-favorite")
        if (!favoriteButton) return;
        const card = favoriteButton.closest(".listing-card")
        if (!card) return;
        const url = card.dataset.url
        const csrf = card.dataset.csrf

        if (confirm("Remove item from watchlist?")) {
            fetch(`${url}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrf,
                    "Accept": "application/json",
                }
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Could not remove item. Please try again.");
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
                alert("An error occurred. Please check the console.");
            });
        }
    })
})