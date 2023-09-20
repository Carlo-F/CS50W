document.addEventListener('DOMContentLoaded', function() {
  console.log('hello world');
});

//searchsuggestion
let products = results = []
fetch("/activities", {
    method: "get",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
})
.then((response) => response.json())
.then((responseData) => {
    products = responseData['result']
});

const searchInput = document.querySelector("#smart-search>input[name='query']")
const searchSuggestion = document.querySelector("#search-suggestion")
const suggestionsList = document.querySelector("#search-suggestion>ul")
const template = document.querySelector('#suggestion');

const SHOW_SUGGESTIONS = () => {
    if (results.length > 0) {
        results.forEach(result => {
            const suggestion = template.content.cloneNode(true)
            let link = suggestion.querySelector("#suggestion-link")
            link.setAttribute('href', `/activities/${result.id}`)
            link.innerText = result.title
            suggestionsList.appendChild(suggestion)
        })
        searchSuggestion.classList.remove("d-none");
    } else {
        searchSuggestion.classList.add("d-none");
    }
}
if (searchInput !== null) {
  searchInput.addEventListener('input', (e) => {
    if (e.target.value.length > 3) {
      results = products.filter(product => product.title.toLowerCase().indexOf(e.target.value.trim().toLowerCase()) !== -1)
    } else {
      results = []
    }
    suggestionsList.innerHTML = ""
    SHOW_SUGGESTIONS()
  })
}

function likeActivity(btn) {
  let activityId = btn.dataset.activityId
  let likes = btn.dataset.activityLikes
  let liked = btn.dataset.activityLiked == 'True'
  let path = liked ? '/dislike' : '/like'

  fetch(path, {
    method: 'POST',
    body: JSON.stringify({
        activity_id: activityId
    })
  })
  .then(response => response.json())
  .then(result => {
      if (result.error) {
        alert(result.error)
      } else {
        if (liked) {
          btn.dataset.activityLikes = parseInt(likes) - 1;
          btn.dataset.activityLiked = 'False'
          if (btn.querySelector('.likes')) {
            btn.querySelector('.likes').innerHTML = parseInt(likes) - 1;
          }
          btn.querySelector('i').classList.replace('bi-star-fill', 'bi-star');
        } else {
          btn.dataset.activityLikes = parseInt(likes) + 1;
          btn.dataset.activityLiked = 'True'
          if (btn.querySelector('.likes')) {
            btn.querySelector('.likes').innerHTML = parseInt(likes) + 1;
          }
          btn.querySelector('i').classList.replace('bi-star', 'bi-star-fill');
        }
        if (location.pathname == '/popular' || location.pathname == '/favourites') {
          location.reload()
        }
    }
  });
}

const likeButtons = document.querySelectorAll('.like-button');

likeButtons.forEach(button => {
  button.addEventListener('click', () => likeActivity(button));
  if (button.querySelector('.likes')) {
    button.querySelector('.likes').innerHTML = button.dataset.activityLikes
  }
})