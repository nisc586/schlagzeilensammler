/* Media Template Logic */
const template = document.getElementById("media-template");
function getNewMediaItem(article) {
    let clone = template.content.cloneNode(true);
    clone.querySelector(".media-title").textContent = article.title;
    clone.querySelector(".media-content").insertAdjacentHTML("afterbegin", DOMPurify.sanitize(article.description));
    clone.querySelector(".media-link").href = article.link;

    const date = new Date(article.published);
    const formatted = new Intl.DateTimeFormat("de-DE", {
        weekday: "long",
        year: "numeric",
        month: "short",
        day: "numeric",
        }).format(date);
    clone.querySelector(".media-date").textContent = formatted

    const channel = channelMap[activeChannelId]; // channelMap defined on server side in the template
    if (channel && channel.image_url) {
        clone.querySelector(".media-icon").src = channel.image_url;
        clone.querySelector(".media-icon").alt = channel.name || "Channel Icon";
    }
    return(clone);
}


/* Articles Load and Refresh Logic */
const articlesList = document.getElementById("articles-list");
const fetchButton = document.getElementById("fetch-rss")
const loader = document.getElementById("loader");

let currentPage = 1;
let loading = false;
let hasMore = true;
let activeChannelId = 1;


async function fetchNew() {
    const response = await fetch(`/fetch-articles/rss?channel_id=${activeChannelId}`);
    const data = await response.json();

    data.articles.forEach(article => {
        newItem = getNewMediaItem(article);
        
        // Flash
        let newMediaItem = newItem.firstElementChild;
        newMediaItem.classList.add("flash");
        
        setTimeout(() => {
            newMediaItem.classList.remove("flash");
        }, 5000);    
        
        articlesList.insertBefore(newItem, articlesList.firstChild);
    })    
}    


async function loadArticles() {
    if (loading || !hasMore) return;

    loading = true;
    try {
        const response = await fetch(`/fetch-articles/db?page=${currentPage}&channel_id=${activeChannelId}`);
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

async function reloadArticles(channelId=1) {
    activeChannelId = channelId;

    // Reset loading
    articlesList.innerHTML = "";
    currentPage = 1;
    loading = false;
    hasMore = true;
    loadArticles();
    fetchNew();
}    

/* Main */
if (typeof DOMPurify !== "undefined") {
    console.log("DOMPurify ist bereit!");
} else {
    console.error("DOMPurify konnte nicht geladen werden.");
}

loadArticles();

