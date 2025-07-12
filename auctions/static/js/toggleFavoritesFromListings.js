document.addEventListener("DOMContentLoaded", () => {
    const favoriteButton = document.querySelector(".btn-favorite")
    const favoriteButtonText = document.getElementById("favorite-button-text")
    const messagesContainer = document.getElementById("messages-container")
    if (!favoriteButton) return;
    favoriteButton.addEventListener("click", () => {
        const url = favoriteButton.dataset.url
        const csrf = favoriteButton.dataset.csrf
        let isFavorited = favoriteButton.dataset.favorited === "true"

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
                favoriteButtonText.innerHTML = isFavorited ? "Remove from watchlist" : "Add to watchlist"

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