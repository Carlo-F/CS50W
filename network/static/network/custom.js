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
  
  const likeButtons = document.querySelectorAll('.like-button');

  likeButtons.forEach(button => {
    button.addEventListener('click', () => likePost(button));
    button.querySelector('.likes').innerHTML = button.dataset.postLikes
  })

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

function likePost(btn) {
  let postId = btn.dataset.postId
  let likes = btn.dataset.postLikes
  let liked = btn.dataset.postLiked == 'True'
  let path = liked ? '/dislike' : '/like'

  fetch(path, {
    method: 'POST',
    body: JSON.stringify({
        post_id: postId
    })
  })
  .then(response => response.json())
  .then(result => {
      if (result.error) {
        alert(result.error)
      } else {
        if (liked) {
          btn.dataset.postLikes = parseInt(likes) - 1;
          btn.dataset.postLiked = 'False'
          btn.querySelector('.likes').innerHTML = parseInt(likes) - 1;
          btn.querySelector('i').classList.replace('bi-heart-fill', 'bi-heart');
        } else {
          btn.dataset.postLikes = parseInt(likes) + 1;
          btn.dataset.postLiked = 'True'
          btn.querySelector('.likes').innerHTML = parseInt(likes) + 1;
          btn.querySelector('i').classList.replace('bi-heart', 'bi-heart-fill');
        }
    }
  });
}