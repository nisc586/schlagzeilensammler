/* Media Template Logic */
const template = document.getElementById("media-template");
function getNewMediaItem(article) {
    let clone = template.content.cloneNode(true);
    clone.querySelector(".media-title").textContent = article.title;
    clone.querySelector(".media-date").textContent = article.published;
    clone.querySelector(".media-content").insertAdjacentHTML("afterbegin", DOMPurify.sanitize(article.description));
    clone.querySelector(".media-link").href = article.link;
    return(clone);
}


/* Articles Refresh Logic */
const articlesList = document.getElementById("articles-list");
const fetchButton = document.getElementById("fetch-rss")

fetchButton.addEventListener("click", async function() {
    const response = await fetch("/fetch-articles/rss");
    const data = await response.json();

    data.articles.forEach(article => {
        newItem = getNewMediaItem(article);
        
        // Flash
        let newMediaItem = newItem.firstElementChild;
        newMediaItem.classList.add("flash");
        
        setTimeout(() => {
            newMediaItem.classList.remove("flash");
        }, 5000);
        
        articlesList.appendChild(newItem);
    })
})


/* Load Articles Logic */
let currentPage = 1;
let loading = false;
let hasMore = true;

const loader = document.getElementById("loader");
/* articlesList got declared earlier*/

async function loadArticles() {
    if (loading || !hasMore) return;

    loading = true;
    try {
        const response = await fetch(`/fetch-articles/db?page=${currentPage}`);
        const data = await response.json();

        data.articles.forEach(article => {
            let newItem = getNewMediaItem(article);
            articlesList.appendChild(newItem);
        });

        hasMore = data.has_next;
        if (!hasMore) {
            loader.textContent = "Keine weiteren Artikel.";
        }

        currentPage += 1;
    } catch (err) {
        console.error("Fehler beim Laden der Artikel:", err);
        loader.textContent = "Fehler beim Laden.";
    }
    loading = false;
}

window.addEventListener("scroll", () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
        loadArticles();
    }
})

/* Main */
if (typeof DOMPurify !== "undefined") {
    console.log("DOMPurify ist bereit!");
} else {
    console.error("DOMPurify konnte nicht geladen werden.");
}

loadArticles();

