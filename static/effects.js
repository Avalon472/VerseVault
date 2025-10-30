const pdb = "https://poetrydb.org"
latestSearch = ""

const toTopButtons = document.querySelectorAll(".toTopButton")
if (toTopButtons){
    toTopButtons.forEach(button => {
    button.addEventListener("click", scrollToTop)
})}

const poemInput = document.getElementById("poemSearch")
const poemComplete = document.getElementById("poemComplete")
const poetInput = document.getElementById("poetSearch")
const poetComplete = document.getElementById("poetComplete")

const favoriteButton = document.getElementById("addFavorite")
const removeFavorites = document.getElementById("removeFavorites")

if (poemInput){
    poemInput.addEventListener("input", () => {
    latestSearch = poemInput.value.trim();
    if (!latestSearch)
        return;
    else fetchResult(latestSearch, 'poem')
})

    poemInput.addEventListener("blur", () => {
    close();
    setTimeout(() => {poemInput.value=""}, 100);
})}


if (poetInput){

    poetInput.addEventListener("input", () => {
    const latestSearch = poetInput.value.trim();
    if (!latestSearch)
        return;
    else fetchResult(latestSearch, 'poet')
})

    poetInput.addEventListener("blur", () => {
    close();
    setTimeout(() => {poetInput.value=""}, 100);
})}


if (favoriteButton){
    favoriteButton.addEventListener("click", async() => {
    const quote = prompt("Enter your favorite quote from this poem: ");
    const tags = prompt("Enter any tags, separated by commas: ");

    const response = await fetch("/add_favorite", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({
            title: poemTitle,
            author: poemAuthor,
            quote: quote,
            tags: tags
        })
    })

    const result = await response.json();
    if(result.status == "success"){
        alert("Poem added to favorites")
    }
    else{
        alert("Error with adding favorite")
    }
})}

if (removeFavorites){
    removeFavorites.addEventListener("click", async() => {
        if (confirm("Are you sure you want to reset your favorites list?")){
            const response = await fetch("/reset_favorites", {
                method: "POST"
            });

        const result = await response.json();
        if (result.status == "success"){
            alert ("Favorites have been reset");
            location.reload();
        }
        else{
            alert ("Error resetting favorites");
        }
    }
    })
}

function scrollToTop(){
    window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
    });
}

async function fetchResult(searchQuery, type){
    if (type == 'poem'){
        const response = await fetch(`${pdb}/title/${encodeURIComponent(searchQuery)}`);
        const results = await response.json()

        if(searchQuery != latestSearch)
            return;

        poemComplete.style.display = "flex";
        let queryResult = results.filter(poem => poem.title.toLowerCase().
        includes(searchQuery.toLowerCase()))
        poemComplete.innerHTML = queryResult.slice(0, 5).map(r => `
        <a href="/poem?title=${encodeURIComponent(r.title)}">
         ${r.title} <br> <small>by ${r.author}</small> </a>
        `).join("");
    }
    else if(type == 'poet'){
        const response = await fetch(`${pdb}/author`);
        const results = await response.json()

        if(searchQuery != latestSearch)
            return;

        poetComplete.style.display = "flex";
        let queryResult = results.authors.filter(author => author.toLowerCase().includes(searchQuery.toLowerCase()))
        poetComplete.innerHTML = queryResult.slice(0, 5).map(r => `
        <a href="/poet?poet=${encodeURIComponent(r)}">
        ${r}
        </a>
        `).join("");
    }

}

function close(){
    setTimeout(() => {
        document.querySelectorAll(".autoComplete").forEach(element => {
            element.style.display = "none";
        })
    }, 100)
}