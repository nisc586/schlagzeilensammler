function confirmDelete(channelId) {
    fetch(`/channels/${channelId}/article_count`)
        .then(response => response.json())
        .then(data => {
            const articleCount = data.count;
            const message = `Möchtest du diesen Channel wirklich löschen? Es werden ${articleCount} Artikel mit gelöscht.`;
            if (confirm(message)) {
                fetch(`/channels/${channelId}/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                }).then(() => {
                    window.location.reload();  // oder ein gezieltes Redirect
                });
            }
        });
}


function dismissMessage(btn) {
    btn.closest(".temporary-message").remove()
}