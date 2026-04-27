let page = 1;
let loading = false;
let query = '';

function searchImages(reset = true) {
    if (loading) return;
    loading = true;
    if (reset) {
        page = 1;
        document.getElementById('gallery').innerHTML = '';
        query = document.getElementById('searchBox').value;
    }

    fetch(`/search?q=${query}&page=${page}&per_page=20`)
    .then(response => response.json())
    .then(data => {
        let gallery = document.getElementById('gallery');
        data.forEach(item => {
            let img = document.createElement('img');
            img.src = item.url;
            img.alt = item.source;
            img.className = 'thumb';
            gallery.appendChild(img);
        });
        page++;
        loading = false;
    });
}

window.addEventListener('scroll', () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
        searchImages(false);
    }
});

document.getElementById('searchBox').addEventListener('keypress', (e) => {
    if(e.key === 'Enter'){
        searchImages(true);
    }
});
