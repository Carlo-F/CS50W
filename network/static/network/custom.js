document.addEventListener('DOMContentLoaded', function() {

  const newPostForm = document.querySelector('#new-post-form');

    if (newPostForm) {
        newPostForm.addEventListener('submit', (event) => save_post(newPostForm, event));
    }

});

function save_post(form, event) {
  event.preventDefault()

  const formData = new FormData(form)

  fetch('/posts/new_post', {
    method: 'POST',
    body: JSON.stringify({
        content: formData.get('content')
    })
  })
  .then(response => response.json())
  .then(result => {
      if (result.error) {
        console.log(result.error)
      } else {
        location.reload()
    }
  });
}