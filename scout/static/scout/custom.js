document.addEventListener('DOMContentLoaded', function() {
  console.log('hello world');
});

//searchsuggestion
let products = results = [
  { 'nome': 'risultato1', 'slug': 'risultato-1' },
  {'nome': 'risultato2', 'slug': 'risultato-2'},
]
// fetch("/products/getProductsSuggestions", {
//     method: "get",
//     headers: {
//         'Accept': 'application/json',
//         'Content-Type': 'application/json'
//     },
// })
// .then((response) => response.json())
// .then((responseData) => {
//     products = responseData['result']
// });

const searchInput = document.querySelector("#smart-search>input[name='query']")
const searchSuggestion = document.querySelector("#search-suggestion")
const suggestionsList = document.querySelector("#search-suggestion>ul")
const template = document.querySelector('#suggestion');

const SHOW_SUGGESTIONS = () => {
    if (results.length > 0) {
        results.forEach(result => {
            const suggestion = template.content.cloneNode(true)
            let link = suggestion.querySelector("#suggestion-link")
            link.setAttribute('href', `/${result.slug}`)
            link.innerText = result.nome
            suggestionsList.appendChild(suggestion)
        })
        searchSuggestion.classList.remove("d-none");
    } else {
        searchSuggestion.classList.add("d-none");
    }
}

searchInput.addEventListener('input', (e) => {
    if (e.target.value.length > 3) {
        results = products.filter(product => product.nome.toLowerCase().indexOf(e.target.value.trim().toLowerCase()) !== -1)
    } else {  
        results = []
    }
    suggestionsList.innerHTML = ""
    SHOW_SUGGESTIONS()
})