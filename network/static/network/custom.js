document.addEventListener('DOMContentLoaded', function() {

  const newPostForm = document.querySelector('#new-post-form');
  const followBtn = document.querySelector('#follow');
  const unfollowBtn = document.querySelector('#unfollow');

    if (newPostForm) {
      newPostForm.addEventListener('submit', (event) => save_post(newPostForm, event));
    }
  
    if (followBtn) {
      followBtn.addEventListener('click', () => follow(followBtn));
    }
    
    if (unfollowBtn) {
      unfollowBtn.addEventListener('click', () => unfollow(unfollowBtn));
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

function follow(btn) {
  
  fetch('/follow', {
    method: 'POST',
    body: JSON.stringify({
        user_id: btn.dataset.userId
    })
  })
  .then(response => response.json())
  .then(result => {
      if (result.error) {
        alert(result.error)
      } else {
        location.reload()
    }
  });
  
}

function unfollow(btn) {
    fetch('/unfollow', {
    method: 'POST',
    body: JSON.stringify({
        user_id: btn.dataset.userId
    })
  })
  .then(response => response.json())
  .then(result => {
      if (result.error) {
        alert(result.error)
      } else {
        location.reload()
    }
  });
}