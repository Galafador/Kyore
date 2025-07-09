document.addEventListener("DOMContentLoaded", () => {
    const listingContainer = document.querySelector(".listing-card-container")
    const messagesContainer = document.getElementById("messages-container")
    if (!listingContainer) return;
    listingContainer.addEventListener("click", (event) => {
        const favoriteButton = event.target.closest(".btn-favorite")
        if (!favoriteButton) return;
        const card = favoriteButton.closest(".listing-card")
        if (!card) return;
        const listingId = card.dataset.id
        const url = card.dataset.url
        const csrf = card.dataset.csrf
        let isFavorited = card.dataset.favorited === "true"
        const favoritesCount = card.querySelector(".favorites-count")
        fetch(`${url}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "Accept": "application/json",
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.favorited !== undefined) {
                isFavorited = data.favorited;
                favoriteButton.classList.toggle("favorited", data.favorited)
                favoriteButton.title = data.favorited ? 
                "Remove from Watchlist"
                :
                "Add to Watchlist";
                if (favoritesCount && data.favorites_count !== undefined) {
                    favoritesCount.innerHTML = data.favorites_count
                }
                if (data.message) {
                    const existingAlert = messagesContainer.querySelector(".alert")
                    if (existingAlert) {
                        const bsExistingAlert = bootstrap.Alert.getOrCreateInstance(existingAlert)
                        bsExistingAlert.close()
                        setTimeout(() => {
                            showNewAlert(data.message)
                        }, 200);
                    }
                    else {
                        showNewAlert(data.message);
                    }
                
                    function showNewAlert(message) {
                        const alert = document.createElement('div')
                        alert.className = "alert alert-primary alert-dismissible fade show"
                        alert.setAttribute("role", "alert")
                        alert.innerHTML = `
                            ${data.message}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        `
                        messagesContainer.appendChild(alert)
                        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                        setTimeout(() => {
                            try {
                                bsAlert.close();
                            }
                            catch (e) {
                                console.warn("Running auto close alert: alert already closed")
                            }
                        }, 2000)
                    }
                }
            }})
        .catch(error => console.error("AJAX error: ", error))
    })
})